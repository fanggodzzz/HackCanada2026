from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class PredictionDetail(BaseModel):
    disease: str
    probability: float
    severity: str
    treatments: List[str]

class ScanResponse(BaseModel):
    id: int
    image_path: str
    body_position: str
    created_at: datetime
    predictions: List[PredictionDetail]

    class Config:
        from_attributes = True

class ScanHistoryItem(BaseModel):
    id: int
    top_disease: str
    probability: float
    severity: str
    body_position: str
    created_at: datetime
    image_path: str

    class Config:
        from_attributes = True
