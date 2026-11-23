"""Flask application factory for the health education platform."""

from pathlib import Path

import mysql.connector
from flask import Flask, abort, render_template, request

from app.algorithms.filtering import filter_lectures
from app.algorithms.recommendations import recommend_lectures
from app.algorithms.search import rank_search_results
from app.data import get_lecture, get_lectures


def create_app():
    """Create and configure the web application."""
    app = Flask(__name__)

    def load_lectures(limit=None):
        """Keep a database setup problem visible without crashing the page."""
        try:
            return get_lectures(limit=limit), None
        except (mysql.connector.Error, KeyError, ValueError) as error:
            app.logger.warning("Could not load lectures from MySQL: %s", error)
            return [], "Lectures are temporarily unavailable. Check the MySQL settings in the README."

    @app.get("/")
    def home():
        all_lectures, database_message = load_lectures()
        return render_template(
            "index.html",
            lectures=all_lectures[:3],
            more_lectures=all_lectures[3:5],
            database_message=database_message,
        )

    @app.get("/lectures")
    def lecture_list():
        all_lectures, database_message = load_lectures()
        query = request.args.get("q", "").strip()
        department = request.args.get("department", "").strip()
        category = request.args.get("category", "").strip()
        date_from = request.args.get("date_from", "").strip()
        date_to = request.args.get("date_to", "").strip()
        filter_error = None

        try:
            filtered_lectures = filter_lectures(
                all_lectures,
                department=department,
                category=category,
                date_from=date_from,
                date_to=date_to,
            )
            lectures = rank_search_results(filtered_lectures, query)
        except ValueError as error:
            filter_error = str(error)
            lectures = []

        departments = sorted(
            {lecture["department"] for lecture in all_lectures if lecture.get("department")},
            key=str.casefold,
        )
        categories = sorted(
            {lecture["category"] for lecture in all_lectures if lecture.get("category")},
            key=str.casefold,
        )
        return render_template(
            "lectures.html",
            lectures=lectures,
            database_message=database_message,
            query=query,
            department=department,
            category=category,
            date_from=date_from,
            date_to=date_to,
            departments=departments,
            categories=categories,
            filter_error=filter_error,
        )

    @app.get("/lectures/<int:lecture_id>")
    def lecture_detail(lecture_id):
        try:
            lecture = get_lecture(lecture_id)
            all_lectures = get_lectures() if lecture is not None else []
        except (mysql.connector.Error, KeyError, ValueError) as error:
            app.logger.warning("Could not load lecture from MySQL: %s", error)
            return render_template("lecture_detail.html", lecture=None, database_error=True), 503

        if lecture is None:
            abort(404)

        related_lectures = recommend_lectures(lecture, all_lectures)

        # Only serve video files stored inside app/static; external URLs are not used.
        video_path = lecture.get("video_location") or ""
        static_root = Path(app.static_folder).resolve()
        candidate = (static_root / video_path).resolve()
        lecture["video_url"] = (
            "/static/" + candidate.relative_to(static_root).as_posix()
            if candidate.is_relative_to(static_root) and candidate.is_file()
            else None
        )
        return render_template(
            "lecture_detail.html",
            lecture=lecture,
            related_lectures=related_lectures,
            database_error=False,
        )

    return app
