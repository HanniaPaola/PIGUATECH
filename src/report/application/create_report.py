# src/report/application/create_report.py

from src.report.domain.repositories.repository import IReportRepository
from src.report.domain.entities import ReportCreate, Report
from src.reading.infrastructure.adapters.reading_mysql import ReadingRepository
from datetime import datetime

class CreateReport:
    def __init__(self, report_repo: IReportRepository, reading_repo: ReadingRepository):
        self.report_repo = report_repo
        self.reading_repo = reading_repo

    def execute(self, report_data: ReportCreate) -> dict:
        # Paso 1: Obtener lecturas
        readings = self.reading_repo.get_readings_by_date_range(
            report_data.start_date, report_data.end_date, report_data.pond_id
        )

        if not readings:
            return {"msg": "No data found for selected range"}

        # Paso 2: Generar archivo (PDF o CSV)
        # Aquí se hace un ejemplo de CSV simple
        import csv, io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=readings[0].keys())
        writer.writeheader()
        writer.writerows(readings)
        output.seek(0)

        file_name = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = f"./reports/{file_name}"

        # Guardar archivo físico (opcional)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output.read())

        # Paso 3: Guardar meta en Report
        report = self.report_repo.create_report(report_data, file_path)

        return {
            "msg": "Report generated successfully",
            "report": report,
            "file_path": file_path
        }
