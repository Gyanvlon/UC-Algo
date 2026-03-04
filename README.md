# MSCS532_Assignment1

## Insertion Sort Algorithm - Decreasing Order

This repository contains an implementation of the Insertion Sort algorithm that sorts arrays in monotonically decreasing order, as presented in Chapter 2 of "Introduction to Algorithms" by Cormen et al. (4th Edition).

## Algorithm Description

The Insertion Sort algorithm works by building a sorted portion of the array one element at a time. For decreasing order:
- Starting from the second element, each element is compared with the elements before it
- Elements smaller than the current element are shifted one position to the right
- The current element is inserted at its correct position

## Features

- **Insertion Sort Implementation**: Sorts arrays in decreasing (descending) order
- **Comprehensive Testing**: Multiple test cases including edge cases
- **Well-Documented**: Detailed comments explaining the algorithm
- **Time Complexity**: O(n²) worst case, O(n) best case
- **Space Complexity**: O(1) - sorts in place

## Usage

Run the program:
```bash
python insertion_sort.py
```

The program will execute all test cases and display the results.

## Test Cases

The implementation includes the following test cases:
1. Regular unsorted array
2. Already sorted array (best case)
3. Reverse sorted array (worst case)
4. Array with duplicate elements
5. Single element array

## Author

Created for MSCS532 - Analysis of Algorithms Course

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
