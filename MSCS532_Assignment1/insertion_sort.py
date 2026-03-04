def insertion_sort_decreasing(arr):
  
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] < key:
            arr[i + 1] = arr[i]
            i = i - 1
        arr[i + 1] = key
    return arr


def test_insertion_sort():
    
    # Test case 1: Regular array
    test1 = [5, 2, 4, 6, 1, 3]
    print(f"Test 1 - Original: {test1}")
    result1 = insertion_sort_decreasing(test1.copy())
    print(f"Test 1 - Sorted:   {result1}")
    print(f"Expected: [6, 5, 4, 3, 2, 1]\n")
    
    # Test case 2: Already sorted in decreasing order
    test2 = [9, 7, 5, 3, 1]
    print(f"Test 2 - Original: {test2}")
    result2 = insertion_sort_decreasing(test2.copy())
    print(f"Test 2 - Sorted:   {result2}")
    print(f"Expected: [9, 7, 5, 3, 1]\n")
    
    # Test case 3: Sorted in increasing order (worst case)
    test3 = [1, 2, 3, 4, 5]
    print(f"Test 3 - Original: {test3}")
    result3 = insertion_sort_decreasing(test3.copy())
    print(f"Test 3 - Sorted:   {result3}")
    print(f"Expected: [5, 4, 3, 2, 1]\n")
    
    # Test case 4: Array with duplicates
    test4 = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Test 4 - Original: {test4}")
    result4 = insertion_sort_decreasing(test4.copy())
    print(f"Test 4 - Sorted:   {result4}")
    print(f"Expected: [9, 6, 5, 4, 3, 2, 1, 1]\n")
    
    # Test case 5: Single element
    test5 = [42]
    print(f"Test 5 - Original: {test5}")
    result5 = insertion_sort_decreasing(test5.copy())
    print(f"Test 5 - Sorted:   {result5}")
    print(f"Expected: [42]\n")


if __name__ == "__main__":
    test_insertion_sort()
