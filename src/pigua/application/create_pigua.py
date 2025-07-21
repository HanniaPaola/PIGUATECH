# src/pigua/application/create_pigua.py

from src.pigua.domain.repositories.repository import IPiguaRepository
from src.pigua.domain.entities import PiguaCreate, Pigua

class CreatePigua:
    def __init__(self, repo: IPiguaRepository):
        self.repo = repo

    def execute(self, pigua_data: PiguaCreate) -> Pigua:
        return self.repo.create_pigua(pigua_data)
