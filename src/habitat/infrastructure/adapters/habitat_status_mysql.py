from sqlalchemy import text

class HabitatStatusRepository:
    def __init__(self, db):
        self.db = db

    def get_latest_reading(self):
        sql = text("""
            SELECT r.*, 
                   t.value AS temperature_value,
                   tb.value AS turbidity_value,
                   wl.value AS water_level_value,
                   w.weight AS weight_value
            FROM Reading r
            LEFT JOIN Temperature t ON r.temperature_id = t.temperature_id
            LEFT JOIN Turbidity tb ON r.turbidity_id = tb.turbidity_id
            LEFT JOIN Water_Level wl ON r.water_level_id = wl.water_level_id
            LEFT JOIN Weight w ON r.weight_id = w.weight_id
            ORDER BY r.date DESC LIMIT 1
        """)
        result = self.db.execute(sql).fetchone()
        return dict(result._mapping) if result else None

    def get_parameters(self):
        sql = text("SELECT * FROM Parameter")
        result = self.db.execute(sql).fetchall()
        return [dict(row._mapping) for row in result]
