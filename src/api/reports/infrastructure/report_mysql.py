from sqlalchemy.orm import Session
from src.api.reports.domain.report_repository import ReportRepository
from src.api.reports.domain.report import Report
from src.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from typing import Optional, List


from src.api.reports.infrastructure.models import ReportModel


class ReportMySQLRepository(ReportRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, report_id: int) -> Optional[Report]:
        report = self.db.query(ReportModel).filter(
            ReportModel.id == report_id).first()
        return self._to_domain(report) if report else None

    def create(self, report: Report) -> Report:
        db_report = ReportModel(
            user_id=report.user_id,
            title=report.title,
            file_url=report.file_url
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return self._to_domain(db_report)

    def list_by_user(self, user_id: int) -> List[Report]:
        reports = self.db.query(ReportModel).filter(
            ReportModel.user_id == user_id).all()
        return [self._to_domain(r) for r in reports]

    def _to_domain(self, report_model: ReportModel) -> Report:
        return Report(
            id=report_model.id,
            user_id=report_model.user_id,
            title=report_model.title,
            file_url=report_model.file_url,
            created_at=report_model.created_at
        )
