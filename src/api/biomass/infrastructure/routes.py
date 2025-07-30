from fastapi import Body

from fastapi import APIRouter, HTTPException, status, Depends
from ...biomass.infrastructure.biomass_mysql import BiomassModel
from typing import List
from src.db.database import SessionLocal
from ...users.infrastructure.routes import get_current_user
from ...biomass.infrastructure.biomass_mysql import BiomassMySQLRepository
from ...biomass.domain.biomass import Biomass
from pydantic import BaseModel
from fastapi import Path


class BiomassRequest(BaseModel):
    id: int
    pond_id: int
    estimated_weight_kg: float
    calculation_date: str


router = APIRouter(prefix="/api/biomass", tags=["biomass"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.patch("/update_by_pond/{pond_id}", response_model=List[BiomassRequest])
def update_biomass_by_pond(
    pond_id: int,
    new_weight: float = Body(..., embed=True),
    db=Depends(get_db)
):
    biomass_list = db.query(BiomassModel).filter(
        BiomassModel.pond_id == pond_id,
        BiomassModel.estimated_weight_kg == 0
    ).all()
    for b in biomass_list:
        b.estimated_weight_kg = new_weight
    db.commit()
    return [
        BiomassRequest(
            id=b.id,
            pond_id=b.pond_id,
            estimated_weight_kg=b.estimated_weight_kg,
            calculation_date=str(b.calculation_date)
        ) for b in biomass_list
    ]


@router.get("/{biomass_id}", response_model=BiomassRequest)
def get_biomass(biomass_id: int = Path(...), db=Depends(get_db)):
    biomass = db.query(BiomassModel).filter(
        BiomassModel.id == biomass_id).first()
    if not biomass:
        raise HTTPException(status_code=404, detail="Biomass not found")
    return BiomassRequest(
        id=biomass.id,
        pond_id=biomass.pond_id,
        estimated_weight_kg=biomass.estimated_weight_kg,
        calculation_date=str(biomass.calculation_date)
    )


@router.put("/{biomass_id}", response_model=BiomassRequest)
def update_biomass(biomass_id: int, request: BiomassRequest, db=Depends(get_db)):
    biomass = db.query(BiomassModel).filter(
        BiomassModel.id == biomass_id).first()
    if not biomass:
        raise HTTPException(status_code=404, detail="Biomass not found")
    biomass.pond_id = request.pond_id
    biomass.estimated_weight_kg = request.estimated_weight_kg
    biomass.calculation_date = request.calculation_date
    db.commit()
    db.refresh(biomass)
    return BiomassRequest(
        id=biomass.id,
        pond_id=biomass.pond_id,
        estimated_weight_kg=biomass.estimated_weight_kg,
        calculation_date=str(biomass.calculation_date)
    )


@router.delete("/{biomass_id}", status_code=204)
def delete_biomass(biomass_id: int, db=Depends(get_db)):
    biomass = db.query(BiomassModel).filter(
        BiomassModel.id == biomass_id).first()
    if not biomass:
        raise HTTPException(status_code=404, detail="Biomass not found")
    db.delete(biomass)
    db.commit()
    return None


# get_db is now defined at the top of the file, so this duplicate can be removed.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BiomassRequest, status_code=201)
def create_biomass(request: BiomassRequest, user=Depends(get_current_user), db=Depends(get_db)):
    repo = BiomassMySQLRepository(db)
    biomass = Biomass(
        id=0,
        pond_id=request.pond_id,
        estimated_weight_kg=request.estimated_weight_kg,
        calculation_date=request.calculation_date
    )
    created = repo.create(biomass)
    return BiomassRequest(
        id=created.id,
        pond_id=created.pond_id,
        estimated_weight_kg=created.estimated_weight_kg,
        calculation_date=str(created.calculation_date)
    )


@router.get("/", response_model=List[BiomassRequest])
def list_biomass(user=Depends(get_current_user), db=Depends(get_db)):
    repo = BiomassMySQLRepository(db)
    # Si quieres todos los registros:
    biomass_list = db.query(BiomassModel).all()
    return [
        BiomassRequest(
            id=b.id,
            pond_id=b.pond_id,
            estimated_weight_kg=b.estimated_weight_kg,
            calculation_date=str(b.calculation_date)
        ) for b in biomass_list
    ]
