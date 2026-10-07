"""
Quantum Computing Lab
Deutsch-Jozsa algorithm with Qiskit.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def create_constant_oracle():
    """Create a constant oracle."""

    return QuantumCircuit(2)


def create_balanced_oracle():
    """Create a balanced oracle."""

    circuit = QuantumCircuit(2)

    circuit.cx(0, 1)

    return circuit


def create_deutsch_jozsa_circuit(oracle):
    """Create the complete Deutsch-Jozsa circuit."""

    circuit = QuantumCircuit(2, 1)

    # Prepare the input qubit.
    circuit.h(0)

    # Prepare the auxiliary qubit in |1>.
    circuit.x(1)
    circuit.h(1)

    # Apply the oracle.
    circuit.compose(oracle, inplace=True)

    # Apply Hadamard to the input qubit.
    circuit.h(0)

    # Measure only the input qubit.
    circuit.measure(0, 0)

    return circuit


def run_algorithm(oracle, shots=1024):
    """Run the Deutsch-Jozsa circuit."""

    circuit = create_deutsch_jozsa_circuit(oracle)

    sampler = StatevectorSampler()

    job = sampler.run([circuit], shots=shots)

    result = job.result()

    return result[0].data.c.get_counts()


if __name__ == "__main__":

    print("Deutsch-Jozsa Algorithm")
    print("=======================")

    print()
    print("Constant Oracle:")

    constant_counts = run_algorithm(
        create_constant_oracle()
    )

    print(constant_counts)

    print()
    print("Balanced Oracle:")

    balanced_counts = run_algorithm(
        create_balanced_oracle()
    )

    print(balanced_counts)
