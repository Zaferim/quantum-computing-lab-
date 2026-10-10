import pytest

from quantum.noise_experiment import run_experiment


def test_experiment_returns_expected_result_type():
    result = run_experiment(probability=0.1, trials=100, seed=42)

    assert result.probability == 0.1
    assert result.trials == 100


def test_success_rates_are_between_zero_and_one():
    result = run_experiment(probability=0.1, trials=1000, seed=42)

    assert 0.0 <= result.single_bit_success_rate <= 1.0
    assert 0.0 <= result.corrected_success_rate <= 1.0


def test_experiment_is_reproducible():
    first = run_experiment(probability=0.1, trials=1000, seed=42)
    second = run_experiment(probability=0.1, trials=1000, seed=42)

    assert first == second


@pytest.mark.parametrize("probability", [0.0, 0.01, 0.05, 0.1, 0.2, 0.3])
def test_error_correction_improves_success_for_low_noise(probability):
    result = run_experiment(probability=probability, trials=10000, seed=42)

    assert (
        result.corrected_success_rate
        >= result.single_bit_success_rate
    )


def test_zero_noise_has_perfect_success():
    result = run_experiment(probability=0.0, trials=100, seed=42)

    assert result.single_bit_success_rate == 1.0
    assert result.corrected_success_rate == 1.0


@pytest.mark.parametrize("probability", [-0.1, 1.1])
def test_invalid_probability_is_rejected(probability):
    with pytest.raises(ValueError):
        run_experiment(probability=probability)


@pytest.mark.parametrize("probability", ["0.1", None, True])
def test_invalid_probability_type_is_rejected(probability):
    with pytest.raises(TypeError):
        run_experiment(probability=probability)


@pytest.mark.parametrize("trials", [0, -1])
def test_non_positive_trials_are_rejected(trials):
    with pytest.raises(ValueError):
        run_experiment(probability=0.1, trials=trials)


@pytest.mark.parametrize("trials", [1.5, "100", True])
def test_invalid_trials_type_is_rejected(trials):
    with pytest.raises(TypeError):
        run_experiment(probability=0.1, trials=trials)


@pytest.mark.parametrize("seed", ["42", 1.5, True])
def test_invalid_seed_is_rejected(seed):
    with pytest.raises(TypeError):
        run_experiment(probability=0.1, seed=seed)