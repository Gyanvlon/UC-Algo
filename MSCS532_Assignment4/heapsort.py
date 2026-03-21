"""
heapsort.py
===========
Implementation of the Heapsort algorithm using an array-based max-heap
stored in a Python list.

Algorithm Overview
------------------
Phase 1 — Build Max-Heap  (O(n))
    Convert the input array into a max-heap by calling heapify on every
    internal node from the last one up to the root.  This "bottom-up"
    build is O(n) — not O(n log n) — because most nodes sit near the
    leaves and each incurs only O(1) work.

Phase 2 — Repeated Extraction  (O(n log n))
    Swap the root (the current maximum) with the last element of the
    heap, shrink the logical heap size by 1, and restore the heap
    property at the root (heapify).  Repeat until the heap is empty.

Total time  : O(n) + O(n log n) = O(n log n)
Extra space : O(1)  — the sort is performed entirely in place.
              (O(log n) if heapify were recursive; here it is iterative.)
"""

from __future__ import annotations
from typing import List


# ---------------------------------------------------------------------------
# Core heap routines
# ---------------------------------------------------------------------------

def heapify(arr: List, n: int, i: int) -> None:
    """
    Restore the max-heap property for the subtree rooted at index *i*.

    Uses an **iterative** loop instead of recursion to keep the call-stack
    depth O(1) regardless of heap height — important for large inputs under
    Python's default recursion limit.

    Parameters
    ----------
    arr : list
        The array representing the heap.
    n : int
        Current logical heap size (elements arr[n:] are already sorted).
    i : int
        Root index of the subtree to heapify.

    Complexity
    ----------
    Time  : O(log n)  — at most h = floor(log2 n) comparisons and swaps.
    Space : O(1)      — no auxiliary storage.
    """
    while True:
        largest = i
        left    = 2 * i + 1   # left child index
        right   = 2 * i + 2   # right child index

        # Is the left child larger than the current 'largest'?
        if left < n and arr[left] > arr[largest]:
            largest = left

        # Is the right child larger?
        if right < n and arr[right] > arr[largest]:
            largest = right

        # If neither child is larger, the heap property is satisfied here.
        if largest == i:
            break

        # Swap root down and continue from where it landed.
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr: List) -> None:
    """
    Transform an arbitrary list into a max-heap **in place** in O(n) time.

    Why start at index (n // 2 − 1)?
    ----------------------------------
    In a 0-based array heap, nodes at indices >= n // 2 are leaf nodes —
    they trivially satisfy the heap property with no children to compare.
    Only the n // 2 internal nodes need heapification.

    Why O(n) and not O(n log n)?
    -----------------------------
    Nodes at depth d have height (h − d) where h = floor(log2 n).
    The cost of heapifying a node at height k is O(k).  Summing over all
    levels gives:

        sum_{k=0}^{h} (n / 2^(k+1)) * k  =  O(n) * sum_{k=0}^{h} k/2^k

    The geometric sum converges to 2, so the total is O(n).

    Parameters
    ----------
    arr : list
        The list to transform (modified in place).

    Complexity
    ----------
    Time  : O(n)
    Space : O(1)
    """
    n = len(arr)
    # Start at the last internal node and work toward the root.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heapsort(arr: List) -> List:
    """
    Sort *arr* in ascending order using the Heapsort algorithm.

    The list is sorted **in place**; the same list object is returned for
    convenience (e.g. allowing assignment or chaining).

    Algorithm
    ---------
    1. Build a max-heap in O(n).
    2. For i from n-1 down to 1:
         a. Swap arr[0] (max element) with arr[i]  → O(1)
         b. Heapify the reduced heap [0..i-1]      → O(log i)
    Total: O(n) + sum_{i=1}^{n-1} O(log i) = O(n) + O(n log n) = O(n log n)

    Parameters
    ----------
    arr : list
        The list to sort.

    Returns
    -------
    list
        The same list, now sorted in ascending order.

    Complexity
    ----------
    Time  : O(n log n) — worst, average, *and* best case.
            Unlike Quicksort there is no better-case scenario because
            even a fully sorted array requires a full heap build and
            n heapify passes.
    Space : O(1)       — in-place; only a constant number of temporary
                         variables are used.
    """
    n = len(arr)

    # ---- Phase 1: Build max-heap ----------------------------------------
    build_max_heap(arr)

    # ---- Phase 2: Extract elements from the heap one by one --------------
    for i in range(n - 1, 0, -1):
        # arr[0] holds the current maximum; move it to its final sorted position.
        arr[0], arr[i] = arr[i], arr[0]

        # The heap now has one fewer element (arr[i] is finalised).
        # Restore the max-heap property for the reduced heap arr[0..i-1].
        heapify(arr, i, 0)

    return arr


# ---------------------------------------------------------------------------
# Demonstration and self-tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import random

    def _assert_sorted(original: list, result: list) -> None:
        expected = sorted(original)
        if result != expected:
            raise AssertionError(
                f"heapsort({original!r}) returned {result!r}, expected {expected!r}"
            )

    print("=" * 60)
    print("Heapsort — Demonstration & Correctness Checks")
    print("=" * 60)

    # ---- Named test cases ------------------------------------------------
    named_cases = [
        ("Random integers",   [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]),
        ("Already sorted",    list(range(1, 11))),
        ("Reverse sorted",    list(range(10, 0, -1))),
        ("All identical",     [7] * 6),
        ("Single element",    [42]),
        ("Empty array",       []),
        ("Negative numbers",  [-5, -1, -3, -2, -4]),
        ("Mixed pos/neg",     [3, -1, 4, -1, 5, -9, 2, -6]),
        ("Two elements",      [2, 1]),
    ]

    for label, data in named_cases:
        result = heapsort(data[:])   # sort a copy so we keep the original
        _assert_sorted(data, result)
        print(f"  {label:25s}  {str(data):35s}  ->  {result}")

    # ---- Stress test ------------------------------------------------------
    print("\nStress-testing with 5 000 random arrays …")
    for _ in range(5_000):
        data = [random.randint(-10_000, 10_000)
                for _ in range(random.randint(0, 120))]
        result = heapsort(data[:])
        _assert_sorted(data, result)

    print("All tests passed.\n")
