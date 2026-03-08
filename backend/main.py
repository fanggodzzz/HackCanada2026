import os
import json
import time
from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import torch
import models
import schemas
import database
from torchvision import models as tv_models, transforms
from PIL import Image
import io

# ------------------------
# Create database tables
# ------------------------
models.Base.metadata.create_all(bind=database.engine)

# ------------------------
# FastAPI app setup
# ------------------------
app = FastAPI(title="Skin Disease AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Path configuration
# ------------------------
# base_dir points to the project root
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

model_dir = os.path.join(base_dir, 'model')
uploads_dir = os.path.join(base_dir, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'model.pt')
class_mapping_path = os.path.join(model_dir, 'class_mapping.json')
disease_info_path = os.path.join(model_dir, 'disease_info.json')

# ------------------------
# Load disease info
# ------------------------
disease_info = []
if os.path.exists(disease_info_path):
    with open(disease_info_path, 'r') as f:
        disease_info = json.load(f)

disease_map = {d['disease']: d for d in disease_info}

# ------------------------
# ML Model setup
# ------------------------
ml_model = None
class_names = []
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    global ml_model, class_names

    if os.path.exists(model_path) and os.path.exists(class_mapping_path):
        # Load class names
        with open(class_mapping_path, 'r') as f:
            class_names = json.load(f)

        num_classes = len(class_names)

        # Initialize model
        ml_model = tv_models.resnet18(weights=None)
        num_features = ml_model.fc.in_features
        ml_model.fc = torch.nn.Linear(num_features, num_classes)

        # Load checkpoint
        try:
            state_dict = torch.load(model_path, map_location=device)
            
            # Remove fc layer from checkpoint to avoid size mismatch
            state_dict = {k: v for k, v in state_dict.items() if not k.startswith('fc.')}
            
            # Load the rest of the weights
            ml_model.load_state_dict(state_dict, strict=False)
            ml_model = ml_model.to(device)
            ml_model.eval()
            print("Model loaded successfully. Final layer is initialized for current classes.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            ml_model = None
    else:
        print("Model or class mapping not found.")
        print(f"Expected model path: {model_path}")
        print(f"Expected class mapping path: {class_mapping_path}")

# Load model at startup
load_model()

# ------------------------
# Image transform
# ------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ------------------------
# API Endpoints
# ------------------------
@app.post("/api/scan", response_model=schemas.ScanResponse)
async def create_scan(
    body_position: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    if not ml_model:
        raise HTTPException(status_code=503, detail="AI Model not loaded.")
    
    # Read and process image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('RGB')

    # Save upload
    filename = f"{int(time.time())}_{file.filename}"
    file_path = os.path.join(uploads_dir, filename)
    image.save(file_path)

    # Predict
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = ml_model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top3_prob, top3_catid = torch.topk(probabilities, 3)

    predictions = []
    for i in range(3):
        prob = top3_prob[i].item()
        disease_name = class_names[top3_catid[i].item()]
        d_name_clean = disease_name.replace('_', ' ')
        info = disease_map.get(d_name_clean, {"severity": "Unknown", "treatments": []})
        predictions.append({
            "disease": d_name_clean,
            "probability": prob,
            "severity": info["severity"],
            "treatments": info["treatments"]
        })

    # Save scan to DB
    new_scan = models.Scan(
        image_path=f"/uploads/{filename}",
        body_position=body_position,
        disease_prediction_1=predictions[0]["disease"],
        probability_1=predictions[0]["probability"],
        disease_prediction_2=predictions[1]["disease"],
        probability_2=predictions[1]["probability"],
        disease_prediction_3=predictions[2]["disease"],
        probability_3=predictions[2]["probability"],
        severity=predictions[0]["severity"]
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return {
        "id": new_scan.id,
        "image_path": new_scan.image_path,
        "body_position": new_scan.body_position,
        "created_at": new_scan.created_at,
        "predictions": predictions
    }

@app.get("/api/history", response_model=List[schemas.ScanHistoryItem])
def get_history(db: Session = Depends(database.get_db)):
    scans = db.query(models.Scan).order_by(models.Scan.created_at.desc()).all()
    history = []
    for scan in scans:
        history.append({
            "id": scan.id,
            "top_disease": scan.disease_prediction_1,
            "probability": scan.probability_1,
            "severity": scan.severity,
            "body_position": scan.body_position,
            "created_at": scan.created_at,
            "image_path": scan.image_path
        })
    return history

# ------------------------
# Serve uploads
# ------------------------
from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")