from datetime import datetime

from ..db.connection import get_cursor


class URLModel:
    @staticmethod
    def get_urls():
        with get_cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC;")
            return cur.fetchall()

    @staticmethod
    def get_url(id):
        with get_cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            return cur.fetchone()

    @staticmethod
    def find_url_by_name(name):
        with get_cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s;", (name,))
            return cur.fetchone()

    @staticmethod
    def save_url(url):
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id;""",
                (
                    url,
                    datetime.now(),
                ),
            )
            return cur.fetchone()[0]
