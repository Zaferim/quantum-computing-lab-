"""Compare error correction under different environmental conditions."""

from dataclasses import dataclass

from quantum.environmental_noise import (
    EnvironmentalConditions,
    estimate_environmental_noise,
)
from quantum.noise_experiment import run_experiment


@dataclass(frozen=True)
class EnvironmentalExperimentResult:
    """Environmental conditions and simulated transmission results."""

    conditions: EnvironmentalConditions
    estimated_noise_probability: float
    single_bit_success_rate: float
    corrected_success_rate: float
    trials: int


def run_environmental_experiment(
    conditions: EnvironmentalConditions,
    trials: int = 10_000,
    seed: int = 42,
) -> EnvironmentalExperimentResult:
    """Estimate noise and compare single-bit and corrected transmission."""

    estimate = estimate_environmental_noise(conditions)

    experiment = run_experiment(
        probability=estimate.probability,
        trials=trials,
        seed=seed,
    )

    return EnvironmentalExperimentResult(
        conditions=conditions,
        estimated_noise_probability=estimate.probability,
        single_bit_success_rate=experiment.single_bit_success_rate,
        corrected_success_rate=experiment.corrected_success_rate,
        trials=trials,
    )


def main() -> None:
    """Run a comparison across illustrative environmental scenarios."""

    scenarios = {
        "Reference environment": EnvironmentalConditions(),
        "High vibration": EnvironmentalConditions(
            vibration_amplitude=2.0,
            vibration_frequency_deviation=1.0,
            vibration_duration=1.0,
        ),
        "Temperature deviation": EnvironmentalConditions(
            temperature_deviation=2.0,
            temperature_change_rate=1.0,
        ),
        "Electromagnetic noise": EnvironmentalConditions(
            electromagnetic_noise=2.0,
        ),
        "Power instability": EnvironmentalConditions(
            voltage_fluctuation=2.0,
        ),
        "Combined disturbances": EnvironmentalConditions(
            vibration_amplitude=1.0,
            vibration_frequency_deviation=0.5,
            vibration_duration=1.0,
            temperature_deviation=1.0,
            humidity_deviation=1.0,
            pressure_deviation=1.0,
            airflow_speed=1.0,
            electromagnetic_noise=1.0,
            voltage_fluctuation=1.0,
            mechanical_stress=1.0,
        ),
    }

    print("Environmental Noise and Error Correction Experiment")
    print("=" * 82)
    print(
        f"{'Scenario':<25} | {'Noise':>8} | "
        f"{'Single-bit':>12} | {'Corrected':>12}"
    )
    print("-" * 82)

    for name, conditions in scenarios.items():
        result = run_environmental_experiment(
            conditions,
            trials=10_000,
            seed=42,
        )
        print(
            f"{name:<25} | "
            f"{result.estimated_noise_probability:>7.2%} | "
            f"{result.single_bit_success_rate:>11.2%} | "
            f"{result.corrected_success_rate:>11.2%}"
        )


if __name__ == "__main__":
    main()