from fastapi import APIRouter, HTTPException, status, Depends, Response
from pydantic import BaseModel
from ...readings.domain.reading import Reading
from ...readings.infrastructure.reading_mysql import ReadingMySQLRepository
from ...users.infrastructure.routes import get_current_user
from src.db.database import SessionLocal
from typing import List
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

router = APIRouter(prefix="/api/readings", tags=["readings"])


class ReadingRequest(BaseModel):
    pond_id: int
    sensor_type: str
    value: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_reading(request: ReadingRequest, user=Depends(get_current_user), db=Depends(get_db)):
    repo = ReadingMySQLRepository(db)
    reading = Reading(
        id=0,
        pond_id=request.pond_id,
        sensor_type=request.sensor_type,
        value=request.value,
        reading_date=None
    )
    created = repo.create(reading)
    return {"success": True, "data": {"id": created.id, "pond_id": created.pond_id, "sensor_type": created.sensor_type, "value": created.value}}


@router.get("/", response_model=List[ReadingRequest])
def list_readings(user=Depends(get_current_user), db=Depends(get_db)):
    repo = ReadingMySQLRepository(db)
    # Aquí deberías filtrar por ponds del usuario, pero para ejemplo, retorna vacío
    return []


# Endpoint para estadísticas y PDF
@router.get("/stats/pdf", response_class=Response)
def readings_stats_pdf(db=Depends(get_db)):
    from ...readings.infrastructure.reading_mysql import ReadingModel
    readings = db.query(ReadingModel).all()
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")

    # Convertir a DataFrame
    data = [{
        'id': r.id,
        'pond_id': r.pond_id,
        'sensor_type': r.sensor_type,
        'value': r.value,
        'reading_date': r.reading_date.strftime('%Y-%m-%d %H:%M') if r.reading_date else ''
    } for r in readings]
    df = pd.DataFrame(data)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("<b>Reporte Detallado de Lecturas (Readings)</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Tabla de datos
    if not df.empty:
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph("<b>Tabla de datos</b>", styles['Heading2']))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Estadísticas y distribución de frecuencias por sensor
    for sensor in df['sensor_type'].unique():
        sensor_df = df[df['sensor_type'] == sensor]
        values = sensor_df['value']
        desc = values.describe()
        elements.append(Paragraph(f"<b>Sensor: {sensor}</b>", styles['Heading2']))
        stats_table = Table([
            ['Count', 'Min', 'Max', 'Mean', 'Std'],
            [f"{desc['count']:.0f}", f"{desc['min']:.2f}", f"{desc['max']:.2f}", f"{desc['mean']:.2f}", f"{desc['std']:.2f}" if not np.isnan(desc['std']) else '0.00']
        ])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 8))

        # Distribución de frecuencias
        freq = values.value_counts().sort_index()
        freq_table = Table([
            ['Valor', 'Frecuencia']
        ] + [[f'{idx:.2f}', f'{val}'] for idx, val in freq.items()])
        freq_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph("<b>Distribución de frecuencias</b>", styles['Heading3']))
        elements.append(freq_table)
        elements.append(Spacer(1, 8))

        # Gráfica
        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.hist(values, bins=10, color='skyblue', edgecolor='black')
        ax.set_title(f"Histograma de {sensor}")
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        plt.tight_layout()
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close(fig)
        img_buffer.seek(0)
        elements.append(Image(img_buffer, width=300, height=180))
        elements.append(Spacer(1, 16))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=readings_stats.pdf"})
