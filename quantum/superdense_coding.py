"""
Superdense Coding simulation.

Demonstrates how Alice can communicate two classical bits to Bob
by sending one qubit, using a shared Bell pair.
"""

from math import sqrt


def apply_single_qubit_gate(state, gate, target, num_qubits=2):
    """Apply a 2x2 gate to a qubit in a state vector."""
    if len(state) != 2**num_qubits:
        raise ValueError("State-vector size does not match qubit count.")
    if not 0 <= target < num_qubits:
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


def apply_cnot(state, control=0, target=1):
    """Apply CNOT to a two-qubit state."""
    if len(state) != 4:
        raise ValueError("A two-qubit state must have four amplitudes.")
    if control not in (0, 1) or target not in (0, 1):
        raise ValueError("Qubit indices must be 0 or 1.")
    if control == target:
        raise ValueError("Control and target must be different.")

    result = [0j] * 4
    control_mask = 1 << (1 - control)
    target_mask = 1 << (1 - target)

    for index, amplitude in enumerate(state):
        output_index = index
        if index & control_mask:
            output_index ^= target_mask
        result[output_index] += amplitude

    return result


def encode_message(state, message):
    """Encode a two-bit classical message on Alice's qubit."""
    if message not in ("00", "01", "10", "11"):
        raise ValueError("Message must be a two-bit string.")

    # Encoding table:
    # 00 -> I, 01 -> X, 10 -> Z, 11 -> XZ.
    alpha = 1 / sqrt(2)

    if message == "00":
        return state[:]

    if message == "01":
        x_gate = [[0, 1], [1, 0]]
        return apply_single_qubit_gate(state, x_gate, target=0)

    if message == "10":
        z_gate = [[1, 0], [0, -1]]
        return apply_single_qubit_gate(state, z_gate, target=0)

    # Apply Z first, then X, which implements XZ on the state.
    z_gate = [[1, 0], [0, -1]]
    x_gate = [[0, 1], [1, 0]]

    return apply_single_qubit_gate(
        apply_single_qubit_gate(state, z_gate, target=0),
        x_gate,
        target=0,
    )


def decode_bell_state(state):
    """Decode a Bell state using CNOT followed by Hadamard."""
    state = apply_cnot(state, control=0, target=1)

    hadamard = [
        [1 / sqrt(2), 1 / sqrt(2)],
        [1 / sqrt(2), -1 / sqrt(2)],
    ]

    state = apply_single_qubit_gate(state, hadamard, target=0)

    probabilities = {
        format(index, "02b"): round(abs(amplitude) ** 2, 12)
        for index, amplitude in enumerate(state)
    }

    return {
        "probabilities": probabilities,
        "decoded_message": max(probabilities, key=probabilities.get),
        "probability_sum": round(sum(probabilities.values()), 12),
    }


def simulate_superdense_coding(message):
    """Run the full superdense coding protocol for a two-bit message."""
    if message not in ("00", "01", "10", "11"):
        raise ValueError("Message must be a two-bit string.")

    # Start with |00>, apply H to Alice's qubit, then CNOT.
    state = [1 + 0j, 0j, 0j, 0j]

    hadamard = [
        [1 / sqrt(2), 1 / sqrt(2)],
        [1 / sqrt(2), -1 / sqrt(2)],
    ]

    state = apply_single_qubit_gate(state, hadamard, target=0)
    state = apply_cnot(state, control=0, target=1)

    encoded_state = encode_message(state, message)
    result = decode_bell_state(encoded_state)

    return {
        "sent_message": message,
        "decoded_message": result["decoded_message"],
        "probabilities": result["probabilities"],
        "probability_sum": result["probability_sum"],
        "success": result["decoded_message"] == message,
    }


if __name__ == "__main__":
    print("Superdense Coding Simulation")
    print("----------------------------")

    for message in ("00", "01", "10", "11"):
        result = simulate_superdense_coding(message)
        print(
            f"Sent: {message} | "
            f"Decoded: {result['decoded_message']} | "
            f"Success: {result['success']} | "
            f"Probability sum: {result['probability_sum']}"
        )