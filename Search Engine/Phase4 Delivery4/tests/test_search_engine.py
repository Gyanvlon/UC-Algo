from __future__ import annotations

import unittest
from pathlib import Path
import sys

# Ensure local src package is importable when running tests directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uc_algo.app.search_engine import SearchEngine


class SearchEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = SearchEngine()
        self.engine.add_document(
            "doc-001", "python search and indexing with hash tables"
        )
        self.engine.add_document(
            "doc-002", "search engine ranking with inverted index"
        )
        self.engine.add_document(
            "doc-003", "graph analytics for social network analysis"
        )

    def test_search_and_mode_returns_intersection(self) -> None:
        results = self.engine.search("search index", mode="and")
        result_ids = {item.doc_id for item in results}
        self.assertEqual(result_ids, {"doc-002"})

    def test_search_or_mode_returns_union(self) -> None:
        results = self.engine.search("search graph", mode="or")
        result_ids = {item.doc_id for item in results}
        self.assertEqual(result_ids, {"doc-001", "doc-002", "doc-003"})

    def test_top_k_limits_results(self) -> None:
        results = self.engine.search("search", mode="or", top_k=1)
        self.assertEqual(len(results), 1)

    def test_suggestions_are_prefix_filtered(self) -> None:
        suggestions = self.engine.suggest_terms("se")
        self.assertIn("search", suggestions)

    def test_remove_document_updates_search_and_suggestions(self) -> None:
        self.engine.add_document("doc-temp", "ultraviolet")
        self.assertIn("ultraviolet", self.engine.suggest_terms("ul"))

        self.engine.remove_document("doc-temp")

        results = self.engine.search("ultraviolet", mode="or")
        self.assertEqual(results, [])
        self.assertNotIn("ultraviolet", self.engine.suggest_terms("ul"))

    def test_replace_document_updates_vocabulary_incrementally(self) -> None:
        self.engine.add_document("doc-replace", "quasar nebula")
        self.assertIn("quasar", self.engine.suggest_terms("qu"))

        self.engine.add_document("doc-replace", "nova pulsar")

        self.assertNotIn("quasar", self.engine.suggest_terms("qu"))
        self.assertIn("nova", self.engine.suggest_terms("no"))

    def test_bm25_ranking_is_supported(self) -> None:
        self.engine.add_document("doc-bm25-a", "search search search engine")
        self.engine.add_document("doc-bm25-b", "search engine ranking retrieval")

        results = self.engine.search("search engine", mode="or", ranker="bm25")
        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0].doc_id, "doc-bm25-a")

    def test_empty_query_returns_no_results(self) -> None:
        self.assertEqual(self.engine.search("   ", mode="or"), [])

    def test_invalid_inputs_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.engine.add_document("", "valid text")

        with self.assertRaises(ValueError):
            self.engine.add_document("doc-x", None)

        with self.assertRaises(ValueError):
            self.engine.search(None)

        with self.assertRaises(ValueError):
            self.engine.search("search", top_k=0)

        with self.assertRaises(ValueError):
            self.engine.search("search", ranker="unknown")

        with self.assertRaises(ValueError):
            self.engine.suggest_terms(None)


if __name__ == "__main__":
    unittest.main()
