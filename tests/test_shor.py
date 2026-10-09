from experiments.shor_period import find_period, factor_from_period


def test_find_period():
    assert find_period(2, 15) == 4


def test_factor_from_period():
    factors = factor_from_period(2, 15, 4)
    assert set(factors) == {3, 5}


import pytest


@pytest.mark.parametrize(
    ("a", "N", "expected_period"),
    [
        (2, 15, 4),
        (2, 7, 3),
        (3, 7, 6),
        (2, 9, 6),
        (4, 15, 2),
    ],
)
def test_find_period_for_multiple_inputs(a, N, expected_period):
    assert find_period(a, N) == expected_period
    assert pow(a, expected_period, N) == 1


@pytest.mark.parametrize(
    ("a", "N"),
    [
        (2, 1),
        (2, 0),
        (2, -5),
        (3, 15),
        (5, 15),
    ],
)
def test_find_period_rejects_invalid_inputs(a, N):
    with pytest.raises(ValueError):
        find_period(a, N)


def test_factor_from_period_rejects_odd_period():
    with pytest.raises(ValueError, match="even"):
        factor_from_period(2, 15, 3)


def test_factor_from_period_rejects_trivial_factors():
    with pytest.raises(ValueError, match="non-trivial"):
        factor_from_period(2, 21, 2)
