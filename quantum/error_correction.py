"""Three-qubit bit-flip error correction simulation.
This module models computational-basis repetition codes using three
classical bits. It demonstrates single-bit error correction, but does not
simulate arbitrary quantum superpositions or phase-flip errors.
"""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class CorrectionResult:
    """Result of encoding, introducing, and correcting a bit-flip error."""
    original_bit: int
    encoded_bits: tuple[int, int, int]
    received_bits: tuple[int, int, int]
    corrected_bits: tuple[int, int, int]
    syndrome: tuple[int, int]
    error_position: int | None
    corrected_bit: int
    success: bool
def _validate_bit(bit: int, name: str = "bit") -> None:
    """Validate that a value is an integer bit (0 or 1)."""
    if isinstance(bit, bool) or not isinstance(bit, int):
        raise TypeError(f"{name} must be an integer (0 or 1)")
    if bit not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")
def encode_bit(bit: int) -> tuple[int, int, int]:
    """Encode one computational-basis bit using a three-bit repetition code."""
    _validate_bit(bit)
    return (bit, bit, bit)
def apply_bit_flip(
    bits: tuple[int, int, int],
    error_position: int | None,
) -> tuple[int, int, int]:
    """Flip one selected bit, or leave the encoded bits unchanged.
    Args:
        bits: A tuple containing exactly three bits.
        error_position: Index 0, 1, or 2; None means no error.
    Returns:
        A new tuple containing the possibly corrupted bits.
    """
    if not isinstance(bits, tuple):
        raise TypeError("bits must be a tuple")
    if len(bits) != 3:
        raise ValueError("bits must contain exactly three bits")
    for bit in bits:
        _validate_bit(bit)
    if error_position is not None:
        if isinstance(error_position, bool) or not isinstance(error_position, int):
            raise TypeError("error_position must be an integer or None")
        if error_position not in (0, 1, 2):
            raise ValueError("error_position must be 0, 1, 2, or None")
    received = list(bits)
    if error_position is not None:
        received[error_position] ^= 1
    return tuple(received)
def measure_syndrome(
    bits: tuple[int, int, int],
) -> tuple[int, int]:
    """Calculate parity-check syndrome (b0 XOR b1, b1 XOR b2)."""
    if not isinstance(bits, tuple):
        raise TypeError("bits must be a tuple")
    if len(bits) != 3:
        raise ValueError("bits must contain exactly three bits")
    for bit in bits:
        _validate_bit(bit)
    return (bits[0] ^ bits[1], bits[1] ^ bits[2])
def correct_bit_flip(
    bits: tuple[int, int, int],
) -> tuple[tuple[int, int, int], int | None]:
    """Correct a single-bit error using majority voting.
    Returns:
        A tuple containing the corrected bits and the inferred error index.
    Note:
        The repetition code can correct any single bit-flip error. It cannot
        guarantee correction when multiple bits are corrupted.
    """
    syndrome = measure_syndrome(bits)
    error_positions = {
        (0, 1): 2,
        (1, 0): 0,
        (1, 1): 1,
        (0, 0): None,
    }
    error_position = error_positions[syndrome]
    corrected = list(bits)
    if error_position is not None:
        corrected[error_position] ^= 1
    return tuple(corrected), error_position
def run_error_correction(
    bit: int,
    error_position: int | None = None,
) -> CorrectionResult:
    """Run the complete three-bit bit-flip correction demonstration."""
    _validate_bit(bit)
    encoded = encode_bit(bit)
    received = apply_bit_flip(encoded, error_position)
    syndrome = measure_syndrome(received)
    corrected, detected_position = correct_bit_flip(received)
    corrected_bit = 1 if sum(corrected) >= 2 else 0
    return CorrectionResult(
        original_bit=bit,
        encoded_bits=encoded,
        received_bits=received,
        corrected_bits=corrected,
        syndrome=syndrome,
        error_position=detected_position,
        corrected_bit=corrected_bit,
        success=corrected_bit == bit,
    )
def main() -> None:
    """Demonstrate correction for each possible single-bit error."""
    print("Three-Qubit Bit-Flip Error Correction")
    print("-" * 44)
    for original_bit in (0, 1):
        for error_position in (None, 0, 1, 2):
            result = run_error_correction(original_bit, error_position)
            error_label = (
                "none" if error_position is None else str(error_position)
            )
            print(
                f"input={result.original_bit}, "
                f"error_position={error_label}, "
                f"received={result.received_bits}, "
                f"syndrome={result.syndrome}, "
                f"corrected={result.corrected_bits}, "
                f"success={result.success}"
            )
if __name__ == "__main__":
    main()