from datetime import date, datetime
from database import initialize_database
from employee import EmployeeManager
from attendance import AttendanceManager
from payroll import Payroll
from reports import export_salary_report, export_attendance_report

employees = EmployeeManager()
attendance = AttendanceManager()
payroll = Payroll()

def read_salary():
    value = float(input("Monthly salary: ").strip())
    if value < 0:
        raise ValueError("Salary cannot be negative.")
    return value

def employee_details():
    name = input("Employee name: ").strip()
    department = input("Department: ").strip()
    designation = input("Designation: ").strip()
    if not name or not department or not designation:
        raise ValueError("All employee fields are required.")
    return name, department, designation, read_salary()

def show_employees():
    rows = employees.view_employees()
    if not rows:
        print("\\nNo employees found.")
        return
    print("\\nID       | Name                 | Department       | Designation       | Salary")
    print("-" * 90)
    for e in rows:
        print(f"{e['employee_id']:<8} | {e['name']:<20} | {e['department']:<16} | "
              f"{e['designation']:<17} | {e['monthly_salary']:.2f}")

def get_month():
    year = int(input("Year (e.g. 2026): "))
    month = int(input("Month (1-12): "))
    if not 1 <= month <= 12:
        raise ValueError("Month must be from 1 to 12.")
    return year, month

def menu():
    initialize_database()
    while True:
        print("""
========================================================
       EMPLOYEE ATTENDANCE & PAYROLL SYSTEM
========================================================
1. Add Employee
2. View Employees
3. Update Employee
4. Delete Employee
5. Mark Daily Attendance
6. Monthly Attendance Summary
7. Individual Salary Report
8. Employee Attendance Report
9. Exit
""")
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                details = employee_details()
                emp_id = employees.add_employee(*details)
                print(f"Employee added successfully. Employee ID: {emp_id}")

            elif choice == "2":
                show_employees()

            elif choice == "3":
                emp_id = input("Employee ID: ").strip().upper()
                if not employees.get_employee(emp_id):
                    print("Employee ID not found.")
                    continue
                print("Enter updated details:")
                updated = employees.update_employee(emp_id, *employee_details())
                print("Employee updated successfully." if updated else "Update failed.")

            elif choice == "4":
                emp_id = input("Employee ID to delete: ").strip().upper()
                confirm = input("Delete this employee and their attendance? (y/n): ").lower()
                if confirm == "y":
                    print("Employee deleted." if employees.delete_employee(emp_id)
                          else "Employee ID not found.")
                else:
                    print("Delete cancelled.")

            elif choice == "5":
                emp_id = input("Employee ID: ").strip().upper()
                raw_date = input(f"Date (YYYY-MM-DD, Enter for today {date.today()}): ").strip()
                attendance_date = date.today().isoformat() if not raw_date else datetime.strptime(raw_date, "%Y-%m-%d").date().isoformat()
                status = input("Status (P=Present, A=Absent, L=Leave): ").strip().upper()
                status_map = {"P": "Present", "A": "Absent", "L": "Leave"}
                if status not in status_map:
                    raise ValueError("Choose P, A, or L.")
                attendance.mark_attendance(emp_id, attendance_date, status_map[status])
                print("Attendance saved. Re-entering a date updates its status.")

            elif choice == "6":
                emp_id = input("Employee ID: ").strip().upper()
                if not employees.get_employee(emp_id):
                    print("Employee ID not found.")
                    continue
                year, month = get_month()
                s = attendance.monthly_summary(emp_id, year, month)
                print(f"\\nAttendance for {emp_id} - {year:04d}-{month:02d}")
                print(f"Present: {s['Present']} | Absent: {s['Absent']} | Leave: {s['Leave']} | Total marked: {s['Total']}")

            elif choice == "7":
                emp_id = input("Employee ID: ").strip().upper()
                employee = employees.get_employee(emp_id)
                if not employee:
                    print("Employee ID not found.")
                    continue
                year, month = get_month()
                report = payroll.calculate_salary(employee, year, month)
                print("\\n========== SALARY REPORT ==========")
                for key, value in report.items():
                    print(f"{key.replace('_', ' ').title():20}: {value}")
                print("Salary is calculated as monthly salary / calendar days * Present days.")
                path = export_salary_report(report)
                print(f"CSV report saved: {path}")

            elif choice == "8":
                emp_id = input("Employee ID: ").strip().upper()
                if not employees.get_employee(emp_id):
                    print("Employee ID not found.")
                    continue
                year, month = get_month()
                rows = attendance.employee_report(emp_id, year, month)
                print(f"\\nAttendance report for {emp_id} ({year:04d}-{month:02d})")
                if rows:
                    for row in rows:
                        print(f"{row['attendance_date']} : {row['status']}")
                else:
                    print("No attendance records for this month.")
                path = export_attendance_report(emp_id, f"{year:04d}-{month:02d}", rows)
                print(f"CSV report saved: {path}")

            elif choice == "9":
                print("Thank you for using the system.")
                break
            else:
                print("Invalid choice. Enter 1 to 9.")
        except (ValueError, TypeError) as error:
            print(f"Input error: {error}")
        except Exception as error:
            print(f"Something went wrong: {error}")

if __name__ == "__main__":
    menu()
