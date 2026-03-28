from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass
class Posting:
    doc_id: str
    term_frequency: int


class InvertedIndex:
    """Hash-based inverted index storing posting lists and term statistics."""

    def __init__(self) -> None:
        self._postings: dict[str, dict[str, int]] = defaultdict(dict)
        self._documents: dict[str, str] = {}
        self._doc_lengths: dict[str, int] = {}

    def add_document(self, doc_id: str, text: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")
        if text is None:
            raise ValueError("text must not be None")

        if doc_id in self._documents:
            self.remove_document(doc_id)

        terms = self.tokenize(text)
        term_counts: dict[str, int] = defaultdict(int)
        for term in terms:
            term_counts[term] += 1

        for term, count in term_counts.items():
            self._postings[term][doc_id] = count

        self._documents[doc_id] = text
        self._doc_lengths[doc_id] = len(terms)

    def remove_document(self, doc_id: str) -> None:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")

        if doc_id not in self._documents:
            return

        for term in list(self._postings.keys()):
            if doc_id in self._postings[term]:
                del self._postings[term][doc_id]
            if not self._postings[term]:
                del self._postings[term]

        del self._documents[doc_id]
        del self._doc_lengths[doc_id]

    def get_postings(self, term: str) -> list[Posting]:
        docs = self._postings.get(term.lower(), {})
        return [Posting(doc_id=doc_id, term_frequency=tf) for doc_id, tf in docs.items()]

    def search_and(self, terms: list[str]) -> set[str]:
        normalized = [t.lower() for t in terms if t]
        if not normalized:
            return set()

        posting_sets = [set(self._postings.get(term, {}).keys()) for term in normalized]
        if not posting_sets:
            return set()
        return set.intersection(*posting_sets)

    def search_or(self, terms: list[str]) -> set[str]:
        normalized = [t.lower() for t in terms if t]
        if not normalized:
            return set()

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
        """Return a snapshot of all indexed documents as (doc_id, text)."""
        return list(self._documents.items())

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())
