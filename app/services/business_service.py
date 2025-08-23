class BusinessService:
    def __init__(self, db):
        self.db = db

    def business_exists(self, business_id: str) -> bool:
        return (
                self.db.query_one(
                    "SELECT 1 FROM Business WHERE business_id = ?", (business_id,)
                )
                is not None
        )

    def insert_business(self, business_id: str, company_name: str):
        self.db.execute(
            "INSERT INTO Business (business_id, company_name) VALUES (?, ?)",
            (business_id, company_name),
        )

    def list_all_businesses(self):
        return self.db.query_all("SELECT * FROM Business ORDER BY company_name")
