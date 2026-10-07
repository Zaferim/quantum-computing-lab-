"""
Quantum Computing Lab
Basic quantum computing concepts.
"""

from math import sqrt


def zero_state():
    """Return the |0> quantum state."""
    return [1, 0]


def one_state():
    """Return the |1> quantum state."""
    return [0, 1]


def hadamard_state():
    """
    Apply the Hadamard transformation
    to the |0> state.

    Result:
    |+> = 1/sqrt(2) [1, 1]
    """

    value = 1 / sqrt(2)

    return [value, value]


def probability(amplitude):
    """Calculate probability from a quantum amplitude."""
    return amplitude ** 2


if __name__ == "__main__":

    print("Quantum Computing Lab")
    print("---------------------")

    print("|0> =", zero_state())
    print("|1> =", one_state())

    state = hadamard_state()

    print("|+> =", state)

    print("P(0) =", probability(state[0]))
    print("P(1) =", probability(state[1]))