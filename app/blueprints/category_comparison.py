from flask import Blueprint, jsonify, current_app

from utilities import require_json

bp = Blueprint("category_comparison_bp", __name__)


@bp.get('/projects/<int:project_id>/category-comparison')
def get_category_comparison(project_id: int):
    """
    Get category comparison data for a specific project
    """
    try:
        service = current_app.config["CategoryComparisonService"]
        comparison_data = service.get_category_comparison_data(project_id)
        return jsonify({
            'status': 'success',
            'data': comparison_data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.get('/projects/<int:project_id>/category-comparison/details')
def get_category_comparison_details(project_id: int):
    """
    Get detailed breakdown for a specific category and supplier
    """
    try:
        data, err = require_json("business_category_id")
        if err:
            return err

        if 'business_category_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameters: business_category_id'
            }), 400

        business_category_id = data['business_category_id']

        service = current_app.config["CategoryComparisonService"]
        details = service.get_supplier_category_details(
            project_id,
            business_category_id
        )
        return jsonify({
            'status': 'success',
            'data': details
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
