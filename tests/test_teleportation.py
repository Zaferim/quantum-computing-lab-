import math

import pytest

from quantum.teleportation import (
    apply_cnot,
    apply_single_qubit_gate,
    prepare_input_state,
    simulate_teleportation,
)


def test_input_state_is_normalized():
    state = prepare_input_state()

    norm = sum(abs(amplitude) ** 2 for amplitude in state)

    assert norm == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("theta", "phi"),
    [
        (0.0, 0.0),
        (math.pi / 2, 0.0),
        (math.pi / 2, math.pi / 2),
        (math.pi, math.pi / 3),
        (1.2, 2.4),
    ],
)
def test_teleportation_recovers_input_state(theta, phi):
    result = simulate_teleportation(theta, phi)

    assert result["probability_sum"] == pytest.approx(1.0)
    assert result["all_branches_fidelity_one"] is True


def test_all_measurement_branches_have_equal_probability():
    result = simulate_teleportation()

    for branch in result["measurement_branches"].values():
        assert branch["probability"] == pytest.approx(0.25)


def test_all_nonzero_branches_have_unit_fidelity():
    result = simulate_teleportation()

    for branch in result["measurement_branches"].values():
        if branch["probability"] > 0:
            assert branch["fidelity"] == pytest.approx(1.0)


def test_cnot_flips_target_when_control_is_one():
    state = [0j] * 8
    state[4] = 1.0 + 0j  # |100>

    result = apply_cnot(state, control=0, target=2)

    assert result[5] == pytest.approx(1.0)
    assert sum(abs(value) ** 2 for value in result) == pytest.approx(1.0)


def test_single_qubit_hadamard_preserves_norm():
    state = [1.0 + 0j] + [0j] * 7

    hadamard = [
        [1 / math.sqrt(2), 1 / math.sqrt(2)],
        [1 / math.sqrt(2), -1 / math.sqrt(2)],
    ]

    result = apply_single_qubit_gate(state, hadamard, target=0)

    norm = sum(abs(amplitude) ** 2 for amplitude in result)

    assert norm == pytest.approx(1.0)