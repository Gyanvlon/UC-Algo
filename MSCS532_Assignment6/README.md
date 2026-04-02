# MSCS532 Assignment 6

Medians and Order Statistics & Elementary Data Structures

## Repository Contents

- `src/selection.py`  
  Deterministic (Median of Medians) and Randomized Quickselect implementations.
- `src/data_structures.py`  
  Implementations of dynamic array, matrix, stack, queue, linked list, and optional rooted tree.
- `benchmarks/selection_benchmark.py`  
  Empirical runtime comparison for selection algorithms.
- `main.py`  
 
## Requirements

- Python 3.10+
- No third-party dependencies required

## How to Run

### 1) Run sanity/demo code

```bash
python main.py
```

### 2) Run selection benchmark

```bash
python -m benchmarks.selection_benchmark --sizes 1000 5000 10000 20000 --trials 5
```

Benchmark output is also written to:

- `results/selection_benchmark_results.csv`

## Notes on Algorithms

### Part 1

- `deterministic_select(values, k)`:
  - Worst-case $O(n)$ time
  - Uses Median of Medians pivoting
- `randomized_select(values, k)`:
  - Expected $O(n)$ time
  - Worst-case $O(n^2)$, but usually very fast in practice

Both functions:
- use 1-based `k`
- support duplicate values correctly via 3-way partitioning

### Part 2

Implemented structures and operations include:
- Dynamic arrays and matrices
- Array-based stacks and queues
- Singly linked lists
- Optional rooted tree nodes


