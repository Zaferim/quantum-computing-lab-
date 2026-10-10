"""Illustrative environmental noise model for quantum experiments."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class EnvironmentalConditions:
    """Environmental measurements and reference values.

    Environmental inputs are normalized unless a field explicitly
    specifies Hz. Coefficients are illustrative, not experimentally
    calibrated.
    """

    vibration_amplitude: float = 0.0
    vibration_frequency_deviation: float = 0.0
    vibration_duration: float = 0.0

    # Optional mechanical resonance parameters.
    vibration_frequency_hz: float = 0.0
    vibration_natural_frequency_hz: float = 1.0
    vibration_damping_ratio: float = 0.1

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


def resonance_factor(
    frequency_hz: float,
    natural_frequency_hz: float,
    damping_ratio: float,
) -> float:
    """Calculate a simplified mechanical frequency-response factor.

    This is a single-degree-of-freedom mechanical response model.
    It is not a calibrated model of a particular quantum device.
    """

    values = (
        frequency_hz,
        natural_frequency_hz,
        damping_ratio,
    )

    if any(
        isinstance(value, bool) or not isinstance(value, (int, float))
        for value in values
    ):
        raise TypeError("Resonance parameters must be numbers")

    if any(not math.isfinite(value) for value in values):
        raise ValueError("Resonance parameters must be finite")

    if frequency_hz < 0:
        raise ValueError("frequency_hz must be non-negative")

    if natural_frequency_hz <= 0:
        raise ValueError(
            "natural_frequency_hz must be greater than zero"
        )

    if damping_ratio <= 0:
        raise ValueError("damping_ratio must be greater than zero")

    ratio = frequency_hz / natural_frequency_hz

    denominator = math.sqrt(
        (1.0 - ratio**2) ** 2
        + (2.0 * damping_ratio * ratio) ** 2
    )

    return 1.0 / denominator


def estimate_environmental_noise(
    conditions: EnvironmentalConditions,
    weights: dict[str, float] | None = None,
) -> EnvironmentalNoiseResult:
    """Estimate illustrative noise probability between 0 and 1."""

    if not isinstance(conditions, EnvironmentalConditions):
        raise TypeError("conditions must be EnvironmentalConditions")

    selected_weights = (
        dict(DEFAULT_WEIGHTS) if weights is None else dict(weights)
    )

    if set(selected_weights) != set(DEFAULT_WEIGHTS):
        raise ValueError(
            "weights must contain exactly the supported factors"
        )

    for name, value in selected_weights.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"weight '{name}' must be a number")

        if not math.isfinite(value) or value < 0:
            raise ValueError(
                f"weight '{name}' must be finite and non-negative"
            )

    values = vars(conditions)

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")

        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    if conditions.vibration_natural_frequency_hz <= 0:
        raise ValueError(
            "vibration_natural_frequency_hz must be greater than zero"
        )

    if conditions.vibration_damping_ratio <= 0:
        raise ValueError(
            "vibration_damping_ratio must be greater than zero"
        )

    # Mechanical resonance response:
    # the response may rise when forcing frequency approaches
    # the system's natural frequency.
    resonance = resonance_factor(
        frequency_hz=conditions.vibration_frequency_hz,
        natural_frequency_hz=conditions.vibration_natural_frequency_hz,
        damping_ratio=conditions.vibration_damping_ratio,
    )

    vibration = (
        conditions.vibration_amplitude
        * (1.0 + conditions.vibration_frequency_deviation)
        * conditions.vibration_duration
        * resonance
    )

    temperature = (
        conditions.temperature_deviation
        + conditions.temperature_change_rate
    )

    raw_contributions = {
        "vibration": selected_weights["vibration"] * vibration,
        "temperature": selected_weights["temperature"] * temperature,
        "humidity": (
            selected_weights["humidity"]
            * conditions.humidity_deviation
        ),
        "pressure": (
            selected_weights["pressure"]
            * conditions.pressure_deviation
        ),
        "airflow": (
            selected_weights["airflow"] * conditions.airflow_speed
        ),
        "electromagnetic": (
            selected_weights["electromagnetic"]
            * conditions.electromagnetic_noise
        ),
        "voltage": (
            selected_weights["voltage"]
            * conditions.voltage_fluctuation
        ),
        "mechanical_stress": (
            selected_weights["mechanical_stress"]
            * conditions.mechanical_stress
        ),
    }

    # Combine contributions as independent illustrative probabilities.
    # Each individual contribution is capped at 1.
    survival_probability = math.prod(
        1.0 - min(contribution, 1.0)
        for contribution in raw_contributions.values()
    )

    probability = 1.0 - survival_probability

    return EnvironmentalNoiseResult(
        probability=probability,
        contributions=raw_contributions,
    )