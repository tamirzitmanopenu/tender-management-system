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
