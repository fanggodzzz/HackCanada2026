from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base



class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    body_position = Column(String)
    
    # Track top 3 predictions
    disease_prediction_1 = Column(String)
    probability_1 = Column(Float)
    disease_prediction_2 = Column(String)
    probability_2 = Column(Float)
    disease_prediction_3 = Column(String)
    probability_3 = Column(Float)
    
    severity = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
