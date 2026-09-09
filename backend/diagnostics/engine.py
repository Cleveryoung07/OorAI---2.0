from typing import Dict, List

from models.system import SystemDefinition
from models.telemetry import Reading


def diagnose(
    readings: List[Reading],
    system: SystemDefinition
) -> dict:

    # Convert readings into an easy-to-search dictionary
    reading_map: Dict[str, Reading] = {
        reading.layer: reading
        for reading in readings
    }

    # Check that all graph components have telemetry
    missing_components = []

    for component in system.components:
        if component.id not in reading_map:
            missing_components.append(component.id)

    if missing_components:
        return {
            "status": "insufficient_data",
            "fault_type": "missing_telemetry",
            "missing_components": missing_components,
            "message": (
                "Telemetry is missing for one or more "
                "components in the system graph."
            )
        }

    # Check each connection in the actual system graph
    for connection in system.connections:

        source = reading_map[connection.source]
        target = reading_map[connection.target]

        # Failed telemetry
        if source.status != "ok":
            return {
                "status": "fault_detected",
                "fault_layer": source.layer,
                "fault_type": "telemetry_failure",
                "message": (
                    f"Telemetry from {source.layer} "
                    f"is marked as {source.status}."
                )
            }

        if target.status != "ok":
            return {
                "status": "fault_detected",
                "fault_layer": target.layer,
                "fault_type": "telemetry_failure",
                "message": (
                    f"Telemetry from {target.layer} "
                    f"is marked as {target.status}."
                )
            }

        # Unit mismatch
        if source.unit != target.unit:
            return {
                "status": "fault_detected",
                "fault_layer": target.layer,
                "fault_type": "unit_mismatch",
                "source_layer": source.layer,
                "target_layer": target.layer,
                "source_unit": source.unit,
                "target_unit": target.unit,
                "message": (
                    f"Unit changed from {source.unit} to "
                    f"{target.unit} between {source.layer} "
                    f"and {target.layer}."
                )
            }

        # Value divergence
        if (
            source.value is not None
            and target.value is not None
            and source.value != target.value
        ):
            return {
                "status": "fault_detected",
                "fault_layer": target.layer,
                "fault_type": "value_divergence",
                "source_layer": source.layer,
                "target_layer": target.layer,
                "expected_value": source.value,
                "observed_value": target.value,
                "unit": target.unit,
                "message": (
                    f"Value changed between {source.layer} "
                    f"and {target.layer}."
                )
            }

    return {
        "status": "healthy",
        "message": (
            "No obvious fault detected across "
            "the defined system connections."
        )
    }