# Phase 4 Presentation Script (Conversational)

## Slide 1: Title
"Hi everyone, thanks for being here.
I’m presenting my phase 4 project on developing and optimizing data structures in Python, using a search engine example.
The whole idea was to build something that doesn’t just work, but works efficiently when data keeps changing and users keep searching."

## Slide 2: Problem and Context
"So, why search engine?
Because it’s one of the clearest real-world cases where data structures really matter.
If your structure is weak, search gets slow, updates are painful, and ranking is inconsistent.
So the challenge here was balancing speed, updates, and good search results."

## Slide 3: Data Structure Choices
"I used three main structures, and each one has a clear job.
The inverted index handles fast retrieval, the trie handles prefix suggestions, and the top-k heap handles ranking efficiently.
Instead of one giant complicated structure, I used a pipeline where each piece does one thing well."

## Slide 4: Phase 1 Design Rationale
"In phase 1, the focus was design decisions.
I chose hash-based indexing for quick lookups, trie traversal for prefix matching, and heap-based selection for top results.
The goal wasn’t to be fancy, it was to match each operation with the best structure."

## Slide 5: Phase 2 Proof of Concept
"Phase 2 was basically: can this architecture work end to end?
At that point I had document add/remove, AND/OR search, and prefix suggestions working.
That gave me a clean baseline before optimization."

## Slide 6: Phase 3 Optimizations
"Phase 3 is where most performance improvements happened.
I stopped rebuilding things unnecessarily and switched to incremental updates.
I made deletion more targeted, improved AND query ordering, and added IDF caching for repeated TF-IDF scoring.
So the pattern was simple: do less repeated work."

## Slide 7: Ranking Methods
"I supported both TF-IDF and BM25.
TF-IDF is a solid baseline and easy to explain.
BM25 is usually stronger for retrieval quality because it accounts for term saturation and document length.
Having both gave me flexibility and better evaluation."

## Slide 8: Testing and Validation
"I didn’t want this to be a demo that only works once.
So I added tests for retrieval, updates, edge cases, suggestions, ranking behavior, and scaling.
That way I could verify correctness and stability, not just happy-path behavior."

## Slide 9: Test Execution Results
"These are actual test run results, not assumptions.
I ran the full unittest discovery command, and the suite passed with 17 out of 17 tests, no failures.
That includes data structures, search engine logic, and scaling tests."

## Slide 10: Performance Discussion
"The optimization story is really about efficiency through structure.
Incremental updates reduced rebuild cost, targeted deletion avoided unnecessary scans, and caching reduced repeated scoring overhead.
So query responsiveness improved without making the code hard to maintain."

## Slide 11: Algorithm Overview and Sample Output
"If we simplify the flow, it’s this: tokenize, build candidates, score candidates, keep top-k.
The key idea is we never score everything.
For example, in my demo set, search index returns doc-002, and search graph returns doc-001, doc-002, and doc-004.
So the pipeline behaves exactly as intended."

## Slide 12: Strengths and Limitations
"Strengths are modularity, clear structure, and reliable behavior under updates and search.
Limitations are mostly scope-related: no compression layer, no persistence, no distributed design yet.
So this is a strong optimized prototype, but not pretending to be production-complete."

## Slide 13: Future Work
"Next steps are pretty clear: phrase or proximity queries, metadata filtering, posting compression, and persistent storage.
Those changes would move this from a course-level search engine to something much closer to production expectations."

## Slide 14: Closing
"To wrap up, this project shows that good data structure choices directly improve performance, scalability, and maintainability.
The final system is correct, tested, and optimized in meaningful ways.
Thanks for listening, and I’m happy to answer questions."