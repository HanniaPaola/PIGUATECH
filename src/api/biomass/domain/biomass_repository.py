from abc import ABC, abstractmethod
from typing import Optional, List
from .biomass import Biomass


class BiomassRepository(ABC):
    @abstractmethod
    def get_by_id(self, biomass_id: int) -> Optional[Biomass]:
        pass

    @abstractmethod
    def create(self, biomass: Biomass) -> Biomass:
        pass

    @abstractmethod
    def list_by_pond(self, pond_id: int) -> List[Biomass]:
        pass
