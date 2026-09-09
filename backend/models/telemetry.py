from pydantic import BaseModel
from typing import Dict


class TelemetryData(BaseModel):
    system: str
    readings: Dict[str, float]
