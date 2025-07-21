# src/report/infrastructure/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from src.report.infrastructure.adapters.report_mysql import MySQLReportRepository
from src.report.application.create_report import CreateReport
from src.report.domain.entities import ReportCreate
from src.reading.infrastructure.adapters.reading_mysql import ReadingRepository
from src.core.db.connection import SessionLocal

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

def get_report_use_case():
    db = SessionLocal()
    report_repo = MySQLReportRepository()
    reading_repo = ReadingRepository(db)
    return CreateReport(report_repo, reading_repo)

@router.post("/", summary="Generar y guardar un reporte")
def create_report(report: ReportCreate, use_case=Depends(get_report_use_case)):
    result = use_case.execute(report)
    if "file_path" not in result:
        raise HTTPException(status_code=404, detail="No data for given range")
    return result

@router.get("/download/{file_name}", summary="Descargar reporte generado")
def download_report(file_name: str):
    file_path = f"./reports/{file_name}"
    return FileResponse(file_path, media_type='text/csv', filename=file_name)
