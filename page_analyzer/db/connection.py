import os
from contextlib import contextmanager

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
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
