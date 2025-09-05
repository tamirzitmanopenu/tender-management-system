                                 -- schema.sql for tender-management-system (SQLite)
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS Permission (
    permission_id INTEGER PRIMARY KEY,
    permission_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS User (
    username TEXT PRIMARY KEY,
    permission_id INTEGER,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    user_type TEXT CHECK(user_type IN ('עובד', 'ספק')),
    FOREIGN KEY (permission_id) REFERENCES Permission(permission_id)
);

CREATE TABLE IF NOT EXISTS Employee (
    username TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    department TEXT,
    FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE IF NOT EXISTS Business (
    business_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Supplier (
    username TEXT PRIMARY KEY,
    business_id INTEGER,
    supplier_id TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES User(username),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS Category (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS BusinessCategory (
    business_category_id INTEGER PRIMARY KEY,
    business_id INTEGER,
    category_id INTEGER,
    rated_employee_username TEXT,
    review TEXT,
    rating_score REAL,
    supplier_contact TEXT DEFAULT NULL,
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (rated_employee_username) REFERENCES Employee(username),
    FOREIGN KEY (supplier_contact) REFERENCES Supplier(username)
);

CREATE TABLE IF NOT EXISTS Project (
    project_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_by TEXT,
    created_at TEXT,
    modified_at TEXT,
    deadline_date TEXT,
    deleted INTEGER DEFAULT 0,
    status TEXT,
    FOREIGN KEY (created_by) REFERENCES Employee(username)
);

CREATE TABLE IF NOT EXISTS ProjectTask (
    project_task_id INTEGER PRIMARY KEY,
    category_id INTEGER,
    project_id INTEGER,
    description TEXT,
    sub_category TEXT,
    unit TEXT,
    quantity REAL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
);

CREATE TABLE IF NOT EXISTS TotalOffer (
    total_offer_id INTEGER PRIMARY KEY,
    supplier_username TEXT,
    signed_date TEXT,
    project_id INTEGER,
    business_category_id INTEGER,
    FOREIGN KEY (supplier_username) REFERENCES Supplier(username),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (business_category_id) REFERENCES BusinessCategory(business_category_id)
);

CREATE TABLE IF NOT EXISTS TaskOffer (
    task_offer_id INTEGER PRIMARY KEY,
    total_offer_id INTEGER,
    project_task_id INTEGER,
    price_offer REAL,
    FOREIGN KEY (total_offer_id) REFERENCES TotalOffer(total_offer_id),
    FOREIGN KEY (project_task_id) REFERENCES ProjectTask(project_task_id)
);

CREATE TABLE IF NOT EXISTS File (
    file_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    uploaded_by TEXT,
    file_type TEXT,
    file_path TEXT,
    uploaded_at TEXT,
    deleted INTEGER DEFAULT 0,
    project_id INTEGER,
    FOREIGN KEY (uploaded_by) REFERENCES Employee(username),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
);

CREATE TABLE IF NOT EXISTS Log (
    log_id INTEGER PRIMARY KEY,
    username TEXT,
    message TEXT,
    level TEXT,
    date TEXT,
    FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE IF NOT EXISTS BusinessCategorySelection (
    selection_id INTEGER PRIMARY KEY,
    project_id INTEGER,
    business_category_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (business_category_id) REFERENCES BusinessCategory(business_category_id)
);

COMMIT;
