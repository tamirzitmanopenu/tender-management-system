from flask import Blueprint, jsonify, current_app, request

from utilities import require_json, log_event, actor_from_headers

bp = Blueprint("offers", __name__)


@bp.post("/offers")
def add_offer():
    service = current_app.config["OfferService"]

    data, err = require_json("project_id", "business_category_id", "items")
    if err:
        return err

    supplier_username = actor_from_headers()
    project_id = str(data["project_id"])
    business_category_id = str(data["business_category_id"])
    items = data["items"]

    if not isinstance(items, list) or not items:
        return jsonify({"error": "items must be a non-empty list"}), 400

    try:
        total_offer_id = service.insert_total_offer(
            supplier_username=supplier_username,
            project_id=project_id,
            business_category_id=business_category_id,
        )
        log_event(
            f"[TotalOffer] created by '{supplier_username}', "
            f"project_id={project_id}, business_category_id={business_category_id}, "
            f"total_offer_id={total_offer_id}"
        )
    except Exception as e:
        log_event(f"[TotalOffer][ERROR] failed to create: {e}", level="ERROR")
        return jsonify({"error": "Failed to create total offer"}), 500

    created = []
    try:
        for i, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                log_event(f"[TaskOffer][ERROR] item #{i} must be an object", level="WARNING")
                return jsonify({"error": f"item #{i} must be an object"}), 400

            if "project_task_id" not in item or "price_offer" not in item:
                log_event(f"[TaskOffer][ERROR] item #{i} missing project_task_id or price_offer", level="WARNING")
                return jsonify({"error": f"item #{i} missing project_task_id or price_offer"}), 400

            try:
                project_task_id = str(item["project_task_id"])
                price_offer = float(item["price_offer"])
            except (TypeError, ValueError):
                log_event(f"[TaskOffer][ERROR] item #{i} invalid price_offer", level="WARNING")
                return jsonify({"error": f"item #{i} has invalid price_offer"}), 400

            # יצירת השורה בפועל
            task_offer_id = service.insert_task_offer(
                total_offer_id=total_offer_id,
                project_task_id=project_task_id,
                price_offer=price_offer
            )


            created.append({"project_task_id": project_task_id, "task_offer_id": task_offer_id})

        log_event(
            f"[TaskOffer] batch created by '{supplier_username}'. "
            f"total_offer_id={total_offer_id}, count={len(created)}"
        )
        return jsonify({"total_offer_id": total_offer_id, "created": created}), 201

    except Exception as e:
        log_event(f"[TaskOffer][ERROR] batch create failed: {e}", level="ERROR")
        return jsonify({"error": "Failed to create task offers"}), 500