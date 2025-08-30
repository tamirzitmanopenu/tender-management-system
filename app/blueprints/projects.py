from flask import Blueprint, jsonify, current_app, request

from utilities import require_json, log_event, actor_from_headers

bp = Blueprint("projects", __name__)


# Add a new project נתיב להוספת פרויקט חדש
@bp.post("/projects")
def add_project():
    service = current_app.config["ProjectService"]
    data, err = require_json("name", "deadline_date")
    if err: return err
    created_by = actor_from_headers()
    project_id = service.insert_project(name=data["name"], created_by=created_by, deadline_date=data["deadline_date"])

    log_event(f"A new project was added, {data['name']} with project_id: {project_id}")
    return jsonify({"project_id": project_id}), 201


# List all projects רשימת כל הפרויקטים
@bp.get("/projects")
def list_projects():
    service = current_app.config["ProjectService"]
    return jsonify(service.list_all_projects())


# Get project details קבלת פרטי פרויקט
@bp.get("/projects/<project_id>")
def get_project(project_id: str):
    service = current_app.config["ProjectService"]
    row = service.get_project_record(project_id)
    if not row:
        return jsonify({"error": f"Could not find project record for project_id {project_id}"}), 400

    return jsonify(row)


@bp.delete("/projects/<project_id>")
def delete_project(project_id: str):
    service = current_app.config["ProjectService"]
    row = service.get_project_record(project_id)
    if not row:
        return jsonify({"error": f"Could not find project record for project_id {project_id}"}), 400

    service.delete_project_record(project_id)
    return jsonify({'deleted': project_id})


# Get tasks
@bp.get("/projects/project_tasks")
def get_project_tasks_by_proj_and_catg():
    service = current_app.config["ProjectTaskService"]

    project_id = request.args.get("project_id")
    category_id = request.args.get("category_id")

    try:
        project_tasks = service.get_project_tasks(project_id, category_id)  # expected: list[dict] or []

        # Normalize to a list
        if project_tasks is None:
            project_tasks = []

        # Exclude IDs from response
        exclude_keys = {"project_id", "category_id"}  # keep both spellings, just in case
        sanitized = [{k: v for k, v in row.items() if k not in exclude_keys} for row in project_tasks]

        # Return 200 with an empty list if nothing matched (friendlier for clients than 400)
        return jsonify({"count": len(sanitized), "items": sanitized}), 200

    except Exception as e:
        current_app.logger.exception(
            "Failed to get project tasks for project_id=%s category_id=%s", project_id, category_id
        )
        return jsonify({"error": "Internal server error"}), 500
