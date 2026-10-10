import pytest

from quantum.environmental_experiment import run_vibration_frequency_sweep


def test_frequency_sweep_returns_all_requested_frequencies():
    results = run_vibration_frequency_sweep(
        frequencies_hz=(50, 100, 150),
        trials=1000,
    )

    assert len(results) == 3
    assert tuple(
        result.conditions.vibration_frequency_hz for result in results
    ) == (50, 100, 150)


def test_resonance_frequency_has_highest_noise_in_default_sweep():
    results = run_vibration_frequency_sweep(trials=1000)

    probabilities = {
        result.conditions.vibration_frequency_hz:
        result.estimated_noise_probability
        for result in results
    }

    assert probabilities[100] == pytest.approx(0.025)
    assert probabilities[100] > probabilities[50]
    assert probabilities[100] > probabilities[150]


def test_frequency_sweep_is_reproducible():
    first = run_vibration_frequency_sweep(
        frequencies_hz=(50, 100, 150),
        trials=1000,
        seed=42,
    )
    second = run_vibration_frequency_sweep(
        frequencies_hz=(50, 100, 150),
        trials=1000,
        seed=42,
    )

    assert first == second


def test_empty_frequency_sweep_is_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        run_vibration_frequency_sweep(frequencies_hz=())
