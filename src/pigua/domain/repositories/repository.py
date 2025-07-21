# src/pigua/domain/repository.py

from abc import ABC, abstractmethod
from ..entities import PiguaCreate, Pigua

class IPiguaRepository(ABC):

    @abstractmethod
    def create_pigua(self, pigua: PiguaCreate) -> Pigua:
        pass
