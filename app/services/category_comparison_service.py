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
            c.category_id,
            c.category_name,
            b.company_name,
            bc.business_category_id,
            SUM(to2.price_offer) as total_category_price,
            COUNT(DISTINCT pt.project_task_id) as tasks_count,
            u.full_name as supplier_name
        FROM Category c
        JOIN ProjectTask pt ON pt.category_id = c.category_id
        JOIN TaskOffer to2 ON to2.project_task_id = pt.project_task_id
        JOIN TotalOffer t ON t.total_offer_id = to2.total_offer_id
        JOIN BusinessCategory bc ON bc.business_category_id = t.business_category_id
        JOIN Business b ON b.business_id = bc.business_id
        JOIN Supplier s ON s.username = t.supplier_username
        JOIN User u ON u.username = s.username
        WHERE pt.project_id = ?
        GROUP BY c.category_id, b.business_id
        ORDER BY c.category_name, total_category_price
        """
        
        rows = self.db.query_all(query, (project_id,))
        
        # Transform the raw data into a structured format
        categories = {}
        for row in rows:
            category_id = row[0]
            if category_id not in categories:
                categories[category_id] = {
                    'category_name': row[1],
                    'suppliers': []
                }
            
            categories[category_id]['suppliers'].append({
                'company_name': row[2],
                'business_category_id': row[3],
                'total_price': row[4],
                'tasks_count': row[5],
                'supplier_name': row[6],
                'average_price_per_task': row[4] / row[5] if row[5] > 0 else 0
            })
        
        # Convert the dictionary to a list for easier frontend handling
        result = []
        for category_id, data in categories.items():
            category_data = {
                'category_id': category_id,
                'category_name': data['category_name'],
                'suppliers': data['suppliers'],
                'lowest_price': min(s['total_price'] for s in data['suppliers']) if data['suppliers'] else 0,
                'highest_price': max(s['total_price'] for s in data['suppliers']) if data['suppliers'] else 0,
                'avg_price': sum(s['total_price'] for s in data['suppliers']) / len(data['suppliers']) if data['suppliers'] else 0
            }
            result.append(category_data)
            
        return result

    def get_supplier_category_details(self, project_id: int, category_id: int, business_category_id: int) -> list[dict]:
        """
        Get detailed breakdown of prices for a specific supplier in a category
        
        Args:
            project_id (int): The ID of the project
            category_id (int): The ID of the category
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
        AND pt.category_id = ?
        AND t.business_category_id = ?
        ORDER BY pt.sub_category, pt.description
        """
        
        rows = self.db.query_all(query, (project_id, category_id, business_category_id))
        
        return [{
            'task_id': row[0],
            'description': row[1],
            'sub_category': row[2],
            'unit': row[3],
            'quantity': row[4],
            'unit_price': row[5],
            'total_price': row[6]
        } for row in rows]
