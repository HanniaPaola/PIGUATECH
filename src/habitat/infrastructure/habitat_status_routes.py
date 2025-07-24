from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db.connection import get_db
from src.habitat.infrastructure.adapters.habitat_status_mysql import HabitatStatusRepository
from src.habitat.application.habitat_status_service import HabitatStatusService
from src.habitat.domain.habitat_status import HabitatStatusResponse

router = APIRouter(
    prefix="/api/habitat-status",
    tags=["habitat-status"]
)

# Factories
def get_repo(db: Session = Depends(get_db)):
    return HabitatStatusRepository(db)

def get_service(repo: HabitatStatusRepository = Depends(get_repo)):
    return HabitatStatusService(repo)

@router.get("/", response_model=HabitatStatusResponse)
async def get_status(service: HabitatStatusService = Depends(get_service)):
    result = service.get_habitat_status()
    if not result:
        return {"message": "No data available"}
    return result


