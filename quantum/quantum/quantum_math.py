"""
Quantum Computing Lab
Mathematical foundations for quantum computing.
"""

from math import sqrt


def normalize_state(state):
    """
    Normalize a quantum state vector.

    The sum of the squared amplitudes
    must be equal to 1.
    """

    norm = sqrt(sum(amplitude ** 2 for amplitude in state))

    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")

    return [amplitude / norm for amplitude in state]


def probability(amplitude):
    """Calculate probability from a quantum amplitude."""
    return amplitude ** 2


def state_probability(state):
    """
    Calculate probabilities for all amplitudes
    in a quantum state.
    """

    return [probability(amplitude) for amplitude in state]


def inner_product(state_a, state_b):
    """
    Calculate the inner product of two real-valued
    quantum state vectors.
    """

    if len(state_a) != len(state_b):
        raise ValueError("States must have the same dimension.")

    return sum(
        a * b
        for a, b in zip(state_a, state_b)
    )


def vector_norm(state):
    """Calculate the norm of a quantum state vector."""

    return sqrt(
        sum(amplitude ** 2 for amplitude in state)
    )


if __name__ == "__main__":

    print("Quantum Mathematics")
    print("===================")

    state = [1, 1]

    normalized = normalize_state(state)

    print("Original state:", state)
    print("Normalized state:", normalized)

    print("Norm:", vector_norm(normalized))

    print("Probabilities:")
    print(state_probability(normalized))

    print(
        "Inner product:",
        inner_product(normalized, normalized)
    )