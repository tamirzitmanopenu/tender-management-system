from flask import Blueprint, jsonify, current_app
from utilities import require_params, log_event

bp = Blueprint("emails", __name__)


@bp.post("/send_email")
def send_email_by_selection_bc():
    data, err = require_params("business_category_selection", "subject", "template_id")
    if err:
        return err

    email_service = current_app.config["EmailService"]
    business_category_service = current_app.config["BusinessCategoryService"]
    user_details = business_category_service.get_business_category_user_contact(
        business_category_selection=data["business_category_selection"])

    cc = data.get("cc", None)
    bcc = data.get("bcc", None)
    try:
        content = email_service.resolve_email_template(template_id=data["template_id"])
        success = email_service.send_email(
            recipient=user_details["email"],
            subject=data["subject"],
            content=content,
            content_type='html',
            cc=cc,
            bcc=bcc
        )

        if success:
            log_event(
                f"Project email sent: '{data['subject']}' for business_category_selection {data['business_category_selection']}")
            return jsonify({
                "success": True,
                "message": "Email sent successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to send email"
            }), 500

    except ValueError as e:
        log_event(
            f"Invalid email parameters for business_category_selection {data.get('business_category_selection')}: {str(e)}",
            level="ERROR")
        return jsonify({
            "success": False,
            "error": "Invalid parameters",
            "message": str(e)
        }), 400

    except Exception as e:
        log_event(
            f"Email sending failed for business_category_selection {data.get('business_category_selection')}: {str(e)}",
            level="ERROR")
        return jsonify({
            "success": False,
            "error": "Email sending failed",
            "message": str(e)
        }), 500


@bp.post("/send_emails/bulk")
def send_bulk_emails_by_selection_bc():
    # Required: items (list of business_category_selection IDs), subject, html_content
    data, err = require_params("items", "subject", "template_id")
    if err:
        return err

    items = data["items"]
    if not isinstance(items, list) or not items:
        return jsonify({
            "success": False,
            "error": "Invalid items",
            "message": "items must be a non-empty list of selection IDs of Business Category"
        }), 400

    email_service = current_app.config["EmailService"]
    business_category_service = current_app.config["BusinessCategoryService"]

    recipients = []
    invalid_items = []
    for selection_id in items:
        try:
            user_details = business_category_service.get_business_category_user_contact(
                business_category_selection=selection_id
            )
            email = (user_details or {}).get("email")
            if email:
                recipients.append(email)
            else:
                invalid_items.append({
                    "business_category_selection": selection_id,
                    "reason": "No email on record"
                })
        except Exception as e:
            invalid_items.append({
                "business_category_selection": selection_id,
                "reason": str(e)
            })

    try:
        content = email_service.resolve_email_template(template_id=data["template_id"])

        result = email_service.send_email(
            recipient=recipients,
            subject=data["subject"],
            content=content,
            content_type="html"
        )

        # Log and respond
        log_event(
            f"Emails sent: '{data['subject']}' | "
            f"from {len(items)} items, {len(recipients)} recipients, {len(invalid_items)} invalid items"
        )

        return jsonify({
            "message": "Bulk email completed",
            "sucess": result,
            "resolved_recipients": len(recipients),
            "invalid_items": invalid_items
        }), 200

    except ValueError as e:
        log_event(f"Invalid bulk email parameters: {str(e)}", level="ERROR")
        return jsonify({
            "success": False,
            "error": "Invalid parameters",
            "message": str(e)
        }), 400

    except Exception as e:
        log_event(f"Bulk email sending failed: {str(e)}", level="ERROR")
        return jsonify({
            "success": False,
            "error": "Bulk email sending failed",
            "message": str(e)
        }), 500

