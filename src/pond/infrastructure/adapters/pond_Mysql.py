# src/pond/infrastructure/adapters/pond_mysql.py
from src.core.db.connection import SessionLocal
from src.pond.domain.entities import PondCreate, Pond
from src.pond.domain.repositories.repository import IPondRepository

from sqlalchemy import text

class MySQLPondRepository(IPondRepository):
    def __init__(self):
        self.db = SessionLocal()

    def create_pond(self, pond: PondCreate) -> Pond:
        
                # Validar que si se envía pigua_id, exista en la tabla Pigua
        if pond.pigua_id is not None:
            query_check = text("SELECT pigua_id FROM Pigua WHERE pigua_id = :pigua_id")
            result = self.db.execute(query_check, {"pigua_id": pond.pigua_id}).fetchone()
            if result is None:
                raise ValueError(f"Pigua con id {pond.pigua_id} no existe")
            
        query = text("""
            INSERT INTO Pond (pigua_id) 
            VALUES (:pigua_id)
        """)
        
        params = {
            "pigua_id": pond.pigua_id
        }
        
        result = self.db.execute(query, params)
        self.db.commit()

        # Recuperar el ID autoincremental
        pond_id = result.lastrowid
        return Pond(
            pond_id=pond_id,
            pigua_id=pond.pigua_id
        )