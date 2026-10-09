import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.qft import N_QUBITS, qft


def test_qft_matches_expected_fourier_state():
    circuit = QuantumCircuit(N_QUBITS)
    circuit.x(0)

    qft(circuit, list(range(N_QUBITS)))

    actual = Statevector.from_instruction(circuit).data

    size = 2**N_QUBITS
    expected = np.array(
        [
            np.exp(2j * np.pi * k / size) / np.sqrt(size)
            for k in range(size)
        ]
    )

    fidelity = abs(np.vdot(expected, actual)) ** 2

    assert np.isclose(fidelity, 1.0, atol=1e-10)


def test_qft_followed_by_inverse_restores_initial_state():
    circuit = QuantumCircuit(N_QUBITS)
    circuit.x(0)

    initial_state = Statevector.from_instruction(circuit)

    qft_circuit = QuantumCircuit(N_QUBITS)
    qft(qft_circuit, list(range(N_QUBITS)))

    circuit.compose(qft_circuit, inplace=True)
    circuit.compose(qft_circuit.inverse(), inplace=True)

    final_state = Statevector.from_instruction(circuit)

    fidelity = abs(
        np.vdot(initial_state.data, final_state.data)
    ) ** 2

    assert np.isclose(fidelity, 1.0, atol=1e-10)


import pytest


@pytest.mark.parametrize("input_value", [0, 2, 7, 15])
def test_qft_matches_expected_fourier_state_for_multiple_inputs(input_value):
    circuit = QuantumCircuit(N_QUBITS)

    for qubit in range(N_QUBITS):
        if (input_value >> qubit) & 1:
            circuit.x(qubit)

    qft(circuit, list(range(N_QUBITS)))

    actual = Statevector.from_instruction(circuit).data

    size = 2**N_QUBITS
    expected = np.array(
        [
            np.exp(2j * np.pi * input_value * k / size) / np.sqrt(size)
            for k in range(size)
        ]
    )

    fidelity = abs(np.vdot(expected, actual)) ** 2

    assert np.isclose(fidelity, 1.0, atol=1e-10)
