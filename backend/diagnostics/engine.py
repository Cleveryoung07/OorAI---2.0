from typing import List
from models.telemetry import Reading


def diagnose(readings: List[Reading]) -> dict:

    if len(readings) < 2:
        return {
            "status": "insufficient_data",
            "message": "At least two system layers are required."
        }

    # Check for missing or failed readings
    for reading in readings:
        if reading.status != "ok":
            return {
                "status": "fault_detected",
                "fault_layer": reading.layer,
                "fault_type": "telemetry_failure",
                "message": (
                    f"Telemetry from {reading.layer} "
                    f"is marked as {reading.status}."
                )
            }

    # Compare consecutive readings
    for i in range(1, len(readings)):

        previous = readings[i - 1]
        current = readings[i]

        if previous.value is None or current.value is None:
            continue

        # Unit mismatch
        if previous.unit != current.unit:
            return {
                "status": "fault_detected",
                "fault_layer": current.layer,
                "fault_type": "unit_mismatch",
                "previous_unit": previous.unit,
                "current_unit": current.unit,
                "message": (
                    f"Unit changed from {previous.unit} "
                    f"to {current.unit} between "
                    f"{previous.layer} and {current.layer}."
                )
            }

        # Value mismatch
        if previous.value != current.value:
            return {
                "status": "fault_detected",
                "fault_layer": current.layer,
                "fault_type": "value_divergence",
                "previous_layer": previous.layer,
                "expected_value": previous.value,
                "observed_value": current.value,
                "unit": current.unit,
                "message": (
                    f"First value divergence detected between "
                    f"{previous.layer} and {current.layer}."
                )
            }

    return {
        "status": "healthy",
        "message": "No obvious fault detected across the system."
    }
