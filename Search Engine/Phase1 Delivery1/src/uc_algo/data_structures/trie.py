from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_terminal: bool = False


class Trie:
    """A trie for storing and querying vocabulary terms by prefix."""

    def __init__(self) -> None:
        self._root = TrieNode()
        self._size = 0

    def insert(self, word: str) -> None:
        if not word:
            return

        node = self._root
        for char in word:
            node = node.children.setdefault(char, TrieNode())

        if not node.is_terminal:
            node.is_terminal = True
            self._size += 1

    def contains(self, word: str) -> bool:
        node = self._find_node(word)
        return bool(node and node.is_terminal)

    def starts_with(self, prefix: str, limit: int = 10) -> list[str]:
        """Return up to ``limit`` words that begin with ``prefix``."""
        if limit <= 0:
            return []

        start = self._find_node(prefix)
        if not start:
            return []

        results: list[str] = []
        stack: list[tuple[TrieNode, str]] = [(start, prefix)]

        while stack and len(results) < limit:
            node, current = stack.pop()
            if node.is_terminal:
                results.append(current)

            for char in sorted(node.children.keys(), reverse=True):
                stack.append((node.children[char], current + char))

        return results

    def __len__(self) -> int:
        return self._size

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self._root
        for char in prefix:
            node = node.children.get(char)
            if node is None:
                return None
        return node
