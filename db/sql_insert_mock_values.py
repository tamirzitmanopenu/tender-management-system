import sqlite3
from datetime import datetime, timedelta

# יצירת חיבור למסד הנתונים
conn = sqlite3.connect(r'tender-management-system.db')
cursor = conn.cursor()

# תאריכים לשימוש
current_date = datetime.now().strftime('%Y-%m-%d')
future_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')

# יצירת טבלאות
cursor.executescript(f"""


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
(3, 'חברת צבעים וציפויים'),
(4, 'חברת בניה ופיתוח'),
(5, 'חברת אינסטלציה מתקדמת');

INSERT INTO User (username, permission_id, full_name, email, password, phone, user_type) VALUES
('sup3', 4, 'חברת בניה ופיתוח', 'contact@building.co.il', 'pass432', '03-5557890', 'ספק'),
('sup4', 4, 'חברת אינסטלציה מתקדמת', 'info@plumbing.co.il', 'pass567', '03-5559999', 'ספק');

INSERT INTO Supplier (username, business_id, supplier_id) VALUES
('sup1', 1, '510111111'),
('sup2', 2, '520222222'),
('sup3', 4, '530333333'),
('sup4', 5, '540444444');

INSERT INTO Category (category_id, category_name) VALUES
(1, 'עבודות שלד'),
(2, 'עבודות חשמל'),
(3, 'עבודות צבע'),
(4, 'עבודות אינסטלציה');

INSERT INTO BusinessCategory (business_category_id, business_id, category_id, rated_employee_username, review, rating_score, supplier_contact) VALUES
(1, 1, 1, 'admin1', 'עבודה מצוינת ואמינה', 4.8, 'sup1'),
(2, 2, 2, 'emp1', 'שירות מהיר ואיכותי', 4.5, 'sup2'),
(3, 3, 3, 'admin1', 'צבע איכותי, עמיד לאורך זמן', 4.7, NULL),
(4, 4, 1, 'emp1', 'ביצוע מקצועי של עבודות שלד', 4.6, 'sup3'),
(5, 5, 4, 'admin1', 'עבודות אינסטלציה ברמה גבוהה', 4.9, 'sup4');

INSERT INTO Project (project_id, name, created_by, created_at, modified_at, deadline_date, status) VALUES
(1, 'בניית בניין משרדים - תל אביב', 'admin1', '{current_date}', '{current_date}', '{future_date}', 'בתהליך'),
(2, 'שיפוץ מבנה מגורים - חיפה', 'emp1', '{current_date}', '{current_date}', '{future_date}', 'בתהליך');

INSERT INTO ProjectTask (project_task_id, category_id, project_id, description, sub_category, unit, quantity) VALUES
(1, 1, 1, 'יציקת בטון לקומת קרקע', 'יציקות', 'קוב', 150),
(2, 1, 1, 'יציקת בטון לקומה ראשונה', 'יציקות', 'קוב', 120),
(3, 2, 1, 'התקנת תשתית חשמל קומת קרקע', 'תשתיות', 'נקודה', 50),
(4, 2, 1, 'התקנת לוח חשמל ראשי', 'לוחות חשמל', 'יחידה', 1),
(5, 4, 1, 'התקנת צנרת מים ראשית', 'צנרת', 'מטר', 200),
(6, 1, 2, 'חיזוק יסודות', 'יציקות', 'קוב', 80),
(7, 2, 2, 'החלפת תשתית חשמל', 'תשתיות', 'קומה', 4),
(8, 4, 2, 'החלפת צנרת ביוב', 'צנרת', 'מטר', 150);

INSERT INTO TotalOffer (total_offer_id, supplier_username, signed_date, project_id, business_category_id) VALUES
(1, 'sup1', '{current_date}', 1, 1),  -- חברת בטון - עבודות שלד
(2, 'sup3', '{current_date}', 1, 4),  -- חברת בניה - עבודות שלד
(3, 'sup2', '{current_date}', 1, 2),  -- חברת חשמליות - עבודות חשמל
(4, 'sup4', '{current_date}', 1, 5),  -- חברת אינסטלציה - עבודות אינסטלציה
(5, 'sup1', '{current_date}', 2, 1),  -- חברת בטון - עבודות שלד
(6, 'sup3', '{current_date}', 2, 4),  -- חברת בניה - עבודות שלד
(7, 'sup2', '{current_date}', 2, 2);  -- חברת חשמליות - עבודות חשמל

INSERT INTO TaskOffer (task_offer_id, total_offer_id, project_task_id, price_offer) VALUES
-- הצעות מחיר לפרויקט 1
(1, 1, 1, 75000),  -- חברת בטון - יציקת קומת קרקע
(2, 1, 2, 60000),  -- חברת בטון - יציקת קומה ראשונה
(3, 2, 1, 78000),  -- חברת בניה - יציקת קומת קרקע
(4, 2, 2, 62000),  -- חברת בניה - יציקת קומה ראשונה
(5, 3, 3, 25000),  -- חברת חשמליות - תשתית חשמל
(6, 3, 4, 15000),  -- חברת חשמליות - לוח חשמל
(7, 4, 5, 40000),  -- חברת אינסטלציה - צנרת מים

-- הצעות מחיר לפרויקט 2
(8, 5, 6, 45000),   -- חברת בטון - חיזוק יסודות
(9, 6, 6, 48000),   -- חברת בניה - חיזוק יסודות
(10, 7, 7, 60000);  -- חברת חשמליות - החלפת תשתית חשמל

""")

# שמירת השינויים
conn.commit()
conn.close()

print("added mock values")
