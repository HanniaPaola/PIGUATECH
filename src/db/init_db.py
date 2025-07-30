from src.db.database import Base, engine
from src.api.users.infrastructure.user_mysql import UserModel
from src.api.ponds.infrastructure.pond_mysql import PondModel
from src.api.readings.infrastructure.reading_mysql import ReadingModel
from src.api.biomass.infrastructure.biomass_mysql import BiomassModel
from src.api.notifications.infrastructure.notification_mysql import NotificationModel
from src.api.reports.infrastructure.report_mysql import ReportModel

# Importa aquí los modelos de los otros módulos cuando estén listos


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
