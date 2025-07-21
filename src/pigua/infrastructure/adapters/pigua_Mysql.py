from src.core.db.connection import SessionLocal
from src.pigua.domain.entities import PiguaCreate, Pigua
from src.pigua.domain.repositories.repository import IPiguaRepository

from sqlalchemy import text

class MySQLPiguaRepository(IPiguaRepository):
    def __init__(self):
        self.db = SessionLocal()

    def create_pigua(self, pigua: PiguaCreate) -> Pigua:
        query = text("""
            INSERT INTO Pigua (weight_id) 
            VALUES (:weight_id)
        """)
        result = self.db.execute(query, {
            "weight_id": pigua.weight_id 
        })
        self.db.commit()

        pigua_id = result.lastrowid
        return Pigua(pigua_id=pigua_id, weight_id=pigua.weight_id)
