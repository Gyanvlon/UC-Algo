# uc-algo

Phase 4 submission for the project "Developing and Optimizing Data Structures for Real-World Applications Using Python."

## Chosen Application Context

Search engine retrieval and query assistance.

## Implemented Data Structures

1. Hash-based inverted index for document retrieval.
2. Trie for prefix-based term suggestions.
3. Fixed-size top-k min-heap for ranked result selection.

## Phase 3 Optimizations Implemented

1. Incremental vocabulary updates using term-level deltas instead of full trie rebuilds.
2. Targeted document deletion using per-document term maps (no full posting scan).
3. Optimized AND queries by intersecting smallest posting lists first.
4. Ranking strategy support for both TF-IDF and BM25.
5. IDF caching with mutation-aware invalidation using index versioning.
6. Index statistics support for scalability analysis: average document length, vocabulary size, and version tracking.

## Project Structure

1. src/uc_algo/data_structures/inverted_index.py
2. src/uc_algo/data_structures/trie.py
3. src/uc_algo/data_structures/topk_heap.py
4. src/uc_algo/app/search_engine.py
5. main.py
6. phase3_benchmark.py
7. tests/test_phase3_scaling.py
8. tests/test_data_structures.py
9. tests/test_search_engine.py
10. docs/phase4_final_report.md
11. docs/phase4_presentation.md

## Phase 3 Validation Features

1. Document insertion, replacement, and deletion.
2. AND and OR query retrieval over an inverted index.
3. TF-IDF and BM25 ranking with top-k selection.
4. Prefix term suggestion using an incrementally maintained trie.
5. Large-dataset integration tests and deletion stress tests.
6. Input validation and edge-case handling.
7. Benchmark script for reproducible performance metrics.

## Phase 4 Submission Artifacts

1. [Final report draft](docs/phase4_final_report.md)
2. [Presentation deck and speaker script](docs/phase4_presentation.md)
3. Existing implementation and test suite from phases 1 through 3

## Submission Notes

1. Replace the GitHub repository placeholder in the report title page with your actual repository link before submitting.
2. Run `python phase3_benchmark.py` locally if you want to paste fresh numeric benchmark results into the report.
3. The phase 4 documents are written to match the existing search engine application and its optimized inverted-index, trie, and top-k heap design.

## Run Demo

```bash
python main.py
```

The demo indexes four sample documents, executes AND/OR retrieval with both TF-IDF and BM25, prints ranked results, shows prefix suggestions, removes a document, and re-runs a query.

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Run Benchmark

```bash
python phase3_benchmark.py
```

Output is printed as CSV-formatted rows:

1. `dataset_size`
2. baseline and optimized build time
3. baseline and optimized query latency (TF-IDF and BM25)
4. baseline and optimized delete time
5. calculated speedup factors

