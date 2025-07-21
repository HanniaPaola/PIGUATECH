from sqlalchemy import text
from fastapi import HTTPException
from src.core.db.connection import SessionLocal
from src.reading.domain.entities import Reading, ReadingCreate

class ReadingRepository:
    def __init__(self, db):
        self.db = db

    def create_reading(self, reading_data):
        try:
            sql = text("""
                INSERT INTO Reading 
                (pond_id, turbidity_id, water_level_id, temperature_id, weight_id, date)
                VALUES 
                (:pond_id, :turbidity_id, :water_level_id, :temperature_id, :weight_id, :date)
            """)
            params = {
                'pond_id': reading_data.pond_id,
                'turbidity_id': reading_data.turbidity_id,
                'water_level_id': reading_data.water_level_id,
                'temperature_id': reading_data.temperature_id,
                'weight_id': reading_data.weight_id,
                'date': reading_data.date.isoformat()
            }
            result = self.db.execute(sql, params)
            self.db.commit()
            return result.lastrowid
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Error creating reading: {str(e)}"
            )

    def get_all_readings(self):
        result = self.db.execute(text("SELECT * FROM Reading")).fetchall()
        return [dict(row._mapping) for row in result]

    def get_reading_by_id(self, reading_id: int):
        try:
            result = self.db.execute(
                text("SELECT * FROM Reading WHERE reading_id = :reading_id"),
                {"reading_id": reading_id}
            ).fetchone()
            
            if not result:
                return None

            reading = dict(result._mapping)
            if 'date' in reading and reading['date']:
                reading['date'] = reading['date'].isoformat()
            return reading
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )


    def get_readings_by_date_range(self, start_date, end_date, pond_id=None):
        sql = "SELECT * FROM Reading WHERE date BETWEEN :start_date AND :end_date"
        params = {"start_date": start_date, "end_date": end_date}
        if pond_id:
            sql += " AND pond_id = :pond_id"
            params["pond_id"] = pond_id
        sql += " ORDER BY date ASC"
        result = self.db.execute(text(sql), params).fetchall()
        return [dict(row._mapping) for row in result]