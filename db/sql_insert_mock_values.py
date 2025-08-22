import sqlite3

# יצירת חיבור למסד הנתונים
conn = sqlite3.connect(r'tender-management-system.db')
cursor = conn.cursor()

# יצירת טבלאות
cursor.executescript("""


INSERT INTO Permission (permission_id, permission_name) VALUES
(1, 'Admin'),
(2, 'Editor'),
(3, 'Viewer'),
(4, 'Supplier');


INSERT INTO User (username, permission_id, full_name, email, password, phone, user_type) VALUES
('admin1', 1, 'אורי כהן', 'ori@example.com', 'pass123', '050-1234567', 'עובד'),
('emp1', 2, 'דנה לוי', 'dana@example.com', 'pass456', '050-7654321', 'עובד'),
('sup1', 4, 'חברת בטון בע״מ', 'contact@beton.co.il', 'pass789', '03-5551234', 'ספק'),
('sup2', 4, 'חברת חשמליות', 'sales@electric.co.il', 'pass321', '03-5554321', 'ספק');


INSERT INTO Employee (username, employee_id, department) VALUES
('admin1', '301111111', 'ניהול'),
('emp1', '302222222', 'הנדסה');


INSERT INTO Business (business_id, company_name) VALUES
(1, 'חברת בטון בע״מ'),
(2, 'חברת חשמליות'),
(3, 'חברת צבעים וציפויים');

INSERT INTO Supplier (username, business_id, supplier_id) VALUES
('sup1', 1, '510111111'),
('sup2', 2, '520222222');

INSERT INTO Category (category_id, category_name) VALUES
(1, 'עבודות שלד'),
(2, 'עבודות חשמל'),
(3, 'עבודות צבע'),
(4, 'עבודות אינסטלציה');

INSERT INTO BusinessCategory (business_category_id, business_id, category_id, rated_employee_username, review, rating_score, supplier_contact) VALUES
(1, 1, 1, 'admin1', 'עבודה מצוינת ואמינה', 4.8, 'sup1'),
(2, 2, 2, 'emp1', 'שירות מהיר ואיכותי', 4.5, 'sup2'),
(3, 3, 3, 'admin1', 'צבע איכותי, עמיד לאורך זמן', 4.7, NULL);


""")

# שמירת השינויים
conn.commit()
conn.close()

print("added mock values")
