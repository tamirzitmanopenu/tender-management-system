import os

from flask import Flask
from flask_cors import CORS

from db.db import get_db
from .error_handlers import register_error_handlers
from .services.ai_recommendation_service import AIRecommendationService
from .services.business_category_service import BusinessCategoryService
from .services.business_service import BusinessService
from .services.category_comparison_service import CategoryComparisonService
from .services.category_service import CategoryService
from .services.email_service import EmailService
from .services.file_service import FileService
from .services.offer_service import OfferService
from .services.project_task_service import ProjectTaskService
from .services.project_service import ProjectService
from .teardown import register_teardown
from .blueprints.businesses import bp as businesses_bp
from .blueprints.categories import bp as categories_bp
from .blueprints.projects import bp as projects_bp
from .blueprints.files import bp as files_bp
from .blueprints.offers import bp as offers_bp
from .blueprints.category_comparison import bp as category_comparison_bp
from .blueprints.emails import bp as emails_bp


def create_app():
    app = Flask(__name__)

    # Allow frontend at localhost:8501 (Streamlit) to access this backend for dev purposes
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

    # blueprints
    app.register_blueprint(businesses_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")
    app.register_blueprint(projects_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/api")
    app.register_blueprint(offers_bp, url_prefix="/api")
    app.register_blueprint(category_comparison_bp, url_prefix="/api")
    app.register_blueprint(emails_bp, url_prefix="/api")

    with app.app_context():
        repo = get_db()

    app.config['BusinessService'] = BusinessService(repo)
    app.config['BusinessCategoryService'] = BusinessCategoryService(repo)
    app.config['CategoryService'] = CategoryService(repo)
    app.config['ProjectService'] = ProjectService(repo)
    upload_folder = os.path.join(os.path.dirname(__file__), "uploads")
    app.config['FileService'] = FileService(db=repo, upload_folder=upload_folder)
    app.config['ProjectTaskService'] = ProjectTaskService(repo)
    app.config['OfferService'] = OfferService(repo)
    app.config['CategoryComparisonService'] = CategoryComparisonService(repo)
    app.config['AIRecommendationService'] = AIRecommendationService(repo)
    templates_dir = os.path.join(os.path.dirname(__file__), "services", "email_templates")
    app.config['EmailService'] = EmailService(db=repo, templates_dir=templates_dir)

    # teardown (close DB connections)
    register_teardown(app)
    register_error_handlers(app)

    return app
