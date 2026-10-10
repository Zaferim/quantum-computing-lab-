import pytest
from quantum.error_correction import (
    apply_bit_flip,
    correct_bit_flip,
    encode_bit,
    measure_syndrome,
    run_error_correction,
)
@pytest.mark.parametrize(
    ("bit", "expected"),
    [
        (0, (0, 0, 0)),
        (1, (1, 1, 1)),
    ],
)
def test_encode_bit(bit, expected):
    assert encode_bit(bit) == expected
@pytest.mark.parametrize("bit", [0, 1])
@pytest.mark.parametrize("error_position", [None, 0, 1, 2])
def test_run_error_correction_succeeds(bit, error_position):
    result = run_error_correction(bit, error_position)
    assert result.original_bit == bit
    assert result.success is True
    assert result.corrected_bit == bit
    assert result.corrected_bits == (bit, bit, bit)
@pytest.mark.parametrize(
    ("position", "expected_received", "expected_syndrome"),
    [
        (0, (1, 0, 0), (1, 0)),
        (1, (0, 1, 0), (1, 1)),
        (2, (0, 0, 1), (0, 1)),
    ],
)
def test_single_bit_flip_and_syndrome(position, expected_received, expected_syndrome):
    received = apply_bit_flip((0, 0, 0), position)
    assert received == expected_received
    assert measure_syndrome(received) == expected_syndrome
@pytest.mark.parametrize(
    ("bits", "expected_corrected", "expected_position"),
    [
        ((1, 0, 0), (0, 0, 0), 0),
        ((0, 1, 0), (0, 0, 0), 1),
        ((0, 0, 1), (0, 0, 0), 2),
        ((1, 1, 1), (1, 1, 1), None),
    ],
)
def test_correct_bit_flip(bits, expected_corrected, expected_position):
    corrected, error_position = correct_bit_flip(bits)
    assert corrected == expected_corrected
    assert error_position == expected_position
@pytest.mark.parametrize("bit", [-1, 2, 1.0, "0", True])
def test_encode_bit_rejects_invalid_input(bit):
    with pytest.raises((TypeError, ValueError)):
        encode_bit(bit)
@pytest.mark.parametrize(
    "bits",
    [
        (0, 1),
        (0, 1, 0, 1),
        [0, 0, 0],
        (0, 2, 0),
        (0, 1, True),
    ],
)
def test_apply_bit_flip_rejects_invalid_bits(bits):
    with pytest.raises((TypeError, ValueError)):
        apply_bit_flip(bits, None)
@pytest.mark.parametrize("position", [-1, 3, 1.5, "0", True])
def test_apply_bit_flip_rejects_invalid_position(position):
    with pytest.raises((TypeError, ValueError)):
        apply_bit_flip((0, 0, 0), position)