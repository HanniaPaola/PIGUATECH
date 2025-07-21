# src/alerts/infrastructure/alert_repository.py

from sqlalchemy import text

class AlertRepository:
    def __init__(self, db):
        self.db = db

    def create_alert(self, reading_id, status):
        sql = text("""
            INSERT INTO Alert (reading_id, status)
            VALUES (:reading_id, :status)
        """)
        params = {
            "reading_id": reading_id,
            "status": status
        }
        result = self.db.execute(sql, params)
        self.db.commit()
        return result.lastrowid

    def resolve_alert(self, alert_id: int):
        sql = text("""
            UPDATE Alert SET status = 'resolved' WHERE alert_id = :alert_id
        """)
        self.db.execute(sql, {"alert_id": alert_id})
        self.db.commit()
        
    def get_all_alerts(self):
        sql = text("SELECT * FROM Alert")
        result = self.db.execute(sql).fetchall()
        return [dict(row._mapping) for row in result]
