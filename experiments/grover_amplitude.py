"""
Quantum Computing Lab
Grover amplitude amplification experiment.
"""


from math import sqrt


def initial_amplitudes():
    """Return equal amplitudes for four states."""

    value = 1 / sqrt(4)

    return [
        value,
        value,
        value,
        value
    ]


def apply_oracle(amplitudes):
    """Mark the target state |11> by flipping its phase."""

    result = amplitudes.copy()

    result[3] = -result[3]

    return result


def apply_diffuser(amplitudes):
    """Apply the Grover diffusion operation."""

    average = sum(amplitudes) / len(amplitudes)

    return [
        2 * average - amplitude
        for amplitude in amplitudes
    ]


def probabilities(amplitudes):
    """Calculate measurement probabilities."""

    return [
        amplitude ** 2
        for amplitude in amplitudes
    ]


def run_experiment():
    """Show amplitude amplification step by step."""

    amplitudes = initial_amplitudes()

    print("Grover Amplitude Amplification")
    print("==============================")

    print()
    print("States:")
    print("|00> |01> |10> |11>")

    print()
    print("Initial amplitudes:")
    print(amplitudes)

    print()
    print("Initial probabilities:")
    print(probabilities(amplitudes))

    amplitudes = apply_oracle(amplitudes)

    print()
    print("After oracle:")
    print(amplitudes)

    print()
    print("After oracle probabilities:")
    print(probabilities(amplitudes))

    amplitudes = apply_diffuser(amplitudes)

    print()
    print("After diffuser:")
    print(amplitudes)

    print()
    print("Final probabilities:")
    print(probabilities(amplitudes))


if __name__ == "__main__":

    run_experiment()