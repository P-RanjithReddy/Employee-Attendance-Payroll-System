import calendar
from attendance import AttendanceManager

class Payroll:
    def __init__(self):
        self.attendance = AttendanceManager()

    def calculate_salary(self, employee, year, month):
        summary = self.attendance.monthly_summary(employee["employee_id"], year, month)
        working_days = calendar.monthrange(year, month)[1]
        per_day_salary = employee["monthly_salary"] / working_days
        payable = per_day_salary * summary["Present"]
        return {
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "month": f"{year:04d}-{month:02d}",
            "monthly_salary": employee["monthly_salary"],
            "working_days": working_days,
            "present": summary["Present"],
            "absent": summary["Absent"],
            "leave": summary["Leave"],
            "payable_salary": round(payable, 2)
        }
