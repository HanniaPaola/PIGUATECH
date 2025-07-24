from datetime import datetime
from src.habitat.infrastructure.adapters.habitat_status_mysql import HabitatStatusRepository
from src.habitat.domain.habitat_status import HabitatStatusResponse, CurrentCondition, ParameterIndicator

class HabitatStatusService:
    def __init__(self, repo: HabitatStatusRepository):
        self.repo = repo

    def get_habitat_status(self):
        reading = self.repo.get_latest_reading()
        parameters = self.repo.get_parameters()

        if not reading:
            return None

        result = {
            "last_update": reading["date"],
            "current_conditions": [],
            "parameter_indicators": []
        }

        mapping = {
            "Temperature": reading.get("temperature_value"),
            "Turbidity": reading.get("turbidity_value"),
            "Water_Level": reading.get("water_level_value"),
            "Weight": reading.get("weight_value")
        }

        for param in parameters:
            name = param["name"]
            value = float(mapping.get(name) or 0)
            min_v = float(param["min_value"])
            max_v = float(param["max_value"])
            unit = param["unit"]

            trend = value - min_v

            if min_v <= value <= max_v:
                state = "optimo"
            elif value < min_v:
                state = "atencion"
            else:
                state = "alerta"

            result["current_conditions"].append(CurrentCondition(
                name=name,
                current_value=value,
                unit=unit,
                trend=round(trend, 2),
                state=state
            ).model_dump())

            result["parameter_indicators"].append(ParameterIndicator(
                name=name,
                optimal_range=f"{min_v} - {max_v}",
                unit=unit,
                state=state
            ).model_dump())

        return HabitatStatusResponse(**result)
