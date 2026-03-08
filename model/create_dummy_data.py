import os
import json
from PIL import Image, ImageDraw

def create_dummy_data(num_images=10):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    info_path = os.path.join(base_dir, 'disease_info.json')
    dataset_dir = os.path.join(base_dir, 'dataset')
    
    with open(info_path, 'r') as f:
        diseases_info = json.load(f)
        
    os.makedirs(dataset_dir, exist_ok=True)
    
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
        (0, 0, 128), (128, 128, 0)
    ]
    
    for idx, info in enumerate(diseases_info):
        disease = info['disease']
        disease_dir = os.path.join(dataset_dir, disease.replace(' ', '_'))
        os.makedirs(disease_dir, exist_ok=True)
        
        color = colors[idx % len(colors)]
        
        for i in range(num_images):
            save_path = os.path.join(disease_dir, f"{i:03d}.jpg")
            img = Image.new('RGB', (224, 224), color=color)
            draw = ImageDraw.Draw(img)
            draw.text((10, 100), f"{disease} {i}", fill=(255,255,255))
            img.save(save_path)
            
        print(f"Created {num_images} dummy images for {disease}")

if __name__ == "__main__":
    create_dummy_data(10)
