"""
Quantum Fourier Transform (QFT)
4-qubit demonstration for Shor's Algorithm
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


N_QUBITS = 4


def qft(circuit: QuantumCircuit, qubits: list[int]) -> None:
    """Apply the Quantum Fourier Transform."""
    n = len(qubits)

    for j in range(n):
        circuit.h(qubits[j])

        for k in range(j + 1, n):
            angle = np.pi / (2 ** (k - j))
            circuit.cp(angle, qubits[k], qubits[j])

    # Reverse qubit order
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - i - 1])


def main() -> None:
    circuit = QuantumCircuit(N_QUBITS)

    # Prepare |0001>
    circuit.x(0)

    # Apply QFT
    qft(circuit, list(range(N_QUBITS)))

    print("Quantum Fourier Transform")
    print("--------------------------")
    print(circuit)

    state = Statevector.from_instruction(circuit)

    probabilities = np.abs(state.data) ** 2

    print()
    print("State probabilities:")

    for index, probability in enumerate(probabilities):
        if probability > 1e-9:
            print(
                f"|{index:04b}> : "
                f"{probability:.6f}"
            )


if __name__ == "__main__":
    main()


def verify_qft() -> None:
    """Verify that QFT(|1>) produces uniform probabilities."""

    circuit = QuantumCircuit(N_QUBITS)
    circuit.x(0)

    qft(circuit, list(range(N_QUBITS)))

    state = Statevector.from_instruction(circuit)
    probabilities = np.abs(state.data) ** 2

    expected = 1 / (2 ** N_QUBITS)

    assert len(probabilities) == 2 ** N_QUBITS

    for probability in probabilities:
        assert np.isclose(probability, expected)

    assert np.isclose(np.sum(probabilities), 1.0)

    print()
    print("✓ QFT probability test passed.")
    print("✓ All 16 basis states have probability 1/16.")
    print("✓ Total probability = 1.0")


if __name__ == "__main__":
    verify_qft()
