"""Illustrative environmental noise model for quantum experiments."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class EnvironmentalConditions:
    """Environmental measurements and reference values.

    All deviations are normalized to a scale where 1.0 represents
    the chosen reference deviation for that factor.
    """

    vibration_amplitude: float = 0.0
    vibration_frequency_deviation: float = 0.0
    vibration_duration: float = 0.0
    temperature_deviation: float = 0.0
    temperature_change_rate: float = 0.0
    humidity_deviation: float = 0.0
    pressure_deviation: float = 0.0
    airflow_speed: float = 0.0
    electromagnetic_noise: float = 0.0
    voltage_fluctuation: float = 0.0
    mechanical_stress: float = 0.0


@dataclass(frozen=True)
class EnvironmentalNoiseResult:
    """Estimated noise contribution from environmental conditions."""

    probability: float
    contributions: dict[str, float]


# Illustrative coefficients only; calibrate against real measurements.
DEFAULT_WEIGHTS = {
    "vibration": 0.010,
    "temperature": 0.020,
    "humidity": 0.005,
    "pressure": 0.005,
    "airflow": 0.005,
    "electromagnetic": 0.030,
    "voltage": 0.025,
    "mechanical_stress": 0.010,
}


def estimate_environmental_noise(
    conditions: EnvironmentalConditions,
    weights: dict[str, float] | None = None,
) -> EnvironmentalNoiseResult:
    """Estimate an illustrative noise probability between 0 and 1."""

    if not isinstance(conditions, EnvironmentalConditions):
        raise TypeError("conditions must be EnvironmentalConditions")

    selected_weights = (
        dict(DEFAULT_WEIGHTS) if weights is None else dict(weights)
    )

    if set(selected_weights) != set(DEFAULT_WEIGHTS):
        raise ValueError("weights must contain exactly the supported factors")

    for name, value in selected_weights.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"weight '{name}' must be a number")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"weight '{name}' must be finite and non-negative")

    values = vars(conditions)

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    vibration = (
        conditions.vibration_amplitude
        * (1.0 + conditions.vibration_frequency_deviation)
        * conditions.vibration_duration
    )
    temperature = (
        conditions.temperature_deviation
        + conditions.temperature_change_rate
    )

    raw_contributions = {
        "vibration": selected_weights["vibration"] * vibration,
        "temperature": selected_weights["temperature"] * temperature,
        "humidity": selected_weights["humidity"]
        * conditions.humidity_deviation,
        "pressure": selected_weights["pressure"]
        * conditions.pressure_deviation,
        "airflow": selected_weights["airflow"] * conditions.airflow_speed,
        "electromagnetic": selected_weights["electromagnetic"]
        * conditions.electromagnetic_noise,
        "voltage": selected_weights["voltage"]
        * conditions.voltage_fluctuation,
        "mechanical_stress": selected_weights["mechanical_stress"]
        * conditions.mechanical_stress,
    }

    # Combine contributions without allowing probability to exceed 1.
    survival_probability = math.prod(
        1.0 - min(contribution, 1.0)
        for contribution in raw_contributions.values()
    )
    probability = 1.0 - survival_probability

    return EnvironmentalNoiseResult(
        probability=probability,
        contributions=raw_contributions,
    )