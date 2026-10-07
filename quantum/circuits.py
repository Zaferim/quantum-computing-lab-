"""
Quantum Computing Lab
Basic quantum circuits.
"""

from math import sqrt


def hadamard_gate():
    """
    Return the Hadamard gate matrix.

    H = 1/sqrt(2) * [[1, 1],
                     [1, -1]]
    """

    value = 1 / sqrt(2)

    return [
        [value, value],
        [value, -value]
    ]


def apply_gate(gate, state):
    """
    Apply a quantum gate to a quantum state.
    """

    result = []

    for row in gate:

        value = 0

        for i in range(len(state)):
            value += row[i] * state[i]

        result.append(value)

    return result


def create_superposition():
    """
    Apply the Hadamard gate to the |0> state.
    """

    zero = [1, 0]

    h = hadamard_gate()

    return apply_gate(h, zero)


if __name__ == "__main__":

    print("Quantum Circuit Test")
    print("---------------------")

    print("Hadamard Gate:")

    for row in hadamard_gate():
        print(row)

    print()

    state = create_superposition()

    print("Initial state: |0>")
    print("After Hadamard:")

    print(state)

    print()

    print("Expected probabilities:")
    print("P(0) = 0.5")
    print("P(1) = 0.5")