from db.db import get_db
from utilities import now_iso


class ProjectService:
    def __init__(self, db=None):
        self.db = db or get_db()

    def insert_project(self, name: str, created_by: str, deadline_date: str) -> int:
        created_at = now_iso()
        modified_at = now_iso()
        status = "New"

        return self.db.execute(
            "INSERT INTO Project (name, created_by, created_at, modified_at, status, deadline_date)"
            "VALUES (?,?,?,?,?,?)",
            (name, created_by, created_at, modified_at, status, deadline_date,))

    def list_all_projects(self, ):
        return self.db.query_all("SELECT * FROM Project")

    def _insert_project_task(self, category_id: str, project_id: str,
                             description: str, sub_category: str, unit: str, quantity: float) -> int:
        return self.db.execute(
            "INSERT INTO ProjectTask (category_id, project_id, description, sub_category, unit, quantity) "
            "VALUES (?,?,?,?,?,?)",
            (category_id, project_id, description, sub_category, unit, quantity)
        )

    def extract_boq(self, data: bytes, project_id: str):
        """This function will extract the data from the SKN file and will populate the appropriate data into the relevant DB tables"""
        # _insert_project_task() # foreach
        # insert_category() # if needed
        pass
