"""
Quantum Computing Lab
Bell state simulation with Qiskit.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def create_bell_circuit():
    """
    Create a Bell state using two qubits.
    """

    circuit = QuantumCircuit(2)

    # Create superposition
    circuit.h(0)

    # Create entanglement
    circuit.cx(0, 1)

    # Measure both qubits
    circuit.measure_all()

    return circuit


def run_bell_experiment(shots=1024):
    """
    Run the Bell state experiment.

    Expected results:
    00 ≈ 50%
    11 ≈ 50%
    """

    circuit = create_bell_circuit()

    sampler = StatevectorSampler()

    job = sampler.run([circuit], shots=shots)

    result = job.result()

    counts = result[0].data.meas.get_counts()

    return counts


if __name__ == "__main__":

    print("Qiskit Bell State Experiment")
    print("============================")

    circuit = create_bell_circuit()

    print()
    print("Bell Circuit:")
    print(circuit)

    print()

    counts = run_bell_experiment()

    print("Measurement Results:")
    print(counts)

    print()
    print("Expected:")
    print("00 ≈ 50%")