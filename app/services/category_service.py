from db.db import query_one, query_all, execute

def normalized(name: str) -> str:
    return (name or "").strip()

def category_by_normalized(name: str):
    return query_one(
        "SELECT category_id FROM Category WHERE LOWER(TRIM(category_name)) = LOWER(TRIM(?))",
        (name,),
    )

def category_id_exists(cid) -> bool:
    return query_one("SELECT 1 FROM Category WHERE category_id = ?", (cid,)) is not None

def insert_category(name: str) -> int:
    return execute("INSERT INTO Category (category_name) VALUES (?)", (name,))

def insert_category_with_id(cid, name: str):
    execute(
        "INSERT INTO Category (category_id, category_name) VALUES (?, ?)",
        (cid, name),
    )

def list_categories():
    return query_all("SELECT category_id, category_name FROM Category ORDER BY category_name")
