from flask import Blueprint, jsonify

from app.services.business_service import BusinessService
from db.db import get_db
from utilities import require_json, log_event

bp = Blueprint("businesses", __name__)


@bp.post("/businesses")
def add_business():
    data, err = require_json("company_name", "business_id")
    if err:
        return err

    service = BusinessService(get_db())
    if service.business_exists(data["business_id"]):
        return {"error": "business_id already exists", "business_id": data["business_id"]}, 409

    service.insert_business(data["business_id"], data["company_name"])

    # NOTE: fix quoting bug vs original (use single quotes inside f-string).
    log_event(
        f"A new business was added, {data['company_name']} with business_id: {data['business_id']}"
    )
    return jsonify({"business_id": data["business_id"]}), 201


@bp.get("/businesses")
def list_businesses():
    rows = get_db().query_all("SELECT * FROM Business ORDER BY company_name")
    return jsonify(rows)
