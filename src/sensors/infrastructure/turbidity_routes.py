from fastapi import APIRouter, Depends
from src.core.db.connection import get_db
from src.sensors.domain.repositories.turbidity_repository import TurbidityRepository
from src.auth.infrastructure.security import get_current_user, require_acuicultor

router = APIRouter(prefix="/turbidity", tags=["turbidity"])

@router.get("/trend")
def get_turbidity_trend(
    db=Depends(get_db),
    user: dict = Depends(require_acuicultor)
):
    repo = TurbidityRepository(db)
    data = repo.get_last_week_trend()
    if not data:
        return {"last_value": None, "trend": None, "series": [], "categories": []}

    series = [row[0] for row in data]
    last_value = series[-1]
    prev_value = series[0]
    trend = round(((last_value - prev_value) / prev_value) * 100, 2) if prev_value else 0

    categories = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return {
        "last_value": last_value,
        "trend": trend,
        "series": series,
        "categories": categories[-len(series):]
    }

    

# Ejemplo supervisor
@router.get("/supervisor-area")
def supervisor_area(user: dict = Depends(require_acuicultor)):
    return {"message": f"Hola supervisor {user['sub']}!"}

# Ejemplo acuicultor
#@router.get("/acuicultor-area")
#def acuicultor_area(user: dict = Depends(require_acuicultor)):
#    return {"message": f"Hola acuicultor {user['sub']}!"}