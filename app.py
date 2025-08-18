from flask import Flask, jsonify, request
from db import get_db, close_db, init_db, query_one, query_all, execute
from utilities import require_json, log_event


def create_app():
    app = Flask(__name__)

    # save resources - close db when not needed
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    # --- Businesses ---
    @app.post("/businesses")
    def add_business():
        data, err = require_json("company_name")
        if err: return err
        business_id = execute(
            "INSERT INTO Business (company_name) VALUES (?)",
            (data["company_name"],),
        )
        log_event(request.headers.get("X-User", "system"),
                  f"נוסף עסק חדש business_id={business_id}")
        return jsonify({"business_id": business_id}), 201

    # --- Categories ---
    @app.get("/api/categories")
    def list_categories():
        return jsonify(
            query_all("SELECT category_id, category_name FROM Category ORDER BY category_name")
        )


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
