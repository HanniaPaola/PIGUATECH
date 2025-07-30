from sqlalchemy import Column, Integer, Float, String, DateTime

from src.core.db.connection import Base
from datetime import datetime, timezone


class ReadingModel(Base):
    __tablename__ = "reading"
    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, nullable=False)
    sensor_type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    reading_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

 
