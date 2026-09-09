from typing import Dict


def diagnose(readings: Dict[str, float]) -> dict:
    layers = list(readings.keys())

    if len(layers) < 2:
        return {
            "status": "insufficient_data",
            "message": "Not enough system layers to diagnose."
        }

    for i in range(1, len(layers)):
        previous_layer = layers[i - 1]
        current_layer = layers[i]

        previous_value = readings[previous_layer]
        current_value = readings[current_layer]

        if previous_value != current_value:
            return {
                "status": "fault_detected",
                "fault_layer": current_layer,
                "previous_layer": previous_layer,
                "expected_value": previous_value,
                "observed_value": current_value,
                "message": (
                    f"First divergence detected between "
                    f"{previous_layer} and {current_layer}."
                )
            }

    return {
        "status": "healthy",
        "message": "No value divergence detected across the system."
    }
