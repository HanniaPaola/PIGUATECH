from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.connection import Base


class BiomassModel(Base):
    __tablename__ = "biomass"
    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("pond.id"), nullable=False)
    estimated_weight_kg = Column(Float, nullable=False)
    calculation_date = Column(Date, nullable=False)
