from __future__ import annotations

import unittest
from pathlib import Path
import sys

# Ensure local src package is importable when running tests directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uc_algo.data_structures.inverted_index import InvertedIndex
from uc_algo.data_structures.topk_heap import TopKHeap
from uc_algo.data_structures.trie import Trie


class InvertedIndexTests(unittest.TestCase):
    def test_add_search_and_remove(self) -> None:
        index = InvertedIndex()
        index.add_document("d1", "search index search")
        index.add_document("d2", "graph search")

        self.assertEqual(index.search_and(["search"]), {"d1", "d2"})
        self.assertEqual(index.search_and(["search", "index"]), {"d1"})
        self.assertEqual(index.search_or(["index", "graph"]), {"d1", "d2"})

        index.remove_document("d1")
        self.assertEqual(index.search_or(["index"]), set())

    def test_invalid_document_inputs_raise(self) -> None:
        index = InvertedIndex()

        with self.assertRaises(ValueError):
            index.add_document("", "abc")

        with self.assertRaises(ValueError):
            index.add_document("d1", None)

        with self.assertRaises(ValueError):
            index.remove_document("")


class TrieTests(unittest.TestCase):
    def test_insert_contains_and_prefix(self) -> None:
        trie = Trie()
        trie.insert("index")
        trie.insert("inverted")
        trie.insert("inside")

        self.assertTrue(trie.contains("index"))
        self.assertFalse(trie.contains("ind"))
        self.assertEqual(trie.starts_with("in", limit=2), ["index", "inside"])


class TopKHeapTests(unittest.TestCase):
    def test_maintains_highest_k_scores(self) -> None:
        heap = TopKHeap(k=2)
        heap.push("a", 0.1)
        heap.push("b", 0.9)
        heap.push("c", 0.5)

        items = heap.items_descending()
        self.assertEqual([item.item_id for item in items], ["b", "c"])

    def test_invalid_k_raises(self) -> None:
        with self.assertRaises(ValueError):
            TopKHeap(k=0)


if __name__ == "__main__":
    unittest.main()
