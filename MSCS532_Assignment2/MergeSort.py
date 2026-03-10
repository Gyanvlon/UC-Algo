"""
MergeSort Implementation - MSCS532 Assignment 2
Author: Gyan Tamang
Date: March 2026

This module implements various MergeSort algorithms including:
1. Basic MergeSort (extra space)
2. In-place MergeSort
3. Optimized MergeSort with insertion sort for small subarrays
4. Bottom-up (iterative) MergeSort
"""

import random
import time
import sys
from typing import List, Callable

# Increase recursion limit for large arrays
sys.setrecursionlimit(10000)


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merge two sorted arrays into a single sorted array.
    
    Time Complexity: O(n + m) where n, m are lengths of left and right
    Space Complexity: O(n + m) for result array
    
    Args:
        left: First sorted list
        right: Second sorted list
        
    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_basic(arr: List[int]) -> List[int]:
    """
    Basic MergeSort implementation using extra space.
    
    Time Complexity: O(n log n) for all cases
    Space Complexity: O(n) for temporary arrays
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list of integers
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    
    left = merge_sort_basic(arr[:mid])
    right = merge_sort_basic(arr[mid:])
    
    return merge(left, right)


def merge_inplace(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    Merge two sorted subarrays in-place.
    
    Args:
        arr: Array containing the subarrays
        left: Starting index of left subarray
        mid: Ending index of left subarray
        right: Ending index of right subarray
    """
    # Create temporary arrays
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


def merge_sort_inplace(arr: List[int], left: int = 0, right: int = None) -> None:
    """
    In-place MergeSort implementation.
    
    Time Complexity: O(n log n) for all cases
    Space Complexity: O(n) for temporary arrays during merge
    
    Args:
        arr: List of integers to sort (modified in-place)
        left: Starting index (default 0)
        right: Ending index (default len(arr) - 1)
    """
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        mid = (left + right) // 2
        
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        
        merge_inplace(arr, left, mid, right)


def insertion_sort(arr: List[int], left: int, right: int) -> None:
    """
    Insertion sort for small subarrays.
    
    Time Complexity: O(n²) but fast for small n
    Space Complexity: O(1)
    
    Args:
        arr: Array to sort
        left: Starting index
        right: Ending index
    """
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_sort_optimized(arr: List[int], left: int = 0, right: int = None, threshold: int = 10) -> None:
    """
    Optimized MergeSort that uses insertion sort for small subarrays.
    
    Time Complexity: O(n log n) for all cases
    Space Complexity: O(n) for temporary arrays
    
    Args:
        arr: List of integers to sort (modified in-place)
        left: Starting index (default 0)
        right: Ending index (default len(arr) - 1)
        threshold: Size threshold for switching to insertion sort
    """
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        # Use insertion sort for small subarrays
        if right - left + 1 <= threshold:
            insertion_sort(arr, left, right)
        else:
            mid = (left + right) // 2
            
            merge_sort_optimized(arr, left, mid, threshold)
            merge_sort_optimized(arr, mid + 1, right, threshold)
            
            # Skip merge if already sorted
            if arr[mid] <= arr[mid + 1]:
                return
            
            merge_inplace(arr, left, mid, right)


def merge_sort_iterative(arr: List[int]) -> None:
    """
    Bottom-up iterative MergeSort implementation.
    
    Time Complexity: O(n log n) for all cases
    Space Complexity: O(n) for temporary arrays
    
    Args:
        arr: List of integers to sort (modified in-place)
    """
    n = len(arr)
    current_size = 1
    
    while current_size < n:
        left = 0
        
        while left < n:
            mid = min(left + current_size - 1, n - 1)
            right = min(left + 2 * current_size - 1, n - 1)
            
            if mid < right:
                merge_inplace(arr, left, mid, right)
            
            left += 2 * current_size
        
        current_size *= 2


def merge_sort_three_way(arr: List[int]) -> List[int]:
    """
    Three-way MergeSort that divides array into three parts.
    
    Time Complexity: O(n log₃ n) ≈ O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list of integers
    """
    if len(arr) <= 1:
        return arr
    
    # For small arrays, use two-way merge sort to avoid recursion issues
    if len(arr) == 2:
        return [arr[0], arr[1]] if arr[0] <= arr[1] else [arr[1], arr[0]]
    
    # Divide into three parts
    third = len(arr) // 3
    
    # Ensure we make progress by having at least one element in each split
    if third == 0:
        third = 1
    
    left = merge_sort_three_way(arr[:third])
    middle = merge_sort_three_way(arr[third:2*third])
    right = merge_sort_three_way(arr[2*third:])
    
    # Merge three sorted arrays
    return merge_three(left, middle, right)


def merge_three(left: List[int], middle: List[int], right: List[int]) -> List[int]:
    """
    Merge three sorted arrays into one.
    
    Args:
        left: First sorted list
        middle: Second sorted list
        right: Third sorted list
        
    Returns:
        Merged sorted list
    """
    result = []
    i = j = k = 0
    
    while i < len(left) and j < len(middle) and k < len(right):
        if left[i] <= middle[j] and left[i] <= right[k]:
            result.append(left[i])
            i += 1
        elif middle[j] <= left[i] and middle[j] <= right[k]:
            result.append(middle[j])
            j += 1
        else:
            result.append(right[k])
            k += 1
    
    # Merge remaining two arrays
    while i < len(left) and j < len(middle):
        if left[i] <= middle[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(middle[j])
            j += 1
    
    while i < len(left) and k < len(right):
        if left[i] <= right[k]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[k])
            k += 1
    
    while j < len(middle) and k < len(right):
        if middle[j] <= right[k]:
            result.append(middle[j])
            j += 1
        else:
            result.append(right[k])
            k += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(middle[j:])
    result.extend(right[k:])
    
    return result


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
    
    if name in ["basic", "three_way"]:
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
    Run comprehensive tests on all MergeSort implementations.
    """
    print("=" * 80)
    print("MergeSort Implementation Tests - MSCS532 Assignment 2")
    print("=" * 80)
    
    # Test Case 1: Already sorted array
    print("\n1. Test Case: Already Sorted Array")
    test1 = list(range(1000))
    print(f"   Input size: {len(test1)}")
    
    time1, sorted1 = measure_performance(merge_sort_basic, test1, "basic")
    print(f"   Basic MergeSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(merge_sort_inplace, test1, "inplace")
    print(f"   In-place MergeSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(merge_sort_optimized, test1, "optimized")
    print(f"   Optimized MergeSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(merge_sort_iterative, test1, "iterative")
    print(f"   Iterative MergeSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    time5, sorted5 = measure_performance(merge_sort_three_way, test1, "three_way")
    print(f"   Three-way MergeSort: {time5:.3f} ms | Correct: {verify_sorted(sorted5)}")
    
    # Test Case 2: Reverse sorted array
    print("\n2. Test Case: Reverse Sorted Array")
    test2 = list(range(1000, 0, -1))
    print(f"   Input size: {len(test2)}")
    
    time1, sorted1 = measure_performance(merge_sort_basic, test2, "basic")
    print(f"   Basic MergeSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(merge_sort_inplace, test2, "inplace")
    print(f"   In-place MergeSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(merge_sort_optimized, test2, "optimized")
    print(f"   Optimized MergeSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(merge_sort_iterative, test2, "iterative")
    print(f"   Iterative MergeSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    time5, sorted5 = measure_performance(merge_sort_three_way, test2, "three_way")
    print(f"   Three-way MergeSort: {time5:.3f} ms | Correct: {verify_sorted(sorted5)}")
    
    # Test Case 3: Random array
    print("\n3. Test Case: Random Array")
    test3 = [random.randint(1, 10000) for _ in range(1000)]
    print(f"   Input size: {len(test3)}")
    
    time1, sorted1 = measure_performance(merge_sort_basic, test3, "basic")
    print(f"   Basic MergeSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(merge_sort_inplace, test3, "inplace")
    print(f"   In-place MergeSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(merge_sort_optimized, test3, "optimized")
    print(f"   Optimized MergeSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(merge_sort_iterative, test3, "iterative")
    print(f"   Iterative MergeSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    time5, sorted5 = measure_performance(merge_sort_three_way, test3, "three_way")
    print(f"   Three-way MergeSort: {time5:.3f} ms | Correct: {verify_sorted(sorted5)}")
    
    # Test Case 4: Array with duplicates
    print("\n4. Test Case: Array with Many Duplicates")
    test4 = [random.randint(1, 10) for _ in range(1000)]
    print(f"   Input size: {len(test4)}")
    
    time1, sorted1 = measure_performance(merge_sort_basic, test4, "basic")
    print(f"   Basic MergeSort: {time1:.3f} ms | Correct: {verify_sorted(sorted1)}")
    
    time2, sorted2 = measure_performance(merge_sort_inplace, test4, "inplace")
    print(f"   In-place MergeSort: {time2:.3f} ms | Correct: {verify_sorted(sorted2)}")
    
    time3, sorted3 = measure_performance(merge_sort_optimized, test4, "optimized")
    print(f"   Optimized MergeSort: {time3:.3f} ms | Correct: {verify_sorted(sorted3)}")
    
    time4, sorted4 = measure_performance(merge_sort_iterative, test4, "iterative")
    print(f"   Iterative MergeSort: {time4:.3f} ms | Correct: {verify_sorted(sorted4)}")
    
    time5, sorted5 = measure_performance(merge_sort_three_way, test4, "three_way")
    print(f"   Three-way MergeSort: {time5:.3f} ms | Correct: {verify_sorted(sorted5)}")
    
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
        sorted_result = merge_sort_basic(test5.copy())
        print(f"   Result: {sorted_result} | Correct: {verify_sorted(sorted_result)}")
    
    # Performance Comparison
    print("\n" + "=" * 80)
    print("Performance Comparison on Large Random Array (5000 elements)")
    print("=" * 80)
    
    large_test = [random.randint(1, 100000) for _ in range(5000)]
    
    algorithms = [
        ("Basic MergeSort", merge_sort_basic, "basic"),
        ("In-place MergeSort", merge_sort_inplace, "inplace"),
        ("Optimized MergeSort", merge_sort_optimized, "optimized"),
        ("Iterative MergeSort", merge_sort_iterative, "iterative"),
        ("Three-way MergeSort", merge_sort_three_way, "three_way")
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
- Best Case:    O(n log n) - consistent performance regardless of input
- Average Case: O(n log n) - always divides array evenly
- Worst Case:   O(n log n) - no degradation like QuickSort

Space Complexity:
- Basic MergeSort:     O(n) - creates new lists at each level
- In-place MergeSort:  O(n) - temporary arrays during merge
- Optimized MergeSort: O(n) - same as in-place but faster
- Iterative MergeSort: O(n) - no recursion stack needed
- Three-way MergeSort: O(n) - similar to basic version

Key Observations:
1. MergeSort guarantees O(n log n) time complexity in all cases
2. Stable sorting algorithm - preserves relative order of equal elements
3. Optimized version with insertion sort improves performance on small arrays
4. Iterative version avoids recursion overhead
5. Three-way version reduces depth of recursion tree
6. Better than QuickSort for linked lists and guaranteed performance
7. Requires additional space, unlike in-place QuickSort

Advantages over QuickSort:
- Guaranteed O(n log n) performance (no worst case O(n²))
- Stable sorting (maintains relative order of equal elements)
- Predictable performance for worst-case scenarios
- Better for external sorting (sorting data that doesn't fit in memory)

Disadvantages compared to QuickSort:
- Requires O(n) extra space
- Slower than QuickSort on average for arrays in memory
- More complex to implement true in-place version
    """)


if __name__ == "__main__":
    run_tests()