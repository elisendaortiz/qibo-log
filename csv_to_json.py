"""
Convert the exported Google Sheets CSV into data.json for the dashboard.

Usage:
    python csv_to_json.py "data/Quantum_Tracker_OompaLumpa - Progress_log.csv" data.json

Rules:
    - Github Issue / Github PR columns must contain full URLs or be empty/"-"
    - No URL construction or guessing — only real URLs from the spreadsheet
    - The issue display label is extracted from the URL (repo#number)
"""

import csv
import json
import re
import sys


def parse_url(raw: str) -> str:
    """Return the URL if it's a real URL, otherwise empty string."""
    raw = raw.strip().strip("-").strip()
    if raw.startswith("http"):
        return raw
    return ""


def label_from_url(url: str) -> str:
    """Extract a display label like 'repo #123' from a GitHub URL."""
    if not url:
        return ""
    m = re.search(r"github\.com/[^/]+/([^/]+)/(issues|pull)/(\d+)", url)
    if m:
        return f"{m.group(1)} #{m.group(3)}"
    return url


def convert(input_path: str, output_path: str):
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        data = []
        for row in reader:
            week = row.get("Week ending on day ...", "").strip()
            if not week:
                continue

            issue_url = parse_url(row.get("Github Issue", ""))
            pr_url = parse_url(row.get("Github PR", ""))

            effort_raw = row.get("Effort", "").strip()
            try:
                effort = int(float(effort_raw)) if effort_raw else None
            except ValueError:
                effort = None

            data.append({
                "week": week,
                "task": row.get("Thing sorted", "").strip(),
                "effort": effort,
                "desc": row.get("Description", "").strip(),
                "issue": label_from_url(issue_url),
                "issue_url": issue_url,
                "pr": pr_url,
                "status": row.get("Status", "").strip().lower(),
                "blockage": row.get("Blockages", "").strip().strip("-").strip(),
                "remark": row.get("Remarks", "").strip(),
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(data)} rows -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python csv_to_json.py "data/Quantum_Tracker_OompaLumpa - Progress_log.csv" data.json')
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])