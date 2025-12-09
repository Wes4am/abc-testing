# backend/exporter.py

import csv
from openpyxl import Workbook
from typing import List


def export_csv(rows: List[List[str]], filepath: str) -> None:
    """Export list of rows to CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Variation", "Message"])
        writer.writerows(rows)


def export_xlsx(rows: List[List[str]], filepath: str) -> None:
    """Export list of rows to XLSX file."""
    wb = Workbook()
    ws = wb.active
    ws.append(["Variation", "Message"])

    for row in rows:
        ws.append(row)

    wb.save(filepath)


if __name__ == '__main__':
    # Quick test
    sample_rows = [["A", "Hello!"], ["B", "Hi there!"]]
    export_csv(sample_rows, "test.csv")
    export_xlsx(sample_rows, "test.xlsx")
    print("Exported CSV and XLSX successfully")