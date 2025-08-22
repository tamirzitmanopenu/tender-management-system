from flask import Flask, jsonify, request
from db.db import close_db, query_one, query_all, execute
from utilities import require_json, log_event


def create_app():
    app = Flask(__name__)

    # save resources - close db when not needed
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    # --- Businesses ---
    @app.post("/api/businesses")
    def add_business():
        data, err = require_json("company_name", "business_id")
        if err: return err
        row = query_one("SELECT 1 FROM Business WHERE business_id = ?", (data["business_id"],))
        if row:
            return {"error": "business_id already exists", "business_id": data["business_id"]}, 409

        execute(
            "INSERT INTO Business (business_id, company_name) VALUES (?, ?)",
            (data["business_id"], data["company_name"]),
        )
        log_event(request.headers.get("X-User", "system"),
                  f"A new business was added, {data['company_name']} with business_id: {data["business_id"]}")
        return jsonify({"business_id": data["business_id"]}), 201

    @app.get("/api/businesses")
    def list_businesses():
        return jsonify(
            query_all("SELECT * FROM Business ORDER BY company_name")
        )

    # --- Categories ---
    @app.get("/api/categories")
    def list_categories():
        return jsonify(
            query_all("SELECT category_id, category_name FROM Category ORDER BY category_name")
        )

    @app.post("/api/categories")
    def add_category():
        data, err = require_json("category_name")
        if err:
            return err

        # Normalize the name: trim whitespace
        name = data["category_name"].strip()
        if not name:
            return {"error": "category_name cannot be empty"}, 400

        dup = query_one(
            "SELECT category_id FROM Category WHERE LOWER(TRIM(category_name)) = LOWER(TRIM(?))",
            (name,),
        )
        if dup:
            return {"error": "category_name already exists", "category_id": dup["category_id"]}, 409

        # If the client supplies a category_id, ensure it's unique
        if "category_id" in data and data["category_id"] is not None:
            row = query_one("SELECT 1 FROM Category WHERE category_id = ?", (data["category_id"],))
            if row:
                return {"error": "category_id already exists", "category_id": data["category_id"]}, 409
            execute(
                "INSERT INTO Category (category_id, category_name) VALUES (?, ?)",
                (data["category_id"], data["category_name"]),
            )
            new_id = data["category_id"]
        else:
            # Let the DB autogenerate the primary key
            new_id = execute("INSERT INTO Category (category_name) VALUES (?)", (name,))

        log_event(request.headers.get("X-User", "system"),
                  f"A new category was added, {name} with category_id: {new_id}")

        return jsonify({"category_id": new_id}), 201

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
