"""Empirical comparison between randomized and deterministic quicksort."""

from __future__ import annotations

import csv
import random
import time
from statistics import mean
from typing import Callable, Dict, List

from RandomizedQuicksort import deterministic_quicksort_first, randomized_quicksort


def generate_dataset(distribution: str, n: int, rng: random.Random) -> List[int]:
    if distribution == "random":
        return [rng.randint(0, 10 * n) for _ in range(n)]
    if distribution == "sorted":
        return list(range(n))
    if distribution == "reverse":
        return list(range(n, 0, -1))
    if distribution == "repeated":
        return [rng.randint(0, 20) for _ in range(n)]
    raise ValueError(f"Unsupported distribution: {distribution}")


def time_algorithm(sort_fn: Callable[[List[int]], List[int]], data: List[int]) -> float:
    start = time.perf_counter()
    out = sort_fn(data)
    elapsed = time.perf_counter() - start

    if out != sorted(data):
        raise RuntimeError("Sort validation failed.")

    return elapsed


def run_benchmark() -> List[Dict[str, object]]:
    rng = random.Random(2026)

    sizes = [200, 500, 1000, 2000, 4000]
    distributions = ["random", "sorted", "reverse", "repeated"]

    results: List[Dict[str, object]] = []

    for distribution in distributions:
        for n in sizes:
            trials = 5 if distribution in {"random", "repeated"} else 3

            random_times = []
            deterministic_times = []

            for t in range(trials):
                data = generate_dataset(distribution, n, rng)
                random_times.append(time_algorithm(lambda arr: randomized_quicksort(arr, seed=t), data))
                deterministic_times.append(time_algorithm(deterministic_quicksort_first, data))

            results.append(
                {
                    "distribution": distribution,
                    "n": n,
                    "trials": trials,
                    "randomized_sec": mean(random_times),
                    "deterministic_sec": mean(deterministic_times),
                    "speedup_randomized_over_deterministic": (
                        mean(deterministic_times) / mean(random_times) if mean(random_times) > 0 else float("inf")
                    ),
                }
            )

    return results


def write_csv(results: List[Dict[str, object]], path: str = "quicksort_benchmark_results.csv") -> None:
    fieldnames = [
        "distribution",
        "n",
        "trials",
        "randomized_sec",
        "deterministic_sec",
        "speedup_randomized_over_deterministic",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_table(results: List[Dict[str, object]]) -> None:
    header = (
        f"{'distribution':<12} {'n':>6} {'trials':>6} {'randomized(s)':>15} "
        f"{'deterministic(s)':>18} {'det/random':>12}"
    )
    print(header)
    print("-" * len(header))

    for row in results:
        print(
            f"{row['distribution']:<12} {row['n']:>6} {row['trials']:>6} "
            f"{row['randomized_sec']:>15.6f} {row['deterministic_sec']:>18.6f} "
            f"{row['speedup_randomized_over_deterministic']:>12.3f}"
        )


if __name__ == "__main__":
    benchmark_results = run_benchmark()
    write_csv(benchmark_results)
    print_table(benchmark_results)
    print("\nSaved results to quicksort_benchmark_results.csv")
