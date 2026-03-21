"""Implementations of randomized and deterministic quicksort.

This module includes:
- Randomized quicksort (pivot chosen uniformly at random)
- Deterministic quicksort (first element as pivot)

Both algorithms use 3-way partitioning to handle repeated elements robustly.
"""

from __future__ import annotations

import random
from typing import Callable, List, Optional, Sequence, Tuple


PivotSelector = Callable[[int, int, random.Random], int]


def _random_pivot(low: int, high: int, rng: random.Random) -> int:
    return rng.randint(low, high)


def _first_pivot(low: int, high: int, rng: random.Random) -> int:
    del high, rng
    return low


def _three_way_partition(arr: List[int], low: int, high: int, pivot_index: int) -> Tuple[int, int]:
    pivot = arr[pivot_index]
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]

    lt = low
    i = low + 1
    gt = high

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    return lt, gt


def _quicksort_in_place(arr: List[int], pivot_selector: PivotSelector, seed: Optional[int] = None) -> List[int]:
    if len(arr) <= 1:
        return arr

    rng = random.Random(seed)
    stack: List[Tuple[int, int]] = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        pivot_index = pivot_selector(low, high, rng)
        lt, gt = _three_way_partition(arr, low, high, pivot_index)

        left = (low, lt - 1)
        right = (gt + 1, high)

        left_size = left[1] - left[0]
        right_size = right[1] - right[0]

        if left_size > right_size:
            stack.append(left)
            stack.append(right)
        else:
            stack.append(right)
            stack.append(left)

    return arr


def randomized_quicksort(values: Sequence[int], seed: Optional[int] = None, in_place: bool = False) -> List[int]:
    """Sort values with randomized quicksort.

    Args:
        values: Input sequence.
        seed: Optional random seed to make runs reproducible.
        in_place: If True and values is a list, sort that list directly.
    """
    arr = values if (in_place and isinstance(values, list)) else list(values)
    return _quicksort_in_place(arr, pivot_selector=_random_pivot, seed=seed)


def deterministic_quicksort_first(values: Sequence[int], in_place: bool = False) -> List[int]:
    """Sort values with deterministic quicksort using first element as pivot."""
    arr = values if (in_place and isinstance(values, list)) else list(values)
    return _quicksort_in_place(arr, pivot_selector=_first_pivot)


def sort_randomized(arr: List[int]) -> List[int]:
    """Compatibility wrapper for assignment starter code behavior."""
    return randomized_quicksort(arr, in_place=True)


if __name__ == "__main__":
    sample = [5, 2, 9, 1, 5, 6, 5, 3]
    print("Original:", sample)
    print("Randomized quicksort:", randomized_quicksort(sample, seed=42))
    print("Deterministic (first pivot):", deterministic_quicksort_first(sample))