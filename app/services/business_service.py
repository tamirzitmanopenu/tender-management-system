class BusinessService:
    
    def __init__(self, db):
        #אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    def business_exists(self, business_id: str) -> bool:
        #בדיקה אם קיים עסק עם מזהה נתון
        return (
                self.db.query_one(
                    "SELECT 1 FROM Business WHERE business_id = ?", (business_id,)
                )
                is not None
        )

    def insert_business(self, business_id: str, company_name: str):
        #הוספת רשומה חדשה של עסק לבסיס הנתונים
        self.db.execute(
            "INSERT INTO Business (business_id, company_name) VALUES (?, ?)",
            (business_id, company_name),
        )

    def list_all_businesses(self):
        #שליפת כל העסקים מבסיס הנתונים
        return self.db.query_all("SELECT * FROM Business ORDER BY company_name")
