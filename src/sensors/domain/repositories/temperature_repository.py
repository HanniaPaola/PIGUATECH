# src/sensors/domain/repositories/temperature_repository.py
from sqlalchemy import text
from src.core.db.connection import SessionLocal

class TemperatureRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, value: str) -> int:
        sql = text("INSERT INTO Temperature (value) VALUES (:value)")
        result = self.db.execute(sql, {"value": value})
        self.db.commit()
        return result.lastrowid
