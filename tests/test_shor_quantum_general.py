import pytest
from experiments.shor_quantum_general import (
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