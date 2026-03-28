from __future__ import annotations

from pathlib import Path
import sys

# Ensure local src package is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uc_algo.app.search_engine import SearchEngine


def main() -> None:
    engine = SearchEngine()

    documents = {
        "doc-001": "Python data structures tutorial for hash tables and binary trees",
        "doc-002": "Search engine indexing strategies for scalable web retrieval",
        "doc-003": "Performance optimization of inverted index and query ranking",
        "doc-004": "Graph algorithms for social network influence analysis",
    }

    for doc_id, text in documents.items():
        engine.add_document(doc_id, text)

    query_and = "search index"
    query_or = "search graph"

    results_and = engine.search(query_and, top_k=3, mode="and")
    results_or = engine.search(query_or, top_k=3, mode="or")

    print(f"AND Query: {query_and}")
    for rank, result in enumerate(results_and, start=1):
        print(f"{rank}. {result.doc_id} (score={result.score:.4f})")

    print(f"\nOR Query: {query_or}")
    for rank, result in enumerate(results_or, start=1):
        print(f"{rank}. {result.doc_id} (score={result.score:.4f})")

    print("\nTerm suggestions for 'in':", engine.suggest_terms("in"))

    print("\nRemoving doc-003 and re-running OR query...")
    engine.remove_document("doc-003")
    results_after_delete = engine.search(query_or, top_k=3, mode="or")
    for rank, result in enumerate(results_after_delete, start=1):
        print(f"{rank}. {result.doc_id} (score={result.score:.4f})")


if __name__ == "__main__":
    main()
