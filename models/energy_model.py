
from pydantic import BaseModel
from datetime import date

class EnergyRecord(BaseModel):
    building_id: int
    timestamp: date
    electricity_kwh: float
    water_tons: float
    gas_m3: float
    co2_tons: float
