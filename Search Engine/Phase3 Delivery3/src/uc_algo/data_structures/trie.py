from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    pass_count: int = 0
    terminal_count: int = 0


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
            node.pass_count += 1

        if node.terminal_count == 0:
            self._size += 1
        node.terminal_count += 1

    def delete(self, word: str) -> bool:
        if not word:
            return False

        node = self._root
        path: list[tuple[TrieNode, str]] = []
        for char in word:
            next_node = node.children.get(char)
            if next_node is None:
                return False
            path.append((node, char))
            node = next_node

        if node.terminal_count == 0:
            return False

        node.terminal_count -= 1
        if node.terminal_count == 0:
            self._size -= 1

        for parent, char in reversed(path):
            child = parent.children[char]
            child.pass_count -= 1
            if (
                child.pass_count <= 0
                and child.terminal_count == 0
                and not child.children
            ):
                del parent.children[char]

        return True

    def contains(self, word: str) -> bool:
        node = self._find_node(word)
        return bool(node and node.terminal_count > 0)

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
            if node.terminal_count > 0:
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
