import pytest

from quantum.superdense_coding import (
    apply_cnot,
    apply_single_qubit_gate,
    decode_bell_state,
    encode_message,
    simulate_superdense_coding,
)


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_all_messages_are_decoded_correctly(message):
    result = simulate_superdense_coding(message)

    assert result["sent_message"] == message
    assert result["decoded_message"] == message
    assert result["success"] is True


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_probability_sum_is_one(message):
    result = simulate_superdense_coding(message)

    assert result["probability_sum"] == pytest.approx(1.0)


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_correct_message_has_probability_one(message):
    result = simulate_superdense_coding(message)

    assert result["probabilities"][message] == pytest.approx(1.0)

    for other_message, probability in result["probabilities"].items():
        if other_message != message:
            assert probability == pytest.approx(0.0)


@pytest.mark.parametrize("message", ["", "0", "000", "2a", "12"])
def test_invalid_messages_are_rejected(message):
    with pytest.raises(ValueError):
        simulate_superdense_coding(message)


def test_cnot_preserves_state_norm():
    state = [1 / 2**0.5, 0j, 0j, 1 / 2**0.5]

    result = apply_cnot(state)

    norm = sum(abs(amplitude) ** 2 for amplitude in result)

    assert norm == pytest.approx(1.0)


def test_hadamard_preserves_state_norm():
    state = [1 + 0j, 0j, 0j, 0j]

    hadamard = [
        [1 / 2**0.5, 1 / 2**0.5],
        [1 / 2**0.5, -1 / 2**0.5],
    ]

    result = apply_single_qubit_gate(state, hadamard, target=0)

    norm = sum(abs(amplitude) ** 2 for amplitude in result)

    assert norm == pytest.approx(1.0)


def test_bell_state_decodes_to_zero_zero():
    bell_state = [1 / 2**0.5, 0j, 0j, 1 / 2**0.5]

    result = decode_bell_state(bell_state)

    assert result["decoded_message"] == "00"
    assert result["probability_sum"] == pytest.approx(1.0)