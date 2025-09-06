from flask import Blueprint, jsonify, current_app
from utilities import require_params, log_event

bp = Blueprint("emails", __name__)


@bp.post("/send_email")
def send_email_by_selection_bc():
    data, err = require_params("business_category_selection", "subject", "html_content")
    if err:
        return err

    email_service = current_app.config["EmailService"]
    business_category_service = current_app.config["BusinessCategoryService"]
    user_details = business_category_service.get_business_category_user_contact(
        business_category_selection=data["business_category_selection"])
    try:
        # parameters
        cc = data.get("cc", None)
        bcc = data.get("bcc", None)

        success = email_service.send_email(
            recipient=user_details["email"],
            subject=data["subject"],
            content=data["html_content"],
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
        log_event(f"Invalid email parameters for business_category_selection {data.get('business_category_selection')}: {str(e)}", level="ERROR")
        return jsonify({
            "success": False,
            "error": "Invalid parameters",
            "message": str(e)
        }), 400

    except Exception as e:
        log_event(f"Email sending failed for business_category_selection {data.get('business_category_selection')}: {str(e)}", level="ERROR")
        return jsonify({
            "success": False,
            "error": "Email sending failed",
            "message": str(e)
        }), 500

