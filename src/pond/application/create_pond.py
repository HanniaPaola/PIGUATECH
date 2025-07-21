# src/pond/application/create_pond.py
from src.pond.domain.repositories.repository import IPondRepository
from src.pond.domain.entities import PondCreate, Pond

class CreatePond:
    def __init__(self, repo: IPondRepository):
        self.repo = repo

    def execute(self, pond_data: PondCreate) -> Pond:
        return self.repo.create_pond(pond_data)