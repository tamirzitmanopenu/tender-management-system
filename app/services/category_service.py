from db.db import get_db


class CategoryService:
    def __init__(self, db=None):
        self.db = db or get_db()

    def normalized(self, name: str) -> str:
        return (name or "").strip()

    def category_by_normalized(self, name: str):
        return self.db.query_one(
            "SELECT category_id FROM Category WHERE LOWER(TRIM(category_name)) = LOWER(TRIM(?))",
            (name,),
        )

    def category_id_exists(self, cid) -> bool:
        return self.db.query_one("SELECT 1 FROM Category WHERE category_id = ?", (cid,)) is not None

    def insert_category(self, name: str) -> int:
        return self.db.execute("INSERT INTO Category (category_name) VALUES (?)", (name,))

    def insert_category_with_id(self, cid, name: str):
        self.db.execute(
            "INSERT INTO Category (category_id, category_name) VALUES (?, ?)",
            (cid, name),
        )

    def list_categories(self):
        return self.db.query_all(
            "SELECT category_id, category_name FROM Category ORDER BY category_name"
        )
