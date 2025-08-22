from flask import Blueprint, jsonify

from app.services.project_service import insert_project, list_all_projects
from utilities import require_json, log_event, actor_from_headers

bp = Blueprint("projects", __name__)


@bp.post("/projects")
def add_project():
    data, err = require_json("name", "deadline_date")
    if err: return err
    created_by = actor_from_headers()
    project_id = insert_project(name=data["name"], created_by=created_by, deadline_date=data["deadline_date"])

    log_event(f"A new project was added, {data['name']} with project_id: {project_id}")
    return jsonify({"project_id": project_id}), 201

# @bp.post("/projects/{project_id}/boq")

@bp.get("/projects")
def list_projects():
    return jsonify(list_all_projects())
