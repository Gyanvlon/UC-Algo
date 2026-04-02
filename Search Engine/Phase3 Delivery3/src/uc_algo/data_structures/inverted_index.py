from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(slots=True)
class Posting:
    doc_id: str
    term_frequency: int


@dataclass(frozen=True)
class DocumentDelta:
    """Tracks vocabulary transitions caused by a document mutation."""

    became_present: set[str]
    became_absent: set[str]


class InvertedIndex:
    """Hash-based inverted index storing posting lists and term statistics."""

    def __init__(self) -> None:
        self._postings: dict[str, dict[str, int]] = defaultdict(dict)
        self._documents: dict[str, str] = {}
        self._doc_term_counts: dict[str, dict[str, int]] = {}
        self._doc_lengths: dict[str, int] = {}
        self._total_terms = 0
        self._version = 0

    def add_document(self, doc_id: str, text: str) -> DocumentDelta:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")
        if text is None:
            raise ValueError("text must not be None")

        terms = self.tokenize(text)
        term_counts: dict[str, int] = defaultdict(int)
        for term in terms:
            term_counts[term] += 1

        old_term_counts = self._doc_term_counts.get(doc_id, {})
        old_terms = set(old_term_counts.keys())
        new_terms = set(term_counts.keys())
        impacted_terms = old_terms | new_terms
        before_df = {
            term: len(self._postings.get(term, {}))
            for term in impacted_terms
        }

        if doc_id in self._documents:
            for term in old_terms:
                postings = self._postings.get(term)
                if postings and doc_id in postings:
                    del postings[doc_id]
                    if not postings:
                        del self._postings[term]
            self._total_terms -= self._doc_lengths[doc_id]

        for term, count in term_counts.items():
            self._postings[term][doc_id] = count

        self._documents[doc_id] = text
        self._doc_term_counts[doc_id] = dict(term_counts)
        self._doc_lengths[doc_id] = len(terms)
        self._total_terms += len(terms)

        after_df = {
            term: len(self._postings.get(term, {}))
            for term in impacted_terms
        }
        self._version += 1

        became_present = {
            term
            for term in impacted_terms
            if before_df.get(term, 0) == 0 and after_df.get(term, 0) > 0
        }
        became_absent = {
            term
            for term in impacted_terms
            if before_df.get(term, 0) > 0 and after_df.get(term, 0) == 0
        }
        return DocumentDelta(became_present=became_present, became_absent=became_absent)

    def remove_document(self, doc_id: str) -> DocumentDelta:
        if not doc_id or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")

        if doc_id not in self._documents:
            return DocumentDelta(became_present=set(), became_absent=set())

        old_term_counts = self._doc_term_counts[doc_id]
        old_terms = set(old_term_counts.keys())
        before_df = {
            term: len(self._postings.get(term, {}))
            for term in old_terms
        }

        for term in old_terms:
            postings = self._postings.get(term)
            if postings and doc_id in postings:
                del postings[doc_id]
                if not postings:
                    del self._postings[term]

        del self._documents[doc_id]
        del self._doc_term_counts[doc_id]
        self._total_terms -= self._doc_lengths[doc_id]
        del self._doc_lengths[doc_id]
        self._version += 1

        after_df = {
            term: len(self._postings.get(term, {}))
            for term in old_terms
        }
        became_absent = {
            term
            for term in old_terms
            if before_df.get(term, 0) > 0 and after_df.get(term, 0) == 0
        }
        return DocumentDelta(became_present=set(), became_absent=became_absent)

    def get_postings(self, term: str) -> list[Posting]:
        docs = self._postings.get(term.lower(), {})
        return [Posting(doc_id=doc_id, term_frequency=tf) for doc_id, tf in docs.items()]

    def search_and(self, terms: list[str]) -> set[str]:
        normalized = list(dict.fromkeys(t.lower() for t in terms if t))
        if not normalized:
            return set()

        posting_sets = [set(self._postings.get(term, {}).keys()) for term in normalized]
        if not posting_sets or any(not postings for postings in posting_sets):
            return set()

        posting_sets.sort(key=len)
        result = posting_sets[0].copy()
        for postings in posting_sets[1:]:
            result.intersection_update(postings)
            if not result:
                break
        return result

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

    def average_doc_length(self) -> float:
        if not self._documents:
            return 0.0
        return self._total_terms / len(self._documents)

    def vocabulary_size(self) -> int:
        return len(self._postings)

    def version(self) -> int:
        return self._version

    def document_terms(self, doc_id: str) -> set[str]:
        return set(self._doc_term_counts.get(doc_id, {}).keys())

    def documents(self) -> list[tuple[str, str]]:
        """Return a snapshot of all indexed documents as (doc_id, text)."""
        return list(self._documents.items())

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())
