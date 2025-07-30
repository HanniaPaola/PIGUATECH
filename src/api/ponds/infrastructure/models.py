from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.connection import Base


class PondModel(Base):
    __tablename__ = "pond"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    farmer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
