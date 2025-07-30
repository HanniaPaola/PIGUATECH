from abc import ABC, abstractmethod
from typing import Optional, List
from .report import Report


class ReportRepository(ABC):
    @abstractmethod
    def get_by_id(self, report_id: int) -> Optional[Report]:
        pass

    @abstractmethod
    def create(self, report: Report) -> Report:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Report]:
        pass
