"""
Convert the exported Google Sheets CSV into data.json for the dashboard.

Usage:
    python csv_to_json.py input.csv data.json

It reads the CSV columns and builds proper GitHub URLs from the
Issue/PR columns. Handles these formats:
    - "CQT-reporting #4"        -> https://github.com/qiboteam/CQT-reporting/issues/4
    - "CQT-reporting/issues/17" -> https://github.com/qiboteam/CQT-reporting/issues/17
    - "qibocal #1332"           -> https://github.com/qiboteam/qibocal/issues/1332
    - Full URLs passed through as-is
    - Empty / "-" -> no link
"""

import csv
import json
import re
import sys

GITHUB_BASE = "https://github.com/qiboteam"


def parse_github_ref(raw: str) -> tuple[str, str]:
    """Return (display_label, url) from a raw GitHub Issue or PR cell value."""
    raw = raw.strip().strip("-").strip()
    if not raw:
        return ("", "")

    # Already a full URL
    if raw.startswith("http"):
        label = raw.split("/")[-1]
        # Try to build a nicer label from the URL
        parts = raw.replace(GITHUB_BASE + "/", "").split("/")
        if len(parts) >= 3:
            repo, kind, num = parts[0], parts[1], parts[2]
            label = f"{repo} #{num}"
        return (label, raw)

    # Format: "repo/issues/17" or "repo/pull/8"
    m = re.match(r"^([\w\-]+)/(issues|pull)/(\d+)$", raw)
    if m:
        repo, kind, num = m.group(1), m.group(2), m.group(3)
        url = f"{GITHUB_BASE}/{repo}/{kind}/{num}"
        return (f"{repo} #{num}", url)

    # Format: "repo #123"
    m = re.match(r"^([\w\-]+)\s*#(\d+)$", raw)
    if m:
        repo, num = m.group(1), m.group(2)
        # Issues by default; PRs should come from the PR column
        url = f"{GITHUB_BASE}/{repo}/issues/{num}"
        return (f"{repo} #{num}", url)

    # Unrecognized — keep as label, no URL
    return (raw, "")


def parse_pr_ref(raw: str) -> str:
    """Return a full PR URL from the Github PR column."""
    raw = raw.strip().strip("-").strip()
    if not raw:
        return ""
    if raw.startswith("http"):
        return raw
    # Format: "repo/pull/8"
    m = re.match(r"^([\w\-]+)/pull/(\d+)$", raw)
    if m:
        return f"{GITHUB_BASE}/{m.group(1)}/pull/{m.group(2)}"
    return ""


def convert(input_path: str, output_path: str):
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Strip whitespace from headers
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        data = []
        for row in reader:
            week = row.get("Week ending on day ...", "").strip()
            if not week:
                continue

            issue_label, issue_url = parse_github_ref(
                row.get("Github Issue", "")
            )
            pr_url = parse_pr_ref(row.get("Github PR", ""))

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
                "issue": issue_label,
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
        print("Usage: python csv_to_json.py <input.csv> <output.json>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])