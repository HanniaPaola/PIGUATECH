from fastapi import APIRouter, HTTPException
from src.reading.domain.entities import ReadingCreate
from src.reading.application.reading_service import ReadingService  

router = APIRouter(prefix="/readings", tags=["readings"])

reading_service = ReadingService()

@router.post("/", response_model=dict, summary="Crear una nueva lectura")
def create_reading(reading: ReadingCreate):
    try:
        reading_id = reading_service.create(reading)
        return {
            "msg": "Reading created successfully",
            "reading_id": reading_id
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/{reading_id}", response_model=Reading, summary="Obtener lectura por ID")
def get_reading_by_id(reading_id: int):
    reading = reading_service.get_reading_by_id(reading_id)
    if not reading:
        raise HTTPException(
            status_code=404,
            detail=f"Reading with ID {reading_id} not found"
        )
    return reading

