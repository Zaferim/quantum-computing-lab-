"""
Simon's algorithm for the Quantum Computing Lab.

Includes:
- Classical post-processing over GF(2).
- A state-vector simulation of Simon's quantum circuit.
- A Simon oracle for a nonzero hidden bit string.
"""

from itertools import product
from math import sqrt
from typing import Iterable, List, Optional


def bitwise_inner_product(a: str, b: str) -> int:
    """Return the bitwise inner product modulo 2."""
    if not a or not b:
        raise ValueError("Bit strings must not be empty.")
    if len(a) != len(b):
        raise ValueError("Bit strings must have equal length.")
    if any(bit not in "01" for bit in a + b):
        raise ValueError("Inputs must contain only '0' and '1'.")
    return sum(int(x) * int(y) for x, y in zip(a, b)) % 2


def satisfies_simon_equations(
    candidate: str,
    measurements: Iterable[str],
) -> bool:
    """Check whether candidate satisfies all Simon equations."""
    return all(
        bitwise_inner_product(candidate, measurement) == 0
        for measurement in measurements
    )


def recover_hidden_string(
    measurements: Iterable[str],
) -> Optional[str]:
    """Recover a unique nonzero null-space vector over GF(2)."""
    rows = list(measurements)
    if not rows:
        return None
    if any(not row for row in rows):
        raise ValueError("Measurement bit strings must not be empty.")

    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("All measurement bit strings must have equal length.")
    if any(bit not in "01" for row in rows for bit in row):
        raise ValueError("Measurements must contain only '0' and '1'.")

    matrix = [[int(bit) for bit in row] for row in rows]
    pivot_columns: List[int] = []
    pivot_row = 0

    for column in range(width):
        selected = next(
            (
                index
                for index in range(pivot_row, len(matrix))
                if matrix[index][column] == 1
            ),
            None,
        )
        if selected is None:
            continue

        matrix[pivot_row], matrix[selected] = (
            matrix[selected],
            matrix[pivot_row],
        )

        for index in range(len(matrix)):
            if index != pivot_row and matrix[index][column]:
                matrix[index] = [
                    left ^ right
                    for left, right in zip(matrix[index], matrix[pivot_row])
                ]

        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    free_columns = [
        column for column in range(width) if column not in pivot_columns
    ]

    if len(free_columns) != 1:
        return None

    free_column = free_columns[0]
    solution = [0] * width
    solution[free_column] = 1

    for row_index, pivot_column in enumerate(pivot_columns):
        solution[pivot_column] = matrix[row_index][free_column]

    candidate = "".join(map(str, solution))
    return None if candidate == "0" * width else candidate


def run_simon_postprocessing(measurements: Iterable[str]) -> dict:
    """Run classical post-processing on measurement outcomes."""
    rows = list(measurements)
    hidden_string = recover_hidden_string(rows)
    return {
        "measurements": rows,
        "hidden_string": hidden_string,
        "recovered": hidden_string is not None,
    }


def simon_oracle_output(x: str, hidden_string: str) -> str:
    """
    Return f(x) for a valid Simon function.

    For nonzero secret s, this construction maps x and x XOR s
    to the same output by clearing the first bit position where s is 1.
    The remaining input bits are retained, giving one representative
    for each pair {x, x XOR s}.
    """
    if not x or not hidden_string:
        raise ValueError("Bit strings must not be empty.")
    if len(x) != len(hidden_string):
        raise ValueError("Input and hidden strings must have equal length.")
    if any(bit not in "01" for bit in x + hidden_string):
        raise ValueError("Inputs must contain only '0' and '1'.")
    if "1" not in hidden_string:
        raise ValueError("The hidden string must be nonzero.")

    first_one = hidden_string.index("1")
    paired_x = "".join(
        str(int(left) ^ int(right))
        for left, right in zip(x, hidden_string)
    )

    representative = min(x, paired_x)
    return representative[:first_one] + representative[first_one + 1:]


def simulate_simon_circuit(hidden_string: str) -> dict:
    """
    Simulate the input-register measurement distribution of Simon's circuit.

    This state-vector calculation analytically applies the two layers of
    Hadamard gates and groups amplitudes by oracle-output equivalence.
    It returns exact probabilities rather than sampling measurements.
    """
    if not hidden_string or any(bit not in "01" for bit in hidden_string):
        raise ValueError("The hidden string must be a nonempty bit string.")
    if "1" not in hidden_string:
        raise ValueError("The hidden string must be nonzero.")

    n = len(hidden_string)
    size = 1 << n
    normalization = 1 / size

    # Each oracle output identifies the pair {x, x XOR s}.
    groups = {}
    for value in range(size):
        x = format(value, f"0{n}b")
        output = simon_oracle_output(x, hidden_string)
        groups.setdefault(output, []).append(x)

    probabilities = {}
    for y_value in range(size):
        y = format(y_value, f"0{n}b")
        amplitude = 0.0

        for inputs in groups.values():
            # The output register states are orthogonal. Within each
            # output group, sum the input-register Hadamard amplitudes.
            amplitude_for_group = sum(
                (-1) ** bitwise_inner_product(x, y)
                for x in inputs
            )
            amplitude += amplitude_for_group ** 2

        probabilities[y] = amplitude / (size * size)

    # Remove tiny floating-point noise and ensure normalized output.
    probabilities = {
        y: round(probability, 12)
        for y, probability in probabilities.items()
    }

    return {
        "hidden_string": hidden_string,
        "probabilities": probabilities,
        "valid_measurements": [
            y for y, probability in probabilities.items()
            if probability > 0
        ],
        "probability_sum": round(sum(probabilities.values()), 12),
    }


if __name__ == "__main__":
    secret = "101"
    result = simulate_simon_circuit(secret)

    print("Simon's Quantum Circuit Simulation")
    print("----------------------------------")
    print("Hidden string:", secret)
    print("Valid measurement outcomes:", result["valid_measurements"])
    print("Probability sum:", result["probability_sum"])
    print("Measurement probabilities:")
    for outcome, probability in result["probabilities"].items():
        if probability > 0:
            print(f"  {outcome}: {probability}")
