from sqlalchemy import func
from sqlalchemy import extract, func
from datetime import datetime, timedelta

from src.core.db.connection import SessionLocal
from src.sensors.domain.repositories import reading_repository, temperature_repository, water_level_repository, weight_repository, turbidity_repository


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
        
    def get_weight_trend(self, pond_id=None):
        query = self.db.query(
            extract('month', reading_repository.date).label('month'),
            func.avg(weight_repository.weight).label('avg_weight')
        ).join(
            weight_repository, reading_repository.weight_id == weight_repository.weight_id
        )

        if pond_id:
            query = query.filter(reading_repository.pond_id == pond_id)

        query = query.group_by(
            extract('month', reading_repository.date)
        ).order_by(
            extract('month', reading_repository.date)
        )

        result = query.all()

        return [
            {"month": int(row.month), "avg_weight": float(row.avg_weight)}
            for row in result if row.avg_weight is not None
        ]

