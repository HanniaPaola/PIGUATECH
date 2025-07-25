# src/sensors/infrastructure/routes.py

from fastapi import APIRouter, Query
from sqlalchemy import text
from src.core.db.connection import SessionLocal
from src.sensors.application.reading_service import ReadingService
from src.sensors.domain.entities.temperature import TemperatureData
from src.sensors.domain.repositories.temperature_repository import TemperatureRepository

router = APIRouter(
    prefix="/readingsSensor",
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

@router.get("/latest-temperatures", response_model=TemperatureData)
async def get_latest_temperature():
    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT t.value, r.date 
                FROM Temperature t
                JOIN Reading r ON t.temperature_id = r.temperature_id
                ORDER BY r.date DESC LIMIT 1
            """)
        ).fetchone()
        return {"value": float(result[0]), "timestamp": result[1].isoformat()}
    finally:
        db.close()
    
@router.get("/weight-trend", summary="Tendencia de peso promedio por mes")
def get_weight_trend(
    pond_id: int = Query(None, description="ID del estanque (opcional)")
):
    return service.get_weight_trend(pond_id)

