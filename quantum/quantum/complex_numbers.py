"""
Quantum Computing Lab
Complex number foundations for quantum computing.
"""

import cmath


def magnitude(number):
    """Return the magnitude of a complex number."""

    return abs(number)


def magnitude_squared(number):
    """
    Return the squared magnitude of a complex number.

    In quantum mechanics, this is used to calculate
    measurement probability.
    """

    return abs(number) ** 2


def conjugate(number):
    """Return the complex conjugate."""

    return number.conjugate()


def normalize_state(state):
    """
    Normalize a complex-valued quantum state.
    """

    norm = sum(
        magnitude_squared(amplitude)
        for amplitude in state
    )

    if norm == 0:
        raise ValueError("Cannot normalize a zero state.")

    factor = 1 / (norm ** 0.5)

    return [
        amplitude * factor
        for amplitude in state
    ]


if __name__ == "__main__":

    print("Complex Numbers")
    print("===============")

    number = 1 + 2j

    print("Number:", number)
    print("Magnitude:", magnitude(number))
    print("Magnitude squared:", magnitude_squared(number))
    print("Conjugate:", conjugate(number))

    state = [1 + 0j, 1 + 0j]

    normalized = normalize_state(state)

    print("Original state:", state)
    print("Normalized state:", normalized)

    print(
        "Total probability:",
        sum(magnitude_squared(amplitude)
            for amplitude in normalized)
    )