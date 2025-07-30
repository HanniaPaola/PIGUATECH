from datetime import datetime
from typing import Optional


class Pond:
    def __init__(self, id: int, farmer_id: int, name: str, location: str, description: Optional[str], water_volume_m3: Optional[float], created_at: datetime):
        self.id = id
        self.farmer_id = farmer_id
        self.name = name
        self.location = location
        self.description = description
        self.water_volume_m3 = water_volume_m3
        self.created_at = created_at
