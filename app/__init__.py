import os

from flask import Flask

from db.db import get_db
from .services.business_service import BusinessService
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
from .blueprints.category_comparison import category_comparison_bp


def create_app():
    app = Flask(__name__)

    # blueprints
    app.register_blueprint(businesses_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")
    app.register_blueprint(projects_bp, url_prefix="/api")
    app.register_blueprint(files_bp, url_prefix="/api")
    app.register_blueprint(offers_bp, url_prefix="/api")
    app.register_blueprint(category_comparison_bp)

    with app.app_context():
        repo = get_db()

    app.config['BusinessService'] = BusinessService(repo)
    app.config['CategoryService'] = CategoryService(repo)
    app.config['ProjectService'] = ProjectService(repo)
    app.config['FileService'] = FileService(repo)
    app.config['ProjectTaskService'] = ProjectTaskService(repo)
    app.config['OfferService'] = OfferService(repo)


    upload_folder = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # teardown (close DB connections)
    register_teardown(app)

    return app
