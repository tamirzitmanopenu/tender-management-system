from db.db import close_db

def register_teardown(app):
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
