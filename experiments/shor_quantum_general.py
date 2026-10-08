"""
General-purpose quantum period finding for Shor's Algorithm.

This implementation uses an ideal Statevector simulation.
Period extraction is heuristic and will be improved later
with continued fractions and measurement sampling.
"""

from math import gcd

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from experiments.shor_quantum_period import (
    build_controlled_modular_exponentiation,
    get_input_qubits,
    get_work_qubits,
)

from experiments.shor_period import factor_from_period


def validate_inputs(a: int, N: int) -> None:
    """Validate the modulus and base."""

    if not isinstance(a, int) or isinstance(a, bool):
        raise ValueError("a must be an integer.")

    if not isinstance(N, int) or isinstance(N, bool):
        raise ValueError("N must be an integer.")

    if N <= 1 or N % 2 == 0:
        raise ValueError("N must be an odd integer greater than 1.")

    if not 1 < a < N:
        raise ValueError("a must satisfy 1 < a < N.")

    if gcd(a, N) != 1:
        raise ValueError("a and N must be coprime.")


def inverse_qft(
    circuit: QuantumCircuit,
    qubits: list[int],
) -> None:
    """Apply the inverse quantum Fourier transform."""

    n = len(qubits)

    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - i - 1])

    for j in range(n):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            circuit.cp(angle, qubits[k], qubits[j])

        circuit.h(qubits[j])


def build_quantum_period_circuit(
    a: int,
    N: int,
) -> QuantumCircuit:
    """Build a parameterized quantum period-finding circuit."""

    validate_inputs(a, N)

    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)

    circuit = QuantumCircuit(input_qubits + work_qubits)

    # Prepare the work register in |1>.
    circuit.x(input_qubits)

    # Create a uniform superposition in the input register.
    for qubit in range(input_qubits):
        circuit.h(qubit)

    modular_circuit = build_controlled_modular_exponentiation(
        a,
        N,
    )

    # The modular exponentiation builder initializes the work
    # register in |1>. Avoid applying that initialization twice.
    if len(modular_circuit.data) == 0:
        raise ValueError(
            "The modular exponentiation circuit is unexpectedly empty."
        )

    modular_circuit.data.pop(0)

    circuit.compose(
        modular_circuit,
        qubits=range(input_qubits + work_qubits),
        inplace=True,
    )

    inverse_qft(
        circuit,
        list(range(input_qubits)),
    )

    return circuit


def get_input_probabilities(
    circuit: QuantumCircuit,
    N: int,
) -> np.ndarray:
    """Calculate the marginal probabilities of the input register."""

    input_qubits = get_input_qubits(N)

    state = Statevector.from_instruction(circuit)
    probabilities = np.abs(state.data) ** 2

    input_size = 2**input_qubits
    input_mask = input_size - 1

    input_probabilities = np.zeros(input_size, dtype=float)

    # Sum over work-register states.
    for index, probability in enumerate(probabilities):
        input_value = index & input_mask
        input_probabilities[input_value] += probability

    return input_probabilities


def extract_period_from_probabilities(
    probabilities: np.ndarray,
    a: int,
    N: int,
) -> int:
    """
    Estimate the period from prominent probability peaks.

    This is a heuristic. It is not a replacement for continued
    fractions and measurement-based post-processing.
    """

    validate_inputs(a, N)

    probabilities = np.asarray(probabilities, dtype=float)

    if probabilities.ndim != 1 or len(probabilities) == 0:
        raise ValueError(
            "A non-empty one-dimensional probability array is required."
        )

    if not np.all(np.isfinite(probabilities)):
        raise ValueError("Probabilities must contain only finite values.")

    if np.any(probabilities < 0):
        raise ValueError("Probabilities cannot be negative.")

    total_probability = float(np.sum(probabilities))

    if total_probability <= 0:
        raise ValueError("The total probability must be positive.")

    probabilities = probabilities / total_probability

    max_probability = float(np.max(probabilities))

    if max_probability <= 0:
        raise ValueError("No probability peaks were found.")

    threshold = max_probability * 0.10
    peak_indices = np.flatnonzero(probabilities >= threshold)

    if len(peak_indices) < 2:
        raise ValueError(
            "Not enough significant peaks to estimate a period."
        )

    register_size = len(probabilities)
    candidates = set()

    # Estimate candidate periods from distances between peaks.
    for i in range(len(peak_indices)):
        for j in range(i + 1, len(peak_indices)):
            spacing = int(peak_indices[j] - peak_indices[i])

            if spacing <= 0:
                continue

            estimate = round(register_size / spacing)

            if estimate > 0:
                candidates.add(estimate)

    if not candidates:
        raise ValueError("No period candidate could be estimated.")

    # Verify candidates against the supplied base.
    valid_candidates = sorted(
        candidate
        for candidate in candidates
        if pow(a, candidate, N) == 1
    )

    if valid_candidates:
        return valid_candidates[0]

    raise ValueError(
        "The probability peaks did not produce a verified period. "
        "Continued-fraction post-processing may be needed."
    )


def reduce_period(
    a: int,
    N: int,
    period: int,
) -> int:
    """Reduce a verified period when a smaller valid period exists."""

    validate_inputs(a, N)

    if not isinstance(period, int) or isinstance(period, bool):
        raise ValueError("The period must be an integer.")

    if period <= 0:
        raise ValueError("The period must be positive.")

    if pow(a, period, N) != 1:
        raise ValueError(
            "The supplied period does not satisfy a**r = 1 (mod N)."
        )

    reduced = period
    divisor = 2

    while divisor * divisor <= reduced:
        if reduced % divisor == 0:
            candidate = reduced // divisor

            if pow(a, candidate, N) == 1:
                reduced = candidate
                continue

        divisor += 1

    return reduced


def quantum_period_finding(
    a: int,
    N: int,
) -> tuple[int, QuantumCircuit, np.ndarray]:
    """Build the circuit and estimate its period."""

    validate_inputs(a, N)

    circuit = build_quantum_period_circuit(a, N)
    probabilities = get_input_probabilities(circuit, N)

    period = extract_period_from_probabilities(
        probabilities,
        a,
        N,
    )

    period = reduce_period(a, N, period)

    return period, circuit, probabilities


def quantum_shor_factorization(
    a: int,
    N: int,
) -> tuple[int, int]:
    """
    Factor N using quantum period finding.

    Try the requested base first. If it does not produce valid
    non-trivial factors, try other coprime bases automatically.
    """

    validate_inputs(a, N)

    # Preserve the requested base as the first attempt.
    candidate_bases = [a]

    # Add other valid bases without duplicates.
    candidate_bases.extend(
        candidate
        for candidate in range(2, N)
        if candidate != a and gcd(candidate, N) == 1
    )

    errors = []

    for candidate_a in candidate_bases:
        try:
            period, _, _ = quantum_period_finding(
                candidate_a,
                N,
            )

            # Verify the period mathematically before factorization.
            if period <= 0 or pow(candidate_a, period, N) != 1:
                errors.append(
                    f"a={candidate_a}: invalid period {period}"
                )
                continue

            # An odd period cannot be used by this factor-extraction step.
            if period % 2 != 0:
                errors.append(
                    f"a={candidate_a}: odd period {period}"
                )
                continue

            factors = factor_from_period(
                candidate_a,
                N,
                period,
            )

            factor1, factor2 = factors

            # Accept only non-trivial factors whose product is N.
            if (
                1 < factor1 < N
                and 1 < factor2 < N
                and factor1 * factor2 == N
            ):
                return factor1, factor2

            errors.append(
                f"a={candidate_a}: invalid or trivial factors"
            )

        except ValueError as error:
            # A failed base does not prevent trying another one.
            errors.append(f"a={candidate_a}: {error}")

    raise ValueError(
        f"Could not factor N={N} after trying "
        f"{len(candidate_bases)} coprime bases. "
        + " | ".join(errors[:5])
    )


def main() -> None:
    """Run a demonstration for N=21 and a=2."""

    N = 21
    a = 2

    period, circuit, probabilities = quantum_period_finding(a, N)

    print("General Quantum Shor")
    print("====================")
    print(f"N = {N}")
    print(f"a = {a}")
    print(f"Input qubits = {get_input_qubits(N)}")
    print(f"Work qubits = {get_work_qubits(N)}")
    print(f"Circuit qubits = {circuit.num_qubits}")
    print(f"Estimated period = {period}")
    print(f"Total probability = {np.sum(probabilities):.6f}")

    factors = quantum_shor_factorization(a, N)

    print(f"Factorization: {N} = {factors[0]} × {factors[1]}")


if __name__ == "__main__":
    main()