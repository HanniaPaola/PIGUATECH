from src.notifications.infrastructure.adapters.notification_mysql import NotificationRepository
from src.notifications.domain.entities import NotificationCreate

class NotificationService:
    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    def create_notification(self, notification: NotificationCreate):
        return self.repo.create_notification(notification)

    def get_all_notifications(self):
        return self.repo.get_all_notifications()
