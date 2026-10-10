"""Simple bit-flip noise simulation for computational-basis bits."""
from __future__ import annotations
import random
from dataclasses import dataclass
@dataclass(frozen=True)
class NoiseResult:
    """Record the result of applying bit-flip noise."""
    original_bit: int
    noisy_bit: int
    flipped: bool
def _validate_bit(bit: int) -> None:
    """Ensure the input is an integer bit."""
    if isinstance(bit, bool) or not isinstance(bit, int):
        raise TypeError("bit must be an integer (0 or 1)")
    if bit not in (0, 1):
        raise ValueError("bit must be 0 or 1")
def _validate_probability(probability: float) -> None:
    """Ensure the probability is between zero and one."""
    if isinstance(probability, bool) or not isinstance(
        probability, (int, float)
    ):
        raise TypeError("probability must be a number")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
def apply_bit_flip_noise(
    bit: int,
    probability: float,
    *,
    rng: random.Random | None = None,
) -> NoiseResult:
    """Apply bit-flip noise to one bit.
    Args:
        bit: Input bit, either 0 or 1.
        probability: Probability of flipping the bit, from 0 to 1.
        rng: Optional random number generator for reproducible experiments.
    Returns:
        A NoiseResult containing the original bit, noisy bit, and outcome.
    """
    _validate_bit(bit)
    _validate_probability(probability)
    generator = rng if rng is not None else random.Random()
    flipped = generator.random() < probability
    noisy_bit = bit ^ int(flipped)
    return NoiseResult(
        original_bit=bit,
        noisy_bit=noisy_bit,
        flipped=flipped,
    )
def simulate_noise(
    bit: int,
    probability: float,
    trials: int = 1000,
    *,
    seed: int | None = None,
) -> dict[str, int | float]:
    """Estimate the bit-flip rate by running repeated trials."""
    _validate_bit(bit)
    _validate_probability(probability)
    if isinstance(trials, bool) or not isinstance(trials, int):
        raise TypeError("trials must be an integer")
    if trials <= 0:
        raise ValueError("trials must be greater than 0")
    if seed is not None and (
        isinstance(seed, bool) or not isinstance(seed, int)
    ):
        raise TypeError("seed must be an integer or None")
    rng = random.Random(seed)
    flips = sum(
        apply_bit_flip_noise(bit, probability, rng=rng).flipped
        for _ in range(trials)
    )
    return {
        "trials": trials,
        "flips": flips,
        "observed_rate": flips / trials,
        "expected_rate": float(probability),
    }
def main() -> None:
    """Print a small comparison of several noise probabilities."""
    print("Quantum Bit-Flip Noise Simulation")
    print("-" * 38)
    for probability in (0.01, 0.05, 0.10, 0.20, 0.30):
        result = simulate_noise(
            bit=0,
            probability=probability,
            trials=10_000,
            seed=42,
        )
        print(
            f"expected={result['expected_rate']:.0%}, "
            f"observed={result['observed_rate']:.2%}, "
            f"flips={result['flips']}/{result['trials']}"
        )
if __name__ == "__main__":
    main()