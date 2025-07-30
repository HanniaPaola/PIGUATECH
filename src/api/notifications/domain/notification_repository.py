from abc import ABC, abstractmethod
from typing import Optional, List
from .notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        pass

    @abstractmethod
    def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Notification]:
        pass
