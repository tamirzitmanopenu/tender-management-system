from utilities import now_iso


class ProjectService:
    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    def insert_project(self, name: str, created_by: str, deadline_date: str) -> int:
        # הוספת פרויקט חדש לבסיס הנתונים
        created_at = now_iso()
        modified_at = now_iso()
        status = "New"

        return self.db.execute(
            "INSERT INTO Project (name, created_by, created_at, modified_at, status, deadline_date)"
            "VALUES (?,?,?,?,?,?)",
            (name, created_by, created_at, modified_at, status, deadline_date,))

    def list_all_projects(self, ):
        # שליפת כל הפרויקטים מבסיס הנתונים (excluding soft-deleted ones)
        return self.db.query_all("SELECT * FROM Project WHERE deleted = 0")

    def get_project_record(self, project_id: str):
        # שליפת רשומת פרויקט מבסיס הנתונים לפי מזהה הפרויקט
        return self.db.get_table_record(
            table='Project',
            filters={'project_id': project_id, 'deleted': 0},
            query_one_only=True
        )

    def delete_project_record(self, project_id: str) -> None:
        """Soft delete a project by marking it as deleted instead of removing it."""
        self.db.update_table_record(
            table='Project',
            updates={'deleted': 1, 'modified_at': now_iso()},
            filters={'project_id': project_id}
        )
