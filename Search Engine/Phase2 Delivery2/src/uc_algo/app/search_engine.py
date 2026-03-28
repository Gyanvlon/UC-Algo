from __future__ import annotations

import math
from dataclasses import dataclass

from uc_algo.data_structures.inverted_index import InvertedIndex
from uc_algo.data_structures.topk_heap import TopKHeap
from uc_algo.data_structures.trie import Trie


@dataclass
class SearchResult:
    doc_id: str
    score: float


class SearchEngine:
    """A simplified search engine built from custom data structures."""

    def __init__(self) -> None:
        self.index = InvertedIndex()
        self.vocabulary = Trie()

    def add_document(self, doc_id: str, text: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")
        if text is None:
            raise ValueError("text must not be None")

        self.index.add_document(doc_id, text)
        self._rebuild_vocabulary()

    def remove_document(self, doc_id: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")

        self.index.remove_document(doc_id)
        self._rebuild_vocabulary()

    def suggest_terms(self, prefix: str, limit: int = 10) -> list[str]:
        if prefix is None:
            raise ValueError("prefix must not be None")
        if limit < 0:
            raise ValueError("limit must be >= 0")

        return self.vocabulary.starts_with(prefix.lower(), limit=limit)

    def search(self, query: str, top_k: int = 5, mode: str = "and") -> list[SearchResult]:
        if query is None:
            raise ValueError("query must not be None")
        if top_k <= 0:
            raise ValueError("top_k must be positive")

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
            score = self._score_document(doc_id, terms)
            topk.push(item_id=doc_id, score=score)

        return [SearchResult(doc_id=item.item_id, score=item.score) for item in topk.items_descending()]

    def _score_document(self, doc_id: str, terms: list[str]) -> float:
        n_docs = self.index.document_count()
        score = 0.0

        for term in terms:
            tf = self.index.term_frequency(doc_id, term)
            if tf == 0:
                continue

            df = self.index.document_frequency(term)
            idf = math.log((n_docs + 1) / (df + 1)) + 1.0
            score += tf * idf

        length = max(self.index.doc_length(doc_id), 1)
        return score / length

    def _rebuild_vocabulary(self) -> None:
        """Rebuild trie from indexed documents to keep suggestions consistent."""
        self.vocabulary = Trie()
        for _, text in self.index.documents():
            for term in self.index.tokenize(text):
                self.vocabulary.insert(term)
