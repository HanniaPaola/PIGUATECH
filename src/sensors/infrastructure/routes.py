# src/sensors/infrastructure/routes.py

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from src.core.db.connection import SessionLocal
from src.sensors.application.reading_service import ReadingService
from src.sensors.domain.entities.temperature import TemperatureData
from src.sensors.domain.repositories.temperature_repository import TemperatureRepository

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

@router.get("/latest-temperature", response_model=TemperatureData)
async def get_latest_temperature():
    db = SessionLocal()
    try:
        # Consulta optimizada
        result = db.execute(
            text("""
                SELECT 
                    t.value, 
                    r.date,
                    p.pond_id
                FROM Reading r
                INNER JOIN Temperature t ON r.temperature_id = t.temperature_id
                LEFT JOIN Pond p ON r.pond_id = p.pond_id
                ORDER BY r.date DESC 
                LIMIT 1
            """)
        ).fetchone()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron registros de temperatura"
            )

        # Procesamiento seguro del valor de temperatura
        temp_value = result[0]
        
        # Si es string, intentar extraer el valor numérico
        if isinstance(temp_value, str):
            try:
                # Eliminar unidades y espacios, luego convertir a float
                temp_value = float(temp_value.replace('°C', '').strip())
            except ValueError:
                # Si falla la conversión, mantener el string original
                pass
        # Si ya es float/número, dejarlo como está

        return {
            "value": temp_value,  # Puede ser float o string
            "timestamp": result[1].isoformat(),
            "pond_id": result[2] if result[2] is not None else "N/A"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener la temperatura: {str(e)}"
        )
    finally:
        db.close()
    
@router.get("/weight-trend", summary="Tendencia de peso promedio por semana")
def get_weekly_weight_trend(
    pond_id: int = Query(None, description="ID del estanque (opcional)"),
    weeks: int = Query(12, description="Cantidad de semanas a consultar")
):
    return service.get_weekly_weight_trend(pond_id, weeks)


