"""Simple exact-match and inclusive date-range lecture filters."""

from datetime import date, datetime


def _parse_date(value):
    """Accept an ISO date string, date object, or an empty value."""
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError as error:
        raise ValueError("Enter dates in YYYY-MM-DD format.") from error


def filter_lectures(lectures, department="", category="", date_from="", date_to=""):
    """Apply all selected filters together; date endpoints are inclusive."""
    start_date = _parse_date(date_from)
    end_date = _parse_date(date_to)
    if start_date and end_date and start_date > end_date:
        raise ValueError("The start date must be on or before the end date.")

    department_filter = (department or "").strip().casefold()
    category_filter = (category or "").strip().casefold()
    filtered = []

    for lecture in lectures:
        lecture_department = str(lecture.get("department") or "").casefold()
        lecture_category = str(lecture.get("category") or "").casefold()
        lecture_date = _parse_date(lecture.get("lecture_date"))

        if department_filter and lecture_department != department_filter:
            continue
        if category_filter and lecture_category != category_filter:
            continue
        if start_date and (lecture_date is None or lecture_date < start_date):
            continue
        if end_date and (lecture_date is None or lecture_date > end_date):
            continue
        filtered.append(lecture)

    return filtered
