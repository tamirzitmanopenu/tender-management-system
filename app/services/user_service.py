class UserService:

    def __init__(self, db):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db


    def get_full_user_details(self, username:str):
        filters = {'username': username}
        user = self.db.get_table_record(table='User', filters=filters,query_one_only=True)
        print(user)
        if user.get('user_type') == 'employee':
            employee = self.db.get_table_record(table='Employee', filters=filters,query_one_only=True)
            if not employee:
                raise ValueError(f"Employee details not found for username: {username}")
            user.update(employee)
        elif user.get('user_type') == 'supplier':
            supplier = self.db.get_table_record(table='Supplier', filters=filters,query_one_only=True)
            if not supplier:
                raise ValueError(f"Supplier details not found for username: {username}")
            user.update(supplier)
        else:
            raise ValueError(f"Unknown user type: {user.get('user_type')}")

        return user
    