# src/pigua/infrastructure/routes.py

from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, Query
from src.pigua.infrastructure.handlers.dependencies import get_pigua_use_case
from src.pigua.domain.entities import PiguaCreate, Pigua

from src.pigua.application.weight_trend_service import PiguaWeightTrendService

router = APIRouter(
    prefix="/pigua",
    tags=["Pigua"]
)

@router.post("/", response_model=Pigua)
def create_pigua(pigua: PiguaCreate, use_case = Depends(get_pigua_use_case)):
    return use_case.execute(pigua)


trend_service = PiguaWeightTrendService()

@router.get("/weight-trend")
def get_weight_trend(
    pond_id: int = Query(None, description="ID del estanque (opcional)")
):
    return trend_service.get_weight_trend(pond_id)