class ProjectTaskService:
    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    def insert_project_task(self, project_id: str, category_id: str,
                            description: str, sub_category: str, unit: str, quantity: float) -> int:
        # הוספת משימה חדשה(task) לפי מזהה פרויקט בבסיס הנתונים
        return self.db.execute(
            "INSERT INTO ProjectTask (category_id, project_id, description, sub_category, unit, quantity) "
            "VALUES (?,?,?,?,?,?)",
            (category_id, project_id, description, sub_category, unit, quantity)
        )

    def get_project_tasks(self, project_id: str = None, category_id: str = None):
        filters = {}
        if project_id is not None:
            filters['project_id'] = project_id
        if category_id is not None:
            filters['category_id'] = category_id
        return self.db.get_table_record(table='ProjectTask', filters=filters)
