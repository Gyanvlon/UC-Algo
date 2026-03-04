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
    
    test1 = [5, 2, 4, 6, 1, 3]
    print(f"Test 1 - Original: {test1}")
    result1 = insertion_sort_decreasing(test1.copy())
    print(f"Test 1 - Sorted:   {result1}")
    print(f"Expected: [6, 5, 4, 3, 2, 1]\n")
    
   

if __name__ == "__main__":
    test_insertion_sort()
