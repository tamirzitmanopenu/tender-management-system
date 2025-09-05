class BusinessCategoryService:

    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db

    ##BusinessCategory:
    def insert_business_category(self, business_id: str,
                                 category_id: str,
                                 rated_employee_username: str,
                                 review: str = None,
                                 rating_score: float = None,
                                 supplier_contact_username: str = None) -> str:
        record = {
            'business_id': business_id,
            'category_id': category_id,
            'rated_employee_username': rated_employee_username
        }

        # Add optional fields only if they are provided
        if review is not None:
            record['review'] = review

        if rating_score is not None:
            record['rating_score'] = str(rating_score)

        if supplier_contact_username is not None:
            record['supplier_contact'] = supplier_contact_username

        return str(self.db.new_table_record(table='BusinessCategory', record=record))

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

    def get_business_category_selection(self, business_category_id: str = None, project_id: str = None):
        filters = {}
        if business_category_id is not None:
            filters['business_category_id'] = business_category_id
        if project_id is not None:
            filters['project_id'] = project_id
        return self.db.get_table_record(table='BusinessCategorySelection', filters=filters)
