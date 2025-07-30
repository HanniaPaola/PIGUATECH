from abc import ABC, abstractmethod
from typing import Optional, List
from .reading import Reading


class ReadingRepository(ABC):
    @abstractmethod
    def get_by_id(self, reading_id: int) -> Optional[Reading]:
        pass

    @abstractmethod
    def create(self, reading: Reading) -> Reading:
        pass

    @abstractmethod
    def list_by_pond(self, pond_id: int) -> List[Reading]:
        pass
