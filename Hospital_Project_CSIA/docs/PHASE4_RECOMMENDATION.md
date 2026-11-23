# Phase 4: Related lecture recommendations

## Purpose and data

When a viewer opens a lecture detail page, the application compares it with the other lectures and displays up to three related results. The existing MySQL schema already stores tags in `tags`/`lecture_tags` and topics in `topics`/`lecture_topics`, so Phase 4 reuses these relationships without changing the schema. The lecture data access queries now return both values as comma-separated strings.

## Similarity calculation

Tags and topics are converted to lowercase sets. Jaccard Similarity is the number of shared values divided by the number of distinct values in either set:

`J(A, B) = |A ∩ B| / |A ∪ B|`

If both sets are empty, their similarity is defined as 0. Category and department use exact case-insensitive matching: equal non-empty values score 1; different or empty values score 0.

The weighted score is:

`tags × 0.40 + topics × 0.30 + category × 0.20 + department × 0.10`

Tags receive the greatest weight because they describe a lecture's specific subject. Topics also describe subject matter but are broader, so they receive 30%. Category describes a broad classification and department indicates the source organization, so they receive 20% and 10%. The weights are defined in `app/algorithms/recommendations.py` and sum to 1, keeping scores between 0 and 1.

## Ranking and top 3

The algorithm excludes the current lecture by its database ID and discards candidates with a score of 0. It passes the remaining copies with a `similarity_score` field to Phase 3's generic `merge_sort_by_score` function. The shared Merge Sort sorts descending and remains stable: equal scores preserve database input order. The result is then limited to three entries. If there are fewer than three positive-score candidates, only those candidates are shown; if there are none, the page says “No related lectures available.”

For `n` candidate lectures, scoring uses the tag/topic set sizes for each comparison, and Merge Sort takes **O(n log n)** time and **O(n)** extra space. The full recommendation process is approximately **O(n × s + n log n)**, where `s` is the average combined tag/topic set size per lecture.

## Display

The lecture detail route loads the current lecture and lecture collection through the existing MySQL data layer, calls the separate recommendation algorithm, and passes its results to the Related Lectures section. Each result links to its own detail page and shows its title, speaker, department, and category. The existing player and lecture information remain in place.

## Tests

Run all tests from the project root with `python -m unittest discover -s tests -v`. Recommendation tests cover identical and partial Jaccard sets, disjoint and empty sets, database comma-separated values, category and department matches, weighted arithmetic, score bounds, descending ranking, stable ties, current-record exclusion, zero-score exclusion, top-3 limiting, and fewer-than-three/no-result cases. Route tests verify recommendation content, links, and the no-related-results message. Route tests use in-memory fictional rows and do not claim to test the MySQL server connection. The Phase 4 changes add 20 tests; the latest full run passed all 36 project tests.
