# src/sensors/domain/repositories/turbidity_repository.py
from sqlalchemy import text
#from src.core.db.connection import SessionLocal

class TurbidityRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, value: str) -> int:
        sql = text("INSERT INTO Turbidity (value) VALUES (:value)")
        result = self.db.execute(sql, {"value": value})
        self.db.commit()
        return result.lastrow

    def get_last_week_trend(self):
        sql = text("""
            SELECT t.value, r.date
            FROM Turbidity t
            JOIN Reading r ON t.turbidity_id = r.turbidity_id
            ORDER BY r.date DESC
            LIMIT 7
        """)
        result = self.db.execute(sql).fetchall()
        data = [(float(row[0]), row[1]) for row in result]
        data.reverse()
        return data
