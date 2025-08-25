from utilities import now_iso


class ProjectService:
    def __init__(self, db):
        #אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    def insert_project(self, name: str, created_by: str, deadline_date: str) -> int:
        #הוספת פרויקט חדש לבסיס הנתונים
        created_at = now_iso()
        modified_at = now_iso()
        status = "New"

        return self.db.execute(
            "INSERT INTO Project (name, created_by, created_at, modified_at, status, deadline_date)"
            "VALUES (?,?,?,?,?,?)",
            (name, created_by, created_at, modified_at, status, deadline_date,))

    def list_all_projects(self, ):
        #שליפת כל הפרויקטים מבסיס הנתונים
        return self.db.query_all("SELECT * FROM Project")

    def get_project_record(self, project_id: str):
        #שליפת רשומת פרויקט מבסיס הנתונים לפי מזהה הפרויקט
        return self.db.get_table_record(table='File', filters={'project_id': project_id}, query_one_only=True)

    def insert_project_task(self, project_id: str, category_id: str,
                            description: str, sub_category: str, unit: str, quantity: float) -> int:
        #הוספת משימה חדשה(task) לפרויקט בבסיס הנתונים
        return self.db.execute(
            "INSERT INTO ProjectTask (category_id, project_id, description, sub_category, unit, quantity) "
            "VALUES (?,?,?,?,?,?)",
            (category_id, project_id, description, sub_category, unit, quantity)
        )
