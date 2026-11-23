"""Unit tests for lecture similarity and recommendation ranking."""

import unittest

from app.algorithms.recommendations import (
    calculate_similarity_score,
    jaccard_similarity,
    recommend_lectures,
)


def lecture(lecture_id, tags=None, topics=None, category="", department=""):
    return {
        "lecture_id": lecture_id,
        "title": f"Lecture {lecture_id}",
        "tags": tags or [],
        "topics": topics or [],
        "category": category,
        "department": department,
    }


class SimilarityTests(unittest.TestCase):
    def test_identical_tags_and_topics_have_full_set_similarity(self):
        self.assertEqual(1.0, jaccard_similarity(["heart", "health"], ["health", "heart"]))
        self.assertEqual(1.0, jaccard_similarity(["wellness"], ["wellness"]))

    def test_partially_shared_tags_and_topics_use_jaccard_ratio(self):
        self.assertAlmostEqual(1 / 3, jaccard_similarity(["heart", "health"], ["heart", "sleep"]))
        self.assertAlmostEqual(1 / 3, jaccard_similarity(["habits", "prevention"], ["habits", "sleep"]))

    def test_no_shared_tags_or_topics_score_zero(self):
        self.assertEqual(0.0, jaccard_similarity(["heart"], ["sleep"]))
        self.assertEqual(0.0, jaccard_similarity(["cardio"], ["nutrition"]))

    def test_two_empty_sets_have_zero_similarity(self):
        self.assertEqual(0.0, jaccard_similarity([], []))
        self.assertEqual(0.0, jaccard_similarity("", None))

    def test_comma_separated_database_values_are_supported(self):
        self.assertAlmostEqual(
            1 / 3,
            jaccard_similarity("heart, prevention", "HEART, sleep"),
        )

    def test_matching_category_contributes_twenty_percent(self):
        current = lecture(1, category="Wellness")
        other = lecture(2, category="wellness")
        self.assertAlmostEqual(0.2, calculate_similarity_score(current, other))

    def test_different_category_contributes_zero(self):
        current = lecture(1, category="Wellness")
        other = lecture(2, category="Nutrition")
        self.assertEqual(0.0, calculate_similarity_score(current, other))

    def test_matching_department_contributes_ten_percent(self):
        current = lecture(1, department="Cardiology")
        other = lecture(2, department="cardiology")
        self.assertAlmostEqual(0.1, calculate_similarity_score(current, other))

    def test_different_department_contributes_zero(self):
        current = lecture(1, department="Cardiology")
        other = lecture(2, department="Nutrition")
        self.assertEqual(0.0, calculate_similarity_score(current, other))

    def test_weighted_score_adds_all_field_contributions(self):
        current = lecture(1, tags=["a", "b"], topics=[], category="Wellness", department="Cardiology")
        other = lecture(2, tags=["a"], topics=[], category="Wellness", department="Cardiology")
        # Tag Jaccard is 1/2 (0.20); category is 0.20; department is 0.10.
        self.assertAlmostEqual(0.5, calculate_similarity_score(current, other))

    def test_similarity_score_stays_between_zero_and_one(self):
        current = lecture(1, ["a", "b"], ["x", "y"], "Wellness", "Cardiology")
        same = lecture(2, ["a", "b"], ["x", "y"], "Wellness", "Cardiology")
        self.assertGreaterEqual(calculate_similarity_score(current, lecture(3)), 0.0)
        self.assertAlmostEqual(1.0, calculate_similarity_score(current, same))


class RecommendationRankingTests(unittest.TestCase):
    def setUp(self):
        self.current = lecture(1, ["heart", "health"], ["prevention"], "Wellness", "Cardiology")

    def test_recommendations_are_ranked_descending(self):
        candidates = [
            lecture(2, ["heart"], ["prevention"], "", ""),
            lecture(3, ["heart", "health"], ["prevention"], "Wellness", "Cardiology"),
            lecture(4, [], [], "Wellness", ""),
        ]
        results = recommend_lectures(self.current, candidates)
        scores = [item["similarity_score"] for item in results]
        self.assertEqual(sorted(scores, reverse=True), scores)
        self.assertEqual([3, 2, 4], [item["lecture_id"] for item in results])

    def test_equal_scores_keep_input_order(self):
        candidates = [lecture(2, ["heart"], [], "", ""), lecture(3, ["health"], [], "", "")]
        results = recommend_lectures(self.current, candidates)
        self.assertEqual([2, 3], [item["lecture_id"] for item in results])

    def test_current_lecture_is_excluded(self):
        results = recommend_lectures(self.current, [self.current, lecture(2, ["heart"])])
        self.assertNotIn(1, [item["lecture_id"] for item in results])

    def test_zero_score_lectures_are_excluded(self):
        results = recommend_lectures(self.current, [lecture(2, ["sleep"], ["nutrition"], "Other", "Other")])
        self.assertEqual([], results)

    def test_returns_fewer_than_three_when_fewer_are_relevant(self):
        candidates = [lecture(2, ["heart"]), lecture(3, ["sleep"])]
        results = recommend_lectures(self.current, candidates)
        self.assertEqual([2], [item["lecture_id"] for item in results])

    def test_no_relevant_lectures_returns_empty_list(self):
        self.assertEqual([], recommend_lectures(self.current, [lecture(2), lecture(3)]))

    def test_never_returns_more_than_three(self):
        candidates = [lecture(index, ["heart"]) for index in range(2, 8)]
        self.assertEqual(3, len(recommend_lectures(self.current, candidates, limit=10)))


if __name__ == "__main__":
    unittest.main()
