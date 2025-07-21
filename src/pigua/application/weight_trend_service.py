from datetime import datetime
from sqlalchemy import func, extract
from src.core.db.connection import SessionLocal
from src.reading.domain.entities import Reading
#from src.reading.domain.entities import Reading, Weight


class PiguaWeightTrendService:
    def __init__(self):
        self.db = SessionLocal()

    def get_weight_trend(self, pond_id: int = None):
        query = self.db.query(
            extract('month', Reading.date).label('month'),
            func.avg(Weight.weight).label('avg_weight')
        ).join(
            Weight, Reading.weight_id == Weight.weight_id
        ).filter(
            Reading.weight_id.isnot(None)
        ).group_by(
            extract('month', Reading.date)
        ).order_by(
            extract('month', Reading.date)
        )

        if pond_id:
            query = query.filter(Reading.pond_id == pond_id)

        result = query.all()

        return [
            {"month": int(row.month), "avg_weight": float(row.avg_weight)}
            for row in result
        ]
