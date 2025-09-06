from flask import jsonify
from utilities import log_event

def register_error_handlers(app):
    # Error handlers for the blueprint
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested email endpoint was not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "Method not allowed",
            "message": "The HTTP method is not allowed for this endpoint"
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        log_event(f"Internal server error in email service: {str(error)}", level="ERROR")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500


