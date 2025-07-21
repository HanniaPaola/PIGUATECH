# src/sensors/infrastructure/routes.py

from fastapi import APIRouter, Query
from src.sensors.application.reading_service import ReadingService

router = APIRouter(
    prefix="/readings",
    tags=["readings"]
)

service = ReadingService()

@router.get("/summary", summary="Resumen de lecturas (semanal, mensual, trimestral)")
def get_summary(
    period: str = Query(default="weekly", enum=["weekly", "monthly", "quarterly"]),
    pond_id: int = Query(None, description="ID del estanque (opcional)")
):
    return service.get_summary(period, pond_id)

@router.get("/trend", summary="Tendencia de lecturas")
def get_trend(
    start_date: str = Query(..., description="Fecha inicio YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha fin YYYY-MM-DD"),
    pond_id: int = Query(None, description="ID del estanque (opcional)")
):
    return service.get_trend(start_date, end_date, pond_id)


@router.get("/temperature-trend", summary="Tendencia de temperatura")
def get_temperature_trend(
    period: str = Query(default="daily", enum=["daily", "weekly", "monthly"]),
    pond_id: int = Query(None)
):
    return service.get_temperature_trend(period, pond_id)
