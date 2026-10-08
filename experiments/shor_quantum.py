"""
Shor's Algorithm - Quantum Period Finding

N = 15
a = 2

Stages:
1. Create uniform superposition.
2. Controlled modular exponentiation.
3. Apply inverse QFT.
4. Inspect period-finding peaks.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.shor_quantum_period import (
    build_controlled_modular_exponentiation,
)


N = 15
A = 2
INPUT_QUBITS = 4
WORK_QUBITS = 4


def inverse_qft(
    circuit: QuantumCircuit,
    qubits: list[int],
) -> None:
    """Apply the inverse of the corrected Quantum Fourier Transform."""

    n = len(qubits)

    # Undo the QFT swap layer.
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - i - 1])

    # Exact inverse of the corrected QFT:
    # QFT:
    #   j = n-1 ... 0
    #   H(j)
    #   CP(k, j)
    #
    # Therefore the inverse runs:
    #   j = 0 ... n-1
    #   CP(-angle)
    #   H(j)
    for j in range(n):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            circuit.cp(angle, qubits[k], qubits[j])

        circuit.h(qubits[j])


def build_shor_period_circuit() -> QuantumCircuit:
    """Build the complete quantum period-finding circuit."""

    circuit = QuantumCircuit(
        INPUT_QUBITS + WORK_QUBITS
    )

    # Prepare work register in |1>.
    circuit.x(INPUT_QUBITS)

    # Create uniform superposition in input register.
    for qubit in range(INPUT_QUBITS):
        circuit.h(qubit)

    # Controlled modular exponentiation.
    modular_circuit = (
        build_controlled_modular_exponentiation()
    )

    # Remove the X gate that prepares |1> because
    # the main circuit already prepared it.
    modular_circuit.data.pop(0)

    circuit.compose(
        modular_circuit,
        qubits=range(INPUT_QUBITS + WORK_QUBITS),
        inplace=True,
    )

    # Apply inverse QFT to the input register.
    inverse_qft(
        circuit,
        list(range(INPUT_QUBITS)),
    )

    return circuit


def verify_period_finding_state(
    circuit: QuantumCircuit,
) -> None:
    """Verify that inverse QFT produces period-related peaks."""

    state = Statevector.from_instruction(circuit)

    probabilities = np.abs(state.data) ** 2

    input_probabilities = np.zeros(2 ** INPUT_QUBITS)

    for index, probability in enumerate(probabilities):
        input_value = index & 0b1111
        input_probabilities[input_value] += probability

    print("Input-register probabilities after inverse QFT:")
    print()

    for x, probability in enumerate(input_probabilities):
        if probability > 1e-9:
            print(
                f"x={x:2d} | probability={probability:.6f}"
            )

    # For r = 4 and a 16-state input register,
    # the ideal peaks are at 0, 4, 8 and 12.
    expected_peaks = [0, 4, 8, 12]

    for peak in expected_peaks:
        assert input_probabilities[peak] > 0.24

    # States outside the four peaks should have
    # negligible probability in the ideal case.
    for x in range(16):
        if x not in expected_peaks:
            assert input_probabilities[x] < 1e-9

    assert np.isclose(
        np.sum(input_probabilities),
        1.0,
    )

    print()
    print("✓ Period-finding peaks verified.")
    print("✓ Peaks occur at 0, 4, 8 and 12.")
    print("✓ Total probability = 1.0")


def main() -> None:
    print("Shor's Algorithm - Quantum Period Finding")
    print("------------------------------------------")
    print(f"N = {N}")
    print(f"a = {A}")
    print()

    circuit = build_shor_period_circuit()

    print("Complete quantum period-finding circuit:")
    print()
    print(circuit)

    print()

    verify_period_finding_state(circuit)


if __name__ == "__main__":
    main()
