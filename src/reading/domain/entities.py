from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReadingCreate(BaseModel):
    pond_id: Optional[int] = None
    turbidity_id: Optional[int] = None
    water_level_id: Optional[int] = None
    temperature_id: Optional[int] = None
    weight_id: Optional[int] = None
    date: datetime

class Reading(BaseModel):
    reading_id: int
    pond_id: Optional[int]
    turbidity_id: Optional[int]
    water_level_id: Optional[int]
    temperature_id: Optional[int]
    weight_id: Optional[int]
    date: datetime

    model_config = {
        "from_attributes": True
    }
