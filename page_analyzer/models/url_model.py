import os
from contextlib import contextmanager
from datetime import datetime

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import DictCursor

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


@contextmanager
def get_cursor():
    conn = connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=DictCursor)

    try:
        yield cur
        conn.commit()

    finally:
        cur.close()
        conn.close()


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
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (
                    url,
                    datetime.now(),
                ),
            )
            return cur.fetchone()[0]
