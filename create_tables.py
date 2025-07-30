from src.core.db.connection import Base, engine
from src.api.users.infrastructure.models import UserModel
from src.api.ponds.infrastructure.models import PondModel
from src.api.readings.infrastructure.models import ReadingModel
from src.api.reports.infrastructure.models import ReportModel
from src.api.notifications.infrastructure.models import NotificationModel
from src.api.biomass.infrastructure.models import BiomassModel

if __name__ == "__main__":
    print("Creando todas las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas!")
