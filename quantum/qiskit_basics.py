"""
Quantum Computing Lab
First quantum circuit with Qiskit.
"""

from qiskit import QuantumCircuit


def create_bell_circuit():
    """
    Create a Bell state using two qubits.

    |00> → H → CX → Bell state
    """

    circuit = QuantumCircuit(2)

    # Put the first qubit into superposition
    circuit.h(0)

    # Entangle the two qubits
    circuit.cx(0, 1)

    return circuit


if __name__ == "__main__":

    circuit = create_bell_circuit()

    print("Qiskit Quantum Circuit")
    print("----------------------")

    print(circuit)