from database import get_connection

class EmployeeManager:
    def generate_employee_id(self):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT MAX(CAST(SUBSTR(employee_id, 4) AS INTEGER)) AS n FROM employees"
            ).fetchone()
            return f"EMP{(row['n'] or 0) + 1:04d}"

    def add_employee(self, name, department, designation, salary):
        employee_id = self.generate_employee_id()
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
                (employee_id, name, department, designation, salary)
            )
        return employee_id

    def view_employees(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM employees ORDER BY employee_id").fetchall()

    def get_employee(self, employee_id):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM employees WHERE employee_id=?", (employee_id,)
            ).fetchone()

    def update_employee(self, employee_id, name, department, designation, salary):
        with get_connection() as conn:
            cur = conn.execute("""
                UPDATE employees SET name=?, department=?, designation=?, monthly_salary=?
                WHERE employee_id=?
            """, (name, department, designation, salary, employee_id))
            return cur.rowcount > 0

    def delete_employee(self, employee_id):
        with get_connection() as conn:
            exists = conn.execute(
                "SELECT 1 FROM employees WHERE employee_id=?", (employee_id,)
            ).fetchone()
            if not exists:
                return False
            conn.execute("DELETE FROM attendance WHERE employee_id=?", (employee_id,))
            conn.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
            return True
