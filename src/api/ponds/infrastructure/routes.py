from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from ...ponds.domain.pond import Pond
from ...ponds.infrastructure.pond_mysql import PondMySQLRepository
from ...users.infrastructure.routes import get_current_user
from src.db.database import SessionLocal
from fastapi import Depends
from typing import List

router = APIRouter(prefix="/api/ponds", tags=["ponds"])


class PondRequest(BaseModel):
    name: str
    location: str
    description: str = None
    water_volume_m3: float = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_pond(request: PondRequest, user=Depends(get_current_user), db=Depends(get_db)):
    if user["role"] != "acuicultor":
        raise HTTPException(
            status_code=403, detail="Only acuicultor can create ponds")
    repo = PondMySQLRepository(db)
    pond = Pond(
        id=0,
        acuicultor_id=user["id"],
        name=request.name,
        location=request.location,
        description=request.description,
        water_volume_m3=request.water_volume_m3,
        created_at=None
    )
    created = repo.create(pond)
    return {"success": True, "data": {"id": created.id, "name": created.name, "location": created.location}}


@router.get("/", response_model=List[PondRequest])
def list_ponds(user=Depends(get_current_user), db=Depends(get_db)):
    repo = PondMySQLRepository(db)
    ponds = repo.list_by_acuicultor(user["id"])
    return [PondRequest(
        name=p.name,
        location=p.location,
        description=p.description,
        water_volume_m3=p.water_volume_m3
    ) for p in ponds]
