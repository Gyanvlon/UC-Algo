"""Elementary data structures implemented from scratch in Python.

Includes:
- DynamicArray and Matrix
- StackArray and QueueArray
- SinglyLinkedList
- Optional RootedTreeNode
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """A simple dynamic array with amortized O(1) append."""

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        self._capacity = initial_capacity
        self._size = 0
        self._data: List[Optional[T]] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _resize(self, new_capacity: int) -> None:
        new_data: List[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: T) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def delete(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1

        if self._size > 0 and self._size <= self._capacity // 4 and self._capacity > 4:
            self._resize(max(4, self._capacity // 2))

        return value  # type: ignore[return-value]

    def get(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        return self._data[index]  # type: ignore[return-value]

    def set(self, index: int, value: T) -> None:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        self._data[index] = value

    def to_list(self) -> List[T]:
        return [self._data[i] for i in range(self._size)]  # type: ignore[misc]


class Matrix(Generic[T]):
    """A 2D matrix backed by a list of row lists."""

    def __init__(self, rows: int, cols: int, default: Optional[T] = None) -> None:
        if rows < 0 or cols < 0:
            raise ValueError("rows and cols must be non-negative")
        self.rows = rows
        self.cols = cols
        self.data: List[List[Optional[T]]] = [[default for _ in range(cols)] for _ in range(rows)]

    def get(self, r: int, c: int) -> Optional[T]:
        return self.data[r][c]

    def set(self, r: int, c: int, value: T) -> None:
        self.data[r][c] = value

    def insert_row(self, index: int, default: Optional[T] = None) -> None:
        if index < 0 or index > self.rows:
            raise IndexError("row index out of range")
        self.data.insert(index, [default for _ in range(self.cols)])
        self.rows += 1

    def delete_row(self, index: int) -> List[Optional[T]]:
        if index < 0 or index >= self.rows:
            raise IndexError("row index out of range")
        self.rows -= 1
        return self.data.pop(index)

    def insert_col(self, index: int, default: Optional[T] = None) -> None:
        if index < 0 or index > self.cols:
            raise IndexError("col index out of range")
        for row in self.data:
            row.insert(index, default)
        self.cols += 1

    def delete_col(self, index: int) -> List[Optional[T]]:
        if index < 0 or index >= self.cols:
            raise IndexError("col index out of range")
        removed: List[Optional[T]] = []
        for row in self.data:
            removed.append(row.pop(index))
        self.cols -= 1
        return removed


class StackArray(Generic[T]):
    """LIFO stack based on DynamicArray semantics using Python list."""

    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, value: T) -> None:
        self._data.append(value)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


class QueueArray(Generic[T]):
    """FIFO queue implemented as a circular buffer."""

    def __init__(self, capacity: int = 4) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._data: List[Optional[T]] = [None] * capacity
        self._capacity = capacity
        self._size = 0
        self._front = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _resize(self, new_capacity: int) -> None:
        new_data: List[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._capacity = new_capacity
        self._front = 0

    def enqueue(self, value: T) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = value
        self._size += 1

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1

        if self._size > 0 and self._size <= self._capacity // 4 and self._capacity > 4:
            self._resize(max(4, self._capacity // 2))

        return value  # type: ignore[return-value]

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._front]  # type: ignore[return-value]


@dataclass
class _Node(Generic[T]):
    value: T
    next: Optional["_Node[T]"] = None


class SinglyLinkedList(Generic[T]):
    """Singly linked list with head/tail pointers."""

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[_Node[T]] = None
        self.tail: Optional[_Node[T]] = None
        self._size = 0

        if values is not None:
            for v in values:
                self.insert_back(v)

    def __len__(self) -> int:
        return self._size

    def insert_front(self, value: T) -> None:
        node = _Node(value=value, next=self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def insert_back(self, value: T) -> None:
        node = _Node(value=value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def delete_value(self, value: T) -> bool:
        prev: Optional[_Node[T]] = None
        curr = self.head

        while curr is not None:
            if curr.value == value:
                if prev is None:
                    self.head = curr.next
                else:
                    prev.next = curr.next
                if curr == self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, curr = curr, curr.next

        return False

    def delete_at_index(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        prev: Optional[_Node[T]] = None
        curr = self.head

        for _ in range(index):
            prev = curr
            curr = curr.next if curr else None

        if curr is None:
            raise IndexError("index out of range")

        if prev is None:
            self.head = curr.next
        else:
            prev.next = curr.next

        if curr == self.tail:
            self.tail = prev

        self._size -= 1
        return curr.value

    def traverse(self) -> List[T]:
        result: List[T] = []
        curr = self.head
        while curr is not None:
            result.append(curr.value)
            curr = curr.next
        return result

    def find(self, value: T) -> int:
        index = 0
        curr = self.head
        while curr is not None:
            if curr.value == value:
                return index
            index += 1
            curr = curr.next
        return -1

    def __iter__(self) -> Iterator[T]:
        curr = self.head
        while curr is not None:
            yield curr.value
            curr = curr.next


class RootedTreeNode(Generic[T]):
    """Optional rooted tree node using linked relationships."""

    def __init__(self, value: T) -> None:
        self.value = value
        self.parent: Optional["RootedTreeNode[T]"] = None
        self.children: List["RootedTreeNode[T]"] = []

    def add_child(self, child: "RootedTreeNode[T]") -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "RootedTreeNode[T]") -> bool:
        for i, c in enumerate(self.children):
            if c is child:
                c.parent = None
                self.children.pop(i)
                return True
        return False

    def dfs_values(self) -> List[T]:
        values = [self.value]
        for child in self.children:
            values.extend(child.dfs_values())
        return values


def _sanity_check() -> None:
    arr = DynamicArray[int]()
    for x in [1, 2, 4]:
        arr.append(x)
    arr.insert(2, 3)
    assert arr.to_list() == [1, 2, 3, 4]
    assert arr.delete(1) == 2
    assert arr.to_list() == [1, 3, 4]

    stack = StackArray[int]()
    stack.push(10)
    stack.push(20)
    assert stack.pop() == 20

    queue = QueueArray[int]()
    queue.enqueue(5)
    queue.enqueue(6)
    assert queue.dequeue() == 5

    ll = SinglyLinkedList[int]([1, 2, 3])
    ll.insert_front(0)
    assert ll.traverse() == [0, 1, 2, 3]
    assert ll.delete_value(2) is True
    assert ll.traverse() == [0, 1, 3]


if __name__ == "__main__":
    _sanity_check()
    print("Data structures sanity check passed.")
