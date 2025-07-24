from pydantic import BaseModel
from typing import List
from datetime import datetime

class CurrentCondition(BaseModel):
    name: str
    current_value: float
    unit: str
    trend: float
    state: str

class ParameterIndicator(BaseModel):
    name: str
    optimal_range: str
    unit: str
    state: str

class HabitatStatusResponse(BaseModel):
    last_update: datetime
    current_conditions: List[CurrentCondition]
    parameter_indicators: List[ParameterIndicator]
