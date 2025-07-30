from abc import ABC, abstractmethod
from typing import Optional, List
from .pond import Pond


class PondRepository(ABC):
    @abstractmethod
    def get_by_id(self, pond_id: int) -> Optional[Pond]:
        pass

    @abstractmethod
    def create(self, pond: Pond) -> Pond:
        pass

    @abstractmethod
    def list_by_farmer(self, farmer_id: int) -> List[Pond]:
        pass
