"""
Variational Quantum Eigensolver (VQE).

A simple state-vector implementation that estimates the ground-state
energy of a single-qubit Hamiltonian H = aI + bX + cZ.
"""

from math import cos, sin, pi, isfinite


def single_qubit_state(theta):
    """Return cos(theta/2)|0> + sin(theta/2)|1>."""
    if not isfinite(theta):
        raise ValueError("theta must be finite.")

    return [cos(theta / 2), sin(theta / 2)]


def expectation_value(theta, a=0.0, b=1.0, c=0.5):
    """Calculate the expectation value <psi|H|psi>."""
    if not all(isfinite(value) for value in (theta, a, b, c)):
        raise ValueError("Arguments must be finite numbers.")

    alpha, beta = single_qubit_state(theta)

    h_alpha = (a + c) * alpha + b * beta
    h_beta = b * alpha + (a - c) * beta

    return alpha * h_alpha + beta * h_beta


def find_ground_state(steps=1000, a=0.0, b=1.0, c=0.5):
    """Search theta in [0, 2*pi] for the lowest energy."""
    if not isinstance(steps, int) or isinstance(steps, bool) or steps < 2:
        raise ValueError("steps must be an integer greater than or equal to 2.")

    best_theta = 0.0
    best_energy = float("inf")

    for index in range(steps + 1):
        theta = 2 * pi * index / steps
        energy = expectation_value(theta, a=a, b=b, c=c)

        if energy < best_energy:
            best_energy = energy
            best_theta = theta

    return {
        "theta": best_theta,
        "energy": best_energy,
        "steps": steps,
    }


if __name__ == "__main__":
    result = find_ground_state()

    print("VQE Simulation")
    print("--------------")
    print(f"Optimal theta: {result['theta']:.6f} radians")
    print(f"Estimated ground-state energy: {result['energy']:.6f}")
    print(f"Search steps: {result['steps']}")