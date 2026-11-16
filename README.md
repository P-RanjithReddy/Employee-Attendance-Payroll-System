# Employee Attendance & Payroll Processing System

## Requirements
- Python 3.9 or newer
- No third-party packages required
- SQLite is included with Python

## Run the project
1. Extract `Employee_Attendance_Payroll_System.zip`.
2. Open the extracted folder in VS Code or your terminal.
3. Run:

   ```bash
   python main.py
   ```

4. Choose menu option 1 to add an employee.
5. Note the generated Employee ID (for example, EMP0001).
6. Use option 5 to mark attendance. Enter P for Present, A for Absent, or L for Leave.
7. Use options 6, 7 and 8 for monthly attendance and reports.

## Features
- Employee CRUD operations
- Automatic unique IDs (EMP0001, EMP0002, ...)
- Daily attendance with Present / Absent / Leave
- Monthly attendance summary
- Salary calculation based on attendance
- Individual salary and attendance reports
- CSV report export
- SQLite database persistence
- OOP, functions, exception handling and file handling

## Salary calculation used
For a simple training-project rule:

`Payable Salary = (Monthly Salary / Number of calendar days in month) * Present days`

Only days explicitly marked Present are paid. Absent and Leave days are not paid in this simple model. This can be adjusted to match your organization's payroll policy.

## Project structure
```
Employee_Attendance_Payroll_System/
|-- main.py
|-- database.py
|-- employee.py
|-- attendance.py
|-- payroll.py
|-- reports.py
|-- README.md
|-- data/
|-- reports/
```

## Important notes
- Attendance is unique per employee per date. If you mark the same employee/date again, the status is updated.
- The monthly attendance summary counts recorded entries; it does not automatically assume unmarked days are Absent.
- Database file is created automatically at `data/attendance.db`.
- CSV reports are created automatically in `reports/`.
