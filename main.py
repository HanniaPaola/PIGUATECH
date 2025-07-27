# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.infrastructure.routes import router as auth_router
from src.pond.infrastructure.routes import router as pond_router
from src.reading.infrastructure.routes import router as sensors_router
from src.alerts.infrastructure.routes import router as alerts_router
from src.pigua.infrastructure.routes import router as pigua_router
from src.report.infrastructure.routes import router as report_router
from src.notifications.infrastructure.routes import router as notification_router
from src.sensors.infrastructure.routes import router as reading_router
from src.sensors.infrastructure import turbidity_routes
from src.habitat.infrastructure import habitat_status_routes

app = FastAPI(
    title="API PIGUATECH",
    description="Sistema de monitoreo IoT",
    version="1.0.0"
)

# Middleware de CORS
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutas
app.include_router(auth_router)
app.include_router(pond_router, prefix="/pond")
app.include_router(sensors_router)
app.include_router(alerts_router, prefix="/api")
app.include_router(pigua_router)
app.include_router(report_router)
app.include_router(notification_router)
app.include_router(reading_router)
app.include_router(turbidity_routes.router)
app.include_router(habitat_status_routes.router)

# uvicorn main:app --reload

# grafica de barras import numpy as np A2.py
#import statistics, import matplotlib.pyplot as pltimport numpy as np act.py
#domingo.py  import pandas as pd, import numpy as np