from flask import Blueprint, jsonify, request, current_app
from app.services.category_comparison_service import CategoryComparisonService
from db.db import get_db

category_comparison_bp = Blueprint('category_comparison', __name__)

@category_comparison_bp.route('/api/projects/<int:project_id>/category-comparison', methods=['GET'])
def get_category_comparison(project_id: int):
    """
    Get category comparison data for a specific project
    """
    try:
        service = CategoryComparisonService(get_db())
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

@category_comparison_bp.route('/api/projects/<int:project_id>/category-comparison/details', methods=['GET'])
def get_category_comparison_details(project_id: int):
    """
    Get detailed breakdown for a specific category and supplier
    """
    try:
        category_id = request.args.get('category_id', type=int)
        business_category_id = request.args.get('business_category_id', type=int)
        
        if not category_id or not business_category_id:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameters: category_id and business_category_id'
            }), 400
            
        service = CategoryComparisonService(get_db())
        details = service.get_supplier_category_details(
            project_id, 
            category_id, 
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
