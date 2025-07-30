from sqlalchemy.orm import Session
from src.api.notifications.domain.notification_repository import NotificationRepository
from src.api.notifications.domain.notification import Notification
from src.db.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from typing import Optional, List


from src.api.notifications.infrastructure.models import NotificationModel


class NotificationMySQLRepository(NotificationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        notification = self.db.query(NotificationModel).filter(
            NotificationModel.id == notification_id).first()
        return self._to_domain(notification) if notification else None

    def create(self, notification: Notification) -> Notification:
        db_notification = NotificationModel(
            user_id=notification.user_id,
            pond_id=notification.pond_id,
            message=notification.message,
            type=notification.type,
            is_read=notification.is_read
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return self._to_domain(db_notification)

    def list_by_user(self, user_id: int) -> List[Notification]:
        notifications = self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id).all()
        return [self._to_domain(n) for n in notifications]

    def _to_domain(self, notification_model: NotificationModel) -> Notification:
        return Notification(
            id=notification_model.id,
            user_id=notification_model.user_id,
            pond_id=notification_model.pond_id,
            message=notification_model.message,
            type=notification_model.type,
            is_read=notification_model.is_read,
            created_at=notification_model.created_at
        )
