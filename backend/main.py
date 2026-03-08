import os
import json
import time
from fastapi import FastAPI, Depends, HTTPException, status, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import torch
from . import models, schemas, database
from torchvision import models as tv_models, transforms
from PIL import Image
import io

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Skin Disease AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
disease_info_path = os.path.join(base_dir, 'model', 'disease_info.json')
class_mapping_path = os.path.join(base_dir, 'model', 'class_mapping.json')
model_path = os.path.join(base_dir, 'model', 'model.pt')

disease_info = []
if os.path.exists(disease_info_path):
    with open(disease_info_path, 'r') as f:
        disease_info = json.load(f)

disease_map = {d['disease']: d for d in disease_info}
class_names = []
ml_model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    global ml_model, class_names
    if os.path.exists(class_mapping_path) and os.path.exists(model_path):
        with open(class_mapping_path, 'r') as f:
            class_names = json.load(f)
        
        ml_model = tv_models.resnet18(weights=None)
        ml_model.fc = torch.nn.Linear(ml_model.fc.in_features, len(class_names))
        state_dict = torch.load(model_path, map_location=device, weights_only=True)
        ml_model.load_state_dict(state_dict)
        ml_model = ml_model.to(device)
        ml_model.eval()
        print("Model loaded successfully.")
    else:
        print("Model or class mapping not found. Inference will not work until trained.")

load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



@app.post("/api/scan", response_model=schemas.ScanResponse)
async def create_scan(
    body_position: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    if not ml_model:
        raise HTTPException(status_code=503, detail="AI Model not loaded.")
        
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    
    uploads_dir = os.path.join(base_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    filename = f"{int(time.time())}_{file.filename}"
    file_path = os.path.join(uploads_dir, filename)
    image.save(file_path)
    
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

from fastapi.staticfiles import StaticFiles

uploads_dir = os.path.join(base_dir, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
