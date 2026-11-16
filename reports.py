import csv
from pathlib import Path

REPORT_DIR = Path(__file__).parent / "reports"

def export_salary_report(report):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / f"salary_{report['employee_id']}_{report['month']}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        for key, value in report.items():
            writer.writerow([key.replace("_", " ").title(), value])
    return path

def export_attendance_report(employee_id, month, rows):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / f"attendance_{employee_id}_{month}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Status"])
        writer.writerows([(r["attendance_date"], r["status"]) for r in rows])
    return path
