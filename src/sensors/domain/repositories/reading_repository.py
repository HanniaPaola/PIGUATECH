# src/sensors/domain/repositories/reading_repository.py
from sqlalchemy import text
from datetime import datetime

class ReadingRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, turbidity_id, water_level_id, temperature_id, weight_id):
        sql = text("""
            INSERT INTO Reading (turbidity_id, water_level_id, temperature_id, weight_id, date)
            VALUES (:turbidity_id, :water_level_id, :temperature_id, :weight_id, :date)
        """)
        params = {
            "turbidity_id": turbidity_id,
            "water_level_id": water_level_id,
            "temperature_id": temperature_id,
            "weight_id": weight_id,
            "date": datetime.now()
        }
        self.db.execute(sql, params)
        self.db.commit()
