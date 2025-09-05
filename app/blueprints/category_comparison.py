from flask import Blueprint, jsonify, current_app

from utilities import require_params

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
        data, err = require_params("business_category_id")
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


@bp.post('/ai/recommendations')
def get_ai_recommendation():
    try:
        data, err = require_params("project_id", "category_id")
        if err:
            return err

        if 'project_id' not in data or "category_id" not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameters: project_id or category_id'
            }), 400

        service = current_app.config["AIRecommendationService"]

        ai_prompt = service.create_ai_prompt(project_id=data['project_id'], category_id=data['category_id'])
        answer = service.get_answer_from_openAI(prompt=ai_prompt)
        return jsonify({
            "project_id": data['project_id'],
            "category_id": data['category_id'],
            "ai_result": answer
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
