import pytest

from experiments.shor_general import (
    find_classical_period,
    factor_with_shor,
)


def test_period_21():
    assert find_classical_period(2, 21) == 6


def test_factor_21():
    factors = factor_with_shor(2, 21)

    assert set(factors) == {3, 7}


def test_period_15():
    assert find_classical_period(2, 15) == 4


def test_factor_15():
    factors = factor_with_shor(2, 15)

    assert set(factors) == {3, 5}


def test_invalid_non_coprime_base():
    with pytest.raises(ValueError):
        find_classical_period(3, 21)


def test_invalid_even_n():
    with pytest.raises(ValueError):
        find_classical_period(2, 20)