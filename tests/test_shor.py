from experiments.shor_period import find_period, factor_from_period


def test_find_period():
    assert find_period(2, 15) == 4


def test_factor_from_period():
    factors = factor_from_period(2, 15, 4)
    assert set(factors) == {3, 5}
