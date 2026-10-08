import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.qft import N_QUBITS, qft
from experiments.shor_quantum import (
    build_shor_period_circuit,
    get_input_qubits,
    N,
)


def test_qft_uniform_distribution():
    circuit = QuantumCircuit(N_QUBITS)
    circuit.x(0)
    qft(circuit, list(range(N_QUBITS)))

    state = Statevector.from_instruction(circuit)
    probabilities = np.abs(state.data) ** 2

    expected = 1 / (2 ** N_QUBITS)

    assert len(probabilities) == 2 ** N_QUBITS
    assert np.allclose(probabilities, expected)
    assert np.isclose(np.sum(probabilities), 1.0)


def test_shor_quantum_period_finding():
    circuit = build_shor_period_circuit()

    state = Statevector.from_instruction(circuit)
    probabilities = np.abs(state.data) ** 2

    input_qubits = get_input_qubits(N)
    input_size = 2 ** input_qubits
    input_probabilities = np.zeros(input_size)

    input_mask = input_size - 1

    for index, probability in enumerate(probabilities):
        input_value = index & input_mask
        input_probabilities[input_value] += probability

    expected_peaks = [0, 64, 128, 192]

    for peak in expected_peaks:
        assert input_probabilities[peak] > 0.24

    for x in range(input_size):
        if x not in expected_peaks:
            assert input_probabilities[x] < 1e-9

    assert np.isclose(np.sum(input_probabilities), 1.0)