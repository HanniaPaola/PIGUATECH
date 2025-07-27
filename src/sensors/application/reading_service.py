from fastapi import HTTPException
from sqlalchemy import text

from datetime import datetime, timedelta


from sqlalchemy import Column, Integer, ForeignKey, DateTime
from src.core.db.connection import Base
from sqlalchemy import select, func, extract, table


from src.core.db.connection import SessionLocal
from src.sensors.domain.repositories import reading_repository, temperature_repository, water_level_repository, weight_repository, turbidity_repository


class Reading(Base):
    __tablename__ = "Reading"
    
    reading_id = Column(Integer, primary_key=True)
    turbidity_id = Column(Integer, ForeignKey("Turbidity.turbidity_id"))
    water_level_id = Column(Integer, ForeignKey("WaterLevel.water_level_id"))
    temperature_id = Column(Integer, ForeignKey("Temperature.temperature_id"))
    weight_id = Column(Integer, ForeignKey("Weight.weight_id"))
    pond_id = Column(Integer, ForeignKey("Pond.pond_id"))
    date = Column(DateTime)

class ReadingService:
    def __init__(self):
        self.db = SessionLocal()
        

    def get_summary(self, period: str = "weekly", pond_id: int = None):
        today = datetime.today()

        if period == "weekly":
            start_date = today - timedelta(days=7)
        elif period == "monthly":
            start_date = today - timedelta(days=30)
        elif period == "quarterly":
            start_date = today - timedelta(days=90)
        else:
            raise ValueError("Invalid period")

        query = self.db.query(
            func.avg(temperature_repository.value).label("temperature_avg"),
            func.avg(water_level_repository.value).label("water_level_avg"),
            func.avg(weight_repository.weight).label("weight_avg"),
            func.avg(turbidity_repository.value).label("turbidity_avg"),
            func.count(reading_repository.reading_id).label("readings_count")
        ).join(
            temperature_repository, reading_repository.temperature_id == temperature_repository.temperature_id, isouter=True
        ).join(
            water_level_repository, reading_repository.water_level_id == water_level_repository.water_level_id, isouter=True
        ).join(
            weight_repository, reading_repository.weight_id == weight_repository.weight_id, isouter=True
        ).join(
            turbidity_repository, reading_repository.turbidity_id == turbidity_repository.turbidity_id, isouter=True
        ).filter(
            reading_repository.date >= start_date
        )

        if pond_id:
            query = query.filter(reading_repository.pond_id == pond_id)

        result = query.one()
        return {
            "period": period,
            "temperature_avg": float(result.temperature_avg) if result.temperature_avg else None,
            "water_level_avg": float(result.water_level_avg) if result.water_level_avg else None,
            "weight_avg": float(result.weight_avg) if result.weight_avg else None,
            "turbidity_avg": float(result.turbidity_avg) if result.turbidity_avg else None,
            "readings_count": result.readings_count
        }

    def get_trend(self, start_date: str, end_date: str, pond_id: int = None):
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)

        query = self.db.query(
            reading_repository.date,
            temperature_repository.value.label("temperature"),
            turbidity_repository.value.label("turbidity"),
            water_level_repository.value.label("water_level"),
            weight_repository.weight.label("weight")
        ).join(
            temperature_repository, reading_repository.temperature_id == temperature_repository.temperature_id, isouter=True
        ).join(
            turbidity_repository, reading_repository.turbidity_id == turbidity_repository.turbidity_id, isouter=True
        ).join(
            water_level_repository, reading_repository.water_level_id == water_level_repository.water_level_id, isouter=True
        ).join(
            weight_repository, reading_repository.weight_id == weight_repository.weight_id, isouter=True
        ).filter(
            reading_repository.date >= start_dt,
            reading_repository.date <= end_dt
        )

        if pond_id:
            query = query.filter(reading_repository.pond_id == pond_id)

        query = query.order_by(reading_repository.date.asc())

        result = query.all()

        return [
            {
                "date": row.date.isoformat(),
                "temperature": float(row.temperature) if row.temperature else None,
                "turbidity": float(row.turbidity) if row.turbidity else None,
                "water_level": float(row.water_level) if row.water_level else None,
                "weight": float(row.weight) if row.weight else None
            }
            for row in result
        ]
        

    def get_temperature_trend(self, period: str = "daily", pond_id: int = None):
        today = datetime.today()

        if period == "daily":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            start_date = today - timedelta(days=7)
        elif period == "monthly":
            start_date = today - timedelta(days=30)
        else:
            raise ValueError("Invalid period")

        query = self.db.query(
            reading_repository.date,
            temperature_repository.value.label("temperature")
        ).join(
            temperature_repository, reading_repository.temperature_id == temperature_repository.temperature_id
        ).filter(
            reading_repository.date >= start_date
        )

        if pond_id:
            query = query.filter(reading_repository.pond_id == pond_id)

        query = query.order_by(reading_repository.date.asc())

        results = query.all()

        return [
            {
                "date": row.date.isoformat(),
                "temperature": float(row.temperature)
            }
            for row in results if row.temperature is not None
        ]
        
    from sqlalchemy import select, func, extract, table

    def get_weekly_weight_trend(self, pond_id=None, weeks=12):
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Consulta de diagnóstico
        diagnostic_sql = """
        SELECT 
            COUNT(r.reading_id) as total_readings,
            COUNT(DISTINCT r.pond_id) as ponds_with_data,
            MIN(r.date) as earliest_date,
            MAX(r.date) as latest_date
        FROM Reading r
        JOIN Weight w ON r.weight_id = w.weight_id
        WHERE r.date BETWEEN :start_date AND :end_date
        {pond_condition}
        """.format(
            pond_condition="AND r.pond_id = :pond_id" if pond_id else ""
        )
        
        diagnostic_params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        if pond_id:
            diagnostic_params["pond_id"] = pond_id
        
        # Ejecutar consulta de diagnóstico
        diagnostic_result = self.db.execute(text(diagnostic_sql), diagnostic_params).fetchone()
        
        # Si no hay datos, retornar el diagnóstico
        if diagnostic_result.total_readings == 0:
            return {
                "status": "success",
                "data": [],
                "diagnostics": {
                    "total_readings": diagnostic_result.total_readings,
                    "ponds_with_data": diagnostic_result.ponds_with_data,
                    "date_range": {
                        "earliest": diagnostic_result.earliest_date.isoformat() if diagnostic_result.earliest_date else None,
                        "latest": diagnostic_result.latest_date.isoformat() if diagnostic_result.latest_date else None
                    },
                    "message": "No se encontraron datos para el rango especificado"
                }
            }
        
        # Consulta principal (original)
        sql = """
        SELECT 
            YEAR(r.date) AS year,
            WEEK(r.date, 1) AS week_number,
            MIN(DATE_FORMAT(r.date, '%Y-%m-%d')) AS week_start,
            AVG(w.weight) AS avg_weight,
            COUNT(*) AS readings_count
        FROM Reading r
        JOIN Weight w ON r.weight_id = w.weight_id
        JOIN Pond p ON r.pond_id = p.pond_id
        JOIN Pigua pg ON p.pigua_id = pg.pigua_id
        WHERE r.date BETWEEN :start_date AND :end_date
        {pond_condition}
        GROUP BY YEAR(r.date), WEEK(r.date, 1)
        ORDER BY year, week_number
        """.format(
            pond_condition="AND r.pond_id = :pond_id" if pond_id else ""
        )
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        if pond_id:
            params["pond_id"] = pond_id
        
        try:
            result = self.db.execute(text(sql), params).fetchall()
            
            if not result:
                return {
                    "status": "success",
                    "data": [],
                    "diagnostics": {
                        "total_readings": diagnostic_result.total_readings,
                        "ponds_with_data": diagnostic_result.ponds_with_data,
                        "date_range": {
                            "earliest": diagnostic_result.earliest_date.isoformat() if diagnostic_result.earliest_date else None,
                            "latest": diagnostic_result.latest_date.isoformat() if diagnostic_result.latest_date else None
                        },
                        "message": "La consulta no devolvió resultados a pesar de haber datos"
                    }
                }
            
            return {
                "status": "success",
                "data": [
                    {
                        "year": row.year,
                        "week": row.week_number,
                        "week_start": row.week_start,
                        "avg_weight": float(row.avg_weight) if row.avg_weight else None,
                        "readings_count": row.readings_count
                    }
                    for row in result
                ],
                "diagnostics": {
                    "total_readings": diagnostic_result.total_readings,
                    "date_range": {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                }
            }
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "diagnostics": {
                        "total_readings": diagnostic_result.total_readings,
                        "ponds_with_data": diagnostic_result.ponds_with_data,
                        "date_range": {
                            "earliest": diagnostic_result.earliest_date.isoformat() if diagnostic_result.earliest_date else None,
                            "latest": diagnostic_result.latest_date.isoformat() if diagnostic_result.latest_date else None
                        }
                    }
                }
            )