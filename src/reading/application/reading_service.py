# src/reading/application/reading_service.py

from typing import List
from fastapi import HTTPException

from src.reading.domain.entities import ReadingCreate
from src.reading.infrastructure.adapters.reading_mysql import ReadingRepository

from src.alerts.infrastructure.adapters.alert_Mysql import AlertRepository
from src.alerts.application.alert_service import AlertService

from src.notifications.infrastructure.adapters.notification_mysql import NotificationRepository
from src.notifications.application.notification_service import NotificationService
from src.notifications.domain.entities import NotificationCreate

from src.core.db.connection import SessionLocal


class ReadingService:
    def __init__(self, repo: ReadingRepository = None):
        self.repo = repo or ReadingRepository()

    def create_reading(self, reading_data: ReadingCreate) -> int:
        """Crea lectura, dispara verificación de alertas y notificaciones"""
        reading_id = self.repo.create_reading(reading_data)
        self.check_alerts_and_notifications(reading_id, reading_data)
        return reading_id

    def get_all_readings(self) -> List[dict]:
        return self.repo.get_all_readings()

    def get_reading_by_id(self, reading_id: int) -> dict:
        reading = self.repo.get_reading_by_id(reading_id)
        if not reading:
            raise HTTPException(
                status_code=404,
                detail=f"Reading {reading_id} not found"
            )
        return reading

    def check_alerts_and_notifications(self, reading_id: int, reading_data: ReadingCreate):
        """Evalúa reglas y guarda alertas y notificaciones"""
        alerts = []
        notifications = []

        db = SessionLocal()
        alert_repo = AlertRepository(db)
        alert_service = AlertService(alert_repo)

        notif_repo = NotificationRepository()
        notif_service = NotificationService(notif_repo)

        # Regla de ejemplo: turbidez alta
        if reading_data.turbidity_id:
            turbidity = self.repo.get_sensor_value('Turbidity', reading_data.turbidity_id)
            if turbidity and float(turbidity) > 50:
                alerts.append("High turbidity detected!")
                notifications.append("La turbidez ha superado el nivel crítico.")

        # Puedes agregar más reglas:
        # if reading_data.temperature_id:
        #     temperature = ...
        #     if ...:
        #         alerts.append(...)
        #         notifications.append(...)

        for msg in alerts:
            alert_service.create_alert(reading_id, msg)

        for msg in notifications:
            notif_service.create_notification(NotificationCreate(
                reading_id=reading_id,
                message=msg
            ))

        db.close()
