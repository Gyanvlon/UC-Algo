"""
Deterministic Quicksort Implementation

This module provides a deterministic implementation of the Quicksort algorithm
using the Lomuto partition scheme where the pivot is always the last element
in the subarray.

Author: Assignment 5
Date: 2026
"""

def quicksort_deterministic(arr, low=0, high=None):
    """
    Deterministic Quicksort: sorts array in-place using last element as pivot.
    
    Time Complexity:
    - Best case: O(n log n) - when pivot divides array into two equal halves
    - Average case: O(n log n) - random distributed pivots
    - Worst case: O(n^2) - when pivot is always smallest or largest element
    
    Space Complexity:
    - O(log n) average due to recursion stack depth (tail recursion optimization)
    - O(n) worst case without tail recursion optimization
    
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
        # Partition and get the pivot index
        pivot_index = partition_lomuto(arr, low, high)
        
        # Tail recursion optimization: recurse on smaller partition first
        # This keeps the recursion stack height at O(log n) in most cases
        if pivot_index - low < high - pivot_index:
            # Left partition is smaller
            quicksort_deterministic(arr, low, pivot_index - 1)
            low = pivot_index + 1  # Tail recursion on right
        else:
            # Right partition is smaller (or equal)
            quicksort_deterministic(arr, pivot_index + 1, high)
            high = pivot_index - 1  # Tail recursion on left
    
    return arr


def partition_lomuto(arr, low, high):
    """
    Lomuto Partition Scheme: uses last element as pivot.
    
    This partition scheme is simpler to understand than Hoare's partition.
    It places the pivot element in its correct sorted position and returns
    the pivot's index.
    
    Time Complexity: O(n) where n = high - low + 1
    
    Args:
        arr (list): The array to partition
        low (int): Starting index
        high (int): Ending index (pivot element)
    
    Returns:
        int: Index of the pivot in its final sorted position
    """
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1  # Index of smaller element
    
    # Traverse through all elements, compare with pivot
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap
    
    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def partition_hoare(arr, low, high):
    """
    Hoare Partition Scheme: uses first element as pivot.
    
    This scheme is more efficient than Lomuto's as it performs fewer swaps
    on average. It uses two pointers moving towards each other.
    
    Time Complexity: O(n) where n = high - low + 1
    
    Args:
        arr (list): The array to partition
        low (int): Starting index (pivot element)
        high (int): Ending index
    
    Returns:
        int: Approximate partition point (left pointer position)
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Find leftmost element greater than or equal to pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        
        # Find rightmost element smaller than or equal to pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        # If pointers crossed, partition is done
        if i >= j:
            return j
        
        # Swap elements at i and j
        arr[i], arr[j] = arr[j], arr[i]


def quicksort_hoare(arr, low=0, high=None):
    """
    Quicksort using Hoare's partition scheme with tail recursion optimization.
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n) 
    - Worst case: O(n^2)
    
    Space Complexity: 
    - O(log n) average due to tail recursion optimization
    - O(n) worst case without optimization
    
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
        # Partition using Hoare's scheme
        p = partition_hoare(arr, low, high)
        
        # Tail recursion optimization: recurse on smaller partition first
        if p - low < high - p:
            # Left partition is smaller
            quicksort_hoare(arr, low, p)
            low = p + 1  # Tail recursion on right
        else:
            # Right partition is smaller
            quicksort_hoare(arr, p + 1, high)
            high = p  # Tail recursion on left
    
    return arr


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
    
    print("Testing Deterministic Quicksort (Lomuto Partition):")
    print("-" * 50)
    for arr in test_arrays:
        original = arr.copy()
        result = quicksort_deterministic(arr)
        print(f"Input:  {original}")
        print(f"Output: {result}")
        print(f"Sorted: {result == sorted(original)}\n")
    
    print("\nTesting Quicksort with Hoare Partition:")
    print("-" * 50)
    for arr in test_arrays:
        original = arr.copy()
        result = quicksort_hoare(arr)
        print(f"Input:  {original}")
        print(f"Output: {result}")
        print(f"Sorted: {result == sorted(original)}\n")
