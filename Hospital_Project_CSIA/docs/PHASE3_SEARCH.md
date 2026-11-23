# Phase 3: Search, relevance, sorting, and filters

## Keyword search

The search form sends a GET request to `/lectures` using the `q` parameter. `tokenize_query` converts the query to lowercase words and removes repeated words. Search is case-insensitive. A lecture matches when every distinct query word appears in at least one of its searchable fields. Different words may match different fields, so `heart health` can match `heart` in the title and `health` in a tag.

For each query word, the algorithm checks the lecture's title, tags, category, speaker, department, and description. If a word appears in a field, that field's weight is added once for that word. Repeating a word in the query does not increase its score. Matching several fields or query words adds their weights together.

| Field | Weight | Reason |
| --- | ---: | --- |
| Title | 5 | A title is a direct, specific summary of a lecture. |
| Tags | 4 | Tags are deliberately assigned to describe the lecture. |
| Category | 3 | A category identifies its broad subject. |
| Speaker | 2 | A speaker name can be a useful but narrower search. |
| Department | 2 | Department narrows the source area. |
| Description | 1 | Descriptions provide context, but broad words can occur often. |

The weights are kept together in `app/algorithms/search.py`, making them easy to explain and adjust.

## Merge Sort

`merge_sort_by_relevance` splits a list into halves until each part contains at most one lecture. It then merges the parts in descending score order. When two scores are equal, it takes the item from the left half first, so the sort is stable and preserves the original order among ties. The implementation does not use Python's built-in `sorted()` or `list.sort()` for relevance ranking.

For `n` lectures, Merge Sort takes **O(n log n)** time. Its recursive merge process uses **O(n)** additional space. Relevance scoring is performed before sorting; its work also depends on the query word count and the text lengths of the six fields.

An empty or punctuation-only query returns all filtered lectures in their existing database order with score zero. A non-empty query with no matching lecture returns an empty result list.

## Filters

The GET form submits the keyword, department, category, start date, and end date together. The filtering module applies all selected conditions to each lecture before ranking. Department and category are case-insensitive exact matches. Date range endpoints are inclusive. Invalid ISO dates and a start date later than the end date produce a validation message. The Clear all link opens `/lectures` without query parameters.

## Testing

Run `python -m unittest discover -s tests -v` from the project root. The tests check:

1. Title and tag search, plus category, speaker, department, and description search.
2. Case-insensitive queries and expected additive field weights.
3. Descending Merge Sort order and stable ordering for equal scores.
4. No matches and an empty keyword.
5. Department, category, and inclusive date filters.
6. Search combined with multiple filters, invalid date ranges, and empty-result UI.
7. Flask routes retaining filter parameters and rendering search results.

The current development run completed **16 tests successfully**. Algorithm tests use fictional records in memory. Flask route tests mock only the lecture data access call; they verify route/template behavior, not MySQL availability. Real database connectivity is checked separately by calling `get_lectures()` in the configured application environment.
