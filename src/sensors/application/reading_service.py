import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from sqlalchemy import func, text
from src.core.db.connection import SessionLocal

from src.reading.domain.reading import Reading
from src.sensors.domain.repositories.temperature_repository import TemperatureRepository
from src.sensors.domain.entities.temperature import TemperatureData

from src.sensors.domain.repositories import (
    temperature_repository,
    weight_repository,
    water_level_repository,
    turbidity_repository
)


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
            func.count(Reading.reading_id).label("readings_count")
        ).join(
            temperature_repository, Reading.temperature_id == temperature_repository.temperature_id, isouter=True
        ).join(
            water_level_repository, Reading.water_level_id == water_level_repository.water_level_id, isouter=True
        ).join(
            weight_repository, Reading.weight_id == weight_repository.weight_id, isouter=True
        ).join(
            turbidity_repository, Reading.turbidity_id == turbidity_repository.turbidity_id, isouter=True
        ).filter(
            Reading.date >= start_date
        )

        if pond_id:
            query = query.filter(Reading.pond_id == pond_id)

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
            Reading.date,
            temperature_repository.value.label("temperature"),
            turbidity_repository.value.label("turbidity"),
            water_level_repository.value.label("water_level"),
            weight_repository.weight.label("weight")
        ).join(
            temperature_repository, Reading.temperature_id == temperature_repository.temperature_id, isouter=True
        ).join(
            turbidity_repository, Reading.turbidity_id == turbidity_repository.turbidity_id, isouter=True
        ).join(
            water_level_repository, Reading.water_level_id == water_level_repository.water_level_id, isouter=True
        ).join(
            weight_repository, Reading.weight_id == weight_repository.weight_id, isouter=True
        ).filter(
            Reading.date >= start_dt,
            Reading.date <= end_dt
        )

        if pond_id:
            query = query.filter(Reading.pond_id == pond_id)

        query = query.order_by(Reading.date.asc())

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
            Reading.date,
            temperature_repository.value.label("temperature")
        ).join(
            temperature_repository, Reading.temperature_id == temperature_repository.temperature_id
        ).filter(
            Reading.date >= start_date
        )

        if pond_id:
            query = query.filter(Reading.pond_id == pond_id)

        query = query.order_by(Reading.date.asc())

        results = query.all()

        return [
            {
                "date": row.date.isoformat(),
                "temperature": float(row.temperature)
            }
            for row in results if row.temperature is not None
        ]

    def get_weekly_weight_trend(self, pond_id=None, weeks=12):
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)

        sql = """
        SELECT 
            YEAR(r.date) AS year,
            WEEK(r.date, 1) AS week_number,
            MIN(DATE_FORMAT(r.date, '%Y-%m-%d')) AS week_start,
            AVG(w.weight) AS avg_weight
        FROM Reading r
        JOIN Weight w ON r.weight_id = w.weight_id
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

        result = self.db.execute(text(sql), params).mappings().fetchall()

        if not result:
            return {"message": "No hay datos para mostrar."}

        df = pd.DataFrame(result)
        weights = df["avg_weight"].dropna().values

        std_dev = float(np.std(weights))
        mean_weight = float(np.mean(weights))
        data = df.to_dict(orient="records")

        return {
            "status": "success",
            "mean_weight": mean_weight,
            "std_dev_weight": std_dev,
            "weeks": data
        }
