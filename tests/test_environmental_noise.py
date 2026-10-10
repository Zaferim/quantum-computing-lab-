import pytest

from quantum.environmental_noise import (
    EnvironmentalConditions,
    estimate_environmental_noise,
    resonance_factor,
)


def test_zero_environmental_conditions_produce_zero_noise():
    result = estimate_environmental_noise(EnvironmentalConditions())

    assert result.probability == 0.0
    assert all(value == 0.0 for value in result.contributions.values())


def test_increased_electromagnetic_noise_increases_probability():
    low = estimate_environmental_noise(
        EnvironmentalConditions(electromagnetic_noise=0.5)
    )
    high = estimate_environmental_noise(
        EnvironmentalConditions(electromagnetic_noise=2.0)
    )

    assert high.probability > low.probability


def test_multiple_environmental_factors_are_combined():
    result = estimate_environmental_noise(
        EnvironmentalConditions(
            temperature_deviation=1.0,
            humidity_deviation=1.0,
            voltage_fluctuation=1.0,
        )
    )

    assert 0.0 < result.probability < 1.0
    assert result.contributions["temperature"] > 0.0
    assert result.contributions["humidity"] > 0.0
    assert result.contributions["voltage"] > 0.0


def test_probability_never_exceeds_one():
    result = estimate_environmental_noise(
        EnvironmentalConditions(
            electromagnetic_noise=1e6,
            voltage_fluctuation=1e6,
        )
    )

    assert 0.0 <= result.probability <= 1.0


@pytest.mark.parametrize(
    "conditions",
    [
        EnvironmentalConditions(temperature_deviation=-1.0),
        EnvironmentalConditions(humidity_deviation=-1.0),
        EnvironmentalConditions(vibration_amplitude=-1.0),
        EnvironmentalConditions(voltage_fluctuation=-1.0),
    ],
)
def test_negative_environmental_measurements_are_rejected(conditions):
    with pytest.raises(ValueError):
        estimate_environmental_noise(conditions)


def test_invalid_conditions_type_is_rejected():
    with pytest.raises(TypeError):
        estimate_environmental_noise(None)


def test_negative_weight_is_rejected():
    weights = {
        "vibration": 0.010,
        "temperature": 0.020,
        "humidity": 0.005,
        "pressure": 0.005,
        "airflow": 0.005,
        "electromagnetic": 0.030,
        "voltage": 0.025,
        "mechanical_stress": -0.010,
    }

    with pytest.raises(ValueError):
        estimate_environmental_noise(
            EnvironmentalConditions(),
            weights=weights,
        )


def test_custom_weights_change_estimate():
    conditions = EnvironmentalConditions(electromagnetic_noise=1.0)

    normal = estimate_environmental_noise(conditions)
    weights = {
        "vibration": 0.010,
        "temperature": 0.020,
        "humidity": 0.005,
        "pressure": 0.005,
        "airflow": 0.005,
        "electromagnetic": 0.100,
        "voltage": 0.025,
        "mechanical_stress": 0.010,
    }
    stronger = estimate_environmental_noise(conditions, weights=weights)

    assert stronger.probability > normal.probability


def test_resonance_is_highest_near_natural_frequency():
    natural_frequency = 100.0
    damping = 0.1

    at_resonance = resonance_factor(
        natural_frequency,
        natural_frequency,
        damping,
    )
    far_from_resonance = resonance_factor(
        200.0,
        natural_frequency,
        damping,
    )

    assert at_resonance > far_from_resonance
    assert at_resonance == pytest.approx(5.0)


def test_higher_damping_reduces_resonance_peak():
    low_damping = resonance_factor(100.0, 100.0, 0.1)
    high_damping = resonance_factor(100.0, 100.0, 0.5)

    assert low_damping > high_damping


@pytest.mark.parametrize(
    "frequency,natural_frequency,damping",
    [
        (-1.0, 100.0, 0.1),
        (100.0, 0.0, 0.1),
        (100.0, 100.0, 0.0),
    ],
)
def test_invalid_resonance_parameters_are_rejected(
    frequency,
    natural_frequency,
    damping,
):
    with pytest.raises(ValueError):
        resonance_factor(frequency, natural_frequency, damping)


def test_resonance_rejects_non_numeric_parameters():
    with pytest.raises(TypeError):
        resonance_factor("100", 100.0, 0.1)