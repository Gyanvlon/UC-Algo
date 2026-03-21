"""
priority_queue.py
=================
Array-based binary max-heap priority queue and a task-scheduler simulation.

Design Choices
--------------
Data structure
    A Python *list* is used as the underlying array for the heap.
    Array-based heaps outperform pointer-based trees for this use case
    because:
      • O(1) random access to any position via index arithmetic.
      • Compact memory layout — no per-node pointer overhead,
        better CPU-cache locality.
      • Parent/child arithmetic is trivial:
          parent(i) = (i - 1) // 2
          left(i)   = 2*i + 1
          right(i)  = 2*i + 2

Heap orientation
    A **max-heap** is used so that the task with the *highest* numeric
    priority is always at the root (index 0) and can be retrieved in O(1)
    or extracted in O(log n).  This directly supports common scheduling
    policies where higher numeric priority → more urgent / more important.

Efficient key lookup for increase_key / decrease_key
    A secondary dict {task_id -> heap_index} lets us locate any task in O(1)
    instead of O(n), making both key-change operations O(log n) overall.

Task representation
    The Task dataclass holds all information a real-world scheduler might
    need: unique ID, numeric priority, arrival timestamp, optional deadline,
    and a free-form description string.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """
    A schedulable unit of work.

    Attributes
    ----------
    task_id      : Unique identifier (string or integer).
    priority     : Numeric priority; higher value means more urgent.
    arrival_time : Simulation timestamp at which the task arrived.
    deadline     : Optional absolute time by which the task must complete.
    description  : Human-readable description of the task.
    """
    task_id:      str | int
    priority:     float
    arrival_time: float = 0.0
    deadline:     Optional[float] = None
    description:  str = ""

    def __repr__(self) -> str:
        dl = f", deadline={self.deadline}" if self.deadline is not None else ""
        desc = f", desc={self.description!r}" if self.description else ""
        return (
            f"Task(id={self.task_id!r}, priority={self.priority}"
            f", arrival={self.arrival_time}{dl}{desc})"
        )


# ---------------------------------------------------------------------------
# MaxHeapPriorityQueue
# ---------------------------------------------------------------------------

class MaxHeapPriorityQueue:
    """
    Binary max-heap priority queue backed by a Python list.

    The task with the **highest** priority value is always at index 0 and
    is the first to be extracted.

    Invariants maintained at all times
    -----------------------------------
    1. Heap property : _heap[parent].priority >= _heap[child].priority
       for every node.
    2. Index map     : _index[task_id] == current position of that task
       in _heap.

    Complexity Summary
    ------------------
    Operation                  Time        Space
    -------------------------  ----------  -----
    insert(task)               O(log n)    O(1)
    extract_max()              O(log n)    O(1)
    increase_key(id, val)      O(log n)    O(1)
    decrease_key(id, val)      O(log n)    O(1)
    peek()                     O(1)        O(1)
    is_empty()                 O(1)        O(1)
    __len__()                  O(1)        O(1)
    """

    def __init__(self) -> None:
        self._heap:  List[Task] = []
        self._index: Dict[str | int, int] = {}   # task_id -> position in _heap

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def insert(self, task: Task) -> None:
        """
        Add a new task to the priority queue.

        Steps
        -----
        1. Append the task to the end of the heap array — O(1) amortised.
        2. Record its index in the lookup dict — O(1).
        3. Sift up until the max-heap property is restored — O(log n).

        Time Complexity : O(log n)
            At most floor(log2 n) comparisons/swaps sifting up.
        Space Complexity: O(1) per call  (O(n) total for storing n tasks).

        Raises
        ------
        ValueError
            If a task with the same task_id already exists.
        """
        if task.task_id in self._index:
            raise ValueError(
                f"Task '{task.task_id}' already exists in the priority queue. "
                "Use increase_key() or decrease_key() to change its priority."
            )
        self._heap.append(task)
        idx = len(self._heap) - 1
        self._index[task.task_id] = idx
        self._sift_up(idx)

    def extract_max(self) -> Task:
        """
        Remove and return the task with the **highest** priority.

        Steps
        -----
        1. Record the root task (the maximum) — O(1).
        2. Replace root with the last element, shrink the heap — O(1) amortised.
        3. Sift the new root down to restore the heap property — O(log n).
        4. Remove the task from the index map — O(1).

        Time Complexity : O(log n)
        Space Complexity: O(1)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("extract_max() called on an empty priority queue.")

        max_task = self._heap[0]

        # Move the last element to the root then shrink.
        last = self._heap.pop()          # O(1) amortised
        if self._heap:                   # heap still has remaining elements
            self._heap[0] = last
            self._index[last.task_id] = 0
            self._sift_down(0)

        del self._index[max_task.task_id]
        return max_task

    def increase_key(self, task_id: str | int, new_priority: float) -> None:
        """
        Raise the priority of an existing task.

        Because the priority can only increase, the task may now violate
        the heap property with respect to its *parent* — sift **up** to fix.

        Time Complexity : O(log n)
        Space Complexity: O(1)

        Raises
        ------
        KeyError
            If task_id is not in the queue.
        ValueError
            If new_priority is strictly less than the current priority.
        """
        if task_id not in self._index:
            raise KeyError(f"Task '{task_id}' not found in priority queue.")
        idx = self._index[task_id]
        if new_priority < self._heap[idx].priority:
            raise ValueError(
                f"increase_key: new priority ({new_priority}) must be >= "
                f"current priority ({self._heap[idx].priority})."
            )
        self._heap[idx].priority = new_priority
        self._sift_up(idx)

    def decrease_key(self, task_id: str | int, new_priority: float) -> None:
        """
        Lower the priority of an existing task.

        Because the priority can only decrease, the task may now violate
        the heap property with respect to its *children* — sift **down**.

        Time Complexity : O(log n)
        Space Complexity: O(1)

        Raises
        ------
        KeyError
            If task_id is not in the queue.
        ValueError
            If new_priority is strictly greater than the current priority.
        """
        if task_id not in self._index:
            raise KeyError(f"Task '{task_id}' not found in priority queue.")
        idx = self._index[task_id]
        if new_priority > self._heap[idx].priority:
            raise ValueError(
                f"decrease_key: new priority ({new_priority}) must be <= "
                f"current priority ({self._heap[idx].priority})."
            )
        self._heap[idx].priority = new_priority
        self._sift_down(idx)

    def peek(self) -> Task:
        """
        Return (without removing) the highest-priority task.

        Time Complexity : O(1)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek() called on an empty priority queue.")
        return self._heap[0]

    def is_empty(self) -> bool:
        """Return True if the queue contains no tasks.  O(1)."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        """Return the number of tasks currently in the queue.  O(1)."""
        return len(self._heap)

    def __repr__(self) -> str:
        top = self._heap[0] if self._heap else None
        return f"MaxHeapPriorityQueue(size={len(self)}, top={top})"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _sift_up(self, idx: int) -> None:
        """
        Move the element at *idx* upward until the max-heap property holds.

        Called after insert() or increase_key() places a potentially
        too-large value below its parent.
        """
        heap = self._heap
        while idx > 0:
            parent = (idx - 1) // 2
            if heap[idx].priority > heap[parent].priority:
                self._swap(idx, parent)
                idx = parent
            else:
                break   # heap property satisfied

    def _sift_down(self, idx: int) -> None:
        """
        Move the element at *idx* downward until the max-heap property holds.

        Called after extract_max() places the last element at the root,
        or after decrease_key() lowers a value.
        """
        heap = self._heap
        n    = len(heap)
        while True:
            largest = idx
            left    = 2 * idx + 1
            right   = 2 * idx + 2

            if left  < n and heap[left].priority  > heap[largest].priority:
                largest = left
            if right < n and heap[right].priority > heap[largest].priority:
                largest = right

            if largest == idx:
                break   # heap property satisfied

            self._swap(idx, largest)
            idx = largest

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at positions i and j and keep the index map consistent."""
        heap = self._heap
        # Update the map BEFORE touching the array so it stays consistent.
        self._index[heap[i].task_id] = j
        self._index[heap[j].task_id] = i
        heap[i], heap[j] = heap[j], heap[i]


# ---------------------------------------------------------------------------
# MinHeapPriorityQueue
# ---------------------------------------------------------------------------

class MinHeapPriorityQueue:
    """
    Binary min-heap priority queue: the task with the **lowest** priority
    value is served first.

    Implemented by negating priorities internally so the underlying
    MaxHeapPriorityQueue treats them correctly.  This is useful when lower
    numeric values represent higher urgency (e.g., priority level 1 runs
    before level 10).

    All complexity bounds are identical to MaxHeapPriorityQueue.
    """

    def __init__(self) -> None:
        self._pq: MaxHeapPriorityQueue = MaxHeapPriorityQueue()

    # Helper: return a copy of task with negated priority for internal storage.
    def _neg(self, task: Task) -> Task:
        return Task(
            task_id=task.task_id,
            priority=-task.priority,
            arrival_time=task.arrival_time,
            deadline=task.deadline,
            description=task.description,
        )

    def insert(self, task: Task) -> None:
        """Insert a task; O(log n)."""
        self._pq.insert(self._neg(task))

    def extract_min(self) -> Task:
        """Remove and return the task with the lowest priority value; O(log n)."""
        t = self._pq.extract_max()
        t.priority = -t.priority   # restore true sign
        return t

    def increase_key(self, task_id: str | int, new_priority: float) -> None:
        """
        Raise the numeric priority value (makes the task *less* urgent).
        O(log n).
        """
        self._pq.decrease_key(task_id, -new_priority)

    def decrease_key(self, task_id: str | int, new_priority: float) -> None:
        """
        Lower the numeric priority value (makes the task *more* urgent).
        O(log n).
        """
        self._pq.increase_key(task_id, -new_priority)

    def peek(self) -> Task:
        """Return the lowest-priority task without removing it; O(1)."""
        t = self._pq.peek()
        return Task(
            task_id=t.task_id,
            priority=-t.priority,
            arrival_time=t.arrival_time,
            deadline=t.deadline,
            description=t.description,
        )

    def is_empty(self) -> bool:
        """Return True if empty; O(1)."""
        return self._pq.is_empty()

    def __len__(self) -> int:
        return len(self._pq)


# ---------------------------------------------------------------------------
# TaskScheduler — simulation of a priority-based CPU scheduler
# ---------------------------------------------------------------------------

class TaskScheduler:
    """
    Priority-based task scheduler backed by a MaxHeapPriorityQueue.

    Simulates a non-preemptive scheduler that:
      1. Accepts task submissions via submit_task().
      2. Always runs the highest-priority ready task via run_next_task().
      3. Maintains an execution log and a list of completed tasks.
    """

    def __init__(self) -> None:
        self._queue:     MaxHeapPriorityQueue = MaxHeapPriorityQueue()
        self._log:       List[str] = []
        self._clock:     float = 0.0
        self._completed: List[Task] = []

    def submit_task(self, task: Task) -> None:
        """Add a task to the ready queue and log the submission."""
        self._queue.insert(task)
        self._log.append(
            f"  [t={self._clock:6.1f}] SUBMITTED  {task}"
        )

    def run_next_task(self, duration: float = 1.0) -> Optional[Task]:
        """
        Execute the highest-priority queued task for *duration* time units.

        Returns
        -------
        Task | None
            The task that ran, or None when the queue was empty (idle cycle).
        """
        if self._queue.is_empty():
            self._log.append(
                f"  [t={self._clock:6.1f}] IDLE       — no tasks in queue."
            )
            self._clock += duration
            return None

        task = self._queue.extract_max()
        self._log.append(
            f"  [t={self._clock:6.1f}] RUNNING    {task}  (duration={duration})"
        )
        self._clock += duration
        self._completed.append(task)
        return task

    def update_priority(self, task_id: str | int, new_priority: float) -> None:
        """
        Change the priority of a task still in the ready queue and log the event.
        """
        old_priority = self._queue._heap[self._queue._index[task_id]].priority
        if new_priority >= old_priority:
            self._queue.increase_key(task_id, new_priority)
        else:
            self._queue.decrease_key(task_id, new_priority)
        self._log.append(
            f"  [t={self._clock:6.1f}] PRIORITY   task={task_id!r}  "
            f"{old_priority} -> {new_priority}"
        )

    def run_all(self, duration_per_task: float = 1.0) -> None:
        """Drain the queue, running tasks in priority order."""
        while not self._queue.is_empty():
            self.run_next_task(duration_per_task)

    def print_log(self) -> None:
        """Print the chronological event log."""
        print("\n".join(self._log))

    def print_summary(self) -> None:
        """Print a summary of completed tasks."""
        print(
            f"\n  Completed {len(self._completed)} task(s) "
            f"in {self._clock:.1f} time units."
        )
        print("  Execution order (highest priority first):")
        for i, t in enumerate(self._completed, 1):
            print(f"    {i:>3}. {t}")


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Part 1: Basic MaxHeapPriorityQueue operations
    # ------------------------------------------------------------------
    print("=" * 65)
    print("MaxHeapPriorityQueue — Basic Operations Demo")
    print("=" * 65)

    pq = MaxHeapPriorityQueue()

    tasks = [
        Task("T1", priority=3,  arrival_time=0.0, description="low-priority batch job"),
        Task("T2", priority=10, arrival_time=0.5, description="critical system alert"),
        Task("T3", priority=5,  arrival_time=1.0, description="user request"),
        Task("T4", priority=7,  arrival_time=1.5, description="scheduled backup"),
        Task("T5", priority=1,  arrival_time=2.0, description="maintenance sweep"),
    ]

    print("\n--- Inserting tasks ---")
    for t in tasks:
        pq.insert(t)
        print(f"  Inserted {t}")
        print(f"  Queue top (highest priority): {pq.peek()}\n")

    print(f"Queue size  : {len(pq)}")
    print(f"is_empty()  : {pq.is_empty()}")

    # ------------------------------------------------------------------
    # Part 2: Key modifications
    # ------------------------------------------------------------------
    print("\n--- Modifying priorities ---")
    pq.increase_key("T1", new_priority=8)
    print(f"  T1 priority raised to 8.  New top: {pq.peek()}")

    pq.decrease_key("T2", new_priority=6)
    print(f"  T2 priority lowered to 6.  New top: {pq.peek()}")

    # ------------------------------------------------------------------
    # Part 3: Extraction in sorted order
    # ------------------------------------------------------------------
    print("\n--- Extracting tasks in priority order ---")
    while not pq.is_empty():
        extracted = pq.extract_max()
        print(f"  Extracted: {extracted}")

    # ------------------------------------------------------------------
    # Part 4: MinHeapPriorityQueue demo
    # ------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("MinHeapPriorityQueue — Extract-min Demo")
    print("=" * 65)

    min_pq = MinHeapPriorityQueue()
    for t in tasks:
        # Re-create tasks since extract_max consumed the originals above.
        min_pq.insert(Task(t.task_id, t.priority, t.arrival_time, t.deadline, t.description))

    print("\n--- Extracting in ascending priority order ---")
    while not min_pq.is_empty():
        print(f"  Extracted: {min_pq.extract_min()}")

    # ------------------------------------------------------------------
    # Part 5: Scheduler simulation
    # ------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("TaskScheduler Simulation — Priority-Based CPU Scheduler")
    print("=" * 65)

    scheduler = TaskScheduler()

    simulation_tasks = [
        Task("JOB-001", priority=4,  arrival_time=0.0, deadline=10.0, description="Data ETL pipeline"),
        Task("JOB-002", priority=9,  arrival_time=0.0, deadline=3.0,  description="Payment processing"),
        Task("JOB-003", priority=2,  arrival_time=0.0, deadline=20.0, description="Report generation"),
        Task("JOB-004", priority=7,  arrival_time=0.0, deadline=5.0,  description="User authentication check"),
        Task("JOB-005", priority=6,  arrival_time=0.0, deadline=8.0,  description="Cache warm-up"),
        Task("JOB-006", priority=10, arrival_time=0.0, deadline=2.0,  description="Emergency security alert"),
        Task("JOB-007", priority=3,  arrival_time=0.0, deadline=15.0, description="Log rotation"),
        Task("JOB-008", priority=8,  arrival_time=0.0, deadline=4.0,  description="Database replication"),
    ]

    print("\nSubmitting all tasks at t=0:")
    for t in simulation_tasks:
        scheduler.submit_task(t)

    # Demonstrate a runtime priority change before the scheduler runs.
    print("\nUpgrading JOB-003 priority from 2 to 5 (deadline tightened):")
    scheduler.update_priority("JOB-003", 5)

    print("\nRunning scheduler (1 time unit per task):")
    scheduler.run_all(duration_per_task=1.0)
    scheduler.print_log()
    scheduler.print_summary()

    # ------------------------------------------------------------------
    # Part 6: Correctness stress test
    # ------------------------------------------------------------------
    import random
    print("\n" + "=" * 65)
    print("Correctness stress test (1 000 random insert/extract sequences)")
    print("=" * 65)

    for trial in range(1_000):
        random.seed(trial)
        pq2 = MaxHeapPriorityQueue()
        inserted: List[float] = []

        n = random.randint(1, 50)
        for k in range(n):
            p = random.uniform(-100, 100)
            t = Task(task_id=k, priority=p)
            pq2.insert(t)
            inserted.append(p)

        # Extract all and verify descending order.
        extracted_priorities = [pq2.extract_max().priority for _ in range(n)]
        expected = sorted(inserted, reverse=True)
        assert extracted_priorities == expected, (
            f"Trial {trial}: got {extracted_priorities}, expected {expected}"
        )

    print("All 1 000 stress-test trials passed.")
