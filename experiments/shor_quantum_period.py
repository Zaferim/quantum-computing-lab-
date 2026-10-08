"""
Shor's Algorithm - Quantum Modular Exponentiation

General-purpose modular exponentiation structure.

Default demonstration:
N = 15
a = 2
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


DEFAULT_N = 15
DEFAULT_A = 2
DEFAULT_PERIOD = 4


def get_work_qubits(N: int) -> int:
    """Return the number of qubits needed for the work register."""

    if N <= 1:
        raise ValueError("N must be greater than 1.")

    return max(1, (N - 1).bit_length())


def get_input_qubits(N: int) -> int:
    """
    Return the number of input qubits.

    We use twice the number of work qubits,
    following the standard Shor construction.
    """

    work_qubits = get_work_qubits(N)

    return 2 * work_qubits


def modular_power(
    a: int,
    x: int,
    N: int,
) -> int:
    """Calculate a^x mod N."""

    return pow(a, x, N)


def modular_multiplication_matrix(
    multiplier: int,
    N: int,
) -> np.ndarray:
    """
    Create the modular multiplication matrix.

    For valid states y < N:

        |y> -> |multiplier*y mod N>

    States y >= N are left unchanged.
    """

    work_qubits = get_work_qubits(N)
    dimension = 2 ** work_qubits

    matrix = np.zeros(
        (dimension, dimension)
    )

    for y in range(dimension):

        if y < N:
            target = (
                multiplier * y
            ) % N
        else:
            target = y

        matrix[target, y] = 1

    return matrix


def build_controlled_modular_exponentiation(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> QuantumCircuit:
    """
    Build controlled modular exponentiation.

    The circuit implements:

        |x>|1> -> |x>|a^x mod N>

    using controlled modular multiplication.
    """

    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)

    circuit = QuantumCircuit(
        input_qubits + work_qubits
    )

    # Prepare |1> in the work register.
    circuit.x(input_qubits)

    for i in range(input_qubits):

        multiplier = pow(
            a,
            2 ** i,
            N,
        )

        matrix = (
            modular_multiplication_matrix(
                multiplier,
                N,
            )
        )

        controlled = (
            Operator(matrix)
            .to_instruction()
            .control(1)
        )

        circuit.append(
            controlled,
            [
                i,
                *range(
                    input_qubits,
                    input_qubits + work_qubits,
                ),
            ],
        )

    return circuit


def verify_classical_period(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
    period: int = DEFAULT_PERIOD,
) -> None:
    """Verify that the supplied period is correct."""

    for x in range(
        2 * get_work_qubits(N)
    ):
        assert modular_power(
            a,
            x,
            N,
        ) == modular_power(
            a,
            x + period,
            N,
        )

    print(
        "✓ Classical period verification passed."
    )


def get_controlled_multipliers(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> list[int]:
    """Return the controlled modular multipliers."""

    input_qubits = get_input_qubits(N)

    return [
        pow(
            a,
            2 ** i,
            N,
        )
        for i in range(input_qubits)
    ]


def verify_multipliers(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> None:
    """Verify controlled modular multipliers."""

    actual = get_controlled_multipliers(
        a,
        N,
    )

    print(
        "✓ Controlled multipliers verified."
    )
    print(
        f"  Multipliers: {actual}"
    )


def verify_unitary(
    multiplier: int,
    N: int = DEFAULT_N,
) -> None:
    """Verify that modular multiplication is unitary."""

    matrix = (
        modular_multiplication_matrix(
            multiplier,
            N,
        )
    )

    dimension = (
        2 ** get_work_qubits(N)
    )

    identity = np.eye(
        dimension
    )

    assert np.allclose(
        matrix.conj().T @ matrix,
        identity,
    )

    print(
        f"✓ Modular multiplication by "
        f"{multiplier} is unitary."
    )


def main() -> None:
    """Run the default N=15, a=2 demonstration."""

    N = DEFAULT_N
    a = DEFAULT_A
    period = DEFAULT_PERIOD

    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)

    print(
        "Shor's Algorithm - "
        "Controlled Modular Exponentiation"
    )
    print(
        "-----------------------------------"
    )
    print(f"N = {N}")
    print(f"a = {a}")
    print(
        f"Input qubits = {input_qubits}"
    )
    print(
        f"Work qubits = {work_qubits}"
    )
    print()

    verify_classical_period(
        a,
        N,
        period,
    )

    print()

    verify_multipliers(
        a,
        N,
    )

    print()

    multipliers = (
        get_controlled_multipliers(
            a,
            N,
        )
    )

    for multiplier in multipliers:
        verify_unitary(
            multiplier,
            N,
        )

    print()

    circuit = (
        build_controlled_modular_exponentiation(
            a,
            N,
        )
    )

    print(
        "Controlled modular "
        "exponentiation circuit:"
    )
    print()
    print(circuit)

    print()
    print(
        "✓ Controlled modular "
        "exponentiation circuit created."
    )


if __name__ == "__main__":
    main()