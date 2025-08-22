from flask import Blueprint, jsonify

from utilities import require_json, log_event
from app.services.category_service import (
    normalized, category_by_normalized, category_id_exists,
    insert_category, insert_category_with_id, list_categories
)

bp = Blueprint("categories", __name__)


@bp.post("/categories")
def add_category():
    data, err = require_json("category_name")
    if err: return err

    name = normalized(data["category_name"])
    if not name:
        return {"error": "category_name cannot be empty"}, 400

    dup = category_by_normalized(name)
    if dup:
        return {"error": "category_name already exists", "category_id": dup["category_id"]}, 409

    if "category_id" in data and data["category_id"] is not None:
        if category_id_exists(data["category_id"]):
            return {"error": "category_id already exists", "category_id": data["category_id"]}, 409
        insert_category_with_id(data["category_id"], name)
        new_id = data["category_id"]
    else:
        new_id = insert_category(name)

    log_event(f"A new category was added, {name} with category_id: {new_id}")
    return jsonify({"category_id": new_id}), 201


@bp.get("/categories")
def get_categories():
    return jsonify(list_categories())
