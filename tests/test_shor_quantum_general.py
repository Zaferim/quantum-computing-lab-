import pytest
from experiments.shor_quantum_general import (
    continued_fraction_period_candidates,
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

