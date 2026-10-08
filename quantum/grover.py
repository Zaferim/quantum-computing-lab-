"""
Quantum Computing Lab
Grover's search algorithm with Qiskit.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def create_oracle():
    """Create an oracle that marks the |11> state."""

    circuit = QuantumCircuit(2)

    circuit.cz(0, 1)

    return circuit

def create_diffuser():
    """Create the Grover diffusion operator."""

    circuit = QuantumCircuit(2)

    circuit.h([0, 1])
    circuit.x([0, 1])
    circuit.cz(0, 1)
    circuit.x([0, 1])
    circuit.h([0, 1])

    return circuit

def create_grover_circuit():
    """Create a two-qubit Grover search circuit."""

    circuit = QuantumCircuit(2)

    circuit.h([0, 1])

    circuit.compose(create_oracle(), inplace=True)
    circuit.compose(create_diffuser(), inplace=True)

    return circuit

def run_grover(shots=1024):
    """Run Grovers algorithm and return measurement counts."""

    circuit = create_grover_circuit()
    circuit.measure_all()

    sampler = StatevectorSampler()

    job = sampler.run([circuit], shots=shots)

    result = job.result()

    return result[0].data.meas.get_counts()

if __name__ == "__main__":

    print("Grovers Search Algorithm")
    print("=========================")

    counts = run_grover()

    print("Measurement Results:")
    print(counts)

    print()
    print("Target state: |11>")
