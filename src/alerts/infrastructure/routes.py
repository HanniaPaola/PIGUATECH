# src/alerts/infrastructure/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.core.db.connection import get_db
from src.alerts.infrastructure.adapters.alert_Mysql import AlertRepository
from src.alerts.application.alert_service import AlertService
from src.alerts.domain.entities import Alert, AlertCreate

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

def get_alert_repo(db: Session = Depends(get_db)):
    return AlertRepository(db)

def get_alert_service(repo: AlertRepository = Depends(get_alert_repo)):
    return AlertService(repo)

@router.post("/", response_model=dict)
async def create_alert(alert: AlertCreate, service: AlertService = Depends(get_alert_service)):
    alert_id = service.create_alert(alert.reading_id, alert.status)
    return {"msg": "Alert created", "alert_id": alert_id}

@router.get("/", response_model=List[Alert])
async def get_all_alerts(service: AlertService = Depends(get_alert_service)):
    return service.get_all_alerts()

@router.patch("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, service: AlertService = Depends(get_alert_service)):
    service.resolve_alert(alert_id)
    return {"msg": f"Alert {alert_id} marked as resolved"}
