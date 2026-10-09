import pytest
from experiments.shor_quantum_general import (
    continued_fraction_period_candidates,
    quantum_period_finding,
    quantum_shor_factorization,
    reduce_period,
    validate_inputs,
)
def test_quantum_shor_factorization_21():
    factors = quantum_shor_factorization(2, 21)
    assert factors[0] * factors[1] == 21
    assert set(factors) == {3, 7}
def test_quantum_shor_factorization_retries_base():
    factors = quantum_shor_factorization(5, 21)
    assert factors[0] * factors[1] == 21
    assert set(factors) == {3, 7}
def test_reduce_period():
    assert reduce_period(2, 21, 6) == 6
def test_invalid_base_raises_value_error():
    with pytest.raises(ValueError):
        validate_inputs(3, 21)
def test_continued_fraction_finds_period():
    candidates = continued_fraction_period_candidates(11, 64, 2, 21)
    assert 6 in candidates
def test_continued_fraction_rejects_out_of_range_measurement():
    with pytest.raises(ValueError):
        continued_fraction_period_candidates(64, 64, 2, 21)
def test_quantum_shor_factorization_15():
    factors = quantum_shor_factorization(2, 15)
    assert factors[0] * factors[1] == 15
    assert set(factors) == {3, 5}
def test_quantum_period_finding_15():
    period, circuit, probabilities = quantum_period_finding(2, 15)
    assert period == 4
    assert pow(2, period, 15) == 1
    assert circuit.num_qubits == 12
    assert probabilities.sum() == pytest.approx(1.0)


@pytest.mark.parametrize(
    "a, n, expected_factors",
    [
        (5, 33, {3, 11}),
        (2, 35, {5, 7}),
    ],
)
def test_shor_factorization_mathematical_examples(a, n, expected_factors):
    from math import gcd

    period = 1
    while pow(a, period, n) != 1:
        period += 1

    assert period % 2 == 0

    x = pow(a, period // 2, n)
    p = gcd(x - 1, n)
    q = gcd(x + 1, n)

    assert p * q == n
    assert {p, q} == expected_factors
from experiments.shor_quantum_period import (
    get_work_qubits,
    get_input_qubits,
    modular_multiplication_matrix,
    verify_classical_period,
    verify_unitary,
)


def test_shor_quantum_period_qubit_counts():
    assert get_work_qubits(15) == 4
    assert get_input_qubits(15) == 8


def test_modular_multiplication_matrix_is_unitary():
    matrix = modular_multiplication_matrix(2, 15)
    identity = matrix.conj().T @ matrix

    import numpy as np

    assert np.allclose(identity, np.eye(16))


def test_verify_classical_period_accepts_valid_period():
    verify_classical_period(2, 15, 4)


def test_modular_multiplication_rejects_non_coprime_multiplier():
    with pytest.raises(ValueError):
        modular_multiplication_matrix(3, 15)