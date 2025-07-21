from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    reading_id: Optional[int] = None
    message: str

class Notification(BaseModel):
    notification_id: int
    reading_id: Optional[int] = None
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
