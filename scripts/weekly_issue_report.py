import requests
import os
from datetime import datetime, timedelta

# Load GitHub token from environment (provided automatically by GitHub Actions)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = "microsoft/documentdb"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_open_issues():
    url = f"https://api.github.com/repos/{REPO}/issues"
    params = {
        "state": "open",
        "per_page": 100,
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def categorize_issues(issues):
    unassigned = []
    needs_triage = []
    now = datetime.utcnow()
    
    for issue in issues:
        if 'pull_request' in issue:
            continue  # Skip PRs

        updated_at = datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        labels = [l["name"] for l in issue["labels"]]

        if not issue["assignees"]:
            unassigned.append(issue)
        elif not labels or (now - updated_at).days > 14:
            needs_triage.append(issue)

    return unassigned, needs_triage

def format_issue_md(issue):
    number = issue["number"]
    title = issue["title"]
    url = issue["html_url"]
    labels = ", ".join(l["name"] for l in issue["labels"]) or "none"
    created = issue["created_at"][:10]
    return f"- [#{number}]({url}) **{title}** – Labels: {labels} | Created: {created}"

def generate_report_md(unassigned, needs_triage):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    lines = [f"# 🛠️ Weekly Issue Report – {today}\n"]

    lines.append("## 🔍 Unassigned Issues\n")
    if unassigned:
        for issue in unassigned:
            lines.append(format_issue_md(issue))
    else:
        lines.append("_No unassigned issues._")

    lines.append("\n## 📋 Issues Needing Triage\n")
    if needs_triage:
        for issue in needs_triage:
            lines.append(format_issue_md(issue))
    else:
        lines.append("_No triage-needed issues._")

    return "\n".join(lines)

def main():
    issues = get_open_issues()
    unassigned, needs_triage = categorize_issues(issues)
    report = generate_report_md(unassigned, needs_triage)

    with open("weekly_issue_report.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()
