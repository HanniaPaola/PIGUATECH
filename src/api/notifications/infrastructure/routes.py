from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from ...notifications.domain.notification import Notification
from ...notifications.infrastructure.notification_mysql import NotificationMySQLRepository
from ...users.infrastructure.routes import get_current_user
from src.db.database import SessionLocal
from typing import List

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class NotificationRequest(BaseModel):
    id: int | None = None
    pond_id: int
    message: str
    type: str
    is_read: bool | None = None
    created_at: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=NotificationRequest, status_code=201)
def create_notification(request: NotificationRequest, user=Depends(get_current_user), db=Depends(get_db)):
    repo = NotificationMySQLRepository(db)
    notification = Notification(
        id=0,
        user_id=user["id"],
        pond_id=request.pond_id,
        message=request.message,
        type=request.type,
        is_read=False,
        created_at=None
    )
    created = repo.create(notification)
    return NotificationRequest(
        id=created.id,
        pond_id=created.pond_id,
        message=created.message,
        type=created.type,
        is_read=created.is_read,
        created_at=str(created.created_at) if created.created_at else None
    )


@router.get("/", response_model=List[NotificationRequest])
def list_notifications(user=Depends(get_current_user), db=Depends(get_db)):
    repo = NotificationMySQLRepository(db)
    notifications = repo.list_by_user(user["id"])
    return [NotificationRequest(
        id=n.id,
        pond_id=n.pond_id,
        message=n.message,
        type=n.type,
        is_read=n.is_read,
        created_at=str(n.created_at) if n.created_at else None
    ) for n in notifications]
