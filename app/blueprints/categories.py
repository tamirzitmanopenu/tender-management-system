from flask import Blueprint, jsonify, current_app

from utilities import require_json, log_event

bp = Blueprint("categories", __name__)

# Add a new category נתיב להוספת קטגוריה חדשה
@bp.post("/categories")
def add_category():
    data, err = require_json("category_name")
    if err:
        return err

    service = current_app.config["CategoryService"]
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

# List all categories רשימת כל הקטגוריות
@bp.get("/categories")
def get_categories():
    service = current_app.config["CategoryService"]
    return jsonify(service.list_categories())
