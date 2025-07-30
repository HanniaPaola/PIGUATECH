from sqlalchemy import Column, Integer, DateTime,Text, Enum
from src.core.db.connection import Base
from datetime import datetime, timezone
import enum


class NotificationType(enum.Enum):
    ALERT = "ALERT"
    INFO = "INFO"


class NotificationModel(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer ,nullable=False)
    pond_id = Column(Integer ,nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Integer, default=0)  # TINYINT(1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  
