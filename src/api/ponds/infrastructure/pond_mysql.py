from sqlalchemy.orm import Session
from src.api.ponds.domain.pond_repository import PondRepository
from src.api.ponds.domain.pond import Pond
from src.db.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from typing import Optional, List
from src.api.ponds.infrastructure.models import PondModel


class PondModel(Base):
    __tablename__ = 'pond'
    id = Column(Integer, primary_key=True, index=True)
    acuicultor_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    water_volume_m3 = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class PondMySQLRepository(PondRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pond_id: int) -> Optional[Pond]:
        pond = self.db.query(PondModel).filter(PondModel.id == pond_id).first()
        return self._to_domain(pond) if pond else None

    def create(self, pond: Pond) -> Pond:
        db_pond = PondModel(
            acuicultor_id=pond.acuicultor_id,
            name=pond.name,
            location=pond.location,
            description=pond.description,
            water_volume_m3=pond.water_volume_m3
        )
        self.db.add(db_pond)
        self.db.commit()
        self.db.refresh(db_pond)
        return self._to_domain(db_pond)

    def list_by_acuicultor(self, acuicultor_id: int) -> List[Pond]:
        ponds = self.db.query(PondModel).filter(
            PondModel.acuicultor_id == acuicultor_id).all()
        return [self._to_domain(p) for p in ponds]

    def _to_domain(self, pond_model: PondModel) -> Pond:
        return Pond(
            id=pond_model.id,
            acuicultor_id=pond_model.acuicultor_id,
            name=pond_model.name,
            location=pond_model.location,
            description=pond_model.description,
            water_volume_m3=pond_model.water_volume_m3,
            created_at=pond_model.created_at
        )
