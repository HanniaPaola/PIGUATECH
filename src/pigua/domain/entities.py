from pydantic import BaseModel
from typing import Optional

class PiguaCreate(BaseModel):
    weight_id: Optional[int] = None 

class Pigua(BaseModel):
    pigua_id: int 
    weight_id: Optional[int] = None

    class Config:
        orm_mode = True
