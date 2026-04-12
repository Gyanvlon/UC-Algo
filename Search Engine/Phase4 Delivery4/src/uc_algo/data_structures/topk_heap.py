from __future__ import annotations

import heapq
from dataclasses import dataclass


@dataclass(order=True)
class ScoredItem:
    score: float
    item_id: str


class TopKHeap:
    """Maintain the top-k highest scored items using a min-heap."""

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("k must be positive")
        self._k = k
        self._heap: list[ScoredItem] = []

    def push(self, item_id: str, score: float) -> None:
        candidate = ScoredItem(score=score, item_id=item_id)

        if len(self._heap) < self._k:
            heapq.heappush(self._heap, candidate)
            return

        if candidate.score > self._heap[0].score:
            heapq.heapreplace(self._heap, candidate)

    def items_descending(self) -> list[ScoredItem]:
        return sorted(self._heap, reverse=True)

    def __len__(self) -> int:
        return len(self._heap)
