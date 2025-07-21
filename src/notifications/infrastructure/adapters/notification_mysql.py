from sqlalchemy import text
from typing import List

from src.core.db.connection import SessionLocal
from src.notifications.domain.entities import Notification, NotificationCreate

class NotificationRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create_notification(self, notification: NotificationCreate) -> Notification:
        sql = text("""
            INSERT INTO Notification (reading_id, message)
            VALUES (:reading_id, :message)
        """)
        params = {
            "reading_id": notification.reading_id,
            "message": notification.message
        }
        result = self.db.execute(sql, params)
        self.db.commit()

        notification_id = result.lastrowid

        row = self.db.execute(
            text("SELECT created_at FROM Notification WHERE notification_id = :id"),
            {"id": notification_id}
        ).fetchone()

        return Notification(
            notification_id=notification_id,
            reading_id=notification.reading_id,
            message=notification.message,
            created_at=row._mapping["created_at"]
        )

    def get_all_notifications(self) -> List[Notification]:
        sql = text("SELECT * FROM Notification ORDER BY created_at DESC")
        result = self.db.execute(sql).fetchall()
        return [dict(row._mapping) for row in result]
