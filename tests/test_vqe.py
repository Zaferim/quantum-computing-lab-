import math

import pytest

from quantum.vqe import (
    expectation_value,
    find_ground_state,
    single_qubit_state,
)


def test_single_qubit_state_is_normalized():
    state = single_qubit_state(0.7)
    norm = sum(abs(amplitude) ** 2 for amplitude in state)
    assert norm == pytest.approx(1.0)


def test_single_qubit_state_at_zero():
    state = single_qubit_state(0.0)
    assert state[0] == pytest.approx(1.0)
    assert state[1] == pytest.approx(0.0)


def test_single_qubit_state_rejects_infinite_angle():
    with pytest.raises(ValueError):
        single_qubit_state(float("inf"))


def test_expectation_value_at_zero():
    assert expectation_value(
        0.0, a=0.2, b=0.5, c=0.7
    ) == pytest.approx(0.9)


def test_expectation_value_rejects_non_finite_values():
    with pytest.raises(ValueError):
        expectation_value(float("nan"))


def test_ground_state_energy_matches_theoretical_minimum():
    result = find_ground_state(steps=10000)
    expected = -math.sqrt(1.0**2 + 0.5**2)
    assert result["energy"] == pytest.approx(expected, abs=1e-6)


def test_ground_state_search_returns_valid_angle():
    result = find_ground_state(steps=1000)
    assert 0.0 <= result["theta"] <= 2 * math.pi
    assert result["steps"] == 1000


def test_ground_state_energy_with_identity_term():
    result = find_ground_state(steps=10000, a=2.0, b=1.0, c=0.5)
    expected = 2.0 - math.sqrt(1.0**2 + 0.5**2)
    assert result["energy"] == pytest.approx(expected, abs=1e-6)


@pytest.mark.parametrize("steps", [0, 1, -10, 2.5, True])
def test_invalid_step_counts_are_rejected(steps):
    with pytest.raises(ValueError):
        find_ground_state(steps=steps)