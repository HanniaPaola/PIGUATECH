# src/pond/domain/repositories/repository.py
from abc import ABC, abstractmethod
from ..entities import PondCreate, Pond

class IPondRepository(ABC):

    @abstractmethod
    def create_pond(self, pond: PondCreate) -> Pond:
        pass