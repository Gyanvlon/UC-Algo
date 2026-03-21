# MSCS532 Assignment 3

This repository contains implementations and analysis for:

- Randomized Quicksort vs Deterministic Quicksort (first pivot)
- Hash Table with Chaining

## Files

- `RandomizedQuicksort.py`: Randomized and deterministic quicksort implementations.
- `benchmark_quicksort.py`: Empirical runtime comparison across required distributions.
- `HashTableChaining.py`: Hash table with chaining, universal-hash-style compression, and dynamic resizing.
- `Assignment3_Report.md`: Theoretical analysis, experiment design, and discussion template.

## Requirements

- Python 3.9+

## How to run

### 1. Run quicksort benchmark

```bash
python benchmark_quicksort.py
```

This prints benchmark results and writes:

- `quicksort_benchmark_results.csv`

### 2. Run quicksort module demo

```bash
python RandomizedQuicksort.py
```

### 3. Run hash table demo

```bash
python HashTableChaining.py
```

## Summary of findings (theory)

- Randomized quicksort has expected $O(n\log n)$ time.
- Deterministic first-pivot quicksort can degrade toward $O(n^2)$ on sorted or reverse-sorted inputs.
- Chaining hash tables provide expected $O(1)$ insert/search/delete when load factor is kept bounded (via resizing).
