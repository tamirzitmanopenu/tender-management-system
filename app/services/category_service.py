class CategoryService:
    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    @staticmethod
    def normalized(name: str) -> str:
        # נרמול שם הקטגוריה על ידי הסרת רווחים מיותרים
        return (name or "").strip()

    def category_by_normalized(self, name: str):
        # חיפוש קטגוריה לפי שם נרמול
        res = self.db.query_one(
            "SELECT category_id FROM Category WHERE LOWER(TRIM(category_name)) = LOWER(TRIM(?))",
            (name,))
        if res:
            return res.get('category_id', None)
        return None

    def category_id_exists(self, cid) -> bool:
        # בדיקה אם קיים מזהה קטגוריה נתון
        return self.db.query_one("SELECT 1 FROM Category WHERE category_id = ?", (cid,)) is not None

    def insert_category(self, name: str) -> int:
        # הוספת קטגוריה חדשה לבסיס הנתונים
        return self.db.execute("INSERT INTO Category (category_name) VALUES (?)", (name,))

    def insert_category_with_id(self, cid, name: str):
        # הוספת קטגוריה חדשה עם מזהה נתון לבסיס הנתונים
        self.db.execute(
            "INSERT INTO Category (category_id, category_name) VALUES (?, ?)",
            (cid, name),
        )

    def list_categories(self, project_id: str = None):
        # שליפת כל הקטגוריות מבסיס הנתונים
        params = ()
        if project_id is not None:
            query = """
            SELECT DISTINCT(c.category_id),c.category_name FROM Category as c
            JOIN ProjectTask as pt ON c.category_id = pt.category_id JOIN Project as p ON pt.project_id = p.project_id
            WHERE p.project_id = ?
            ORDER BY category_name
            """
            params = (project_id,)
        else:
            query = "SELECT category_id, category_name FROM Category ORDER BY category_name"
        return self.db.query_all(query, params)

    def list_categories_by_user_and_project(self, username: str, project_id: str):
        """
        שליפת קטגוריות לפי משתמש ופרויקט על בסיס BusinessCategorySelection
        מחזיר רק את הקטגוריות שנבחרו עבור הפרויקט ושהמשתמש יכול לעבוד איתן
        """
        # בדיקת סוג המשתמש
        user_query = "SELECT user_type FROM User WHERE username = ?"
        user_result = self.db.query_one(user_query, (username,))
        
        if not user_result:
            return []
        
        user_type = user_result.get('user_type')
        
        if user_type == 'supplier':
            # עבור supplier - מחזיר קטגוריות שנבחרו לפרויקט ושהעסק שלו רשום עליהן
            query = """
            SELECT DISTINCT c.category_id, c.category_name 
            FROM Category c
            JOIN BusinessCategory bc ON c.category_id = bc.category_id
            JOIN BusinessCategorySelection bcs ON bc.business_category_id = bcs.business_category_id
            JOIN Supplier s ON bc.business_id = s.business_id
            WHERE s.username = ? AND bcs.project_id = ?
            ORDER BY c.category_name
            """
            return self.db.query_all(query, (username, project_id))
        else:
        
            return self.list_categories(project_id)
