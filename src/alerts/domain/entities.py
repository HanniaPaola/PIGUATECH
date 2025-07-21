# src/alerts/domain/entities.py

from pydantic import BaseModel
from typing import Optional

class AlertCreate(BaseModel):
    reading_id: Optional[int]  
    status: str

class Alert(BaseModel):
    alert_id: int
    reading_id: Optional[int]  
    status: str

    class Config:
        from_attributes = True
