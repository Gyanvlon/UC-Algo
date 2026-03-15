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

    query = "search index optimization"
    results = engine.search(query, top_k=3, mode="or")

    print(f"Query: {query}")
    for rank, result in enumerate(results, start=1):
        print(f"{rank}. {result.doc_id} (score={result.score:.4f})")

    print("\nTerm suggestions for 'in':", engine.suggest_terms("in"))


if __name__ == "__main__":
    main()
