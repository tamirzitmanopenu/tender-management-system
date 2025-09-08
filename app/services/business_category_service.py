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

    def get_business_category_user_contact(self, business_category_id: str = None,
                                           business_category_selection: str = None):
        if business_category_id is not None:
            query = """
            SELECT *
            FROM BusinessCategory 
            JOIN User on User.username = BusinessCategory.supplier_contact
            JOIN Business ON Business.business_id = BusinessCategory.business_id
            WHERE BusinessCategory.business_category_id = ?
            """
            return self.db.query_one(query, (business_category_id,))
        elif business_category_selection is not None:
            query = """
            SELECT *
            FROM BusinessCategory as bc
            JOIN User on User.username = bc.supplier_contact
            JOIN Business ON Business.business_id = bc.business_id
            JOIN BusinessCategorySelection ON BusinessCategorySelection.business_category_id = bc.business_category_id
            WHERE BusinessCategorySelection.selection_id = ?
            """
            return self.db.query_one(query, (business_category_selection,))
        else:
            raise ValueError("....")


if __name__ == "__main__":
    # Example of how to integrate with your existing app utilities
    from db.db import get_db
    from dotenv import load_dotenv

    load_dotenv()
    db = get_db()

    serv = BusinessCategoryService(db)
    print(serv.get_business_category_user_contact(business_category_id='1'))
