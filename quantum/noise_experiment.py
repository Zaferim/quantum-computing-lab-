"""Compare single-bit transmission with three-bit error correction."""

import random
from dataclasses import dataclass

from quantum.error_correction import encode_bit, correct_bit_flip
from quantum.noise import apply_bit_flip_noise


@dataclass(frozen=True)
class ExperimentResult:
    """Results of a noise and error-correction experiment."""

    probability: float
    trials: int
    single_bit_success_rate: float
    corrected_success_rate: float


def run_experiment(
    probability: float,
    trials: int = 10_000,
    seed: int = 42,
) -> ExperimentResult:
    """Compare single-bit transmission with three-bit error correction."""

    if isinstance(probability, bool) or not isinstance(
        probability, (int, float)
    ):
        raise TypeError("probability must be a number")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if isinstance(trials, bool) or not isinstance(trials, int):
        raise TypeError("trials must be an integer")
    if trials <= 0:
        raise ValueError("trials must be greater than 0")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")

    rng = random.Random(seed)
    single_successes = 0
    corrected_successes = 0

    for _ in range(trials):
        original_bit = rng.randint(0, 1)

        # Method A: send one bit through a noisy channel.
        noisy_single = apply_bit_flip_noise(
            original_bit, probability, rng=rng
        )
        if noisy_single.noisy_bit == original_bit:
            single_successes += 1

        # Method B: encode the bit into three physical bits.
        encoded = encode_bit(original_bit)
        received = tuple(
            apply_bit_flip_noise(bit, probability, rng=rng).noisy_bit
            for bit in encoded
        )

        corrected, _ = correct_bit_flip(received)
        decoded_bit = 1 if sum(corrected) >= 2 else 0

        if decoded_bit == original_bit:
            corrected_successes += 1

    return ExperimentResult(
        probability=float(probability),
        trials=trials,
        single_bit_success_rate=single_successes / trials,
        corrected_success_rate=corrected_successes / trials,
    )


def main() -> None:
    """Run experiments at several noise levels."""

    print("Quantum Noise: Error Correction Comparison")
    print("=" * 66)
    print(
        f"{'Noise':>8} | {'Single-bit success':>20} | "
        f"{'Corrected success':>19}"
    )
    print("-" * 66)

    for probability in (0.01, 0.05, 0.10, 0.20, 0.30):
        result = run_experiment(
            probability=probability,
            trials=10_000,
            seed=42,
        )
        print(
            f"{probability:>7.0%} | "
            f"{result.single_bit_success_rate:>19.2%} | "
            f"{result.corrected_success_rate:>18.2%}"
        )


if __name__ == "__main__":
    main()