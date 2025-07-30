from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.connection import Base
from datetime import datetime, UTC


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    supervisor = relationship("UserModel", remote_side=[id])
