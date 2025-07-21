# src/sensors/infrastructure/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.db.connection import get_db
from src.reading.domain.entities import ReadingCreate, Reading
from src.reading.application.reading_service import ReadingService
from src.reading.infrastructure.adapters.reading_mysql import ReadingRepository

router = APIRouter(
    prefix="/readings",
    tags=["readings"],
    responses={404: {"description": "Not found"}}
)

def get_reading_repository(db: Session = Depends(get_db)) -> ReadingRepository:
    return ReadingRepository(db)

def get_reading_service(repo: ReadingRepository = Depends(get_reading_repository)) -> ReadingService:
    return ReadingService(repo)

@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva lectura",
    responses={
        201: {"description": "Lectura creada exitosamente"},
        400: {"description": "Datos inválidos proporcionados"}
    }
)
async def create_reading(
    reading: ReadingCreate,
    service: ReadingService = Depends(get_reading_service)
):
    """
    Crea una nueva lectura de sensor con los siguientes datos:
    - **turbidity_id**: ID de turbidez (opcional)
    - **water_level_id**: ID de nivel de agua (opcional)
    - **temperature_id**: ID de temperatura (opcional)
    - **weight_id**: ID de peso (opcional)
    - **date**: Fecha y hora de la lectura
    """
    try:
        reading_id = service.create_reading(reading)
        return {
            "message": "Reading created successfully",
            "reading_id": reading_id,
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[Reading],
    summary="Obtener todas las lecturas",
    responses={
        200: {"description": "Lista de lecturas obtenida exitosamente"}
    }
)
async def get_all_readings(
    service: ReadingService = Depends(get_reading_service)
):
    """
    Obtiene todas las lecturas de sensores registradas en el sistema.
    """
    return service.get_all_readings()

@router.get(
    "/{reading_id}",
    response_model=Reading,
    summary="Obtener una lectura específica",
    responses={
        200: {"description": "Lectura encontrada"},
        404: {"description": "Lectura no encontrada"}
    }
)
async def get_reading_by_id(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service)
):
    """
    Obtiene una lectura específica por su ID.

    - **reading_id**: El ID de la lectura a recuperar
    """
    reading = service.get_reading_by_id(reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading with ID {reading_id} not found"
        )
    return reading