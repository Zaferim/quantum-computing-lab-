"""Lightweight performance benchmarking utilities for quantum algorithms."""
from __future__ import annotations
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class BenchmarkResult:
    """Performance measurements for a single callable."""
    name: str
    iterations: int
    average_seconds: float
    min_seconds: float
    max_seconds: float
    def to_dict(self) -> dict[str, Any]:
        """Return the result as a dictionary."""
        return {
            "name": self.name,
            "iterations": self.iterations,
            "average_seconds": self.average_seconds,
            "min_seconds": self.min_seconds,
            "max_seconds": self.max_seconds,
        }
def benchmark(
    function: Callable[[], Any],
    *,
    name: str | None = None,
    iterations: int = 5,
    warmup: int = 1,
) -> BenchmarkResult:
    """Measure the execution time of a zero-argument callable."""
    if not callable(function):
        raise TypeError("function must be callable")
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an integer")
    if isinstance(warmup, bool) or not isinstance(warmup, int):
        raise TypeError("warmup must be an integer")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if warmup < 0:
        raise ValueError("warmup cannot be negative")
    for _ in range(warmup):
        function()
    durations = []
    for _ in range(iterations):
        start = time.perf_counter()
        function()
        durations.append(time.perf_counter() - start)
    return BenchmarkResult(
        name=name or getattr(function, "__name__", "benchmark"),
        iterations=iterations,
        average_seconds=statistics.fmean(durations),
        min_seconds=min(durations),
        max_seconds=max(durations),
    )
def benchmark_algorithms(
    *,
    iterations: int = 5,
    warmup: int = 1,
) -> list[BenchmarkResult]:
    """Benchmark four algorithms implemented in this project."""
    from quantum.deutsch_jozsa import (
        create_constant_oracle,
        run_algorithm,
    )
    from quantum.grover import run_grover
    from quantum.superdense_coding import simulate_superdense_coding
    from quantum.teleportation import simulate_teleportation
    cases = [
        (
            "Deutsch-Jozsa",
            lambda: run_algorithm(create_constant_oracle()),
        ),
        (
            "Grover",
            run_grover,
        ),
        (
            "Superdense Coding",
            lambda: simulate_superdense_coding("10"),
        ),
        (
            "Quantum Teleportation",
            simulate_teleportation,
        ),
    ]
    results = []
    for algorithm_name, function in cases:
        results.append(
            benchmark(
                function,
                name=algorithm_name,
                iterations=iterations,
                warmup=warmup,
            )
        )
    return results
def main() -> None:
    """Run and display the sample benchmarks."""
    results = benchmark_algorithms()
    print("Quantum Algorithm Performance Benchmark")
    print("-" * 48)
    for result in results:
        print(
            f"{result.name}: "
            f"average={result.average_seconds:.6f}s, "
            f"min={result.min_seconds:.6f}s, "
            f"max={result.max_seconds:.6f}s "
            f"({result.iterations} iterations)"
        )
if __name__ == "__main__":
    main()