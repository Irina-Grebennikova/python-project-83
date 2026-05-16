from datetime import datetime

from ..db.connection import get_cursor


class CheckModel:
    @staticmethod
    def get_checks(url_id):
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC;", (url_id,)
            )
            return cur.fetchall()

    @staticmethod
    def get_last_check(url_id):
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC LIMIT 1;",
                (url_id,),
            )
            return cur.fetchone()

    @staticmethod
    def save_check(data):
        with get_cursor() as cur:
            cur.execute(
                """
                    INSERT INTO url_checks (url_id, status_code, created_at) 
                    VALUES (%s, %s, %s) RETURNING id
                """,
                (
                    data["url_id"],
                    data["status_code"],
                    datetime.now(),
                ),
            )
            return cur.fetchone()[0]
