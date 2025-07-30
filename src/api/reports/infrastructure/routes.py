from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from ...reports.domain.report import Report
from ...reports.infrastructure.report_mysql import ReportMySQLRepository
from ...users.infrastructure.routes import get_current_user
from src.db.database import SessionLocal
from typing import List

router = APIRouter(prefix="/api/reports", tags=["reports"])


class ReportRequest(BaseModel):
    id: int | None = None
    title: str
    file_url: str | None = None
    created_at: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReportRequest, status_code=201)
def create_report(request: ReportRequest, user=Depends(get_current_user), db=Depends(get_db)):
    repo = ReportMySQLRepository(db)
    report = Report(
        id=0,
        user_id=user["id"],
        title=request.title,
        file_url=request.file_url,
        created_at=None
    )
    created = repo.create(report)
    return ReportRequest(
        id=created.id,
        title=created.title,
        file_url=created.file_url,
        created_at=str(created.created_at) if created.created_at else None
    )


@router.get("/", response_model=List[ReportRequest])
def list_reports(user=Depends(get_current_user), db=Depends(get_db)):
    repo = ReportMySQLRepository(db)
    reports = repo.list_by_user(user["id"])
    return [ReportRequest(
        id=r.id,
        title=r.title,
        file_url=r.file_url,
        created_at=str(r.created_at) if r.created_at else None
    ) for r in reports]
