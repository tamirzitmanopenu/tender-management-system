from db.db import query_one, execute

def business_exists(business_id: str) -> bool:
    return query_one("SELECT 1 FROM Business WHERE business_id = ?", (business_id,)) is not None

def insert_business(business_id: str, company_name: str):
    execute(
        "INSERT INTO Business (business_id, company_name) VALUES (?, ?)",
        (business_id, company_name),
    )
