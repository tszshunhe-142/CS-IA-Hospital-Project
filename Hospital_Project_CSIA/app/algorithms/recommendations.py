"""Weighted lecture similarity and top-related-lecture selection."""

from app.algorithms.search import merge_sort_by_score


SIMILARITY_WEIGHTS = {
    "tags": 0.40,
    "topics": 0.30,
    "category": 0.20,
    "department": 0.10,
}
MAX_RECOMMENDATIONS = 3


def _as_set(values):
    """Normalize database comma-separated text or a collection to a set."""
    if values is None:
        return set()
    if isinstance(values, str):
        values = values.split(",")
    return {str(value).strip().casefold() for value in values if str(value).strip()}


def jaccard_similarity(first_values, second_values):
    """Return shared-set size divided by combined-set size; empty sets score 0."""
    first_set = _as_set(first_values)
    second_set = _as_set(second_values)
    union = first_set | second_set
    if not union:
        return 0.0
    return len(first_set & second_set) / len(union)


def _exact_match_similarity(first_value, second_value):
    """Return 1 for equal, non-empty category/department values; otherwise 0."""
    first_text = str(first_value or "").strip().casefold()
    second_text = str(second_value or "").strip().casefold()
    return 1.0 if first_text and first_text == second_text else 0.0


def calculate_similarity_score(current_lecture, other_lecture):
    """Calculate a weighted score in the range 0..1 for two lectures."""
    tag_similarity = jaccard_similarity(
        current_lecture.get("tags"), other_lecture.get("tags")
    )
    topic_similarity = jaccard_similarity(
        current_lecture.get("topics"), other_lecture.get("topics")
    )
    category_similarity = _exact_match_similarity(
        current_lecture.get("category"), other_lecture.get("category")
    )
    department_similarity = _exact_match_similarity(
        current_lecture.get("department"), other_lecture.get("department")
    )

    return (
        tag_similarity * SIMILARITY_WEIGHTS["tags"]
        + topic_similarity * SIMILARITY_WEIGHTS["topics"]
        + category_similarity * SIMILARITY_WEIGHTS["category"]
        + department_similarity * SIMILARITY_WEIGHTS["department"]
    )


def recommend_lectures(current_lecture, lectures, limit=MAX_RECOMMENDATIONS):
    """Return up to three positive-score matches, excluding the current lecture."""
    current_id = current_lecture.get("lecture_id")
    scored_lectures = []

    for lecture in lectures:
        lecture_id = lecture.get("lecture_id")
        if current_id is not None and lecture_id == current_id:
            continue
        if current_id is None and lecture is current_lecture:
            continue

        score = calculate_similarity_score(current_lecture, lecture)
        if score > 0:
            recommendation = dict(lecture)
            recommendation["similarity_score"] = score
            scored_lectures.append(recommendation)

    ranked_lectures = merge_sort_by_score(scored_lectures, "similarity_score")
    requested_limit = max(0, int(limit))
    return ranked_lectures[: min(requested_limit, MAX_RECOMMENDATIONS)]
