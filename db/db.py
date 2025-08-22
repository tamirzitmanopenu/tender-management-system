# db.py
import sqlite3
from flask import g

DB_PATH = r"db/tender-management-system.db"


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class Database:
    """Simple SQLite wrapper used by the application."""

    def __init__(self, path: str = DB_PATH):
        self.path = path
        self.conn: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self.conn is None:
            conn = sqlite3.connect(self.path)
            conn.row_factory = dict_factory
            conn.execute("PRAGMA foreign_keys = ON;")
            self.conn = conn
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def query_one(self, sql, params=()):
        cur = self.connect().execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row

    def query_all(self, sql, params=()):
        cur = self.connect().execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def execute(self, sql, params=()):
        cur = self.connect().execute(sql, params)
        self.connect().commit()
        last_id = cur.lastrowid
        cur.close()
        return last_id


def get_db() -> Database:
    if "db" not in g:
        g.db = Database()
    return g.db


def close_db(e=None):
    db: Database | None = g.pop("db", None)
    if db is not None:
        db.close()
