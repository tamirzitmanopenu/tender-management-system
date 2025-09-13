import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
db_file = SCRIPT_DIR / 'tender-management-system.db'

# יצירת חיבור למסד הנתונים
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# תאריכים לשימוש
current_date = datetime.now().strftime('%Y-%m-%d')
future_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')

# יצירת טבלאות
cursor.executescript(f"""

INSERT INTO Permission (permission_id, permission_name) VALUES
(1, 'Admin'),
(2, 'Supplier');

INSERT INTO User (username, permission_id, full_name, email, password, phone, user_type) VALUES
('admin1', 1, 'אורי כהן', 'tamirzitman@gmail.com', 'pass123', '050-1234567', 'employee'),
('emp1', 2, 'דנה לוי', 'tamirzitman@gmail.com', 'pass456', '050-7654321', 'employee'),
('sup1', 4, 'שמחה לוי', 'tamirzitman@gmail.com', 'pass789', '03-5551234', 'supplier'),
('sup2', 4, 'רועי שמעוני', 'tamirzitman@gmail.com', 'pass321', '03-5554321', 'supplier');

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
('sup3', 4, 'אביב יוסף', 'tamirzitman@gmail.com', 'pass432', '03-5557890', 'supplier'),
('sup4', 4, 'שרית כהן', 'yuvalsayag2@gmail.com', 'pass567', '03-5559999', 'supplier');

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

-- BusinessCategory: All combinations with real supplier contacts and Hebrew reviews
INSERT INTO BusinessCategory (business_category_id, business_id, category_id, rated_employee_username, review, rating_score, supplier_contact) VALUES
(1, 1, 1, 'admin1', 'עבודה מצוינת ואמינה', 4.8, 'sup1'),
(2, 1, 2, 'emp1', 'שירות חשמל מקצועי ומהיר', 4.6, 'sup1'),
(3, 1, 3, 'admin1', 'צביעה איכותית, גימור מושלם', 4.7, 'sup1'),
(4, 1, 4, 'emp1', 'אינסטלציה ללא תקלות', 4.9, 'sup1'),

(5, 2, 1, 'admin1', 'עבודות שלד מדויקות', 4.5, 'sup1'),
(6, 2, 2, 'emp1', 'חשמלאים מקצועיים', 4.8, 'sup2'),
(7, 2, 3, 'admin1', 'צביעה מהירה ונקייה', 4.4, 'sup1'),
(8, 2, 4, 'emp1', 'פתרונות אינסטלציה מתקדמים', 4.7, 'sup1'),

(9, 3, 1, 'admin1', 'שלד חזק ועמיד', 4.6, 'sup1'),
(10, 3, 2, 'emp1', 'עבודות חשמל בטיחותיות', 4.5, 'sup1'),
(11, 3, 3, 'admin1', 'צבעים איכותיים', 4.9, 'sup3'),
(12, 3, 4, 'emp1', 'אינסטלטורים מקצועיים', 4.8, 'sup4'),

(13, 4, 1, 'admin1', 'ביצוע מקצועי של עבודות שלד', 4.6, 'sup3'),
(14, 4, 2, 'emp1', 'חשמל חכם ומתקדם', 4.7, 'sup2'),
(15, 4, 3, 'admin1', 'גימור צבע ברמה גבוהה', 4.8, 'sup3'),
(16, 4, 4, 'emp1', 'אינסטלציה אמינה', 4.9, 'sup4'),

(17, 5, 1, 'admin1', 'עבודות שלד מדויקות', 4.7, 'sup1'),
(18, 5, 2, 'emp1', 'חשמל מקצועי', 4.6, 'sup2'),
(19, 5, 3, 'admin1', 'צביעה איכותית', 4.8, 'sup3'),
(20, 5, 4, 'admin1', 'עבודות אינסטלציה ברמה גבוהה', 4.9, 'sup4');

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


""")

# שמירת השינויים
conn.commit()
conn.close()

print("added mock values")
