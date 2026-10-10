import random
import pytest
from quantum.noise import apply_bit_flip_noise, simulate_noise
@pytest.mark.parametrize("bit", [0, 1])
def test_zero_probability_never_flips(bit):
    result = apply_bit_flip_noise(bit, 0.0, rng=random.Random(42))
    assert result.original_bit == bit
    assert result.noisy_bit == bit
    assert result.flipped is False
@pytest.mark.parametrize("bit", [0, 1])
def test_probability_one_always_flips(bit):
    result = apply_bit_flip_noise(bit, 1.0, rng=random.Random(42))
    assert result.original_bit == bit
    assert result.noisy_bit == 1 - bit
    assert result.flipped is True
def test_noise_is_reproducible_with_same_seed():
    first = simulate_noise(0, 0.15, trials=1000, seed=123)
    second = simulate_noise(0, 0.15, trials=1000, seed=123)
    assert first == second
@pytest.mark.parametrize("probability", [0.01, 0.05, 0.10, 0.20, 0.30])
def test_observed_rate_is_close_to_expected(probability):
    result = simulate_noise(
        bit=0,
        probability=probability,
        trials=10_000,
        seed=42,
    )
    assert result["trials"] == 10_000
    assert abs(result["observed_rate"] - probability) < 0.02
    assert result["expected_rate"] == probability
@pytest.mark.parametrize("bit", [-1, 2, 1.0, "0", True])
def test_invalid_bit_is_rejected(bit):
    with pytest.raises((TypeError, ValueError)):
        apply_bit_flip_noise(bit, 0.5)
@pytest.mark.parametrize("probability", [-0.1, 1.1])
def test_out_of_range_probability_is_rejected(probability):
    with pytest.raises(ValueError):
        apply_bit_flip_noise(0, probability)
@pytest.mark.parametrize("probability", ["0.5", None, True])
def test_invalid_probability_type_is_rejected(probability):
    with pytest.raises(TypeError):
        apply_bit_flip_noise(0, probability)
@pytest.mark.parametrize("trials", [0, -1])
def test_non_positive_trial_count_is_rejected(trials):
    with pytest.raises(ValueError):
        simulate_noise(0, 0.5, trials=trials)
@pytest.mark.parametrize("trials", [1.5, "100", True])
def test_invalid_trial_count_type_is_rejected(trials):
    with pytest.raises(TypeError):
        simulate_noise(0, 0.5, trials=trials)
@pytest.mark.parametrize("seed", ["42", 1.5, True])
def test_invalid_seed_is_rejected(seed):
    with pytest.raises(TypeError):
        simulate_noise(0, 0.5, seed=seed)