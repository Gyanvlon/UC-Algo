"""Hash table implementation using chaining collision resolution.

Uses a universal-hash-style compression function with random parameters and
supports insert, search, and delete with dynamic resizing.
"""

from __future__ import annotations

import random
from typing import Any, List, Optional, Tuple


class HashTableChaining:
    """Hash table with separate chaining and dynamic resizing."""

    _DEFAULT_INITIAL_CAPACITY = 8
    _DEFAULT_MAX_LOAD = 0.75
    _DEFAULT_MIN_LOAD = 0.25
    _LARGE_PRIME = 2305843009213693951

    def __init__(self, initial_capacity: int = _DEFAULT_INITIAL_CAPACITY, max_load_factor: float = _DEFAULT_MAX_LOAD) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        if max_load_factor <= 0:
            raise ValueError("max_load_factor must be > 0")

        capacity = 1
        while capacity < initial_capacity:
            capacity *= 2

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._min_load_factor = self._DEFAULT_MIN_LOAD
        self._size = 0
        self._buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self._capacity)]

        self._rng = random.SystemRandom()
        self._choose_new_hash_parameters()

    def _choose_new_hash_parameters(self) -> None:
        self._a = self._rng.randrange(1, self._LARGE_PRIME - 1)
        self._b = self._rng.randrange(0, self._LARGE_PRIME - 1)

    def _index(self, key: Any) -> int:
        key_hash = hash(key) % self._LARGE_PRIME
        return ((self._a * key_hash + self._b) % self._LARGE_PRIME) % self._capacity

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def insert(self, key: Any, value: Any) -> None:
        idx = self._index(key)
        bucket = self._buckets[idx]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._size += 1

        if self.load_factor > self._max_load_factor:
            self._resize(self._capacity * 2)

    def search(self, key: Any) -> Optional[Any]:
        idx = self._index(key)
        for existing_key, value in self._buckets[idx]:
            if existing_key == key:
                return value
        return None

    def delete(self, key: Any) -> bool:
        idx = self._index(key)
        bucket = self._buckets[idx]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1

                if self._capacity > self._DEFAULT_INITIAL_CAPACITY and self.load_factor < self._min_load_factor:
                    self._resize(max(self._DEFAULT_INITIAL_CAPACITY, self._capacity // 2))

                return True

        return False

    def _resize(self, new_capacity: int) -> None:
        old_items = []
        for bucket in self._buckets:
            old_items.extend(bucket)

        self._capacity = new_capacity
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        self._choose_new_hash_parameters()

        for key, value in old_items:
            self.insert(key, value)


if __name__ == "__main__":
    table = HashTableChaining(initial_capacity=4)

    table.insert("alice", 95)
    table.insert("bob", 88)
    table.insert("carol", 91)

    print("alice ->", table.search("alice"))
    print("bob ->", table.search("bob"))
    print("delete bob:", table.delete("bob"))
    print("bob after delete ->", table.search("bob"))
    print("size:", len(table), "capacity:", table.capacity, "load:", round(table.load_factor, 3))
