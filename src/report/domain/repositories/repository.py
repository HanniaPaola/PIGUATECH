from abc import ABC, abstractmethod
from typing import List
from src.report.domain.entities import ReportCreate, Report

class IReportRepository(ABC):

    @abstractmethod
    def create_report(self, report: ReportCreate, file_path: str) -> Report:
        pass

    @abstractmethod
    def get_reports(self) -> List[Report]:  
        pass
