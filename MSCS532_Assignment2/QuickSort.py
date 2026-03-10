"""
QuickSort Implementation - MSCS532 Assignment 2
Author: Gyan Tamang
Date: March 2026

This module implements various QuickSort algorithms including:
1. Basic QuickSort (extra space)
2. In-place QuickSort
3. Randomized QuickSort
4. QuickSort with different pivot strategies
"""

import random
import time
import sys
from typing import List, Callable

# Increase recursion limit for large arrays
sys.setrecursionlimit(10000)


def quick_sort_basic(arr: List[int]) -> List[int]:
    """
    Basic QuickSort implementation using extra space.
    
    Time Complexity: O(n log n) average, O(n^2) worst case
    Space Complexity: O(n) due to creating new lists
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list of integers
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort_basic(left) + middle + quick_sort_basic(right)


def partition(arr: List[int], low: int, high: int) -> int:
    """
    Partition function for in-place QuickSort using Lomuto partition scheme.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Final position of pivot element
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    In-place QuickSort implementation.
    
    Time Complexity: O(n log n) average, O(n^2) worst case
    Space Complexity: O(log n) due to recursion stack
    
    Args:
        arr: List of integers to sort (modified in-place)
        low: Starting index (default 0)
        high: Ending index (default len(arr) - 1)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)


def partition_randomized(arr: List[int], low: int, high: int) -> int:
    """
    Randomized partition function that selects a random pivot.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Final position of pivot element
    """
    
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    
    return partition(arr, low, high)


def quick_sort_randomized(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    Randomized QuickSort implementation.
    
    Time Complexity: O(n log n) expected for all cases
    Space Complexity: O(log n) due to recursion stack
    
    Args:
        arr: List of integers to sort (modified in-place)
        low: Starting index (default 0)
        high: Ending index (default len(arr) - 1)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition_randomized(arr, low, high)
        quick_sort_randomized(arr, low, pi - 1)
        quick_sort_randomized(arr, pi + 1, high)


def partition_median_of_three(arr: List[int], low: int, high: int) -> int:
    """
    Partition using median-of-three pivot selection.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Final position of pivot element
    """
    mid = (low + high) // 2
    
    # Find median of arr[low], arr[mid], arr[high]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Place median at second-to-last position
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    
    pivot = arr[high - 1]
    i = low
    
    for j in range(low, high - 1):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    
    arr[i], arr[high - 1] = arr[high - 1], arr[i]
    return i


def quick_sort_median_of_three(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    QuickSort with median-of-three pivot selection.
    
    Time Complexity: O(n log n) average, better than standard pivot
    Space Complexity: O(log n) due to recursion stack
    
    Args:
        arr: List of integers to sort (modified in-place)
        low: Starting index (default 0)
        high: Ending index (default len(arr) - 1)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high and high - low >= 2:
        pi = partition_median_of_three(arr, low, high)
        quick_sort_median_of_three(arr, low, pi - 1)
        quick_sort_median_of_three(arr, pi + 1, high)
    elif low < high:
        # Use simple partition for small subarrays
        pi = partition(arr, low, high)
        quick_sort_median_of_three(arr, low, pi - 1)
        quick_sort_median_of_three(arr, pi + 1, high)


def measure_performance(sort_func: Callable, arr: List[int], name: str) -> tuple:
    """
    Measure the performance of a sorting function.
    
    Args:
        sort_func: Sorting function to test
        arr: List to sort
        name: Name of the sorting algorithm
        
    Returns:
        Tuple of (execution_time, sorted_array)
    """
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    
    if name == "basic":
        result = sort_func(arr_copy)
    else:
        sort_func(arr_copy)
        result = arr_copy
    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    return execution_time, result


def verify_sorted(arr: List[int]) -> bool:
    """
    Verify if an array is sorted in ascending order.
    
    Args:
        arr: List to verify
        
    Returns:
        True if sorted, False otherwise
    """
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def run_tests():
    """
    Run comprehensive tests on all QuickSort implementations.
    """
    print("=" * 80)
    print("QuickSort Implementation Tests - MSCS532 Assignment 2")
    print("=" * 80)
    
    # Test Case 1: Already sorted array
    print("\n1. Test Case: Already Sorted Array")
    test1 = list(range(1000))
    print(f"   Input size: {len(test1)}")
    
    time1, sorted1 = measure_performance(quick_sort_basic, test1, "basic")
    print(f"   Basic QuickSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(quick_sort_inplace, test1, "inplace")
    print(f"   In-place QuickSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(quick_sort_randomized, test1, "randomized")
    print(f"   Randomized QuickSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(quick_sort_median_of_three, test1, "median")
    print(f"   Median-of-Three QuickSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    # Test Case 2: Reverse sorted array
    print("\n2. Test Case: Reverse Sorted Array")
    test2 = list(range(1000, 0, -1))
    print(f"   Input size: {len(test2)}")
    
    time1, sorted1 = measure_performance(quick_sort_basic, test2, "basic")
    print(f"   Basic QuickSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(quick_sort_inplace, test2, "inplace")
    print(f"   In-place QuickSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(quick_sort_randomized, test2, "randomized")
    print(f"   Randomized QuickSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(quick_sort_median_of_three, test2, "median")
    print(f"   Median-of-Three QuickSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    # Test Case 3: Random array
    print("\n3. Test Case: Random Array")
    test3 = [random.randint(1, 10000) for _ in range(1000)]
    print(f"   Input size: {len(test3)}")
    
    time1, sorted1 = measure_performance(quick_sort_basic, test3, "basic")
    print(f"   Basic QuickSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(quick_sort_inplace, test3, "inplace")
    print(f"   In-place QuickSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(quick_sort_randomized, test3, "randomized")
    print(f"   Randomized QuickSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(quick_sort_median_of_three, test3, "median")
    print(f"   Median-of-Three QuickSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    # Test Case 4: Array with duplicates
    print("\n4. Test Case: Array with Many Duplicates")
    test4 = [random.randint(1, 10) for _ in range(1000)]
    print(f"   Input size: {len(test4)}")
    
    time1, sorted1 = measure_performance(quick_sort_basic, test4, "basic")
    print(f"   Basic QuickSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(quick_sort_inplace, test4, "inplace")
    print(f"   In-place QuickSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(quick_sort_randomized, test4, "randomized")
    print(f"   Randomized QuickSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(quick_sort_median_of_three, test4, "median")
    print(f"   Median-of-Three QuickSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    # Test Case 5: Small arrays
    print("\n5. Test Case: Small Arrays")
    test5_cases = [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 2, 8, 1, 9]
    ]
    
    for i, test5 in enumerate(test5_cases):
        print(f"   Test 5.{i+1}: {test5}")
        sorted_result = quick_sort_basic(test5.copy())
        print(f"   Result: {sorted_result} | Correct: {verify_sorted(sorted_result)}")
    
    # Performance Comparison
    print("\n" + "=" * 80)
    print("Performance Comparison on Large Random Array (5000 elements)")
    print("=" * 80)
    
    large_test = [random.randint(1, 100000) for _ in range(5000)]
    
    algorithms = [
        ("Basic QuickSort", quick_sort_basic, "basic"),
        ("In-place QuickSort", quick_sort_inplace, "inplace"),
        ("Randomized QuickSort", quick_sort_randomized, "randomized"),
        ("Median-of-Three QuickSort", quick_sort_median_of_three, "median")
    ]
    
    results = []
    for name, func, func_type in algorithms:
        exec_time, sorted_arr = measure_performance(func, large_test, func_type)
        results.append((name, exec_time, verify_sorted(sorted_arr)))
        print(f"{name:30s}: {exec_time:8.3f} ms | Correct: {verify_sorted(sorted_arr)}")
    
    print("\n" + "=" * 80)
    print("Analysis Summary:")
    print("=" * 80)
    print("""
Time Complexity:
- Best Case:    O(n log n) - when partition divides array evenly
- Average Case: O(n log n) - expected performance with random pivots
- Worst Case:   O(n²) - when partition is unbalanced (sorted/reverse sorted)

Space Complexity:
- Basic QuickSort:     O(n) - creates new lists at each recursion
- In-place QuickSort:  O(log n) - recursion stack only
- Randomized:          O(log n) - recursion stack only
- Median-of-Three:     O(log n) - recursion stack only

Key Observations:
1. Randomized QuickSort performs well on all input types
2. Median-of-Three strategy improves performance on sorted data
3. In-place versions use less memory than basic implementation
4. All versions correctly handle duplicates and edge cases
    """)


if __name__ == "__main__":
    run_tests()