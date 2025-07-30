from sqlalchemy.orm import Session
from src.api.readings.domain.reading_repository import ReadingRepository
from src.api.readings.domain.reading import Reading
from src.db.database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from typing import Optional, List


class ReadingModel(Base):
    __tablename__ = 'reading'
    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey('pond.id'), nullable=False)
    sensor_type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    reading_date = Column(DateTime, default=func.now())


class ReadingMySQLRepository(ReadingRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reading_id: int) -> Optional[Reading]:
        reading = self.db.query(ReadingModel).filter(
            ReadingModel.id == reading_id).first()
        return self._to_domain(reading) if reading else None

    def create(self, reading: Reading) -> Reading:
        db_reading = ReadingModel(
            pond_id=reading.pond_id,
            sensor_type=reading.sensor_type,
            value=reading.value,
            reading_date=reading.reading_date
        )
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return self._to_domain(db_reading)

    def list_by_pond(self, pond_id: int) -> List[Reading]:
        readings = self.db.query(ReadingModel).filter(
            ReadingModel.pond_id == pond_id).all()
        return [self._to_domain(r) for r in readings]

    def _to_domain(self, reading_model: ReadingModel) -> Reading:
        return Reading(
            id=reading_model.id,
            pond_id=reading_model.pond_id,
            sensor_type=reading_model.sensor_type,
            value=reading_model.value,
            reading_date=reading_model.reading_date
        )
