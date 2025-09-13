from flask import Blueprint, jsonify, current_app

from utilities import require_params, log_event

bp = Blueprint("users", __name__)

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