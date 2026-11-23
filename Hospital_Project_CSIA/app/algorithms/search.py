"""Weighted keyword relevance scoring and a stable, manual Merge Sort."""

import re


# Title matches should matter most; descriptive text is useful but less specific.
FIELD_WEIGHTS = (
    ("title", 5),
    ("tags", 4),
    ("category", 3),
    ("speaker", 2),
    ("department", 2),
    ("description", 1),
)


def tokenize_query(query):
    """Return distinct, lowercase query words in the order they were entered."""
    words = re.findall(r"[^\W_]+", (query or "").casefold(), flags=re.UNICODE)
    return list(dict.fromkeys(words))


def _field_text(value):
    """Convert text or a collection of tags into searchable lowercase text."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        value = " ".join(str(item) for item in value)
    return str(value).casefold()


def calculate_relevance_score(lecture, query):
    """Score each distinct query word in every matching weighted field."""
    words = tokenize_query(query)
    if not words:
        return 0

    score = 0
    matched_words = set()
    for word in words:
        for field_name, weight in FIELD_WEIGHTS:
            field_text = _field_text(lecture.get(field_name))
            if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", field_text, flags=re.UNICODE):
                score += weight
                matched_words.add(word)

    # Treat a multiword search as all terms required, even if they occur in
    # different fields (for example, one in the title and another in the tags).
    return score if len(matched_words) == len(words) else 0


def merge_sort_by_relevance(lectures):
    """Return a stable copy sorted from highest relevance score to lowest."""
    return merge_sort_by_score(lectures, "relevance_score")


def merge_sort_by_score(lectures, score_key):
    """Stable descending Merge Sort reusable for any numeric score field."""
    if len(lectures) <= 1:
        return list(lectures)

    midpoint = len(lectures) // 2
    left = merge_sort_by_score(lectures[:midpoint], score_key)
    right = merge_sort_by_score(lectures[midpoint:], score_key)
    return _merge_by_score(left, right, score_key)


def _merge_by_score(left, right, score_key):
    """Merge two descending lists; taking left on ties keeps sorting stable."""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_score = left[left_index].get(score_key, 0)
        right_score = right[right_index].get(score_key, 0)
        if left_score >= right_score:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def rank_search_results(lectures, query):
    """Score matching lectures and rank them; blank searches preserve input order."""
    words = tokenize_query(query)
    ranked = []
    for lecture in lectures:
        result = dict(lecture)
        result["relevance_score"] = calculate_relevance_score(lecture, query)
        if not words or result["relevance_score"] > 0:
            ranked.append(result)

    if not words:
        return ranked
    return merge_sort_by_relevance(ranked)
