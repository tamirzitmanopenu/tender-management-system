from flask import Blueprint, jsonify, current_app

from utilities import require_params, log_event, actor_from_headers

bp = Blueprint("businesses", __name__)


# Add a new business נתיב להוספת עסק חדש
@bp.post("/businesses")
def add_business():
    data, err = require_params("company_name", "business_id")
    if err:
        return err

    service = current_app.config["BusinessService"]
    if service.business_exists(data["business_id"]):
        return {"error": "business_id already exists", "business_id": data["business_id"]}, 409

    service.insert_business(data["business_id"], data["company_name"])

    log_event(
        f"A new business was added, {data['company_name']} with business_id: {data['business_id']}"
    )
    return jsonify({"business_id": data["business_id"]}), 201


# List all businesses רשימת כל העסקים
@bp.get("/businesses")
def list_businesses():
    service = current_app.config["BusinessService"]
    rows = service.list_all_businesses()
    return jsonify({
        'status': 'success',
        'data': rows
    }), 200


@bp.post("/businesses-category-selections")
def add_business_category_selection():
    data, err = require_params("project_id", "items")
    if err:
        return err

    project_id = str(data["project_id"])
    items = data["items"]

    if not isinstance(items, list) or not items:
        return jsonify({"error": "items must be a non-empty list"}), 400

    service = current_app.config["BusinessCategoryService"]

    created = []
    try:
        for i, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                log_event(f"[BusinessCategorySelection][ERROR] item #{i} must be an object", level="WARNING")
                return jsonify({"error": f"item #{i} must be an object"}), 400

            if "business_category_id" not in item:
                log_event(f"[BusinessCategorySelection][ERROR] item #{i} missing business_category_id", level="WARNING")
                return jsonify({"error": f"item #{i} missing business_category_id"}), 400

            business_category_id = str(item["business_category_id"])

            selection_id = service.insert_business_category_selection(
                business_category_id=business_category_id,
                project_id=project_id
            )

            created.append({"business_category_id": business_category_id, "selection_id": selection_id})

        log_event(
            f"[BusinessCategorySelection] batch created. project_id={project_id}, count={len(created)}"
        )
        return jsonify({"project_id": project_id, "created": created}), 201

    except Exception as e:
        log_event(f"[BusinessCategorySelection][ERROR] batch create failed: {e}", level="ERROR")
        return jsonify({"error": "Failed to create business category selections"}), 500


@bp.get("/businesses-category-selections")
def list_business_category_selection():
    data, err = require_params()
    if err:
        return err

    business_category_id = data.get("business_category_id", None)
    project_id = data.get("project_id", None)

    service = current_app.config["BusinessCategoryService"]
    rows = service.get_business_category_selection(business_category_id, project_id)
    return jsonify({
        'status': 'success',
        'data': rows
    }), 200


# Get business category מידע על דירוג ספק בקטגוריה
@bp.get("/business-category")
def get_business_category():
    data, err = require_params()
    if err:
        return err

    business_id = data.get("business_id", None)
    category_id = data.get("category_id", None)

    service = current_app.config["BusinessCategoryService"]
    try:
        results = service.get_business_category(business_id=business_id, category_id=category_id)
        return jsonify({
            'status': 'success',
            'data': results
        }), 200
    except Exception as e:
        log_event(f"[BusinessCategory][ERROR] Retrieval failed: {e}", level="ERROR")
        return jsonify({"error": "Failed to retrieve business category"}), 500


@bp.post("/business-category")
def add_business_category():
    data, err = require_params("business_id", "category_id")
    if err:
        return err

    rated_employee_username = actor_from_headers()

    service = current_app.config["BusinessCategoryService"]

    try:
        business_category_id = service.insert_business_category(
            business_id=data["business_id"],
            category_id=data["category_id"],
            rated_employee_username=rated_employee_username,
            review=data.get("review"),
            rating_score=data.get("rating_score"),
            supplier_contact_username=data.get("supplier_contact_username"),
        )

        log_event(
            f"BusinessCategory created for business_id={data['business_id']} and category_id={data['category_id']} → ID: {business_category_id}"
        )

        return jsonify({
            "business_category_id": business_category_id
        }), 201

    except Exception as e:
        log_event(f"[BusinessCategory][ERROR] Insertion failed: {e}", level="ERROR")
        return jsonify({"error": "Failed to create business category"}), 500
