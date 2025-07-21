# src/report/infrastructure/adapters/report_mysql.py

from sqlalchemy import text
from typing import List
from datetime import datetime
from src.core.db.connection import SessionLocal
from src.report.domain.repositories.repository import IReportRepository
from src.report.domain.entities import Report, ReportCreate

class MySQLReportRepository(IReportRepository):
    def __init__(self):
        self.db = SessionLocal()

    def create_report(self, report: ReportCreate, file_path: str) -> Report:
        query = text("""
            INSERT INTO Report (pond_id, start_date, end_date, created_by, file_path)
            VALUES (:pond_id, :start_date, :end_date, :created_by, :file_path)
        """)
        params = {
            "pond_id": report.pond_id,
            "start_date": report.start_date,
            "end_date": report.end_date,
            "created_by": report.created_by,
            "file_path": file_path
        }
        result = self.db.execute(query, params)
        self.db.commit()

        report_id = result.lastrowid

        return Report(
            report_id=report_id,
            pond_id=report.pond_id,
            start_date=report.start_date,
            end_date=report.end_date,
            created_at=datetime.now(),
            created_by=report.created_by,
            file_path=file_path
        )

    def get_reports(self) -> List[Report]:
        query = text("SELECT * FROM Report ORDER BY created_at DESC")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
