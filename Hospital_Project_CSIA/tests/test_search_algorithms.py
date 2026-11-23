"""Unit tests for weighted keyword scoring, Merge Sort, and filters."""

import unittest
from datetime import date

from app.algorithms.filtering import filter_lectures
from app.algorithms.search import (
    calculate_relevance_score,
    merge_sort_by_relevance,
    rank_search_results,
)


def sample_lectures():
    return [
        {
            "lecture_id": 1,
            "title": "Heart Health Introduction",
            "speaker": "Dr. Heart Chen",
            "department": "Cardiology",
            "lecture_date": date(2025, 1, 10),
            "category": "Heart Health",
            "description": "Learn about heart health and prevention.",
            "tags": "heart, prevention",
        },
        {
            "lecture_id": 2,
            "title": "Healthy Meals",
            "speaker": "Jordan Lee",
            "department": "Nutrition Services",
            "lecture_date": date(2025, 2, 10),
            "category": "Nutrition",
            "description": "Simple hydration and balanced meal ideas.",
            "tags": "nutrition, wellness",
        },
        {
            "lecture_id": 3,
            "title": "Managing Stress",
            "speaker": "Dr. Alex Morgan",
            "department": "Psychiatry",
            "lecture_date": date(2025, 3, 10),
            "category": "Mental Health",
            "description": "A fictional introduction to stress management.",
            "tags": "stress, wellness",
        },
    ]


class SearchAlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.lectures = sample_lectures()

    def test_search_by_title_is_case_insensitive(self):
        results = rank_search_results(self.lectures, "HEART HEALTH")
        self.assertEqual([1], [lecture["lecture_id"] for lecture in results])

    def test_search_by_tags(self):
        results = rank_search_results(self.lectures, "prevention")
        self.assertEqual([1], [lecture["lecture_id"] for lecture in results])

    def test_search_category_speaker_department_and_description(self):
        searches = (("nutrition", 2), ("morgan", 3), ("cardiology", 1), ("hydration", 2))
        for query, expected_id in searches:
            with self.subTest(query=query):
                results = rank_search_results(self.lectures, query)
                self.assertEqual([expected_id], [lecture["lecture_id"] for lecture in results])

    def test_weighted_score_adds_each_matching_field(self):
        self.assertEqual(15, calculate_relevance_score(self.lectures[0], "heart"))

    def test_merge_sort_orders_relevance_descending(self):
        items = [{"relevance_score": score} for score in (2, 9, 4, 0, 9)]
        ranked = merge_sort_by_relevance(items)
        self.assertEqual([9, 9, 4, 2, 0], [item["relevance_score"] for item in ranked])

    def test_equal_scores_keep_their_original_order(self):
        items = [{"name": name, "relevance_score": 5} for name in ("first", "second", "third")]
        ranked = merge_sort_by_relevance(items)
        self.assertEqual(["first", "second", "third"], [item["name"] for item in ranked])

    def test_nonmatching_search_returns_no_results(self):
        self.assertEqual([], rank_search_results(self.lectures, "volcano"))

    def test_empty_keyword_returns_all_in_original_order(self):
        results = rank_search_results(self.lectures, "   ")
        self.assertEqual([1, 2, 3], [lecture["lecture_id"] for lecture in results])
        self.assertTrue(all(lecture["relevance_score"] == 0 for lecture in results))


class LectureFilterTests(unittest.TestCase):
    def setUp(self):
        self.lectures = sample_lectures()

    def test_filter_by_department_case_insensitively(self):
        results = filter_lectures(self.lectures, department="cardiology")
        self.assertEqual([1], [lecture["lecture_id"] for lecture in results])

    def test_filter_by_category(self):
        results = filter_lectures(self.lectures, category="Nutrition")
        self.assertEqual([2], [lecture["lecture_id"] for lecture in results])

    def test_filter_by_inclusive_date_range(self):
        results = filter_lectures(self.lectures, date_from="2025-02-10", date_to="2025-03-10")
        self.assertEqual([2, 3], [lecture["lecture_id"] for lecture in results])

    def test_combine_keyword_with_multiple_filters(self):
        filtered = filter_lectures(
            self.lectures,
            department="Cardiology",
            category="Heart Health",
            date_from="2025-01-01",
            date_to="2025-01-31",
        )
        results = rank_search_results(filtered, "heart")
        self.assertEqual([1], [lecture["lecture_id"] for lecture in results])

    def test_invalid_or_reversed_date_range_is_rejected(self):
        with self.assertRaises(ValueError):
            filter_lectures(self.lectures, date_from="2025-04-01", date_to="2025-01-01")
        with self.assertRaises(ValueError):
            filter_lectures(self.lectures, date_from="not-a-date")


if __name__ == "__main__":
    unittest.main()
