"""
Shor's Algorithm - Quantum Modular Exponentiation
General-purpose modular exponentiation structure.
Default demonstration:
N = 15
a = 2
"""
from functools import lru_cache
from math import gcd
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
DEFAULT_N = 15
DEFAULT_A = 2
DEFAULT_PERIOD = 4
def validate_inputs(a: int, N: int) -> None:
    """Validate the base and modulus."""
    if isinstance(N, bool) or not isinstance(N, int) or N <= 1:
        raise ValueError("N must be an integer greater than 1.")
    if N % 2 == 0:
        raise ValueError("N must be odd.")
    if isinstance(a, bool) or not isinstance(a, int):
        raise ValueError("a must be an integer.")
    if not 1 < a < N:
        raise ValueError("a must satisfy 1 < a < N.")
    if gcd(a, N) != 1:
        raise ValueError("a and N must be coprime.")
def get_work_qubits(N: int) -> int:
    """Return the number of qubits needed for the work register."""
    if isinstance(N, bool) or not isinstance(N, int) or N <= 1:
        raise ValueError("N must be an integer greater than 1.")
    return (N - 1).bit_length()
def get_input_qubits(N: int) -> int:
    """Return twice the number of work qubits."""
    return 2 * get_work_qubits(N)
def modular_power(a: int, x: int, N: int) -> int:
    """Calculate a^x mod N."""
    if isinstance(x, bool) or not isinstance(x, int) or x < 0:
        raise ValueError("x must be a non-negative integer.")
    if N <= 1:
        raise ValueError("N must be greater than 1.")
    return pow(a, x, N)
@lru_cache(maxsize=256)
def _cached_modular_multiplication_matrix(
    multiplier: int,
    N: int,
) -> np.ndarray:
    """Create and cache a read-only modular multiplication matrix."""
    dimension = 1 << get_work_qubits(N)
    matrix = np.zeros(
        (dimension, dimension),
        dtype=np.complex128,
    )
    for y in range(dimension):
        target = (multiplier * y) % N if y < N else y
        matrix[target, y] = 1.0
    matrix.setflags(write=False)
    return matrix
def modular_multiplication_matrix(
    multiplier: int,
    N: int,
) -> np.ndarray:
    """
    Create the modular multiplication matrix.
    Valid states y < N map to (multiplier * y) mod N.
    States y >= N remain unchanged.
    """
    if isinstance(multiplier, bool) or not isinstance(multiplier, int):
        raise ValueError("multiplier must be an integer.")
    if isinstance(N, bool) or not isinstance(N, int) or N <= 1:
        raise ValueError("N must be an integer greater than 1.")
    multiplier %= N
    if gcd(multiplier, N) != 1:
        raise ValueError("multiplier and N must be coprime.")
    return _cached_modular_multiplication_matrix(multiplier, N)
@lru_cache(maxsize=256)
def _cached_controlled_instruction(multiplier: int, N: int):
    """Build and cache a controlled modular multiplication instruction."""
    matrix = modular_multiplication_matrix(multiplier, N)
    return Operator(matrix).to_instruction().control(1)
def build_controlled_modular_exponentiation(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> QuantumCircuit:
    """
    Build controlled modular exponentiation.
    The circuit applies controlled modular multiplication to the work
    register, implementing the modular-power mapping on the initialized
    work state |1>.
    """
    validate_inputs(a, N)
    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)
    circuit = QuantumCircuit(input_qubits + work_qubits)
    # Prepare |1> in the work register.
    circuit.x(input_qubits)
    work_register = list(
        range(input_qubits, input_qubits + work_qubits)
    )
    for i in range(input_qubits):
        multiplier = pow(a, 1 << i, N)
        controlled = _cached_controlled_instruction(
            multiplier,
            N,
        )
        circuit.append(controlled, [i, *work_register])
    return circuit
def verify_classical_period(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
    period: int = DEFAULT_PERIOD,
) -> None:
    """Verify the supplied period against modular exponentiation."""
    validate_inputs(a, N)
    if isinstance(period, bool) or not isinstance(period, int) or period <= 0:
        raise ValueError("period must be a positive integer.")
    if pow(a, period, N) != 1:
        raise ValueError("The supplied period is not valid.")
    for x in range(get_input_qubits(N)):
        assert modular_power(a, x, N) == modular_power(a, x + period, N)
    print("Classical period verification passed.")
def get_controlled_multipliers(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> list[int]:
    """Return the controlled modular multipliers."""
    validate_inputs(a, N)
    return [
        pow(a, 1 << i, N)
        for i in range(get_input_qubits(N))
    ]
def verify_multipliers(
    a: int = DEFAULT_A,
    N: int = DEFAULT_N,
) -> None:
    """Verify that all controlled multipliers are coprime to N."""
    actual = get_controlled_multipliers(a, N)
    assert all(gcd(multiplier, N) == 1 for multiplier in actual)
    print("Controlled multipliers verified.")
    print(f"Multipliers: {actual}")
def verify_unitary(
    multiplier: int,
    N: int = DEFAULT_N,
) -> None:
    """Verify that modular multiplication is unitary."""
    matrix = modular_multiplication_matrix(multiplier, N)
    dimension = 1 << get_work_qubits(N)
    identity = np.eye(dimension, dtype=np.complex128)
    assert np.allclose(matrix.conj().T @ matrix, identity)
    print(f"Modular multiplication by {multiplier} is unitary.")
def main() -> None:
    """Run the default N=15, a=2 demonstration."""
    N = DEFAULT_N
    a = DEFAULT_A
    period = DEFAULT_PERIOD
    input_qubits = get_input_qubits(N)
    work_qubits = get_work_qubits(N)
    print("Shor's Algorithm - Controlled Modular Exponentiation")
    print("-" * 52)
    print(f"N = {N}")
    print(f"a = {a}")
    print(f"Input qubits = {input_qubits}")
    print(f"Work qubits = {work_qubits}")
    print()
    verify_classical_period(a, N, period)
    print()
    verify_multipliers(a, N)
    print()
    for multiplier in sorted(set(get_controlled_multipliers(a, N))):
        verify_unitary(multiplier, N)
    print()
    circuit = build_controlled_modular_exponentiation(a, N)
    print("Controlled modular exponentiation circuit:")
    print(circuit.draw())
    print()
    print("Controlled modular exponentiation circuit created.")
if __name__ == "__main__":
    main()
