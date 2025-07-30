
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.auth.infrastructure.routes import router as auth_router
from src.api.users.infrastructure.routes import router as users_router

from src.api.ponds.infrastructure.routes import router as ponds_router
from src.api.readings.infrastructure.routes import router as readings_router
from src.api.biomass.infrastructure.routes import router as biomass_router
from src.api.notifications.infrastructure.routes import router as notifications_router

from src.api.reports.infrastructure.routes import router as reports_router
from src.api.files.infrastructure.routes import router as files_router

app = FastAPI(
    title="PIGUATECH API v4.0",
    description="Sistema de monitoreo IoT",
    version="4.0"
)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://piguafront.ddns.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)

app.include_router(ponds_router)
app.include_router(readings_router)
app.include_router(biomass_router)
app.include_router(notifications_router)

app.include_router(reports_router)
app.include_router(files_router)


@app.get("/")
def root():
    return {"message": "PIGUATECH API v4.0 running"}
