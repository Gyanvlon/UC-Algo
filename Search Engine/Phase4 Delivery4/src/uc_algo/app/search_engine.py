from __future__ import annotations

import math
from dataclasses import dataclass

from uc_algo.data_structures.inverted_index import DocumentDelta, InvertedIndex
from uc_algo.data_structures.topk_heap import TopKHeap
from uc_algo.data_structures.trie import Trie


@dataclass
class SearchResult:
    doc_id: str
    score: float


class SearchEngine:
    """Search engine with optimized indexing, ranking, and suggestion updates."""

    def __init__(self) -> None:
        self.index = InvertedIndex()
        self.vocabulary = Trie()
        self._idf_cache: dict[str, float] = {}
        self._idf_cache_version = -1

    def add_document(self, doc_id: str, text: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")
        if text is None:
            raise ValueError("text must not be None")

        delta = self.index.add_document(doc_id, text)
        self._apply_vocabulary_delta(delta)

    def remove_document(self, doc_id: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")

        delta = self.index.remove_document(doc_id)
        self._apply_vocabulary_delta(delta)

    def suggest_terms(self, prefix: str, limit: int = 10) -> list[str]:
        if prefix is None:
            raise ValueError("prefix must not be None")
        if limit < 0:
            raise ValueError("limit must be >= 0")

        return self.vocabulary.starts_with(prefix.lower(), limit=limit)

    def search(
        self,
        query: str,
        top_k: int = 5,
        mode: str = "and",
        ranker: str = "tfidf",
    ) -> list[SearchResult]:
        if query is None:
            raise ValueError("query must not be None")
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        if ranker not in {"tfidf", "bm25"}:
            raise ValueError("ranker must be either 'tfidf' or 'bm25'")

        terms = self.index.tokenize(query)
        if not terms:
            return []

        if mode == "and":
            candidate_docs = self.index.search_and(terms)
        elif mode == "or":
            candidate_docs = self.index.search_or(terms)
        else:
            raise ValueError("mode must be either 'and' or 'or'")

        if not candidate_docs:
            return []

        topk = TopKHeap(k=top_k)
        for doc_id in candidate_docs:
            score = self._score_document(doc_id, terms, ranker=ranker)
            topk.push(item_id=doc_id, score=score)

        return [SearchResult(doc_id=item.item_id, score=item.score) for item in topk.items_descending()]

    def _score_document(self, doc_id: str, terms: list[str], ranker: str) -> float:
        if ranker == "bm25":
            return self._score_bm25(doc_id, terms)
        return self._score_tfidf(doc_id, terms)

    def _score_tfidf(self, doc_id: str, terms: list[str]) -> float:
        n_docs = self.index.document_count()
        score = 0.0
        if n_docs == 0:
            return score

        for term in terms:
            tf = self.index.term_frequency(doc_id, term)
            if tf == 0:
                continue

            idf = self._idf_tfidf(term)
            score += tf * idf

        length = max(self.index.doc_length(doc_id), 1)
        return score / length

    def _score_bm25(self, doc_id: str, terms: list[str], k1: float = 1.5, b: float = 0.75) -> float:
        n_docs = self.index.document_count()
        if n_docs == 0:
            return 0.0

        avg_doc_len = max(self.index.average_doc_length(), 1e-9)
        doc_len = self.index.doc_length(doc_id)
        score = 0.0

        for term in terms:
            tf = self.index.term_frequency(doc_id, term)
            if tf == 0:
                continue

            df = self.index.document_frequency(term)
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            denominator = tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len))
            score += idf * ((tf * (k1 + 1.0)) / denominator)

        return score

    def _idf_tfidf(self, term: str) -> float:
        current_version = self.index.version()
        if self._idf_cache_version != current_version:
            self._idf_cache.clear()
            self._idf_cache_version = current_version

        if term not in self._idf_cache:
            n_docs = self.index.document_count()
            df = self.index.document_frequency(term)
            self._idf_cache[term] = math.log((n_docs + 1) / (df + 1)) + 1.0

        return self._idf_cache[term]

    def _apply_vocabulary_delta(self, delta: DocumentDelta) -> None:
        for term in delta.became_present:
            self.vocabulary.insert(term)
        for term in delta.became_absent:
            self.vocabulary.delete(term)

    def _rebuild_vocabulary(self) -> None:
        """Rebuild trie from indexed documents to recover from inconsistent state."""
        self.vocabulary = Trie()
        for _, text in self.index.documents():
            for term in self.index.tokenize(text):
                self.vocabulary.insert(term)
