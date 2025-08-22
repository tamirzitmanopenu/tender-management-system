from flask import Blueprint, jsonify

from utilities import require_json, log_event
from app.services.category_service import CategoryService
from db.db import get_db

bp = Blueprint("categories", __name__)


@bp.post("/categories")
def add_category():
    data, err = require_json("category_name")
    if err:
        return err

    service = CategoryService(get_db())
    name = service.normalized(data["category_name"])
    if not name:
        return {"error": "category_name cannot be empty"}, 400

    dup = service.category_by_normalized(name)
    if dup:
        return {"error": "category_name already exists", "category_id": dup["category_id"]}, 409

    if "category_id" in data and data["category_id"] is not None:
        if service.category_id_exists(data["category_id"]):
            return {"error": "category_id already exists", "category_id": data["category_id"]}, 409
        service.insert_category_with_id(data["category_id"], name)
        new_id = data["category_id"]
    else:
        new_id = service.insert_category(name)

    log_event(f"A new category was added, {name} with category_id: {new_id}")
    return jsonify({"category_id": new_id}), 201


@bp.get("/categories")
def get_categories():
    service = CategoryService(get_db())
    return jsonify(service.list_categories())
