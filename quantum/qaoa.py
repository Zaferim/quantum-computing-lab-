"""
Quantum Approximate Optimization Algorithm (QAOA).

A small state-vector QAOA simulation for the Max-Cut problem.
The graph is represented by its edges, and each edge contributes
one point when its endpoints have different bit values.
"""

from itertools import product
from math import cos, sin, pi, sqrt


def validate_graph(num_qubits, edges):
    """Validate the graph and its edges."""
    if (
        not isinstance(num_qubits, int)
        or isinstance(num_qubits, bool)
        or num_qubits < 2
    ):
        raise ValueError("num_qubits must be an integer >= 2.")

    try:
        edges = list(edges)
    except TypeError as exc:
        raise ValueError("edges must be an iterable of pairs.") from exc

    normalized_edges = []

    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("Each edge must contain two vertex indices.")

        u, v = edge

        if (
            not isinstance(u, int)
            or isinstance(u, bool)
            or not isinstance(v, int)
            or isinstance(v, bool)
        ):
            raise ValueError("Vertex indices must be integers.")

        if not (0 <= u < num_qubits and 0 <= v < num_qubits):
            raise ValueError("Vertex index is out of range.")

        if u == v:
            raise ValueError("Self-loops are not supported.")

        normalized_edges.append((u, v))

    return normalized_edges


def cut_value(bitstring, edges):
    """Count graph edges whose endpoints have different bits."""
    if not isinstance(bitstring, str) or not bitstring:
        raise ValueError("bitstring must be a non-empty binary string.")

    if any(bit not in "01" for bit in bitstring):
        raise ValueError("bitstring must contain only 0 and 1.")

    for edge in edges:
        if (
            not isinstance(edge, (tuple, list))
            or len(edge) != 2
        ):
            raise ValueError("Each edge must contain two vertex indices.")

        u, v = edge

        if not (0 <= u < len(bitstring) and 0 <= v < len(bitstring)):
            raise ValueError("Vertex index is out of range.")

        if u == v:
            raise ValueError("Self-loops are not supported.")

    return sum(bitstring[u] != bitstring[v] for u, v in edges)


def apply_mixer(state, beta, num_qubits):
    """Apply the QAOA X-mixer unitary to every qubit."""
    if len(state) != 2**num_qubits:
        raise ValueError("State-vector size does not match qubit count.")

    result = list(state)
    c = cos(beta)
    s = -1j * sin(beta)

    for qubit in range(num_qubits):
        mask = 1 << (num_qubits - 1 - qubit)
        updated = [0j] * len(result)

        for index, amplitude in enumerate(result):
            flipped_index = index ^ mask
            updated[index] += c * amplitude
            updated[flipped_index] += s * amplitude

        result = updated

    return result


def qaoa_state(num_qubits, edges, gamma, beta):
    """Build a depth-p=1 QAOA state for a Max-Cut graph."""
    edges = validate_graph(num_qubits, edges)

    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in (gamma, beta)
    ):
        raise ValueError("gamma and beta must be real numbers.")

    # Start in the uniform superposition.
    size = 2**num_qubits
    state = [1 / sqrt(size) + 0j] * size

    # Apply the Max-Cut cost unitary.
    for index in range(size):
        bitstring = format(index, f"0{num_qubits}b")
        cost = cut_value(bitstring, edges)
        state[index] *= complex(cos(gamma * cost), -sin(gamma * cost))

    # Apply the X-mixer.
    return apply_mixer(state, beta, num_qubits)


def expected_cut(state, num_qubits, edges):
    """Calculate the expected cut value of a quantum state."""
    if len(state) != 2**num_qubits:
        raise ValueError("State-vector size does not match qubit count.")

    edges = validate_graph(num_qubits, edges)

    return sum(
        abs(amplitude) ** 2
        * cut_value(format(index, f"0{num_qubits}b"), edges)
        for index, amplitude in enumerate(state)
    )


def optimize_qaoa(num_qubits, edges, grid_size=20):
    """Find good depth-p=1 QAOA parameters using a grid search."""
    edges = validate_graph(num_qubits, edges)

    if (
        not isinstance(grid_size, int)
        or isinstance(grid_size, bool)
        or grid_size < 2
    ):
        raise ValueError("grid_size must be an integer >= 2.")

    best = {
        "gamma": 0.0,
        "beta": 0.0,
        "expected_cut": float("-inf"),
    }

    for gamma_index in range(grid_size + 1):
        gamma = pi * gamma_index / grid_size

        for beta_index in range(grid_size + 1):
            beta = (pi / 2) * beta_index / grid_size
            state = qaoa_state(num_qubits, edges, gamma, beta)
            score = expected_cut(state, num_qubits, edges)

            if score > best["expected_cut"]:
                best = {
                    "gamma": gamma,
                    "beta": beta,
                    "expected_cut": score,
                }

    best["expected_cut"] = round(best["expected_cut"], 12)
    return best


if __name__ == "__main__":
    # A two-vertex graph with one edge has a maximum cut of 1.
    graph_edges = [(0, 1)]
    result = optimize_qaoa(num_qubits=2, edges=graph_edges)

    print("QAOA Max-Cut Simulation")
    print("-----------------------")
    print(f"Edges: {graph_edges}")
    print(f"Best gamma: {result['gamma']:.6f}")
    print(f"Best beta: {result['beta']:.6f}")
    print(f"Expected cut: {result['expected_cut']:.6f}")
    print("Maximum possible cut: 1")