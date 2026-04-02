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


class Phase3ScalingTests(unittest.TestCase):
    def test_index_and_query_large_dataset(self) -> None:
        engine = SearchEngine()

        for i in range(1200):
            text = (
                f"doc{i} common_term token_{i % 50} token_{(i + 7) % 50} "
                f"category_{i % 10}"
            )
            engine.add_document(f"doc-{i}", text)

        tfidf_results = engine.search(
            "common_term token_4 category_4",
            mode="and",
            top_k=15,
            ranker="tfidf",
        )
        bm25_results = engine.search(
            "common_term token_4 category_4",
            mode="and",
            top_k=15,
            ranker="bm25",
        )

        self.assertTrue(tfidf_results)
        self.assertTrue(bm25_results)
        self.assertLessEqual(len(tfidf_results), 15)
        self.assertLessEqual(len(bm25_results), 15)

        # Validate query still succeeds after a large delete batch.
        for i in range(0, 1200, 3):
            engine.remove_document(f"doc-{i}")

        post_delete_results = engine.search(
            "common_term token_4",
            mode="or",
            top_k=20,
            ranker="bm25",
        )
        self.assertLessEqual(len(post_delete_results), 20)


if __name__ == "__main__":
    unittest.main()
