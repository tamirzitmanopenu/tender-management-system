from datetime import datetime, UTC

from flask import request, jsonify

from db.db import get_db


def now_iso():
    return datetime.now(UTC).isoformat(timespec="seconds")


def actor_from_headers():
    return request.headers.get("X-User")


def log_event(message, username=None, level="INFO"):
    if username is None:
        username = actor_from_headers()
    get_db().execute(
        "INSERT INTO Log (username, message, level, date) VALUES (?, ?, ?, ?)",
        (username, message, level, now_iso()),
    )


def require_json(*fields):
    data = request.get_json(silent=True) or {}
    missing = [f for f in fields if f not in data]
    if missing:
        return None, (jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400)
    return data, None
