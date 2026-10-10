"""Tests for quantum algorithm benchmarking utilities."""
import pytest
from quantum.benchmark import (
    BenchmarkResult,
    benchmark,
    benchmark_algorithms,
)
def test_benchmark_returns_result():
    result = benchmark(lambda: 1 + 1, iterations=3, warmup=0)
    assert isinstance(result, BenchmarkResult)
    assert result.iterations == 3
    assert result.average_seconds >= 0
    assert result.min_seconds >= 0
    assert result.max_seconds >= result.min_seconds
def test_benchmark_uses_custom_name():
    result = benchmark(
        lambda: None,
        name="custom-test",
        iterations=1,
        warmup=0,
    )
    assert result.name == "custom-test"
def test_benchmark_uses_callable_name():
    def example_function():
        return None
    result = benchmark(example_function, iterations=1, warmup=0)
    assert result.name == "example_function"
def test_benchmark_fallback_name_for_callable_without_name():
    class CallableObject:
        def __call__(self):
            return None
    result = benchmark(CallableObject(), iterations=1, warmup=0)
    assert result.name == "benchmark"
def test_benchmark_counts_warmup_and_iterations():
    calls = 0
    def function():
        nonlocal calls
        calls += 1
    result = benchmark(function, iterations=4, warmup=2)
    assert calls == 6
    assert result.iterations == 4
def test_benchmark_to_dict():
    result = benchmark(
        lambda: None,
        name="dictionary-test",
        iterations=2,
        warmup=0,
    )
    data = result.to_dict()
    assert data["name"] == "dictionary-test"
    assert data["iterations"] == 2
    assert data["average_seconds"] >= 0
    assert data["min_seconds"] >= 0
    assert data["max_seconds"] >= data["min_seconds"]
def test_benchmark_rejects_non_callable():
    with pytest.raises(TypeError, match="function must be callable"):
        benchmark(None, iterations=1, warmup=0)
@pytest.mark.parametrize("iterations", [0, -1])
def test_benchmark_rejects_invalid_iterations(iterations):
    with pytest.raises(ValueError, match="iterations must be at least 1"):
        benchmark(lambda: None, iterations=iterations, warmup=0)
@pytest.mark.parametrize("warmup", [-1, -5])
def test_benchmark_rejects_negative_warmup(warmup):
    with pytest.raises(ValueError, match="warmup cannot be negative"):
        benchmark(lambda: None, iterations=1, warmup=warmup)
@pytest.mark.parametrize("iterations", [1.5, "3", True])
def test_benchmark_rejects_non_integer_iterations(iterations):
    with pytest.raises(TypeError, match="iterations must be an integer"):
        benchmark(lambda: None, iterations=iterations, warmup=0)
@pytest.mark.parametrize("warmup", [1.5, "2", True])
def test_benchmark_rejects_non_integer_warmup(warmup):
    with pytest.raises(TypeError, match="warmup must be an integer"):
        benchmark(lambda: None, iterations=1, warmup=warmup)
def test_benchmark_propagates_function_errors():
    def failing_function():
        raise RuntimeError("test failure")
    with pytest.raises(RuntimeError, match="test failure"):
        benchmark(failing_function, iterations=1, warmup=0)
def test_benchmark_algorithms_returns_four_results():
    results = benchmark_algorithms(iterations=1, warmup=0)
    assert len(results) == 4
    assert all(isinstance(result, BenchmarkResult) for result in results)
    assert all(result.iterations == 1 for result in results)
def test_benchmark_algorithm_names():
    results = benchmark_algorithms(iterations=1, warmup=0)
    names = [result.name for result in results]
    assert names == [
        "Deutsch-Jozsa",
        "Grover",
        "Superdense Coding",
        "Quantum Teleportation",
    ]
def test_benchmark_algorithms_rejects_invalid_iterations():
    with pytest.raises(ValueError, match="iterations must be at least 1"):
        benchmark_algorithms(iterations=0, warmup=0)