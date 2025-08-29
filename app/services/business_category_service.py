class BusinessCategoryService:

    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    ##BusinessCategory:
    def insert_business_category(self, business_id: str,
                                 category_id: str,
                                 rated_employee_username: str,
                                 review: str,
                                 rating_score: float,
                                 supplier_contact_username: str) -> str:
        return str(self.db.new_table_record(table='BusinessCategory', record={
            'business_id': business_id,
            'category_id': category_id,
            'rated_employee_username': rated_employee_username,
            'review': review,
            'rating_score': rating_score,
            'supplier_contact': supplier_contact_username
        }))

    def get_business_category(self, business_id: str = None, category_id: str = None):
        filters = {}
        if business_id is not None:
            filters['business_id'] = business_id
        if category_id is not None:
            filters['category_id'] = category_id
        return self.db.get_table_record(table='BusinessCategory', filters=filters)

    ##BusinessCategorySelection:
    def insert_business_category_selection(self, business_category_id: str, project_id: str):
        return str(self.db.new_table_record(table='BusinessCategorySelection', record={
            'project_id': project_id,
            'business_category_id': business_category_id,
        }))
