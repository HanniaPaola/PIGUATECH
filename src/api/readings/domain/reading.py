from datetime import datetime


class Reading:
    def __init__(self, id: int, pond_id: int, sensor_type: str, value: float, reading_date: datetime):
        self.id = id
        self.pond_id = pond_id
        # e.g., 'temperature', 'turbidity', etc.
        self.sensor_type = sensor_type
        self.value = value
        self.reading_date = reading_date
