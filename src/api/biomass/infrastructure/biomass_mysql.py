from sqlalchemy.orm import Session
from src.api.biomass.domain.biomass_repository import BiomassRepository
from src.api.biomass.domain.biomass import Biomass
from src.db.database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from typing import Optional, List


from src.api.biomass.infrastructure.models import BiomassModel


class BiomassMySQLRepository(BiomassRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, biomass_id: int) -> Optional[Biomass]:
        biomass = self.db.query(BiomassModel).filter(
            BiomassModel.id == biomass_id).first()
        return self._to_domain(biomass) if biomass else None

    def create(self, biomass: Biomass) -> Biomass:
        db_biomass = BiomassModel(
            pond_id=biomass.pond_id,
            estimated_weight_kg=biomass.estimated_weight_kg,
            calculation_date=biomass.calculation_date
        )
        self.db.add(db_biomass)
        self.db.commit()
        self.db.refresh(db_biomass)
        return self._to_domain(db_biomass)

    def list_by_pond(self, pond_id: int) -> List[Biomass]:
        biomass_list = self.db.query(BiomassModel).filter(
            BiomassModel.pond_id == pond_id).all()
        return [self._to_domain(b) for b in biomass_list]

    def _to_domain(self, biomass_model: BiomassModel) -> Biomass:
        return Biomass(
            id=biomass_model.id,
            pond_id=biomass_model.pond_id,
            estimated_weight_kg=biomass_model.estimated_weight_kg,
            calculation_date=biomass_model.calculation_date
        )
