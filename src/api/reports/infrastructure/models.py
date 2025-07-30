from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.connection import Base
from datetime import datetime, UTC


class ReportModel(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    user = relationship("UserModel")
