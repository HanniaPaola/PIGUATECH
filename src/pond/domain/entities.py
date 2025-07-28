# src/pond/domain/entities.py
from pydantic import BaseModel
from typing import Optional

class PondCreate(BaseModel):
    pigua_id: Optional[int] = None

class Pond(BaseModel):
    pond_id: int
    pigua_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }