# src/pond/infrastructure/routes.py
from fastapi import APIRouter, Depends, HTTPException
from src.pond.infrastructure.handlers.dependencies import get_pond_use_case
from src.pond.domain.entities import PondCreate, Pond

router = APIRouter(
    prefix="/ponds",
    tags=["Ponds"]
)

@router.post("/", response_model=Pond)
def create_pond(pond: PondCreate, use_case = Depends(get_pond_use_case)):
    try:
        return use_case.execute(pond)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
