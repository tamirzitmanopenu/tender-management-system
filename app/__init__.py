from flask import Flask
from .teardown import register_teardown
from .blueprints.businesses import bp as businesses_bp
from .blueprints.categories import bp as categories_bp


def create_app():
    app = Flask(__name__)

    # blueprints
    app.register_blueprint(businesses_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")

    # teardown (close DB connections)
    register_teardown(app)

    return app
