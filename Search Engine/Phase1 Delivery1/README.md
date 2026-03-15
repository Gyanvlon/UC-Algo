# uc-algo

Phase 1 implementation for the project "Developing and Optimizing Data Structures for Real-World Applications Using Python."

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
6. phase1_report.md

## Run Demo

```bash
python main.py
```

The demo indexes four sample documents, executes a query, prints top-ranked results, and displays prefix suggestions.

