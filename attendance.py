from datetime import date
from database import get_connection

class AttendanceManager:
    VALID_STATUSES = ("Present", "Absent", "Leave")

    def mark_attendance(self, employee_id, attendance_date, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Status must be Present, Absent, or Leave.")
        with get_connection() as conn:
            if not conn.execute(
                "SELECT 1 FROM employees WHERE employee_id=?", (employee_id,)
            ).fetchone():
                raise ValueError("Employee ID not found.")
            conn.execute("""
                INSERT INTO attendance(employee_id, attendance_date, status)
                VALUES (?, ?, ?)
                ON CONFLICT(employee_id, attendance_date)
                DO UPDATE SET status=excluded.status
            """, (employee_id, attendance_date, status))

    def monthly_summary(self, employee_id, year, month):
        prefix = f"{year:04d}-{month:02d}-%"
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT status, COUNT(*) AS total FROM attendance
                WHERE employee_id=? AND attendance_date LIKE ?
                GROUP BY status
            """, (employee_id, prefix)).fetchall()
        result = {"Present": 0, "Absent": 0, "Leave": 0}
        for row in rows:
            result[row["status"]] = row["total"]
        result["Total"] = sum(result.values())
        return result

    def employee_report(self, employee_id, year, month):
        with get_connection() as conn:
            return conn.execute("""
                SELECT attendance_date, status FROM attendance
                WHERE employee_id=? AND attendance_date LIKE ?
                ORDER BY attendance_date
            """, (employee_id, f"{year:04d}-{month:02d}-%")).fetchall()
