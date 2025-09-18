from flask import Blueprint, jsonify, current_app

from utilities import require_params, log_event, actor_from_headers

bp = Blueprint("categories", __name__)


# Add a new category נתיב להוספת קטגוריה חדשה
@bp.post("/categories")
def add_category():
    data, err = require_params("category_name")
    if err:
        return err

    service = current_app.config["CategoryService"]
    name = service.normalized(data["category_name"])
    if not name:
        return {"error": "category_name cannot be empty"}, 400

    category_id_exists = service.category_by_normalized(name)
    if category_id_exists:
        return {"error": "category_name already exists", "category_id": category_id_exists}, 409

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
    data, err = require_params()
    if err:
        return err
    project_id = data.get("project_id", None)
    service = current_app.config["CategoryService"]
    return jsonify(service.list_categories(project_id)), 200        


# List categories by user and project רשימת קטגוריות לפי משתמש ופרויקט
@bp.get("/categories/by-user-and-project")
def get_categories_by_user_and_project():
    data, err = require_params("project_id")
    if err:
        return err
    
    # אם לא סופק username, ניקח מה-header
    username = data.get("username")
    if not username:
        username = actor_from_headers()
        if not username:
            return {"error": "username is required"}, 400
    
    project_id = data["project_id"]
    service = current_app.config["CategoryService"]
    categories = service.list_categories_by_user_and_project(username, project_id)
    return jsonify(categories), 200
