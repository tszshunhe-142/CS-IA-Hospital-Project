"""Route checks for the search form, combined filters, and empty results."""

import unittest
from datetime import date
from unittest.mock import patch

from app import create_app


class SearchRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.lectures = [
            {
                "lecture_id": 1,
                "title": "Heart Health Introduction",
                "speaker": "Dr. Chen",
                "department": "Cardiology",
                "lecture_date": date(2025, 1, 10),
                "category": "Heart Health",
                "description": "Fictional heart education.",
                "video_location": None,
                "tags": "heart, prevention",
            },
            {
                "lecture_id": 2,
                "title": "Healthy Meals",
                "speaker": "Jordan Lee",
                "department": "Nutrition Services",
                "lecture_date": date(2025, 2, 10),
                "category": "Nutrition",
                "description": "Fictional nutrition education.",
                "video_location": None,
                "tags": "nutrition, wellness",
            },
        ]

    def test_search_combined_with_department_category_and_dates(self):
        with patch("app.get_lectures", return_value=self.lectures):
            response = self.client.get(
                "/lectures?q=heart&department=Cardiology&category=Heart+Health"
                "&date_from=2025-01-01&date_to=2025-01-31"
            )
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Heart Health Introduction", response.data)
        self.assertNotIn(b"Healthy Meals", response.data)
        self.assertIn(b"1 result for", response.data)

    def test_no_matches_displays_a_helpful_message(self):
        with patch("app.get_lectures", return_value=self.lectures):
            response = self.client.get("/lectures?q=volcano")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"No lectures match your search and filters", response.data)

    def test_clear_all_link_is_available(self):
        with patch("app.get_lectures", return_value=self.lectures):
            response = self.client.get("/lectures?q=heart")
        self.assertIn(b"Clear all", response.data)
        self.assertIn(b"name=\"date_from\"", response.data)


if __name__ == "__main__":
    unittest.main()
