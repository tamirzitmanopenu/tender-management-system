import sqlite3
import warnings

from flask import g

DB_PATH = r"db/tender-management-system.db"


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class Database:
    """Simple SQLite wrapper used by the application."""

    def __init__(self, path: str = DB_PATH):
        self.path = path

    def _get_conn(self) -> sqlite3.Connection:
        # one connection per request/thread
        if "db_conn" not in g:
            conn = sqlite3.connect(self.path)
            conn.row_factory = dict_factory
            conn.execute("PRAGMA foreign_keys = ON;")
            g.db_conn = conn
        return g.db_conn

    def query_one(self, sql, params=()):
        cur = self._get_conn().execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row

    def query_all(self, sql, params=()):
        cur = self._get_conn().execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def execute(self, sql, params=()):
        conn = self._get_conn()
        cur = conn.execute(sql, params)
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        return last_id

    def get_table_record(self, table: str, filters: dict | None = None,
                         normalized_fields: list[str] | None = None, query_one_only: bool = False):
        sql = f"SELECT * FROM {table}"
        params = []

        if filters:
            conditions = []
            for field, value in filters.items():
                if normalized_fields and field in normalized_fields:
                    conditions.append(f"LOWER(TRIM({field})) = LOWER(TRIM(?))")
                else:
                    conditions.append(f"{field} = ?")
                params.append(value)

            sql += " WHERE " + " AND ".join(conditions)

        return self.query_one(sql, tuple(params)) if query_one_only else self.query_all(sql, tuple(params))

    def new_table_record(self, table: str, record: dict, returning: str | list[str] | None = None):
        cols = list(record.keys())
        params = tuple(record[c] for c in cols)

        placeholders = ", ".join(["?"] * len(cols))
        col_list = ", ".join(cols)

        sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

        if returning is not None:
            # Normalize RETURNING columns
            if returning == "*" or (isinstance(returning, str) and returning.strip() == "*"):
                returning_sql = "*"
            elif isinstance(returning, str):
                returning_sql = ", ".join([c.strip() for c in returning.split(",") if c.strip()])
            elif isinstance(returning, (list, tuple)):
                returning_sql = ", ".join(returning)
            else:
                raise ValueError("returning must be None, '*', a column name, or a list of columns")
            # Try SQLite RETURNING first (>= 3.35)
            try:
                sql += f" RETURNING {returning_sql}"
                return self.query_one(sql, params)
            except Exception:
                warnings.warn("Could not use return - using older method of SQLite")

        # RETURNING default
        return self.execute(sql, params)


def get_db() -> Database:
    # return a lightweight repo; the actual connection lives in g
    return Database()


def close_db(e=None):
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()
