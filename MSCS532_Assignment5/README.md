# Quicksort Algorithm: Implementation and Analysis

## Overview

This repository contains a comprehensive implementation and analysis of the Quicksort algorithm, including both **deterministic** and **randomized** variants. The project includes detailed performance analysis, empirical testing, and a thorough report explaining the theoretical and practical aspects of Quicksort.

## Project Structure

```
.
├── quicksort.py                    # Deterministic Quicksort implementations
├── quicksort_randomized.py         # Randomized Quicksort implementations
├── empirical_analysis.py           # Performance testing and analysis
├── REPORT.md                       # Detailed analysis and findings
├── README.md                       # This file
└── requirements.txt                # Python dependencies (if needed)
```

## File Descriptions

### `quicksort.py`
**Deterministic implementations of Quicksort**

Contains:
- `quicksort_deterministic()` - Main implementation with Lomuto partition
- `partition_lomuto()` - Simple partition scheme (last element as pivot)
- `partition_hoare()` - Efficient partition scheme with two pointers
- `quicksort_hoare()` - Alternative implementation using Hoare partition

**Use Cases**:
- Understanding basic Quicksort algorithm
- When input is known to be random
- Comparing with randomized version

### `quicksort_randomized.py`
**Randomized implementations of Quicksort**

Contains:
- `quicksort_randomized()` - Basic randomized version
- `partition_random()` - Random pivot selection
- `quicksort_randomized_median_of_three()` - Enhanced version
- `partition_median_of_three()` - Median-of-three pivot selection
- `QuicksortStats` - Statistics tracking class
- `quicksort_randomized_with_stats()` - Version with operation counting

**Use Cases**:
- Production systems with unknown input
- Guaranteed expected O(n log n) performance
- Handling potentially adversarial input

### `empirical_analysis.py`
**Performance testing and empirical analysis**

Contains:
- `PerformanceTester` - Main testing class
- `test_correctness()` - Verifies all implementations
- `test_statistics()` - Analyzes operation counts
- `main()` - Runs comprehensive empirical tests

**Features**:
- Tests on different input sizes (100, 500, 1000, 5000)
- Tests on different distributions (random, sorted, reverse-sorted, nearly-sorted)
- Timing measurements using `time.perf_counter()`
- Multiple runs with statistics (min, max, average)
- Comparative analysis across all variants


## Installation and Setup

### Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd quicksort-analysis
   ```

2. **Verify Python installation**:
   ```bash
   python --version
   ```

3. **No additional installation needed** - all code uses Python standard library

---

## Usage

### 1. Test Individual Implementations

#### Test Deterministic Quicksort:
```bash
python quicksort.py
```

**Output**: Tests both Lomuto and Hoare partition schemes on sample arrays

#### Test Randomized Quicksort:
```bash
python quicksort_randomized.py
```

**Output**: Tests randomized variants and statistics tracking

### 2. Run Empirical Analysis

```bash
python empirical_analysis.py
```

This will:
1. **Verify Correctness**: Tests all implementations on various inputs
2. **Analyze Statistics**: Shows operation counts for different input sizes
3. **Performance Comparison**: Compares all variants on:
   - Random arrays
   - Sorted arrays
   - Reverse-sorted arrays
   - Nearly-sorted arrays
4. **Summary**: Provides comparative timing at each size

**Expected Runtime**: 30-60 seconds (depending on system)

#### Output Sections:

```
===================================================================
EMPIRICAL PERFORMANCE ANALYSIS: QUICKSORT VARIANTS
===================================================================

Testing Correctness of All Implementations
===========================================================
✓ All implementations are CORRECT!

STATISTICS ANALYSIS: OPERATION COUNTS
===================================================================
Size        Comparisons      Swaps              Partitions
...

EMPIRICAL PERFORMANCE ANALYSIS
...

SUMMARY COMPARISON
...
```

### 3. Use in Your Code

```python
from quicksort import quicksort_deterministic, quicksort_hoare
from quicksort_randomized import quicksort_randomized, quicksort_randomized_median_of_three

# Deterministic version
arr1 = [3, 1, 4, 1, 5, 9, 2, 6]
quicksort_deterministic(arr1)
print(arr1)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Randomized version  
arr2 = [3, 1, 4, 1, 5, 9, 2, 6]
quicksort_randomized(arr2)
print(arr2)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Randomized with median-of-three
arr3 = [3, 1, 4, 1, 5, 9, 2, 6]
quicksort_randomized_median_of_three(arr3)
print(arr3)  # [1, 1, 2, 3, 4, 5, 6, 9]
```

---

## API Reference

### `quicksort.quicksort_deterministic(arr, low=0, high=None)`

Sorts array using deterministic Quicksort with Lomuto partition.

**Parameters**:
- `arr` (list): Array to sort
- `low` (int): Starting index (default: 0)
- `high` (int): Ending index (default: len(arr)-1)

**Returns**: `list` - Sorted array (modified in-place)

**Time Complexity**:
- Best: O(n log n)
- Average: O(n log n)
- Worst: O(n²)

**Space Complexity**: O(log n) average, O(n) worst case

---

### `quicksort.quicksort_hoare(arr, low=0, high=None)`

Sorts array using Quicksort with Hoare partition (more efficient).

**Parameters**: Same as `quicksort_deterministic`

**Returns**: `list` - Sorted array (modified in-place)

**Advantages**: Fewer swaps, better cache behavior

---

### `quicksort_randomized.quicksort_randomized(arr, low=0, high=None)`

Sorts array using randomized Quicksort with random pivot selection.

**Parameters**: Same as `quicksort_deterministic`

**Returns**: `list` - Sorted array (modified in-place)

**Time Complexity**:
- Best: O(n log n)
- Average: **O(n log n) with high probability**
- Worst: **O(n log n) with high probability** (O(n²) exponentially unlikely)

**Space Complexity**: O(log n) average, O(n) worst case

---

### `quicksort_randomized.quicksort_randomized_median_of_three(arr, low=0, high=None)`

Enhanced randomized Quicksort using median-of-three pivot selection.

**Parameters**: Same as `quicksort_deterministic`

**Returns**: `list` - Sorted array (modified in-place)

**Advantages**: 
- Better pivot selection probability
- Faster in practice than basic randomized version
- Still maintains O(n log n) expected time

---

## Key Findings

### Performance on Different Input Distributions

| Distribution | Deterministic | Randomized | Winner |
|-------------|---------------|-----------|--------|
| Random | O(n log n) | O(n log n) | Tie |
| Sorted | **O(n²)** | **O(n log n)** | Randomized ✓ |
| Reverse-Sorted | **O(n²)** | **O(n log n)** | Randomized ✓ |
| Nearly-Sorted | O(n log n)* | O(n log n) | Deterministic* |

*Deterministic may have better constants on nearly-sorted data

### Key Insights

1. **Randomization Eliminates Worst Case**
   - Deterministic: O(n²) on structured input (sorted, reverse-sorted)
   - Randomized: Expected O(n log n) on ANY input

2. **Random Data Shows No Difference**
   - Both achieve O(n log n) on random input
   - Randomization overhead is minimal

3. **Practical Guarantees**
   - With randomization, worst-case probability < 10⁻³⁰⁰
   - Effectively impossible in practice
   - Safe to use in production systems

4. **Space Efficiency**
   - In-place sorting uses only O(log n) space
   - Better than Mergesort's required O(n)
   - Competitive with Heapsort

---

## Algorithm Comparison

### Quicksort vs Other Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Notes |
|-----------|------|---------|-------|-------|-------|
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | Fast in practice |
| Randomized QS | O(n log n) | O(n log n) | O(n log n)* | O(log n) | Guaranteed average |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Stable, predictable |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | In-place, stable |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Good for small n |

*With high probability; O(n²) exponentially unlikely

---

## Example Output

### Correctness Testing
```
Testing Correctness of All Implementations
===========================================================================
Test: random - [3, 1, 4, 1, 5, 9, 2, 6]
---------------------------------------------------------------------------
  Deterministic Quicksort               ✓ PASS
  Hoare Partition                       ✓ PASS
  Randomized Quicksort                  ✓ PASS
  Randomized (Median-of-3)              ✓ PASS
...
✓ All implementations are CORRECT!
```

### Performance on Sorted Data
```
Testing Deterministic (Lomuto) on Sorted data:
Size        Run 1 (s)       Run 2 (s)       Run 3 (s)       Avg (s)    
1000        0.015000        0.016000        0.015000        0.015333
5000        0.375000        0.378000        0.376000        0.376333  ← O(n²)
...

Testing Randomized on Sorted data:
Size        Run 1 (s)       Run 2 (s)       Run 3 (s)       Avg (s)    
1000        0.001000        0.001000        0.001000        0.001000
5000        0.005000        0.005200        0.005100        0.005100  ← O(n log n)
```

---

## Development and Testing

### Running Tests

```bash
# Test all implementations
python quicksort.py
python quicksort_randomized.py

# Run comprehensive analysis
python empirical_analysis.py

# Run with timing
time python empirical_analysis.py
```

### Adding Custom Test Cases

```python
from empirical_analysis import PerformanceTester

tester = PerformanceTester()

# Test on custom array
custom_array = [10, 3, 5, 2, 8, 1]
result = tester.measure_time(quicksort_randomized, custom_array)
print(f"Time: {result:.6f} seconds")

# Test on custom size with custom distribution
arr = tester.generate_random_array(10000)
results = tester.test_algorithm(
    "Custom Test", 
    quicksort_randomized, 
    lambda size: tester.generate_random_array(size),
    [10000],
    "custom"
)
```






