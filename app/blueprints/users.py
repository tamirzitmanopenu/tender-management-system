from flask import Blueprint, jsonify, current_app

from utilities import require_params, log_event

bp = Blueprint("users", __name__)

@bp.get("/permissions")
def get_permissions():
    """
    מחזיר רשימת כל ההרשאות במערכת
    """
    try:
        user_service = current_app.config["UserService"]
        permissions = user_service.get_all_permissions()
        log_event(f"[Permissions] Retrieved all permissions")
        return jsonify(permissions), 200
    except Exception as e:
        log_event(f"[Permissions][ERROR] Failed to retrieve permissions: {e}", level="ERROR")
        return jsonify({"error": "Failed to retrieve permissions"}), 500



@bp.get("/user/details")
def get_user():
    data, err = require_params("username")
    if err:
        return err
    username = data.get("username", None)
    service = current_app.config["UserService"]
    try:
        user_details = service.get_full_user_details(username=username)
        log_event(f"[User] Retrieved details for username={username}")
        return jsonify({
            'status': 'success',
            'data': user_details
        }), 200
    except Exception as e:
        log_event(f"[User][ERROR] Retrieval failed for username={username}: {e}", level="ERROR")
        return jsonify({"error": "Failed to retrieve user details"}), 500

@bp.get("/user/business-categories")
def get_user_business_categories():
    data, err = require_params("username")
    if err:
        return err
    username = data.get("username", None)
    service = current_app.config["UserService"]
    bc_service = current_app.config["BusinessCategoryService"]

    try:
        user_details = service.get_full_user_details(username=username)
        log_event(f"[User] Retrieved details for username={username}")
        business_categories = bc_service.get_business_category(business_id=user_details['business_id'])
        log_event(f"[User] Retrieved business categories for username={username}")
        return jsonify({
            'status': 'success',
            'data': business_categories
        }), 200
    except Exception as e:
        log_event(f"[User][ERROR] Business categories retrieval failed for username={username}: {e}", level="ERROR")
        return jsonify({"error": "Failed to retrieve user business categories"}), 500

@bp.get("/user/accessible-projects")
def get_user_accessible_projects():
    data, err = require_params("username")
    if err:
        return err
    username = data.get("username", None)
    user_service = current_app.config["UserService"]
    bc_service = current_app.config["BusinessCategoryService"]
    project_service = current_app.config["ProjectService"]

    try:
        user_details = user_service.get_full_user_details(username=username)
        business_categories = bc_service.get_business_category(business_id=user_details['business_id'])
        
        # Get projects based on business category selections
        accessible_projects = project_service.get_projects_by_business_categories(business_categories)
        
        log_event(f"[User] Retrieved accessible projects for username={username}")
        return jsonify({
            'status': 'success',
            'data': accessible_projects
        }), 200
    except Exception as e:
        log_event(f"[User][ERROR] Accessible projects retrieval failed for username={username}: {e}", level="ERROR")
        return jsonify({"error": "Failed to retrieve accessible projects"}), 500