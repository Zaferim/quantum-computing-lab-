"""
Quantum Computing Lab
Probability foundations for quantum computing.
"""

from random import random


def probability_from_amplitude(amplitude):
    """Calculate probability from a real-valued amplitude."""

    return amplitude ** 2


def normalize_probabilities(probabilities):
    """Normalize a list of probabilities so their sum is 1."""

    total = sum(probabilities)

    if total <= 0:
        raise ValueError("Probability sum must be positive.")

    return [
        probability / total
        for probability in probabilities
    ]


def cumulative_probabilities(probabilities):
    """Calculate cumulative probabilities."""

    normalized = normalize_probabilities(probabilities)

    cumulative = []
    total = 0

    for probability in normalized:
        total += probability
        cumulative.append(total)

    return cumulative


def sample(probabilities):
    """
    Randomly sample an index according to
    the given probability distribution.
    """

    cumulative = cumulative_probabilities(probabilities)

    value = random()

    for index, probability in enumerate(cumulative):
        if value < probability:
            return index

    return len(cumulative) - 1


if __name__ == "__main__":

    print("Quantum Probability")
    print("===================")

    probabilities = [0.25, 0.75]

    print("Probabilities:", probabilities)

    normalized = normalize_probabilities(probabilities)

    print("Normalized:", normalized)

    print(
        "Cumulative:",
        cumulative_probabilities(probabilities)
    )

    print(
        "Random sample:",
        sample(probabilities)
    )