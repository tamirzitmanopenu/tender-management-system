import os

from flask import Flask

from db.db import get_db
from .config import Config
from .services.ai_recommendation_service import AIRecommendationService
from .services.business_category_service import BusinessCategoryService
from .services.business_service import BusinessService
from .services.category_comparison_service import CategoryComparisonService
from .services.category_service import CategoryService
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


def _register_blueprints(app: Flask) -> None:
    """Attach all Flask blueprints."""
    app.register_blueprint(businesses_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")
    app.register_blueprint(projects_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/api")
    app.register_blueprint(offers_bp, url_prefix="/api")
    app.register_blueprint(category_comparison_bp, url_prefix="/api")


def _init_services(app: Flask, repo) -> None:
    """Store service instances on the app config."""
    app.config['BusinessService'] = BusinessService(repo)
    app.config['BusinessCategoryService'] = BusinessCategoryService(repo)
    app.config['CategoryService'] = CategoryService(repo)
    app.config['ProjectService'] = ProjectService(repo)
    app.config['FileService'] = FileService(repo)
    app.config['ProjectTaskService'] = ProjectTaskService(repo)
    app.config['OfferService'] = OfferService(repo)
    app.config['CategoryComparisonService'] = CategoryComparisonService(repo)
    app.config['AIRecommendationService'] = AIRecommendationService(repo)


def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    _register_blueprints(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        repo = get_db(app.config['DATABASE_PATH'])

    _init_services(app, repo)

    # teardown (close DB connections)
    register_teardown(app)

    return app
