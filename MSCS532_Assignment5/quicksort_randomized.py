"""
Randomized Quicksort Implementation

This module provides a randomized implementation of the Quicksort algorithm
where the pivot is chosen randomly from the subarray being sorted.

The randomization helps avoid worst-case scenarios that occur with 
deterministic pivot selection strategies.

Author: Assignment 5
Date: 2026
"""

import random


def quicksort_randomized(arr, low=0, high=None):
    """
    Randomized Quicksort: sorts array in-place using a random pivot.
    
    By choosing the pivot randomly, we reduce the probability of hitting
    the worst-case O(n^2) scenario. On average, randomized quicksort provides
    O(n log n) expected time complexity with high probability.
    
    Time Complexity:
    - Best case: O(n log n) - optimal partitions
    - Average case: O(n log n) with high probability
    - Worst case: O(n^2) - very unlikely with random pivots
      (probability decreases exponentially with input size)
    
    Space Complexity:
    - O(log n) average due to tail recursion optimization
    - O(n) worst case without optimization
    
    Args:
        arr (list): The array to be sorted
        low (int): Starting index of the subarray (default: 0)
        high (int): Ending index of the subarray (default: len(arr) - 1)
    
    Returns:
        list: The sorted array (modified in-place)
    """
    if high is None:
        high = len(arr) - 1
    
    while low < high:
        # Partition with random pivot selection
        pivot_index = partition_random(arr, low, high)
        
        # Tail recursion optimization: recurse on smaller partition first
        if pivot_index - low < high - pivot_index:
            # Left partition is smaller
            quicksort_randomized(arr, low, pivot_index - 1)
            low = pivot_index + 1  # Tail recursion on right
        else:
            # Right partition is smaller
            quicksort_randomized(arr, pivot_index + 1, high)
            high = pivot_index - 1  # Tail recursion on left
    
    return arr


def partition_random(arr, low, high):
    """
    Partition scheme with random pivot selection.
    
    This function randomly selects a pivot from the subarray [low, high],
    moves it to the end, and then performs Lomuto partition.
    
    Time Complexity: O(n) where n = high - low + 1
    
    Args:
        arr (list): The array to partition
        low (int): Starting index
        high (int): Ending index
    
    Returns:
        int: Index of the pivot in its final sorted position
    """
    # Random index between low and high
    random_index = random.randint(low, high)
    
    # Swap random element with last element
    arr[random_index], arr[high] = arr[high], arr[random_index]
    
    # Use Lomuto partition on the modified array
    return partition_lomuto(arr, low, high)


def partition_lomuto(arr, low, high):
    """
    Lomuto Partition Scheme (helper for randomized version).
    
    Places the pivot element at high in its correct sorted position.
    
    Time Complexity: O(n)
    
    Args:
        arr (list): The array to partition
        low (int): Starting index
        high (int): Ending index (pivot element)
    
    Returns:
        int: Index of the pivot in its final sorted position
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_randomized_median_of_three(arr, low=0, high=None):
    """
    Randomized Quicksort with Median-of-Three pivot selection.
    
    This variant selects the pivot as the median of three random elements,
    which further improves performance by reducing the chance of bad pivots.
    Includes tail recursion optimization to keep space complexity O(log n).
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n) with better constants
    - Worst case: O(n^2) - but extremely unlikely
    
    Space Complexity: 
    - O(log n) average due to tail recursion optimization
    - O(n) worst case without optimization (unlikely)
    
    Args:
        arr (list): The array to be sorted
        low (int): Starting index (default: 0)
        high (int): Ending index (default: len(arr) - 1)
    
    Returns:
        list: The sorted array (modified in-place)
    """
    if high is None:
        high = len(arr) - 1
    
    while low < high:
        pivot_index = partition_median_of_three(arr, low, high)
        
        # Tail recursion optimization: recurse on smaller partition first
        if pivot_index - low < high - pivot_index:
            # Left partition is smaller
            quicksort_randomized_median_of_three(arr, low, pivot_index - 1)
            low = pivot_index + 1  # Tail recursion on right
        else:
            # Right partition is smaller
            quicksort_randomized_median_of_three(arr, pivot_index + 1, high)
            high = pivot_index - 1  # Tail recursion on left
    
    return arr


def partition_median_of_three(arr, low, high):
    """
    Partition with median-of-three pivot selection.
    
    Selects three random elements and uses their median as the pivot.
    This reduces the chance of selecting a very bad pivot.
    
    Time Complexity: O(n)
    
    Args:
        arr (list): The array to partition
        low (int): Starting index
        high (int): Ending index
    
    Returns:
        int: Index of the pivot in its final sorted position
    """
    # Select three random indices
    idx1 = random.randint(low, high)
    idx2 = random.randint(low, high)
    idx3 = random.randint(low, high)
    
    # Find the median of three elements
    vals = [(arr[idx1], idx1), (arr[idx2], idx2), (arr[idx3], idx3)]
    vals.sort(key=lambda x: x[0])
    median_idx = vals[1][1]
    
    # Swap median to the end
    arr[median_idx], arr[high] = arr[high], arr[median_idx]
    
    # Perform Lomuto partition
    return partition_lomuto(arr, low, high)


# Statistics tracking for analysis
class QuicksortStats:
    """Helper class to track Quicksort statistics during execution."""
    
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.partitions = 0
    
    def reset(self):
        """Reset all counters."""
        self.comparisons = 0
        self.swaps = 0
        self.partitions = 0


def quicksort_randomized_with_stats(arr, low=0, high=None, stats=None):
    """
    Randomized Quicksort with statistics tracking and tail recursion optimization.
    
    Uses the same algorithm as quicksort_randomized but tracks
    the number of comparisons, swaps, and partition operations.
    Includes tail recursion optimization for better space efficiency.
    
    Args:
        arr (list): The array to be sorted
        low (int): Starting index (default: 0)
        high (int): Ending index (default: len(arr) - 1)
        stats (QuicksortStats): Statistics object to update
    
    Returns:
        list: The sorted array (modified in-place)
    """
    if stats is None:
        stats = QuicksortStats()
    
    if high is None:
        high = len(arr) - 1
    
    while low < high:
        stats.partitions += 1
        pivot_index = partition_random_with_stats(arr, low, high, stats)
        
        # Tail recursion optimization: recurse on smaller partition first
        if pivot_index - low < high - pivot_index:
            # Left partition is smaller
            quicksort_randomized_with_stats(arr, low, pivot_index - 1, stats)
            low = pivot_index + 1  # Tail recursion on right
        else:
            # Right partition is smaller
            quicksort_randomized_with_stats(arr, pivot_index + 1, high, stats)
            high = pivot_index - 1  # Tail recursion on left
    
    return arr


def partition_random_with_stats(arr, low, high, stats):
    """Partition with statistics tracking."""
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    stats.swaps += 1
    
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        stats.comparisons += 1
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            stats.swaps += 1
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    stats.swaps += 1
    return i + 1


if __name__ == "__main__":
    # Simple test cases
    test_arrays = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        [5, 2, 8, 1, 9],
        [1],
        [2, 1],
        [3, 2, 1, 5, 4],
        list(range(10, 0, -1)),  # Reverse sorted
        list(range(1, 6)),  # Already sorted
    ]
    
    print("Testing Randomized Quicksort:")
    print("-" * 50)
    for arr in test_arrays:
        original = arr.copy()
        result = quicksort_randomized(arr)
        print(f"Input:  {original}")
        print(f"Output: {result}")
        print(f"Sorted: {result == sorted(original)}\n")
    
    print("\nTesting Randomized Quicksort with Median-of-Three:")
    print("-" * 50)
    for arr in test_arrays:
        original = arr.copy()
        result = quicksort_randomized_median_of_three(arr)
        print(f"Input:  {original}")
        print(f"Output: {result}")
        print(f"Sorted: {result == sorted(original)}\n")
    
    # Test statistics tracking
    print("\nTesting Statistics Tracking:")
    print("-" * 50)
    test_arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    stats = QuicksortStats()
    quicksort_randomized_with_stats(test_arr, stats=stats)
    print(f"Array: [5, 2, 8, 1, 9, 3, 7, 4, 6]")
    print(f"Comparisons: {stats.comparisons}")
    print(f"Swaps: {stats.swaps}")
    print(f"Partitions: {stats.partitions}")
