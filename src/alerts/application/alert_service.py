# src/alerts/application/alert_service.py

from src.alerts.infrastructure.adapters.alert_Mysql import AlertRepository

class AlertService:
    def __init__(self, repo: AlertRepository):
        self.repo = repo

    def create_alert(self, reading_id: int, status: str):
        return self.repo.create_alert(reading_id, status)

    def get_all_alerts(self):
        return self.repo.get_all_alerts()

    def resolve_alert(self, alert_id: int):
        self.repo.resolve_alert(alert_id)
