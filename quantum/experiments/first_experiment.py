"""
Quantum Computing Lab
First experiment.

Compare classical calculation
with quantum superposition.
"""

from quantum.algorithms import run_first_algorithm


def run_experiment():

    result = run_first_algorithm()

    print("Quantum Experiment #1")
    print("=====================")

    print(
        "Quantum state:",
        result["state"]
    )

    print(
        "Probability of 0:",
        result["probability_0"]
    )

    print(
        "Probability of 1:",
        result["probability_1"]
    )


if __name__ == "__main__":
    run_experiment()