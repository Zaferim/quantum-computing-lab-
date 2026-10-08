"""
Shor's Algorithm - Complete Quantum Factoring Pipeline

Default demonstration:
N = 15
a = 2

Pipeline:
1. Create uniform superposition.
2. Controlled modular exponentiation.
3. Apply inverse QFT.
4. Extract period r automatically.
5. Use classical Shor post-processing.
6. Obtain factors 3 and 5.
"""

import numpy as np
from math import gcd
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.shor_quantum_period import (
    build_controlled_modular_exponentiation,
    get_input_qubits,
    get_work_qubits,
)

from experiments.shor_period import (
    factor_from_period,
)


N = 15
A = 2

INPUT_QUBITS = get_input_qubits(N)
WORK_QUBITS = get_work_qubits(N)


def inverse_qft(
    circuit: QuantumCircuit,
    qubits: list[int],
) -> None:
    """Apply the inverse Quantum Fourier Transform."""

    n = len(qubits)

    # Undo the QFT swap layer.
    for i in range(n // 2):
        circuit.swap(
            qubits[i],
            qubits[n - i - 1],
        )

    # Exact inverse of the corrected QFT.
    for j in range(n):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))

            circuit.cp(
                angle,
                qubits[k],
                qubits[j],
            )

        circuit.h(qubits[j])


def build_shor_period_circuit() -> QuantumCircuit:
    """Build the complete quantum period-finding circuit."""

    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)

    circuit = QuantumCircuit(
        input_qubits + work_qubits
    )

    # Prepare work register in |1>.
    circuit.x(input_qubits)

    # Create uniform superposition
    # in the input register.
    for qubit in range(input_qubits):
        circuit.h(qubit)

    # Build controlled modular exponentiation.
    modular_circuit = (
        build_controlled_modular_exponentiation(
            A,
            N,
        )
    )

    # Remove the X gate that prepares |1>
    # because the main circuit already prepared it.
    modular_circuit.data.pop(0)

    circuit.compose(
        modular_circuit,
        qubits=range(
            input_qubits + work_qubits
        ),
        inplace=True,
    )

    # Apply inverse QFT to input register.
    inverse_qft(
        circuit,
        list(range(input_qubits)),
    )

    return circuit


def get_input_probabilities(
    circuit: QuantumCircuit,
) -> np.ndarray:
    """Return probabilities for the input register."""

    input_qubits = get_input_qubits(N)

    state = Statevector.from_instruction(
        circuit
    )

    probabilities = (
        np.abs(state.data) ** 2
    )

    input_probabilities = np.zeros(
        2 ** input_qubits
    )

    input_mask = (
        2 ** input_qubits
    ) - 1

    for index, probability in enumerate(
        probabilities
    ):
        input_value = (
            index & input_mask
        )

        input_probabilities[
            input_value
        ] += probability

    return input_probabilities


def extract_period_from_probabilities(
    input_probabilities: np.ndarray,
) -> int:
    """
    Extract the period from ideal period-finding peaks.

    For an input register of size Q, peaks are
    approximately separated by Q / r.
    """

    peak_threshold = (
        0.20
    )

    peaks = [
        i
        for i, probability in enumerate(
            input_probabilities
        )
        if probability > peak_threshold
    ]

    if len(peaks) < 2:
        raise ValueError(
            "Not enough period-finding peaks detected."
        )

    differences = [
        peaks[i + 1] - peaks[i]
        for i in range(len(peaks) - 1)
    ]

    spacing = min(differences)

    if spacing <= 0:
        raise ValueError(
            "Invalid peak spacing."
        )

    input_size = len(
        input_probabilities
    )

    period_estimate = round(
        input_size / spacing
    )

    if period_estimate <= 0:
        raise ValueError(
            "Invalid period candidate."
        )

    return period_estimate


def verify_period_finding_state(
    circuit: QuantumCircuit,
) -> int:
    """Verify period-finding peaks and return r."""

    input_probabilities = (
        get_input_probabilities(circuit)
    )

    input_qubits = get_input_qubits(N)
    input_size = 2 ** input_qubits

    print(
        "Input-register probabilities after inverse QFT:"
    )
    print()

    for x, probability in enumerate(
        input_probabilities
    ):
        if probability > 1e-9:
            print(
                f"x={x:3d} | "
                f"probability={probability:.6f}"
            )

    period = (
        extract_period_from_probabilities(
            input_probabilities
        )
    )

    # Verify the extracted period classically.
    for x in range(
        2 * get_work_qubits(N)
    ):
        assert (
            pow(A, x, N)
            == pow(A, x + period, N)
        )

    assert (
        pow(A, period, N) == 1
    )

    assert np.isclose(
        np.sum(input_probabilities),
        1.0,
    )

    print()
    print(
        "✓ Period-finding peaks verified."
    )
    print(
        f"✓ Input register size = {input_size}"
    )
    print(
        f"✓ Extracted period r = {period}."
    )
    print(
        "✓ Total probability = 1.0"
    )

    return period


def quantum_shor_factorization() -> tuple[int, int]:
    """
    Complete Shor pipeline.

    Quantum period finding produces r.
    Classical post-processing produces factors.
    """

    circuit = build_shor_period_circuit()

    period = verify_period_finding_state(
        circuit
    )

    factors = factor_from_period(
        A,
        N,
        period,
    )

    return factors


def main() -> None:
    print(
        "Shor's Algorithm - Complete Quantum Factoring"
    )
    print(
        "============================================="
    )
    print(f"N = {N}")
    print(f"a = {A}")
    print(
        f"Input qubits = {INPUT_QUBITS}"
    )
    print(
        f"Work qubits = {WORK_QUBITS}"
    )
    print()

    circuit = build_shor_period_circuit()

    print(
        "Complete quantum period-finding circuit:"
    )
    print()
    print(circuit)
    print()

    period = verify_period_finding_state(
        circuit
    )

    factor1, factor2 = factor_from_period(
        A,
        N,
        period,
    )

    print()
    print("Classical post-processing")
    print("-------------------------")
    print(f"Quantum period r = {period}")
    print(
        f"a^(r/2) mod N = "
        f"{pow(A, period // 2, N)}"
    )
    print(
        f"gcd(a^(r/2) - 1, N) = "
        f"{gcd(pow(A, period // 2, N) - 1, N)}"
    )
    print(
        f"gcd(a^(r/2) + 1, N) = "
        f"{gcd(pow(A, period // 2, N) + 1, N)}"
    )

    print()
    print(
        "✓ Shor factorization result:"
    )
    print(
        f"✓ {N} = {factor1} × {factor2}"
    )

    assert {
        factor1,
        factor2,
    } == {3, 5}


if __name__ == "__main__":
    main()