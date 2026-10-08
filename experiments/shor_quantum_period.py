"""
Shor's Algorithm - Quantum Period Finding
N = 15, a = 2

Stage:
- Classical period verification
- Reversible modular multiplication
- Controlled modular exponentiation structure
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


N = 15
A = 2
PERIOD = 4
N_QUBITS = 4


def modular_power(a: int, x: int, N: int) -> int:
    return pow(a, x, N)


def modular_multiplication_matrix(multiplier: int) -> np.ndarray:
    """Create |y> -> |multiplier*y mod 15>."""
    dimension = 2 ** N_QUBITS
    matrix = np.zeros((dimension, dimension))

    for y in range(dimension):
        if y < N:
            target = (multiplier * y) % N
        else:
            target = y

        matrix[target, y] = 1

    return matrix


def build_controlled_modular_exponentiation() -> QuantumCircuit:
    """
    Build:

        |x>|1> -> |x>|2^x mod 15>

    using four control qubits and four target qubits.

    For each control bit i we apply multiplication by:

        2^(2^i) mod 15
    """

    circuit = QuantumCircuit(8)

    # Input register: q[0..3]
    # Work/output register: q[4..7]

    # Prepare |1> in the output register.
    circuit.x(4)

    for i in range(4):
        multiplier = pow(A, 2 ** i, N)

        matrix = modular_multiplication_matrix(multiplier)

        controlled = Operator(matrix).to_instruction().control(1)

        circuit.append(
            controlled,
            [i, 4, 5, 6, 7]
        )

    return circuit


def verify_classical_period() -> None:
    for x in range(16):
        assert modular_power(A, x, N) == modular_power(
            A, x + PERIOD, N
        )

    print("✓ Classical period verification passed.")


def verify_multipliers() -> None:
    expected = [2, 4, 1, 1]

    actual = [
        pow(A, 2 ** i, N)
        for i in range(4)
    ]

    assert actual == expected

    print("✓ Controlled multipliers verified.")
    print(f"  Multipliers: {actual}")


def verify_unitary(multiplier: int) -> None:
    matrix = modular_multiplication_matrix(multiplier)

    identity = np.eye(2 ** N_QUBITS)

    assert np.allclose(
        matrix.conj().T @ matrix,
        identity
    )

    print(
        f"✓ Modular multiplication by {multiplier} "
        f"is unitary."
    )


def main() -> None:
    print("Shor's Algorithm - Controlled Modular Exponentiation")
    print("---------------------------------------------------")
    print(f"N = {N}")
    print(f"a = {A}")
    print()

    verify_classical_period()

    print()

    verify_multipliers()

    print()

    for multiplier in [2, 4, 1]:
        verify_unitary(multiplier)

    print()

    circuit = build_controlled_modular_exponentiation()

    print("Controlled modular exponentiation circuit:")
    print()
    print(circuit)

    print()
    print("✓ Controlled modular exponentiation circuit created.")


if __name__ == "__main__":
    main()
