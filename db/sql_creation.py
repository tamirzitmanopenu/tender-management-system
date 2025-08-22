import sqlite3
from pathlib import Path


db_file = r'tender-management-system.db'
schema_file = "schema.sql"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Run schema.sql if it exists
if Path(schema_file).exists():
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()
    print("Schema applied from schema.sql")
else:
    print("schema.sql not found. Connected to existing database.")

conn.close()
