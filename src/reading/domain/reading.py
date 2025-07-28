from sqlalchemy import Column, Integer, ForeignKey, DateTime
from src.core.db.connection import Base

class Reading(Base):
    __tablename__ = "Reading"

    reading_id = Column(Integer, primary_key=True)
    turbidity_id = Column(Integer, ForeignKey("Turbidity.turbidity_id"))
    water_level_id = Column(Integer, ForeignKey("WaterLevel.water_level_id"))
    temperature_id = Column(Integer, ForeignKey("Temperature.temperature_id"))
    weight_id = Column(Integer, ForeignKey("Weight.weight_id"))
    pond_id = Column(Integer, ForeignKey("Pond.pond_id"))
    date = Column(DateTime)
