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

    def get_projects_by_business_categories(self, business_categories):
        """
        Get projects that are accessible based on business categories.
        
        Args:
            business_categories: List of business category records or single business category record
            
        Returns:
            List of project records that match the business categories
        """
        if not business_categories:
            return []
        
        # Handle both single record and list of records
        if isinstance(business_categories, dict):
            business_categories = [business_categories]
        
        # Extract business_category_ids
        business_category_ids = [str(bc['business_category_id']) for bc in business_categories]
        
        if not business_category_ids:
            return []
        
        # Create placeholders for the IN clause
        placeholders = ','.join(['?' for _ in business_category_ids])
        
        # Query to get projects that have business category selections matching the user's business categories
        query = f"""
        SELECT DISTINCT p.*
        FROM Project p
        JOIN BusinessCategorySelection bcs ON p.project_id = bcs.project_id
        WHERE bcs.business_category_id IN ({placeholders})
        AND p.deleted = 0
        ORDER BY p.created_at DESC
        """
        
        return self.db.query_all(query, business_category_ids)
