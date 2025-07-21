from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.core.db.connection import get_db
from src.notifications.infrastructure.adapters.notification_mysql import NotificationRepository
from src.notifications.application.notification_service import NotificationService
from src.notifications.domain.entities import Notification, NotificationCreate

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

def get_notification_repo(db: Session = Depends(get_db)):
    return NotificationRepository()

def get_notification_service(repo: NotificationRepository = Depends(get_notification_repo)):
    return NotificationService(repo)

@router.post("/", response_model=Notification)
async def create_notification(
    notification: NotificationCreate,
    service: NotificationService = Depends(get_notification_service)
):
    return service.create_notification(notification)

@router.get("/", response_model=List[Notification])
async def get_all_notifications(
    service: NotificationService = Depends(get_notification_service)
):
    return service.get_all_notifications()
