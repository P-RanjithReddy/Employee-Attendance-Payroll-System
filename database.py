import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "attendance.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                designation TEXT NOT NULL,
                monthly_salary REAL NOT NULL CHECK(monthly_salary >= 0)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present','Absent','Leave')),
                UNIQUE(employee_id, attendance_date),
                FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
            )
        """)
