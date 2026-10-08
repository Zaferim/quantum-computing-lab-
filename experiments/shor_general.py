"""
General-purpose Shor's Algorithm.

Supports different odd composite N values
and valid coprime bases a.
"""

from math import gcd

from experiments.shor_period import factor_from_period
from experiments.shor_quantum_period import (
    get_input_qubits,
    get_work_qubits,
)


def validate_inputs(a: int, N: int) -> None:
    """Validate Shor's algorithm inputs."""

    if N <= 1:
        raise ValueError("N must be greater than 1.")

    if N % 2 == 0:
        raise ValueError("N must be odd for this implementation.")

    if a <= 1 or a >= N:
        raise ValueError(
            "a must satisfy 1 < a < N."
        )

    if gcd(a, N) != 1:
        raise ValueError(
            "a and N must be coprime."
        )


def find_classical_period(
    a: int,
    N: int,
) -> int:
    """Find the multiplicative period classically."""

    validate_inputs(a, N)

    value = 1

    for r in range(1, N):
        value = (value * a) % N

        if value == 1:
            return r

    raise ValueError(
        "No period found."
    )


def factor_with_shor(
    a: int,
    N: int,
) -> tuple[int, int]:
    """
    Run the classical Shor factoring pipeline.

    This first version uses classical period finding.
    The quantum period-finding circuit will replace
    this step in the next stage.
    """

    validate_inputs(a, N)

    period = find_classical_period(
        a,
        N,
    )

    if period % 2 != 0:
        raise ValueError(
            "Found period is odd."
        )

    factors = factor_from_period(
        a,
        N,
        period,
    )

    return factors


def describe_problem(
    a: int,
    N: int,
) -> None:
    """Print the Shor problem configuration."""

    validate_inputs(a, N)

    print(
        "General Shor's Algorithm"
    )
    print(
        "========================"
    )
    print(f"N = {N}")
    print(f"a = {a}")
    print(
        f"Input qubits = "
        f"{get_input_qubits(N)}"
    )
    print(
        f"Work qubits = "
        f"{get_work_qubits(N)}"
    )


def main() -> None:
    """Run a default demonstration with N=21, a=2."""

    N = 21
    a = 2

    describe_problem(
        a,
        N,
    )

    period = find_classical_period(
        a,
        N,
    )

    print(
        f"Classical period r = {period}"
    )

    factor1, factor2 = factor_with_shor(
        a,
        N,
    )

    print()
    print(
        f"✓ {N} = {factor1} × {factor2}"
    )


if __name__ == "__main__":
    main()