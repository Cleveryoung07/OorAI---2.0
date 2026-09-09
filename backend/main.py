from fastapi import FastAPI

from models.telemetry import TelemetryData
from models.system import SystemDefinition
from models.diagnostics import DiagnosticRequest

from diagnostics.engine import diagnose
from diagnostics.graph import build_graph


app = FastAPI(
    title="OorAI Diagnostic Engine",
    description="Cross-layer diagnostics for connected systems",
    version="0.4.0"
)


@app.get("/")
def root():
    return {
        "name": "OorAI",
        "status": "online",
        "service": "diagnostic-engine",
        "version": "0.4.0"
    }


@app.post("/diagnose")
def run_diagnosis(data: DiagnosticRequest):

    result = diagnose(
        data.telemetry.readings,
        data.system_definition
    )

    return {
        "system": data.telemetry.system,
        "sensor_type": data.telemetry.sensor_type,
        "diagnosis": result
    }


@app.post("/system/graph")
def create_system_graph(system: SystemDefinition):

    graph = build_graph(system)

    return {
        "system": system.system,
        "graph": graph
    }