"""
Quantum Computing Lab
Classical optimization foundation.

This section starts with classical optimization.
Later, we will compare the same problem
with quantum optimization methods.
"""


def calculate_score(values):
    """
    Calculate the total score of a list of values.
    """

    if not values:
        return 0

    return sum(values)


def find_best(values):
    """
    Find the highest value in a list.
    """

    if not values:
        return None

    return max(values)


def optimize(values):
    """
    Simple classical optimization.

    For now, select the highest score.
    """

    best = find_best(values)

    return {
        "best_value": best,
        "score": calculate_score(values)
    }


if __name__ == "__main__":

    values = [10, 25, 18, 42, 31]

    result = optimize(values)

    print("Classical Optimization")
    print("----------------------")

    print("Values:", values)

    print("Best value:", result["best_value"])

    print("Total score:", result["score"])