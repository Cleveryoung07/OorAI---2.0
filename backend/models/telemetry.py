from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Reading(BaseModel):
    layer: str
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    status: str = "ok"


class TelemetryData(BaseModel):
    system: str
    sensor_type: str
    readings: list[Reading]
