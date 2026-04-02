from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import random
import statistics
import re
import sys
import time

# Ensure local src package is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uc_algo.app.search_engine import SearchEngine


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


class BaselineTrieNode:
    def __init__(self) -> None:
        self.children: dict[str, BaselineTrieNode] = {}
        self.is_terminal = False


class BaselineTrie:
    def __init__(self) -> None:
        self._root = BaselineTrieNode()

    def insert(self, word: str) -> None:
        if not word:
            return
        node = self._root
        for char in word:
            node = node.children.setdefault(char, BaselineTrieNode())
        node.is_terminal = True


class BaselineInvertedIndex:
    def __init__(self) -> None:
        self._postings: dict[str, dict[str, int]] = {}
        self._documents: dict[str, str] = {}
        self._doc_lengths: dict[str, int] = {}

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())

    def add_document(self, doc_id: str, text: str) -> None:
        if doc_id in self._documents:
            self.remove_document(doc_id)

        terms = self.tokenize(text)
        term_counts: dict[str, int] = {}
        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1

        for term, count in term_counts.items():
            self._postings.setdefault(term, {})[doc_id] = count

        self._documents[doc_id] = text
        self._doc_lengths[doc_id] = len(terms)

    def remove_document(self, doc_id: str) -> None:
        if doc_id not in self._documents:
            return

        for term in list(self._postings.keys()):
            if doc_id in self._postings[term]:
                del self._postings[term][doc_id]
            if not self._postings[term]:
                del self._postings[term]

        del self._documents[doc_id]
        del self._doc_lengths[doc_id]

    def search_or(self, terms: list[str]) -> set[str]:
        normalized = [t.lower() for t in terms if t]
        result: set[str] = set()
        for term in normalized:
            result.update(self._postings.get(term, {}).keys())
        return result

    def document_count(self) -> int:
        return len(self._documents)

    def document_frequency(self, term: str) -> int:
        return len(self._postings.get(term.lower(), {}))

    def term_frequency(self, doc_id: str, term: str) -> int:
        return self._postings.get(term.lower(), {}).get(doc_id, 0)

    def doc_length(self, doc_id: str) -> int:
        return self._doc_lengths.get(doc_id, 0)

    def documents(self) -> list[tuple[str, str]]:
        return list(self._documents.items())


class BaselineSearchEngine:
    """Phase 2 style baseline: full vocabulary rebuild on each mutation."""

    def __init__(self) -> None:
        self.index = BaselineInvertedIndex()
        self.vocabulary = BaselineTrie()

    def add_document(self, doc_id: str, text: str) -> None:
        self.index.add_document(doc_id, text)
        self._rebuild_vocabulary()

    def remove_document(self, doc_id: str) -> None:
        self.index.remove_document(doc_id)
        self._rebuild_vocabulary()

    def search(self, query: str, top_k: int = 20) -> list[tuple[str, float]]:
        terms = self.index.tokenize(query)
        if not terms:
            return []

        candidates = self.index.search_or(terms)
        scored: list[tuple[str, float]] = []
        n_docs = self.index.document_count()

        for doc_id in candidates:
            score = 0.0
            for term in terms:
                tf = self.index.term_frequency(doc_id, term)
                if tf == 0:
                    continue
                df = self.index.document_frequency(term)
                idf = math.log((n_docs + 1) / (df + 1)) + 1.0
                score += tf * idf

            length = max(self.index.doc_length(doc_id), 1)
            scored.append((doc_id, score / length))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def _rebuild_vocabulary(self) -> None:
        self.vocabulary = BaselineTrie()
        for _, text in self.index.documents():
            for term in self.index.tokenize(text):
                self.vocabulary.insert(term)


@dataclass
class BenchmarkResult:
    dataset_size: int
    baseline_build_seconds: float
    optimized_build_seconds: float
    baseline_query_ms: float
    optimized_tfidf_query_ms: float
    optimized_bm25_query_ms: float
    baseline_delete_seconds: float
    optimized_delete_seconds: float


def generate_documents(size: int, vocab: list[str]) -> dict[str, str]:
    random.seed(42 + size)
    documents: dict[str, str] = {}
    for i in range(size):
        terms = [
            "common",
            f"segment_{i % 25}",
            f"topic_{i % 15}",
            random.choice(vocab),
            random.choice(vocab),
            random.choice(vocab),
        ]
        documents[f"doc-{i}"] = " ".join(terms)
    return documents


def timed_query(engine: SearchEngine, query: str, ranker: str, runs: int = 20) -> float:
    durations_ms: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        engine.search(query, mode="or", top_k=20, ranker=ranker)
        end = time.perf_counter()
        durations_ms.append((end - start) * 1000.0)
    return statistics.mean(durations_ms)


def timed_query_baseline(engine: BaselineSearchEngine, query: str, runs: int = 20) -> float:
    durations_ms: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        engine.search(query, top_k=20)
        end = time.perf_counter()
        durations_ms.append((end - start) * 1000.0)
    return statistics.mean(durations_ms)


def run_benchmark(sizes: list[int]) -> list[BenchmarkResult]:
    vocab = [f"term_{i}" for i in range(400)]
    queries = [
        "common topic_2",
        "common segment_7 term_11",
        "topic_8 term_120",
    ]

    results: list[BenchmarkResult] = []
    for size in sizes:
        baseline_engine = BaselineSearchEngine()
        optimized_engine = SearchEngine()
        docs = generate_documents(size, vocab)

        baseline_build_start = time.perf_counter()
        for doc_id, text in docs.items():
            baseline_engine.add_document(doc_id, text)
        baseline_build_seconds = time.perf_counter() - baseline_build_start

        build_start = time.perf_counter()
        for doc_id, text in docs.items():
            optimized_engine.add_document(doc_id, text)
        optimized_build_seconds = time.perf_counter() - build_start

        baseline_query_samples = [timed_query_baseline(baseline_engine, q) for q in queries]
        tfidf_samples = [timed_query(optimized_engine, q, ranker="tfidf") for q in queries]
        bm25_samples = [timed_query(optimized_engine, q, ranker="bm25") for q in queries]

        baseline_delete_start = time.perf_counter()
        for i in range(0, size, 5):
            baseline_engine.remove_document(f"doc-{i}")
        baseline_delete_seconds = time.perf_counter() - baseline_delete_start

        delete_start = time.perf_counter()
        for i in range(0, size, 5):
            optimized_engine.remove_document(f"doc-{i}")
        optimized_delete_seconds = time.perf_counter() - delete_start

        results.append(
            BenchmarkResult(
                dataset_size=size,
                baseline_build_seconds=baseline_build_seconds,
                optimized_build_seconds=optimized_build_seconds,
                baseline_query_ms=statistics.mean(baseline_query_samples),
                optimized_tfidf_query_ms=statistics.mean(tfidf_samples),
                optimized_bm25_query_ms=statistics.mean(bm25_samples),
                baseline_delete_seconds=baseline_delete_seconds,
                optimized_delete_seconds=optimized_delete_seconds,
            )
        )

    return results


def print_results_table(results: list[BenchmarkResult]) -> None:
    header = (
        "dataset_size,baseline_build_seconds,optimized_build_seconds,"
        "baseline_query_ms,optimized_tfidf_query_ms,optimized_bm25_query_ms,"
        "baseline_delete_seconds,optimized_delete_seconds,"
        "build_speedup_x,query_speedup_x,delete_speedup_x"
    )
    print(header)
    for row in results:
        build_speedup = row.baseline_build_seconds / max(row.optimized_build_seconds, 1e-12)
        query_speedup = row.baseline_query_ms / max(row.optimized_tfidf_query_ms, 1e-12)
        delete_speedup = row.baseline_delete_seconds / max(row.optimized_delete_seconds, 1e-12)
        print(
            f"{row.dataset_size},"
            f"{row.baseline_build_seconds:.6f},"
            f"{row.optimized_build_seconds:.6f},"
            f"{row.baseline_query_ms:.3f},"
            f"{row.optimized_tfidf_query_ms:.3f},"
            f"{row.optimized_bm25_query_ms:.3f},"
            f"{row.baseline_delete_seconds:.6f},"
            f"{row.optimized_delete_seconds:.6f},"
            f"{build_speedup:.2f},"
            f"{query_speedup:.2f},"
            f"{delete_speedup:.2f}"
        )


if __name__ == "__main__":
    benchmark_sizes = [200, 500, 1000]
    benchmark_results = run_benchmark(benchmark_sizes)
    print_results_table(benchmark_results)
