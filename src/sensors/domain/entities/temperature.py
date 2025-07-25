# src/sensors/domain/entities.py

from pydantic import BaseModel
from datetime import datetime

class TemperatureData(BaseModel):
    value: float
    timestamp: datetime
