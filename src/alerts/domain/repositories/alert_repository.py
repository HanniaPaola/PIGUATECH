from abc import ABC, abstractmethod
from src.alerts.domain.entities import AlertCreate

class IAlertRepository(ABC):
    @abstractmethod
    def create_alert(self, alert: AlertCreate) -> int:
        pass
