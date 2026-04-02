"""Selection algorithms for order statistics.

This module implements:
1. Deterministic selection (Median of Medians), worst-case O(n)
2. Randomized Quickselect, expected O(n)

All public APIs use 1-based k:
- k=1 gives the minimum element
- k=len(arr) gives the maximum element
"""

from __future__ import annotations

from random import randrange
from typing import List, Sequence, Tuple, TypeVar

T = TypeVar("T")


def _three_way_partition(values: Sequence[T], pivot: T) -> Tuple[List[T], List[T], List[T]]:
    """Partition values into (< pivot), (== pivot), (> pivot)."""
    less: List[T] = []
    equal: List[T] = []
    greater: List[T] = []

    for v in values:
        if v < pivot:
            less.append(v)
        elif v > pivot:
            greater.append(v)
        else:
            equal.append(v)

    return less, equal, greater


def _median_of_small_group(group: Sequence[T]) -> T:
    """Return the median of a group of up to 5 elements."""
    sorted_group = sorted(group)
    return sorted_group[len(sorted_group) // 2]


def _median_of_medians(values: Sequence[T]) -> T:
    """Choose a pivot with guaranteed balance using median-of-medians."""
    n = len(values)
    if n <= 5:
        return _median_of_small_group(values)

    medians = [_median_of_small_group(values[i : i + 5]) for i in range(0, n, 5)]
    return _deterministic_select_zero_based(medians, len(medians) // 2)


def _deterministic_select_zero_based(values: Sequence[T], k_index: int) -> T:
    """Select the k_index-th smallest element using deterministic O(n) selection."""
    if not values:
        raise ValueError("Cannot select from an empty sequence")
    if k_index < 0 or k_index >= len(values):
        raise IndexError("k is out of range")

    if len(values) <= 5:
        return sorted(values)[k_index]

    pivot = _median_of_medians(values)
    less, equal, greater = _three_way_partition(values, pivot)

    if k_index < len(less):
        return _deterministic_select_zero_based(less, k_index)

    if k_index < len(less) + len(equal):
        return pivot

    return _deterministic_select_zero_based(greater, k_index - len(less) - len(equal))


def _randomized_select_zero_based(values: Sequence[T], k_index: int) -> T:
    """Select the k_index-th smallest element using randomized Quickselect."""
    if not values:
        raise ValueError("Cannot select from an empty sequence")
    if k_index < 0 or k_index >= len(values):
        raise IndexError("k is out of range")

    # Iterative form avoids deep recursion on unlucky partitions.
    current = list(values)
    target = k_index

    while True:
        if len(current) <= 5:
            return sorted(current)[target]

        pivot = current[randrange(len(current))]
        less, equal, greater = _three_way_partition(current, pivot)

        if target < len(less):
            current = less
            continue

        if target < len(less) + len(equal):
            return pivot

        target -= len(less) + len(equal)
        current = greater


def deterministic_select(values: Sequence[T], k: int) -> T:
    """Return the k-th smallest element using median-of-medians.

    Args:
        values: Input sequence.
        k: 1-based order statistic (1 <= k <= len(values)).

    Returns:
        The k-th smallest element.
    """
    if k < 1 or k > len(values):
        raise IndexError("k must satisfy 1 <= k <= len(values)")
    return _deterministic_select_zero_based(values, k - 1)


def randomized_select(values: Sequence[T], k: int) -> T:
    """Return the k-th smallest element using randomized Quickselect.

    Args:
        values: Input sequence.
        k: 1-based order statistic (1 <= k <= len(values)).

    Returns:
        The k-th smallest element.
    """
    if k < 1 or k > len(values):
        raise IndexError("k must satisfy 1 <= k <= len(values)")
    return _randomized_select_zero_based(values, k - 1)


def _sanity_check() -> None:
    """Small self-check used when running this module directly."""
    data = [7, 3, 5, 3, 9, 1, 1, 4, 8, 6, 2]
    ordered = sorted(data)

    for i in range(1, len(data) + 1):
        d = deterministic_select(data, i)
        r = randomized_select(data, i)
        assert d == ordered[i - 1], f"deterministic mismatch at k={i}"
        assert r == ordered[i - 1], f"randomized mismatch at k={i}"


if __name__ == "__main__":
    _sanity_check()
    print("Selection algorithms sanity check passed.")
