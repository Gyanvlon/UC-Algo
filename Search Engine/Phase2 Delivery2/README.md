# uc-algo

Phase 2 (Proof of Concept) implementation for the project "Developing and Optimizing Data Structures for Real-World Applications Using Python."

## Chosen Application Context

Search engine retrieval and query assistance.

## Implemented Data Structures

1. Hash-based inverted index for document retrieval.
2. Trie for prefix-based term suggestions.
3. Fixed-size top-k min-heap for ranked result selection.

## Project Structure

1. src/uc_algo/data_structures/inverted_index.py
2. src/uc_algo/data_structures/trie.py
3. src/uc_algo/data_structures/topk_heap.py
4. src/uc_algo/app/search_engine.py
5. main.py
6. tests/test_data_structures.py
7. tests/test_search_engine.py
8. phase2_report.md

## Phase 2 PoC Features

1. Document insertion, replacement, and deletion.
2. AND and OR query retrieval over an inverted index.
3. TF-IDF-style ranking with top-k selection.
4. Prefix term suggestion using a trie.
5. Input validation and edge-case handling.
6. Unit tests for data structures and integrated search behavior.

## Run Demo

```bash
python main.py
```

The demo indexes four sample documents, executes both AND and OR queries, prints top-ranked results, shows prefix suggestions, removes a document, and re-runs a query.

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

