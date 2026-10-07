"""
Quantum Computing Lab
Basic quantum tests.
"""

from quantum.basics import (
    zero_state,
    one_state,
    hadamard_state,
    probability
)

from quantum.circuits import create_superposition


def test_zero_state():
    assert zero_state() == [1, 0]


def test_one_state():
    assert one_state() == [0, 1]


def test_superposition():

    state = hadamard_state()

    assert len(state) == 2

    assert abs(
        probability(state[0]) - 0.5
    ) < 0.0001

    assert abs(
        probability(state[1]) - 0.5
    ) < 0.0001


def test_circuit():

    state = create_superposition()

    assert len(state) == 2

    assert abs(
        probability(state[0]) - 0.5
    ) < 0.0001

    assert abs(
        probability(state[1]) - 0.5
    ) < 0.0001


if __name__ == "__main__":

    test_zero_state()
    test_one_state()
    test_superposition()
    test_circuit()

    print("All quantum tests passed!")