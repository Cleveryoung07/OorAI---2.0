from fastapi import FastAPI

from models.telemetry import TelemetryData
from models.system import SystemDefinition

from diagnostics.engine import diagnose
from diagnostics.graph import build_graph


app = FastAPI(
    title="OorAI Diagnostic Engine",
    description="Cross-layer diagnostics for connected systems",
    version="0.3.0"
)


@app.get("/")
def root():
    return {
        "name": "OorAI",
        "status": "online",
        "service": "diagnostic-engine",
        "version": "0.3.0"
    }


@app.post("/diagnose")
def run_diagnosis(data: TelemetryData):

    result = diagnose(data.readings)

    return {
        "system": data.system,
        "sensor_type": data.sensor_type,
        "diagnosis": result
    }


@app.post("/system/graph")
def create_system_graph(system: SystemDefinition):

    graph = build_graph(system)

    return {
        "system": system.system,
        "graph": graph
    }