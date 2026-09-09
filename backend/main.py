from fastapi import FastAPI

from models.telemetry import TelemetryData
from diagnostics.engine import diagnose


app = FastAPI(
    title="OorAI Diagnostic Engine",
    description="Cross-layer diagnostics for connected systems",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "name": "OorAI",
        "status": "online",
        "service": "diagnostic-engine"
    }


@app.post("/diagnose")
def run_diagnosis(data: TelemetryData):
    result = diagnose(data.readings)

    return {
        "system": data.system,
        "diagnosis": result
    }
