"""Flask detail page tests for related lectures."""

import unittest
from datetime import date
from unittest.mock import patch

from app import create_app


def make_lecture(lecture_id, title, tags, topics, category, department):
    return {
        "lecture_id": lecture_id,
        "title": title,
        "speaker": f"Dr. Speaker {lecture_id}",
        "department": department,
        "lecture_date": date(2025, 5, lecture_id),
        "category": category,
        "description": "Fictional educational content.",
        "video_location": None,
        "tags": tags,
        "topics": topics,
    }


class RecommendationRouteTests(unittest.TestCase):
    def setUp(self):
        self.current = make_lecture(1, "Current Heart Talk", "heart, prevention", "healthy habits", "Wellness", "Cardiology")
        self.first_related = make_lecture(2, "Related Heart Talk", "heart, prevention", "healthy habits", "Wellness", "Cardiology")
        self.second_related = make_lecture(3, "Related Prevention Talk", "prevention", "healthy habits", "Wellness", "Endocrinology")
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_detail_displays_related_records_and_links(self):
        records = [self.current, self.first_related, self.second_related]
        with patch("app.get_lecture", return_value=self.current), patch("app.get_lectures", return_value=records):
            response = self.client.get("/lectures/1")

        self.assertEqual(200, response.status_code)
        related_section = response.data.split(b'<aside class="related-column">', 1)[1]
        self.assertIn(b"Related Heart Talk", related_section)
        self.assertIn(b"Related Prevention Talk", related_section)
        self.assertNotIn(b"Current Heart Talk", related_section)
        self.assertIn(b"Dr. Speaker 2", related_section)
        self.assertIn(b"Cardiology", related_section)
        self.assertIn(b"Wellness", related_section)
        self.assertIn(b'href="/lectures/2"', related_section)

    def test_detail_shows_message_when_no_related_records_exist(self):
        with patch("app.get_lecture", return_value=self.current), patch("app.get_lectures", return_value=[self.current]):
            response = self.client.get("/lectures/1")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"No related lectures available.", response.data)


if __name__ == "__main__":
    unittest.main()
