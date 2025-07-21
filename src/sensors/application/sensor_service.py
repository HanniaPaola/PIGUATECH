# src/sensors/application/sensor_service.py
from src.sensors.domain.repositories.temperature_repository import TemperatureRepository
from src.sensors.domain.repositories.turbidity_repository import TurbidityRepository
from src.sensors.domain.repositories.water_level_repository import WaterLevelRepository
from src.sensors.domain.repositories.weight_repository import WeightRepository
from src.sensors.domain.repositories.reading_repository import ReadingRepository

from datetime import datetime
from src.reading.domain.entities import ReadingCreate 

class SensorService:
    def __init__(self, db, pond_id=None):
        self.db = db
        self.pond_id = pond_id 
        self.temperature_repo = TemperatureRepository(db)
        self.turbidity_repo = TurbidityRepository(db)
        self.water_level_repo = WaterLevelRepository(db)
        self.weight_repo = WeightRepository(db)
        self.reading_repo = ReadingRepository(db)

        self.buffer = {}

    def process_temperature(self, value):
        temp_id = self.temperature_repo.insert(value)
        self.buffer['temperature'] = temp_id
        self._try_create_reading()

    def process_turbidity(self, value):
        turb_id = self.turbidity_repo.insert(value)
        self.buffer['turbidity'] = turb_id
        self._try_create_reading()

    def process_water_level(self, value):
        water_id = self.water_level_repo.insert(value)
        self.buffer['water_level'] = water_id
        self._try_create_reading()

    def process_weight(self, value):
        weight_id = self.weight_repo.insert(value)
        self.buffer['weight'] = weight_id
        self._try_create_reading()

    def _try_create_reading(self):
        if all(k in self.buffer for k in ('temperature', 'turbidity', 'water_level', 'weight')):
            reading_data = ReadingCreate(
                pond_id=self.pond_id, 
                turbidity_id=self.buffer['turbidity'],
                water_level_id=self.buffer['water_level'],
                temperature_id=self.buffer['temperature'],
                weight_id=self.buffer['weight'],
                date=datetime.utcnow()
            )
            self.reading_repo.create_reading(reading_data)
            print("Reading creada con datos:", self.buffer)
            self.buffer.clear()
