from flask import Blueprint, jsonify, current_app

from app.services.business_service import BusinessService
from db.db import get_db
from utilities import require_json, log_event

bp = Blueprint("businesses", __name__)


@bp.post("/businesses")
def add_business():
    data, err = require_json("company_name", "business_id")
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


@bp.get("/businesses")
def list_businesses():
    service = current_app.config["BusinessService"]
    rows = service.list_all_businesses()
    return jsonify(rows)
