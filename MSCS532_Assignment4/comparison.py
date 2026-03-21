"""
comparison.py
=============
Empirical running-time comparison of Heapsort, Quicksort, and Merge Sort.

Measures wall-clock time via time.perf_counter() across multiple input
sizes and distribution types, then prints a formatted results table,
saves a CSV, and optionally generates a matplotlib plot.

Algorithms
----------
  heapsort    — our implementation in heapsort.py
  quicksort   — in-place, randomised pivot (avoids O(n²) on sorted inputs)
  merge_sort  — classic top-down merge sort returning a new list

Input distributions
-------------------
  random          — uniformly random integers
  sorted          — ascending order
  reverse_sorted  — descending order
  nearly_sorted   — sorted with ~2 % positions randomly swapped
  many_duplicates — values drawn from a tiny pool (n // 100 distinct values)
"""

from __future__ import annotations

import csv
import os
import random
import sys
import time
from typing import Callable, Dict, List

# Raise the recursion limit so that quicksort / merge_sort do not hit
# Python's default of 1 000 on large inputs. log2(50 000) ≈ 16 levels,
# so the default is already fine in practice, but this is defensive.
sys.setrecursionlimit(200_000)

# Make heapsort importable from the same directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from heapsort import heapsort


# ---------------------------------------------------------------------------
# Comparison sorting algorithms
# ---------------------------------------------------------------------------

def quicksort(arr: List) -> List:
    """
    In-place randomised Quicksort.

    Randomly selecting the pivot gives expected O(n log n) performance on
    any input distribution, avoiding the O(n²) worst case that a fixed
    'last-element' pivot exhibits on already-sorted data.

    Time  : Expected O(n log n);  O(n²) worst case (probability ~ 1/n!)
    Space : O(log n) average call-stack depth;  O(n) worst case
    """
    _qs(arr, 0, len(arr) - 1)
    return arr


def _qs(arr: List, lo: int, hi: int) -> None:
    if lo < hi:
        p = _partition(arr, lo, hi)
        _qs(arr, lo, p - 1)
        _qs(arr, p + 1, hi)


def _partition(arr: List, lo: int, hi: int) -> int:
    # Randomised pivot: swap a random element to the end, then partition.
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def merge_sort(arr: List) -> List:
    """
    Top-down merge sort.  Returns a *new* sorted list (non-destructive).

    Time  : O(n log n) — all cases
    Space : O(n)       — auxiliary arrays at each merge level
    """
    if len(arr) <= 1:
        return arr[:]
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: List, right: List) -> List:
    result: List = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Input generators
# ---------------------------------------------------------------------------

def _nearly_sorted(n: int) -> List[int]:
    arr = list(range(n))
    num_swaps = max(1, n // 50)   # ~2 % of positions
    for _ in range(num_swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


DISTRIBUTIONS: Dict[str, Callable[[int], List[int]]] = {
    "random":          lambda n: [random.randint(0, n * 10) for _ in range(n)],
    "sorted":          lambda n: list(range(n)),
    "reverse_sorted":  lambda n: list(range(n, 0, -1)),
    "nearly_sorted":   _nearly_sorted,
    "many_duplicates": lambda n: [random.randint(0, max(1, n // 100)) for _ in range(n)],
}


# ---------------------------------------------------------------------------
# Timing harness
# ---------------------------------------------------------------------------

# Number of independent trials per (algorithm, size, distribution) combination.
# The *minimum* time across trials is reported — this reflects the algorithm's
# true cost, since the minimum has the least OS-scheduling noise.
TRIALS = 5

SIZES: List[int] = [100, 500, 1_000, 5_000, 10_000, 30_000]

ALGORITHMS: Dict[str, Callable[[List], List]] = {
    "Heapsort":   heapsort,
    "Quicksort":  quicksort,
    "Merge Sort": merge_sort,
}


def time_one(fn: Callable[[List], List], data: List) -> float:
    """
    Return the minimum wall-clock time (seconds) for *fn* on a copy of *data*
    over TRIALS independent runs.
    """
    best = float("inf")
    for _ in range(TRIALS):
        copy = data[:]            # sort a fresh copy every trial
        t0 = time.perf_counter()
        fn(copy)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return best


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------

def run_comparison() -> List[dict]:
    """
    Execute all benchmarks and return a list of result rows (one per
    distribution × size combination), each containing timing in seconds
    for every algorithm.
    """
    results: List[dict] = []
    total = len(DISTRIBUTIONS) * len(SIZES) * len(ALGORITHMS)
    done  = 0

    print(
        f"Running {total} combinations  "
        f"({TRIALS} trials each, reporting minimum time) …\n"
    )

    for dist_name, gen in DISTRIBUTIONS.items():
        for size in SIZES:
            data = gen(size)
            row: dict = {"distribution": dist_name, "size": size}
            for algo_name, fn in ALGORITHMS.items():
                elapsed = time_one(fn, data)
                row[algo_name] = elapsed
                done += 1
                print(
                    f"  [{done:>3}/{total}]  {algo_name:<12s}  "
                    f"n={size:>6}  dist={dist_name:<18s}  "
                    f"{elapsed * 1000:>9.3f} ms"
                )
            results.append(row)

    return results


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_table(results: List[dict]) -> None:
    """Print a human-readable results table grouped by distribution."""
    col_w      = 13
    algo_names = list(ALGORITHMS.keys())
    header     = (
        f"  {'Distribution':<20} {'Size':>7} "
        + "".join(f"{a:>{col_w}}" for a in algo_names)
        + "   (ms, min of 5)"
    )
    sep = "-" * len(header)

    current_dist = None
    for row in results:
        dist = row["distribution"]
        if dist != current_dist:
            if current_dist is not None:
                print(sep)
            print(f"\n{sep}")
            print(header)
            print(sep)
            current_dist = dist

        times = "".join(f"{row[a] * 1000:>{col_w}.3f}" for a in algo_names)
        print(f"  {dist:<20} {row['size']:>7} {times}")

    print(sep)


def save_csv(results: List[dict], path: str = "comparison_results.csv") -> None:
    """Write timing results to a CSV file (times in milliseconds)."""
    fields = ["distribution", "size"] + list(ALGORITHMS.keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow({
                k: (f"{v * 1000:.4f}" if isinstance(v, float) else v)
                for k, v in row.items()
            })
    print(f"\nCSV results saved to: {path}")


def plot_results(results: List[dict]) -> None:
    """Generate comparison line plots (requires matplotlib; skipped if absent)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib not installed — skipping plot generation.")
        print("Install it with: pip install matplotlib")
        return

    dist_names = list(DISTRIBUTIONS.keys())
    n_dists    = len(dist_names)
    ncols      = 3
    nrows      = (n_dists + ncols - 1) // ncols

    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols,
        figsize=(16, 5 * nrows),
        constrained_layout=True,
    )
    fig.suptitle(
        "Sorting Algorithm Comparison — Time (ms) vs. Input Size\n"
        "(lower is faster; min of 5 trials)",
        fontsize=13, fontweight="bold",
    )

    axes_flat = axes.flatten() if nrows > 1 else axes
    for ax, dist in zip(axes_flat, dist_names):
        dist_rows  = [r for r in results if r["distribution"] == dist]
        sizes      = [r["size"] for r in dist_rows]
        for algo in ALGORITHMS:
            times_ms = [r[algo] * 1000 for r in dist_rows]
            ax.plot(sizes, times_ms, marker="o", label=algo)
        ax.set_title(dist.replace("_", " ").title(), fontsize=11)
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Time (ms)")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.35)

    # Hide any unused subplot cells.
    for ax in axes_flat[n_dists:]:
        ax.set_visible(False)

    out_path = "comparison_plot.png"
    plt.savefig(out_path, dpi=150)
    print(f"Plot saved to: {out_path}")
    plt.show()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)   # reproducible results

    results = run_comparison()

    print("\n\n" + "=" * 75)
    print("RESULTS TABLE  —  time in milliseconds, best of 5 trials per cell")
    print("=" * 75)
    print_table(results)

    save_csv(results)
    plot_results(results)
