# MSCS 532 – Assignment 4 Report
## Heap Data Structures: Implementation, Analysis, and Applications

**Course:** MSCS 532 – Algorithm Design and Analysis  
**Date:** March 16, 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)  
2. [Part 1 – Heapsort](#2-part-1--heapsort)  
   - 2.1 [Algorithm Description](#21-algorithm-description)  
   - 2.2 [Implementation Details](#22-implementation-details)  
   - 2.3 [Time Complexity Analysis](#23-time-complexity-analysis)  
   - 2.4 [Space Complexity](#24-space-complexity)  
   - 2.5 [Empirical Comparison](#25-empirical-comparison)  
   - 2.6 [Discussion of Results](#26-discussion-of-results)  
3. [Part 2 – Priority Queue](#3-part-2--priority-queue)  
   - 3.1 [Design Choices](#31-design-choices)  
   - 3.2 [Task Class](#32-task-class)  
   - 3.3 [Core Operations and Complexity](#33-core-operations-and-complexity)  
   - 3.4 [Scheduler Simulation](#34-scheduler-simulation)  
4. [Conclusion](#4-conclusion)  
5. [References](#5-references)

---

## 1. Executive Summary

This report covers the implementation and analysis of two heap-based systems:

1. **Heapsort** – an in-place, array-based sorting algorithm using a max-heap that achieves guaranteed O(n log n) time in all cases with O(1) auxiliary space.
2. **Priority Queue** – an array-backed max-heap priority queue supporting O(log n) insert, extract-max, increase-key, and decrease-key, demonstrated through a task-scheduler simulation.

Empirical benchmarks on five input distributions (random, sorted, reverse-sorted, nearly-sorted, many-duplicates) across sizes up to n = 30,000 confirm the theoretical complexity predictions and reveal important practical tradeoffs between Heapsort, Quicksort, and Merge Sort.

---

## 2. Part 1 – Heapsort

### 2.1 Algorithm Description

Heapsort sorts an array in two phases using a **max-heap** — a nearly complete binary tree stored implicitly in an array, satisfying the invariant that every parent is ≥ its children.

**Phase 1 — Build Max-Heap (O(n))**

Call `heapify` on every internal node starting from the last (index `n//2 − 1`) and working toward the root. This bottom-up procedure converts the array into a valid max-heap.

**Phase 2 — Repeated Extraction (O(n log n))**

For `i = n−1` down to `1`:
1. Swap `arr[0]` (the current maximum) with `arr[i]` — placing the maximum in its final sorted position.
2. Shrink the logical heap size to `i`.
3. Call `heapify(arr, i, 0)` to restore the max-heap property.

After n−1 such steps, the array is sorted in ascending order.

**Array representation of the heap**

For a node at index `i` (0-based):
- Left child  : `2i + 1`
- Right child : `2i + 2`
- Parent      : `(i − 1) // 2`

This mapping gives O(1) random access to any node with no pointer overhead.

### 2.2 Implementation Details

The implementation in `heapsort.py` provides three functions:

| Function | Purpose |
|---|---|
| `heapify(arr, n, i)` | Restore heap property at root `i` for heap of size `n` |
| `build_max_heap(arr)` | Bottom-up heap construction in O(n) |
| `heapsort(arr)` | Full sort (in-place); returns the same list |

**Key implementation decision – iterative `heapify`:**  
The standard textbook `heapify` is recursive with depth proportional to tree height (O(log n)). Our implementation converts this to an explicit `while` loop, keeping call-stack depth _constant_ (O(1)) regardless of input size. This avoids Python's default recursion limit and reduces function-call overhead.

```
def heapify(arr, n, i):
    while True:
        largest = i
        left, right = 2*i + 1, 2*i + 2
        if left  < n and arr[left]  > arr[largest]: largest = left
        if right < n and arr[right] > arr[largest]: largest = right
        if largest == i: break
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest
```

### 2.3 Time Complexity Analysis

#### Phase 1 – `build_max_heap` is O(n)

A common misconception is that building the heap takes O(n log n) because we call heapify n/2 times and each heapify is O(log n). The actual bound is tighter.

Let h = ⌊log₂ n⌋ be the height of the heap. A node at height k (counted from leaves) has at most ⌈n / 2^(k+1)⌉ nodes, and heapifying a subtree of height k costs O(k). The total work is:

$$T_{\text{build}} = \sum_{k=0}^{h} \left\lceil \frac{n}{2^{k+1}} \right\rceil \cdot O(k) \leq n \sum_{k=0}^{\infty} \frac{k}{2^k} = n \cdot 2 = O(n)$$

The geometric series $\sum_{k=0}^{\infty} k / 2^k = 2$ converges, confirming the O(n) build.

#### Phase 2 – Extraction loop is O(n log n)

We perform n−1 extractions. The i-th extraction calls `heapify` on a heap of size i, costing O(log i). Summing:

$$T_{\text{extract}} = \sum_{i=2}^{n} O(\log i) = O\!\left(\sum_{i=2}^{n} \log i\right) = O(\log(n!)) = O(n \log n)$$

by Stirling's approximation: $\log(n!) = \sum_{i=1}^{n} \log i \approx n \log n - n \log e = \Theta(n \log n)$.

#### Why O(n log n) in **all** cases

Heapsort is unusual in that its best, average, and worst-case time complexity are all **Θ(n log n)**:

- **Best case (already sorted input):** Build-max-heap still costs O(n). The extraction phase still performs n−1 heapify calls, each pushing the placed root down O(log n) levels before it finds its place. There is no short-circuit. Empirical data confirms this: at n = 30,000 the sorted-input time (97.9 ms) is virtually identical to random-input time (98.3 ms).
  
- **Worst case:** No specific permutation triggers dramatically worse behavior. The heap tree is always balanced (a complete binary tree), so heapify always costs exactly O(log n).

- **Average case:** By the same argument — the heap structure is independent of the input distribution, so average cost = O(n log n).

This distinguishes Heapsort from Quicksort (O(n²) worst case) and gives it an absolute guarantee not available from comparison sorts like Quicksort or Insertion Sort.

#### Comparison of lower bound

The information-theoretic lower bound for comparison-based sorting is Ω(n log n). Heapsort achieves this bound in all cases, making it **asymptotically optimal** among comparison sorts.

### 2.4 Space Complexity

| Component | Space |
|---|---|
| Input array | O(n) (required regardless of algorithm) |
| Auxiliary (local variables in heapify) | O(1) with iterative implementation |
| Call stack (recursive heapify) | O(log n) — **eliminated** by our iterative version |
| **Total auxiliary** | **O(1)** |

Heapsort achieves **in-place** sorting — the only comparison sort to guarantee both O(n log n) time and O(1) auxiliary space simultaneously. Merge Sort requires O(n) extra space; Quicksort requires O(log n) stack space on average.

### 2.5 Empirical Comparison

All timings below are in **milliseconds**, reporting the **minimum** of 5 independent trials (seed = 42 for reproducibility). Machine: Windows, Python 3.x; algorithms are pure-Python implementations.

Algorithms compared:
- **Heapsort** — `heapsort.py` (this implementation)
- **Quicksort** — in-place with randomised pivot
- **Merge Sort** — top-down, returns new list

#### Distribution: Random (uniformly random integers in [0, 10n])

| n | Heapsort (ms) | Quicksort (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 100 | 0.146 | 0.135 | 0.160 |
| 500 | 0.892 | 0.550 | 0.894 |
| 1,000 | 1.996 | 1.316 | 2.032 |
| 5,000 | 12.411 | 7.053 | 12.202 |
| 10,000 | 27.650 | 16.196 | 25.216 |
| 30,000 | 98.267 | 53.690 | 89.049 |

#### Distribution: Sorted (ascending)

| n | Heapsort (ms) | Quicksort (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 100 | 0.115 | 0.082 | 0.101 |
| 500 | 0.833 | 0.518 | 0.633 |
| 1,000 | 2.051 | 1.339 | 1.473 |
| 5,000 | 13.486 | 7.860 | 7.703 |
| 10,000 | 29.596 | 15.601 | 16.440 |
| 30,000 | 97.854 | 50.891 | 52.476 |

#### Distribution: Reverse-Sorted (descending)

| n | Heapsort (ms) | Quicksort (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 100 | 0.097 | 0.080 | 0.110 |
| 500 | 0.699 | 0.752 | 0.660 |
| 1,000 | 1.714 | 1.181 | 1.396 |
| 5,000 | 11.918 | 7.210 | 7.840 |
| 10,000 | 26.010 | 16.218 | 16.988 |
| 30,000 | 88.647 | 53.128 | 54.568 |

#### Distribution: Nearly Sorted (~2% positions swapped)

| n | Heapsort (ms) | Quicksort (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 100 | 0.115 | 0.077 | 0.113 |
| 500 | 0.900 | 0.552 | 0.739 |
| 1,000 | 1.995 | 1.251 | 1.685 |
| 5,000 | 13.657 | 7.141 | 9.969 |
| 10,000 | 29.313 | 15.674 | 21.362 |
| 30,000 | 100.680 | 51.778 | 72.956 |

#### Distribution: Many Duplicates (values in [0, n//100])

| n | Heapsort (ms) | Quicksort (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 100 | 0.066 | 0.222 | 0.120 |
| 500 | 0.688 | 2.016 | 0.875 |
| 1,000 | 1.770 | 4.809 | 1.875 |
| 5,000 | 11.621 | 28.122 | 11.568 |
| 10,000 | 26.699 | 59.812 | 25.184 |
| 30,000 | 93.312 | 190.156 | 88.288 |

### 2.6 Discussion of Results

#### Finding 1 — Quicksort leads on most distributions

Randomised Quicksort is the fastest on random, sorted, reverse-sorted, and nearly-sorted inputs. At n = 30,000 on random data, Quicksort (53.7 ms) is roughly **1.8× faster** than Heapsort (98.3 ms) and **1.6× faster** than Merge Sort (89.0 ms).

This is explained by superior **cache locality**: Quicksort's partition step scans the array linearly and performs fewer memory accesses per comparison. Heapsort's heapify jumps between distant indices (parent ↔ child at distance ~n/2), causing more cache misses. This is a well-known practical weakness of Heapsort despite its equal asymptotic complexity.

#### Finding 2 — Heapsort is completely insensitive to input order

The Heapsort times across random, sorted, reverse-sorted, and nearly-sorted distributions are nearly identical for the same n. At n = 30,000:

| Distribution | Heapsort | Quicksort | Merge Sort |
|---|---:|---:|---:|
| random | 98.3 ms | 53.7 ms | 89.0 ms |
| sorted | 97.9 ms | 50.9 ms | 52.5 ms |
| reverse_sorted | 88.6 ms | 53.1 ms | 54.6 ms |
| nearly_sorted | 100.7 ms | 51.8 ms | 73.0 ms |

Variation across Heapsort rows: **< 12 ms (~12%)** — a direct empirical confirmation that Heapsort's O(n log n) guarantee is uniform across all orderings.

Merge Sort exploits sorted/partially-sorted structure through fewer comparisons in the merge step, achieving ~52 ms on sorted vs. ~89 ms on random. The "nearly sorted" case is intermediate (73 ms) because the merge occasionally has to compare elements across the boundary introduced by the ~2% swaps.

#### Finding 3 — Quicksort degrades severely on many-duplicates (critical weakness)

This is the most striking finding. With many duplicates, the two-way partition scheme places all equal-to-pivot elements on one side, creating highly unbalanced partitions and approaching O(n²) behavior:

| n | Heapsort | Quicksort | Slowdown factor |
|---:|---:|---:|---:|
| 100 | 0.066 ms | 0.222 ms | **3.4×** |
| 1,000 | 1.770 ms | 4.809 ms | **2.7×** |
| 10,000 | 26.7 ms | 59.8 ms | **2.2×** |
| 30,000 | 93.3 ms | 190.2 ms | **2.0×** |

At n = 30,000, Quicksort takes **190 ms** — more than **2× slower** than both Heapsort (93 ms) and Merge Sort (88 ms). Heapsort is completely immune to this pathology because heap structure is determined only by the comparison result, not by value distribution.

> **Note:** A three-way partition (Dutch National Flag / fat-pivot) Quicksort would resolve this weakness, reducing many-duplicates to O(n) in the extreme case. Our comparison uses a standard two-way partition for a fair and educational contrast.

#### Finding 4 — Merge Sort is a middle ground

Merge Sort consistently performs between Quicksort (fast, unstable on edge cases) and Heapsort (slower but uniform). Its O(n) auxiliary space is a real-world cost that the benchmark does not fully capture.

#### Summary table: algorithm trade-offs

| Property | Heapsort | Quicksort (random pivot) | Merge Sort |
|---|---|---|---|
| Worst-case time | **O(n log n)** | O(n²) | **O(n log n)** |
| Average-case time | O(n log n) | **O(n log n)** | O(n log n) |
| Auxiliary space | **O(1)** | O(log n) avg | O(n) |
| Stable sort | No | No | **Yes** |
| Cache-friendly | Poor | **Good** | Moderate |
| Many-duplicates | **Robust** | Degrades | Moderate |
| Adaptive (sorted input) | No | Partial | **Yes** |

---

## 3. Part 2 – Priority Queue

### 3.1 Design Choices

#### Data Structure: Array-Based Binary Heap

A Python `list` is used as the underlying array for the heap. The choice is justified by:

1. **O(1) random access** — moving to parent or child is pure arithmetic; no pointer traversal.
2. **Memory compactness** — no per-node pointers; all data is stored contiguously, improving cache performance.
3. **Simple index arithmetic:**
   - Parent of node at `i` : `(i-1) // 2`
   - Left child            : `2i + 1`
   - Right child           : `2i + 2`
4. **Dynamic resizing** — Python lists grow automatically, giving O(1) amortised append.

Alternative considered: a pointer-based binary tree would be equally correct but adds per-node overhead (left/right pointers) and loses cache locality. For this use case the array representation is strictly superior.

#### Heap Orientation: Max-Heap

A **max-heap** was chosen (highest priority value → served first). This maps naturally to scenarios where higher numeric priority indicates greater urgency (e.g., an emergency alert with priority 10 runs before a batch job at priority 2).

A min-heap (`MinHeapPriorityQueue`) is also implemented via priority negation for use cases where lower numeric value means higher urgency (e.g., deadline-first scheduling where deadline = 2.0 is more urgent than deadline = 10.0).

#### O(1) Task Lookup via Auxiliary Dictionary

To support efficient `increase_key` and `decrease_key`, the implementation maintains a secondary dict `_index: {task_id → heap_position}`. Without this, locating a task would require O(n) linear scan, making both key-change operations O(n). With the dict, lookup is O(1), and the full operation remains O(log n).

The dict is kept consistent with every swap via the `_swap()` helper, which updates both entries before touching the array.

### 3.2 Task Class

```python
@dataclass
class Task:
    task_id:      str | int   # Unique identifier
    priority:     float       # Numeric priority (higher = more urgent)
    arrival_time: float       # Simulation timestamp of submission
    deadline:     float|None  # Optional absolute deadline
    description:  str         # Human-readable label
```

Using a `@dataclass` provides automatic `__init__`, equality comparison, and a clean `__repr__`. The `task_id` field is the unique key used in the index dictionary. Storing `arrival_time` and `deadline` enables simulation of deadline-aware scheduling policies.

### 3.3 Core Operations and Complexity

#### `insert(task)` — O(log n)

1. Validate `task_id` uniqueness — O(1).
2. Append to end of heap array — O(1) amortised.
3. Record position in `_index` — O(1).
4. Call `_sift_up` from the new element — O(log n).

**Why O(log n):** A newly inserted element may be larger than its parent. `_sift_up` repeatedly swaps the element with its parent (at index `(i-1)//2`) until the heap property is satisfied or the root is reached. The maximum number of swaps equals the height of the heap, which is ⌊log₂ n⌋.

```
_sift_up(idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if heap[idx].priority > heap[parent].priority:
            swap(idx, parent); idx = parent
        else: break
```

#### `extract_max()` — O(log n)

1. Record the root task (the maximum) — O(1).
2. Move the last task to the root; shrink the array — O(1) amortised.
3. Call `_sift_down` from the root — O(log n).
4. Delete from `_index` — O(1).

**Why O(log n):** The displaced element placed at the root may be smaller than one or both children. `_sift_down` swaps it with the larger child at each level until `largest == idx`. The path length is bounded by the tree height ⌊log₂ n⌋.

```
_sift_down(idx):
    while True:
        largest = idx
        for child in [2*idx+1, 2*idx+2]:
            if child < n and heap[child].priority > heap[largest].priority:
                largest = child
        if largest == idx: break
        swap(idx, largest); idx = largest
```

#### `increase_key(task_id, new_priority)` — O(log n)

1. Look up position via `_index` — O(1).
2. Validate new_priority ≥ current — O(1).
3. Update priority in-place — O(1).
4. Call `_sift_up` — O(log n).

The key insight: increasing a priority can only cause a violation upward (element becomes larger than its parent), so only sifting up is needed.

#### `decrease_key(task_id, new_priority)` — O(log n)

1. Look up position via `_index` — O(1).
2. Validate new_priority ≤ current — O(1).
3. Update priority in-place — O(1).
4. Call `_sift_down` — O(log n).

Decreasing a priority can only cause a violation downward (element becomes smaller than a child), so only sifting down is needed.

#### `is_empty()` — O(1)

Returns `len(self._heap) == 0`. Python list length is stored as a field; this is a constant-time operation.

#### `peek()` — O(1)

Returns `self._heap[0]` without removing it. The root of a max-heap is always the maximum element by the heap invariant.

#### Complexity Summary Table

| Operation | Time | Space | Direction |
|---|---|---|---|
| `insert` | O(log n) | O(1) | sift up |
| `extract_max` | O(log n) | O(1) | sift down |
| `increase_key` | O(log n) | O(1) | sift up |
| `decrease_key` | O(log n) | O(1) | sift down |
| `peek` | O(1) | O(1) | — |
| `is_empty` | O(1) | O(1) | — |
| `__len__` | O(1) | O(1) | — |
| Build from n elements | O(n log n) via n inserts; O(n) via heapify | O(n) | — |

### 3.4 Scheduler Simulation

The `TaskScheduler` class demonstrates the priority queue in a simulated non-preemptive CPU scheduler scenario. The simulation was run with 8 tasks submitted simultaneously at t = 0:

| Task | Priority | Deadline | Description |
|---|---|---|---|
| JOB-006 | 10 | 2.0 | Emergency security alert |
| JOB-002 | 9 | 3.0 | Payment processing |
| JOB-008 | 8 | 4.0 | Database replication |
| JOB-004 | 7 | 5.0 | User authentication check |
| JOB-005 | 6 | 8.0 | Cache warm-up |
| JOB-003 | 5* | 20.0 | Report generation *(upgraded from 2)* |
| JOB-001 | 4 | 10.0 | Data ETL pipeline |
| JOB-007 | 3 | 15.0 | Log rotation |

*JOB-003's priority was raised from 2 to 5 before execution began (via `increase_key`), demonstrating dynamic priority promotion.*

**Execution order observed:**
```
JOB-006 (p=10) → JOB-002 (p=9) → JOB-008 (p=8) → JOB-004 (p=7)
→ JOB-005 (p=6) → JOB-003 (p=5) → JOB-001 (p=4) → JOB-007 (p=3)
```

This matches the expected descending-priority order. Importantly, JOB-003 (the dynamically promoted task) runs at position 6, ahead of JOB-001 (p=4) and JOB-007 (p=3) — the `increase_key` operation correctly repositioned it in the heap in O(log n) time.

**Real-world applicability:**

- **Operating systems** use priority queues for process/thread scheduling (CFS in Linux, priority threads in Windows).
- **Network routers** use them for Quality-of-Service packet prioritisation.
- **Event-driven simulators** maintain a min-heap of future events sorted by timestamp.
- **Dijkstra's shortest path** and **Prim's MST** algorithms rely on `decrease_key` to update vertex priorities, achieving O((V + E) log V) complexity with a binary heap.

---

## 4. Conclusion

This assignment demonstrated two key applications of the heap data structure:

1. **Heapsort** provides a provably optimal O(n log n) sort in all cases with O(1) auxiliary space — the only comparison sort with both guarantees simultaneously. Empirical data confirmed its insensitivity to input ordering. Its main practical weakness is poor cache locality compared to Quicksort, making it 1.5–1.8× slower on typical hardware despite equal asymptotic complexity.

2. **MaxHeapPriorityQueue** achieves O(log n) for all modification operations and O(1) for reads, enabled by an auxiliary index dictionary that eliminates the O(n) task-lookup bottleneck for key changes. The scheduler simulation demonstrated that `increase_key` and `decrease_key` allow real-time priority adjustments critical for dynamic scheduling workloads.

The most important practical insight from the benchmarks is the **many-duplicates degradation of two-way Quicksort** (2× slowdown at n = 30,000 vs. Heapsort). Heapsort's uniformity across all input distributions makes it the right choice when worst-case guarantees matter and memory is constrained, while randomised Quicksort remains the fastest average-case algorithm for typical data distributions.

---

## 5. References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Chapter 6 (Heapsort), Chapter 8 (Priority Queues).
- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley. Chapter 2 (Sorting).
- Williams, J. W. J. (1964). Algorithm 232 – Heapsort. *Communications of the ACM*, 7(6), 347–348.
- Floyd, R. W. (1964). Algorithm 245 – Treesort 3. *Communications of the ACM*, 7(12), 701.
