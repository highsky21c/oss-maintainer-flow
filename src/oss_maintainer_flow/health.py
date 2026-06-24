from __future__ import annotations

from .release_notes import PullRequest
from .triage import Issue, suggest_issue


def issue_triage_coverage(issues: list[Issue]) -> float:
    if not issues:
        return 1.0
    triaged = [issue for issue in issues if issue.labels]
    return len(triaged) / len(issues)


def pull_request_release_coverage(pulls: list[PullRequest]) -> float:
    if not pulls:
        return 1.0
    release_ready = [pull for pull in pulls if pull.labels and pull.merged_at]
    return len(release_ready) / len(pulls)


def security_review_count(issues: list[Issue]) -> int:
    return sum(1 for issue in issues if suggest_issue(issue).security_review)


def render_percent(value: float) -> str:
    return f"{round(value * 100)}%"


def render_health_report(issues: list[Issue], pulls: list[PullRequest]) -> str:
    triage_coverage = issue_triage_coverage(issues)
    release_coverage = pull_request_release_coverage(pulls)
    security_count = security_review_count(issues)

    lines = [
        "# Maintainer Health Report",
        "",
        f"- Issues reviewed: {len(issues)}",
        f"- Pull requests reviewed: {len(pulls)}",
        f"- Issue triage coverage: {render_percent(triage_coverage)}",
        f"- Release-note coverage: {render_percent(release_coverage)}",
        f"- Security-sensitive issues needing review: {security_count}",
        "",
        "## Recommended next actions",
    ]

    if triage_coverage < 1:
        lines.append("- Add labels or triage notes to unclassified issues.")
    if release_coverage < 1:
        lines.append("- Add release labels and merged timestamps to pull request metadata.")
    if security_count:
        lines.append("- Route security-sensitive issues to the private disclosure process.")
    if triage_coverage == 1 and release_coverage == 1 and not security_count:
        lines.append("- Maintenance metadata is complete for this export.")

    return "\n".join(lines).rstrip() + "\n"
