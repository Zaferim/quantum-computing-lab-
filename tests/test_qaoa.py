import math

import pytest

from quantum.qaoa import (
    apply_mixer,
    cut_value,
    expected_cut,
    optimize_qaoa,
    qaoa_state,
    validate_graph,
)


def test_cut_value_for_different_bits():
    assert cut_value("01", [(0, 1)]) == 1


def test_cut_value_for_same_bits():
    assert cut_value("00", [(0, 1)]) == 0


def test_cut_value_for_triangle():
    edges = [(0, 1), (1, 2), (0, 2)]
    assert cut_value("010", edges) == 2


def test_validate_graph_accepts_valid_edges():
    assert validate_graph(3, [(0, 1), (1, 2)]) == [(0, 1), (1, 2)]


@pytest.mark.parametrize(
    "num_qubits, edges",
    [
        (1, [(0, 1)]),
        (2, [(0, 2)]),
        (2, [(0, 0)]),
        (True, [(0, 1)]),
        (2, [(0, 1, 0)]),
    ],
)
def test_validate_graph_rejects_invalid_graphs(num_qubits, edges):
    with pytest.raises(ValueError):
        validate_graph(num_qubits, edges)


@pytest.mark.parametrize("bitstring", ["", "02", "abc"])
def test_cut_value_rejects_invalid_bitstrings(bitstring):
    with pytest.raises(ValueError):
        cut_value(bitstring, [(0, 1)])


def test_qaoa_state_has_correct_size():
    state = qaoa_state(2, [(0, 1)], gamma=0.5, beta=0.3)
    assert len(state) == 4


def test_qaoa_state_is_normalized():
    state = qaoa_state(2, [(0, 1)], gamma=0.5, beta=0.3)
    norm = sum(abs(amplitude) ** 2 for amplitude in state)
    assert norm == pytest.approx(1.0)


def test_mixer_preserves_state_norm():
    state = [0.5 + 0j, 0.5 + 0j, 0.5 + 0j, 0.5 + 0j]
    result = apply_mixer(state, beta=0.4, num_qubits=2)
    norm = sum(abs(amplitude) ** 2 for amplitude in result)
    assert norm == pytest.approx(1.0)


def test_expected_cut_for_basis_state():
    state = [0j, 1 + 0j, 0j, 0j]
    assert expected_cut(state, 2, [(0, 1)]) == pytest.approx(1.0)


def test_optimizer_finds_maximum_for_single_edge():
    result = optimize_qaoa(2, [(0, 1)], grid_size=20)
    assert result["expected_cut"] == pytest.approx(1.0, abs=1e-9)


def test_optimizer_returns_valid_parameters():
    result = optimize_qaoa(2, [(0, 1)], grid_size=10)
    assert 0.0 <= result["gamma"] <= math.pi
    assert 0.0 <= result["beta"] <= math.pi / 2


@pytest.mark.parametrize("grid_size", [0, 1, -1, 2.5, True])
def test_optimizer_rejects_invalid_grid_size(grid_size):
    with pytest.raises(ValueError):
        optimize_qaoa(2, [(0, 1)], grid_size=grid_size)