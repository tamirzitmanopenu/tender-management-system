class CategoryComparisonService:
    def __init__(self, db):
        self.db = db

    def get_category_comparison_data(self, project_id: int) -> list[dict]:
        """
        Fetch and compare data from TaskOffer, ProjectTask, and TotalOffer tables
        to show supplier category comparisons in total price offers.
        
        Args:
            project_id (int): The ID of the project to analyze
            
        Returns:
            list[dict]: A list of dictionaries containing comparison data for each category
        """
        query = """
        SELECT 
            c.category_name,
            b.company_name,
            bc.business_category_id,
            SUM(pt.quantity * to2.price_offer) as total_category_price,
            COUNT(DISTINCT pt.project_task_id) as tasks_count
        FROM Category c
        JOIN ProjectTask pt ON pt.category_id = c.category_id
        JOIN TaskOffer to2 ON to2.project_task_id = pt.project_task_id
        JOIN TotalOffer t ON t.total_offer_id = to2.total_offer_id
        JOIN BusinessCategory bc ON bc.business_category_id = t.business_category_id
        JOIN Business b ON b.business_id = bc.business_id
        JOIN Supplier s ON s.username = t.supplier_username
        WHERE pt.project_id = ?
        GROUP BY bc.business_category_id
        ORDER BY c.category_name, total_category_price
        """
        
        rows = self.db.query_all(query, (project_id,))
        return rows

    def get_supplier_category_details(self, project_id: int, business_category_id: int) -> list[dict]:
        """
        Get detailed breakdown of prices for a specific supplier in a category
        
        Args:
            project_id (int): The ID of the project
            business_category_id (int): The ID of the business category
            
        Returns:
            list[dict]: A list of dictionaries containing detailed price breakdown
        """
        query = """
        SELECT 
            pt.project_task_id,
            pt.description,
            pt.sub_category,
            pt.unit,
            pt.quantity,
            to2.price_offer,
            (to2.price_offer * pt.quantity) as total_task_price
        FROM ProjectTask pt
        JOIN TaskOffer to2 ON to2.project_task_id = pt.project_task_id
        JOIN TotalOffer t ON t.total_offer_id = to2.total_offer_id
        WHERE pt.project_id = ?
        AND t.business_category_id = ?
        ORDER BY pt.sub_category, pt.description
        """
        
        rows = self.db.query_all(query, (project_id, business_category_id))
        return rows
