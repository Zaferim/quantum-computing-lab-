"""
Quantum Teleportation simulation using a three-qubit state vector.

Qubit order:
    q0: Alice's input qubit
    q1: Alice's entangled qubit
    q2: Bob's entangled qubit
"""

from math import cos, sin, pi, sqrt


def prepare_input_state(theta=pi / 3, phi=pi / 5):
    """Prepare |psi> = alpha|0> + beta|1>."""
    alpha = complex(cos(theta / 2))
    beta = complex(cos(phi), sin(phi)) * sin(theta / 2)
    return [alpha, beta]


def apply_single_qubit_gate(state, gate, target, num_qubits=3):
    """Apply a 2x2 gate to one qubit."""
    if len(state) != 2**num_qubits:
        raise ValueError("State-vector size does not match qubit count.")
    if target < 0 or target >= num_qubits:
        raise ValueError("Target qubit is out of range.")

    result = [0j] * len(state)
    mask = 1 << (num_qubits - 1 - target)

    for index, amplitude in enumerate(state):
        input_bit = 1 if index & mask else 0

        for output_bit in (0, 1):
            output_index = index
            if output_bit != input_bit:
                output_index ^= mask
            result[output_index] += gate[output_bit][input_bit] * amplitude

    return result


def apply_cnot(state, control, target, num_qubits=3):
    """Apply a controlled-NOT gate."""
    if len(state) != 2**num_qubits:
        raise ValueError("State-vector size does not match qubit count.")
    if not (0 <= control < num_qubits):
        raise ValueError("Control qubit is out of range.")
    if not (0 <= target < num_qubits):
        raise ValueError("Target qubit is out of range.")
    if control == target:
        raise ValueError("Control and target must be different.")

    result = [0j] * len(state)
    control_mask = 1 << (num_qubits - 1 - control)
    target_mask = 1 << (num_qubits - 1 - target)

    for index, amplitude in enumerate(state):
        output_index = index
        if index & control_mask:
            output_index ^= target_mask
        result[output_index] += amplitude

    return result


def simulate_teleportation(theta=pi / 3, phi=pi / 5):
    """Simulate all measurement branches of quantum teleportation."""
    alpha, beta = prepare_input_state(theta, phi)

    # Initial state |psi>_0 |0>_1 |0>_2.
    state = [0j] * 8
    state[0] = alpha
    state[4] = beta

    h = [
        [1 / sqrt(2), 1 / sqrt(2)],
        [1 / sqrt(2), -1 / sqrt(2)],
    ]

    # Create a Bell pair between Alice's q1 and Bob's q2.
    state = apply_single_qubit_gate(state, h, target=1)
    state = apply_cnot(state, control=1, target=2)

    # Alice performs the Bell-basis operations.
    state = apply_cnot(state, control=0, target=1)
    state = apply_single_qubit_gate(state, h, target=0)

    branches = {}

    # Measure Alice's q0 and q1; calculate each conditional Bob state.
    for measurement in range(4):
        m0 = (measurement >> 1) & 1
        m1 = measurement & 1
        label = f"{m0}{m1}"

        bob_unnormalized = [0j, 0j]

        for index, amplitude in enumerate(state):
            bits = format(index, "03b")
            if int(bits[0]) == m0 and int(bits[1]) == m1:
                bob_unnormalized[int(bits[2])] = amplitude

        probability = sum(abs(value) ** 2 for value in bob_unnormalized)

        if probability > 1e-15:
            bob = [
                value / sqrt(probability)
                for value in bob_unnormalized
            ]

            # Corrections: X if m1=1, then Z if m0=1.
            if m1:
                bob = [bob[1], bob[0]]
            if m0:
                bob = [bob[0], -bob[1]]

            overlap = alpha.conjugate() * bob[0] + beta.conjugate() * bob[1]
            fidelity = abs(overlap) ** 2
        else:
            bob = [0j, 0j]
            fidelity = 0.0

        branches[label] = {
            "probability": round(probability, 12),
            "corrected_state": bob,
            "fidelity": round(fidelity, 12),
        }

    probability_sum = sum(
        branch["probability"] for branch in branches.values()
    )

    return {
        "input_state": [alpha, beta],
        "measurement_branches": branches,
        "probability_sum": round(probability_sum, 12),
        "all_branches_fidelity_one": all(
            abs(branch["fidelity"] - 1.0) < 1e-10
            for branch in branches.values()
            if branch["probability"] > 1e-15
        ),
    }


if __name__ == "__main__":
    result = simulate_teleportation()

    print("Quantum Teleportation Simulation")
    print("--------------------------------")
    print("Measurement probability sum:", result["probability_sum"])
    print("All branches recover the input state:",
          result["all_branches_fidelity_one"])

    for measurement, branch in result["measurement_branches"].items():
        print(
            f"Measurement {measurement}: "
            f"probability={branch['probability']}, "
            f"fidelity={branch['fidelity']}"
        )