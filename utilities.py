from datetime import datetime, UTC

from db import execute
from flask import request, jsonify


def now_iso():
    return datetime.now(UTC).isoformat(timespec="seconds")


def log_event(username, message, level="INFO"):
    execute(
        "INSERT INTO Log (username, message, level, date) VALUES (?, ?, ?, ?)",
        (username, message, level, now_iso()),
    )


def require_json(*fields):
    data = request.get_json(silent=True) or {}
    missing = [f for f in fields if f not in data]
    if missing:
        return None, (jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400)
    return data, None
