"""Database queries used by the Flask routes."""

from app.database.connection import get_connection


def get_lectures(limit=None):
    """Return lecture rows with their tags, newest lecture first."""
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT l.lecture_id, l.title, l.speaker, l.department,
                   l.lecture_date, l.category, l.description, l.video_location,
                   COALESCE(GROUP_CONCAT(DISTINCT t.name ORDER BY t.name SEPARATOR ', '), '') AS tags,
                   COALESCE(GROUP_CONCAT(DISTINCT tp.name ORDER BY tp.name SEPARATOR ', '), '') AS topics
            FROM lectures AS l
            LEFT JOIN lecture_tags AS lt ON lt.lecture_id = l.lecture_id
            LEFT JOIN tags AS t ON t.tag_id = lt.tag_id
            LEFT JOIN lecture_topics AS ltp ON ltp.lecture_id = l.lecture_id
            LEFT JOIN topics AS tp ON tp.topic_id = ltp.topic_id
            GROUP BY l.lecture_id
            ORDER BY l.lecture_date DESC, l.lecture_id DESC
        """
        if limit is not None:
            query += " LIMIT %s"
            cursor.execute(query, (limit,))
        else:
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_lecture(lecture_id):
    """Return one lecture and its tags, or None when it does not exist."""
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT l.lecture_id, l.title, l.speaker, l.department,
                   l.lecture_date, l.category, l.description, l.video_location,
                   COALESCE(GROUP_CONCAT(DISTINCT t.name ORDER BY t.name SEPARATOR ', '), '') AS tags,
                   COALESCE(GROUP_CONCAT(DISTINCT tp.name ORDER BY tp.name SEPARATOR ', '), '') AS topics
            FROM lectures AS l
            LEFT JOIN lecture_tags AS lt ON lt.lecture_id = l.lecture_id
            LEFT JOIN tags AS t ON t.tag_id = lt.tag_id
            LEFT JOIN lecture_topics AS ltp ON ltp.lecture_id = l.lecture_id
            LEFT JOIN topics AS tp ON tp.topic_id = ltp.topic_id
            WHERE l.lecture_id = %s
            GROUP BY l.lecture_id
            """,
            (lecture_id,),
        )
        return cursor.fetchone()
    finally:
        connection.close()
