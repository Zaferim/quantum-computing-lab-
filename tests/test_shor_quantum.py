import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.qft import N_QUBITS, qft
from experiments.shor_quantum import build_shor_period_circuit


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
    input_probabilities = np.zeros(16)
    for index, probability in enumerate(probabilities):
        input_value = index & 0b1111
        input_probabilities[input_value] += probability
    expected_peaks = [0, 4, 8, 12]
    for peak in expected_peaks:
        assert input_probabilities[peak] > 0.24
    for x in range(16):
        if x not in expected_peaks:
            assert input_probabilities[x] < 1e-9
    assert np.isclose(np.sum(input_probabilities), 1.0)
