# src/sensors/domain/repositories/water_level_repository.py
from sqlalchemy import text
from src.core.db.connection import SessionLocal

class WaterLevelRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, value: str) -> int:
        sql = text("INSERT INTO Water_Level (value) VALUES (:value)")
        result = self.db.execute(sql, {"value": value})
        self.db.commit()
        return result.lastrowid 
