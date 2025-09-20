from utilities import now_iso


class OfferService:
    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    def insert_total_offer(self, supplier_username: str, project_id: str, business_category_id: str) -> str:
        record={
            'supplier_username': supplier_username,
            'signed_date': now_iso(),
            'project_id': project_id,
            'business_category_id': business_category_id,
        }
        return str(self.db.new_table_record(table='TotalOffer', record=record))

    def insert_task_offer(self, total_offer_id: str, project_task_id: str, price_offer: float) -> str:
        record={
            'total_offer_id': total_offer_id,
            'project_task_id': project_task_id,
            'price_offer': price_offer
        }
        return str(self.db.new_table_record(table='TaskOffer', record=record))

    def get_offer_status_report(self, project_id: str):
        """
        מחזיר דוח סטטוס הצעות - כל העסקים שנבחרו לפרויקט ואם הגישו הצעה או לא
        """
       
        query = f"""
        SELECT 
            c.category_name,
            b.company_name,
            CASE 
            WHEN to_table.total_offer_id IS NOT NULL THEN 'הוגש'
            ELSE 'טרם הוגש'
            END as offer_status,
            COALESCE(to_table.signed_date, '-') as submission_date,
            COALESCE(to_table.supplier_username, '-') as submitted_by
        FROM BusinessCategorySelection bcs
        JOIN BusinessCategory bc ON bcs.business_category_id = bc.business_category_id
        JOIN Business b ON bc.business_id = b.business_id
        JOIN Category c ON bc.category_id = c.category_id
        JOIN Project p ON bcs.project_id = p.project_id
        LEFT JOIN TotalOffer to_table ON bcs.business_category_id = to_table.business_category_id 
                        AND bcs.project_id = to_table.project_id
        WHERE bcs.project_id = ?
        ORDER BY bcs.project_id, b.company_name
        """

        return self.db.query_all(query, (project_id,))
