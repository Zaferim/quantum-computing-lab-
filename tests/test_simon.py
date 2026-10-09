import pytest

from quantum.simon import (
    bitwise_inner_product,
    recover_hidden_string,
    run_simon_postprocessing,
    satisfies_simon_equations,
)


def test_bitwise_inner_product():
    assert bitwise_inner_product("101", "110") == 1
    assert bitwise_inner_product("101", "101") == 0


def test_recover_hidden_string():
    measurements = ["010", "001"]
    assert recover_hidden_string(measurements) == "100"


def test_recovered_string_satisfies_equations():
    measurements = ["010", "001"]
    hidden = recover_hidden_string(measurements)

    assert hidden is not None
    assert satisfies_simon_equations(hidden, measurements)


def test_insufficient_measurements_return_none():
    assert recover_hidden_string(["000"]) is None


def test_empty_measurements_return_none():
    assert recover_hidden_string([]) is None


def test_invalid_bits_raise_value_error():
    with pytest.raises(ValueError):
        bitwise_inner_product("102", "100")


def test_different_lengths_raise_value_error():
    with pytest.raises(ValueError):
        bitwise_inner_product("10", "100")


def test_postprocessing_summary():
    result = run_simon_postprocessing(["010", "001"])

    assert result["hidden_string"] == "100"
    assert result["recovered"] is True


def test_simon_oracle_pairs_inputs():
    from quantum.simon import simon_oracle_output

    secret = "101"
    for value in range(2 ** len(secret)):
        x = format(value, f"0{len(secret)}b")
        paired = "".join(
            str(int(left) ^ int(right))
            for left, right in zip(x, secret)
        )
        assert simon_oracle_output(x, secret) == simon_oracle_output(
            paired, secret
        )


def test_quantum_simulation_probabilities_sum_to_one():
    from quantum.simon import simulate_simon_circuit

    result = simulate_simon_circuit("101")
    assert result["probability_sum"] == 1.0


def test_quantum_simulation_only_returns_valid_measurements():
    from quantum.simon import (
        bitwise_inner_product,
        simulate_simon_circuit,
    )

    result = simulate_simon_circuit("101")

    for outcome, probability in result["probabilities"].items():
        if probability > 0:
            assert bitwise_inner_product(outcome, "101") == 0


def test_quantum_simulation_rejects_zero_secret():
    from quantum.simon import simulate_simon_circuit

    with pytest.raises(ValueError):
        simulate_simon_circuit("000")
