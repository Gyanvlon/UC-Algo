"""Empirical benchmark for deterministic vs randomized selection.

Run from project root:
    python -m benchmarks.selection_benchmark
"""

from __future__ import annotations

import argparse
import csv
import random
import statistics
import time
from pathlib import Path
from typing import Callable, Dict, List, Sequence

from src.selection import deterministic_select, randomized_select


Generator = Callable[[int, random.Random], List[int]]


def gen_random(n: int, rng: random.Random) -> List[int]:
    return [rng.randint(0, 10 * n) for _ in range(n)]


def gen_sorted(n: int, rng: random.Random) -> List[int]:
    _ = rng
    return list(range(n))


def gen_reverse_sorted(n: int, rng: random.Random) -> List[int]:
    _ = rng
    return list(range(n, 0, -1))


def gen_few_unique(n: int, rng: random.Random) -> List[int]:
    domain = max(5, n // 20)
    return [rng.randint(0, domain) for _ in range(n)]


def benchmark_once(values: Sequence[int], k: int) -> Dict[str, float]:
    t0 = time.perf_counter()
    d = deterministic_select(values, k)
    t1 = time.perf_counter()

    r = randomized_select(values, k)
    t2 = time.perf_counter()

    expected = sorted(values)[k - 1]
    if d != expected or r != expected:
        raise AssertionError("Selection output mismatch detected")

    return {
        "deterministic_seconds": t1 - t0,
        "randomized_seconds": t2 - t1,
    }


def run_benchmarks(
    sizes: Sequence[int],
    trials: int,
    seed: int,
    output_csv: Path,
) -> List[Dict[str, object]]:
    rng = random.Random(seed)
    distributions: Dict[str, Generator] = {
        "random": gen_random,
        "sorted": gen_sorted,
        "reverse_sorted": gen_reverse_sorted,
        "few_unique": gen_few_unique,
    }

    records: List[Dict[str, object]] = []

    for n in sizes:
        for dist_name, generator in distributions.items():
            d_times: List[float] = []
            r_times: List[float] = []

            for _ in range(trials):
                arr = generator(n, rng)
                k = rng.randint(1, n)
                result = benchmark_once(arr, k)
                d_times.append(result["deterministic_seconds"])
                r_times.append(result["randomized_seconds"])

            record = {
                "n": n,
                "distribution": dist_name,
                "trials": trials,
                "deterministic_mean_sec": statistics.mean(d_times),
                "deterministic_std_sec": statistics.pstdev(d_times),
                "randomized_mean_sec": statistics.mean(r_times),
                "randomized_std_sec": statistics.pstdev(r_times),
            }
            records.append(record)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "n",
                "distribution",
                "trials",
                "deterministic_mean_sec",
                "deterministic_std_sec",
                "randomized_mean_sec",
                "randomized_std_sec",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    return records


def print_table(records: Sequence[Dict[str, object]]) -> None:
    header = (
        f"{'n':>8} | {'distribution':>14} | {'det mean (s)':>13} | "
        f"{'rand mean (s)':>13} | {'faster':>13}"
    )
    print(header)
    print("-" * len(header))

    for row in records:
        d = float(row["deterministic_mean_sec"])
        r = float(row["randomized_mean_sec"])
        faster = "deterministic" if d < r else "randomized"
        print(
            f"{int(row['n']):>8} | {str(row['distribution']):>14} | "
            f"{d:>13.6f} | {r:>13.6f} | {faster:>13}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark selection algorithms")
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=[1000, 5000, 10000, 20000],
        help="Input sizes to benchmark",
    )
    parser.add_argument("--trials", type=int, default=5, help="Trials per setting")
    parser.add_argument("--seed", type=int, default=5326, help="Random seed")
    parser.add_argument(
        "--output",
        type=str,
        default="results/selection_benchmark_results.csv",
        help="Path to CSV output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = run_benchmarks(
        sizes=args.sizes,
        trials=args.trials,
        seed=args.seed,
        output_csv=Path(args.output),
    )
    print_table(records)
    print(f"\nSaved CSV results to: {args.output}")


if __name__ == "__main__":
    main()
