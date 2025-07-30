from datetime import date


class Biomass:
    def __init__(self, id: int, pond_id: int, estimated_weight_kg: float, calculation_date: date):
        self.id = id
        self.pond_id = pond_id
        self.estimated_weight_kg = estimated_weight_kg
        self.calculation_date = calculation_date
