from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    body: str = ""
    labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class TriageSuggestion:
    issue: Issue
    labels: tuple[str, ...]
    security_review: bool
    rationale: tuple[str, ...]


RULES: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("bug", ("crash", "traceback", "exception", "broken", "error", "fails"), "bug"),
    ("documentation", ("docs", "documentation", "readme", "tutorial"), "documentation"),
    ("enhancement", ("feature", "support", "add", "improve"), "enhancement"),
    ("question", ("how do i", "how to", "question", "help"), "question"),
)

SECURITY_TERMS = (
    "vulnerability",
    "security",
    "xss",
    "csrf",
    "injection",
    "rce",
    "secret",
    "token leak",
    "credential",
)


def suggest_issue(issue: Issue) -> TriageSuggestion:
    text = f"{issue.title}\n{issue.body}".lower()
    existing = {label.lower() for label in issue.labels}
    labels: list[str] = []
    rationale: list[str] = []

    for label, terms, reason in RULES:
        if label in existing:
            continue
        if any(term in text for term in terms):
            labels.append(label)
            rationale.append(f"Matched {reason} language in the issue text.")

    security_review = any(term in text for term in SECURITY_TERMS)
    if security_review and "security" not in existing:
        labels.append("security-review")
        rationale.append("Contains security-sensitive language and should be reviewed privately.")

    if not labels:
        labels.append("needs-triage")
        rationale.append("No specific rule matched, so maintainer review is needed.")

    return TriageSuggestion(issue, tuple(dict.fromkeys(labels)), security_review, tuple(rationale))


def render_triage_report(suggestions: list[TriageSuggestion]) -> str:
    lines = ["# Triage Report", ""]
    for suggestion in suggestions:
        issue = suggestion.issue
        labels = ", ".join(f"`{label}`" for label in suggestion.labels)
        lines.append(f"## #{issue.number} {issue.title}")
        lines.append(f"- Suggested labels: {labels}")
        lines.append(f"- Security review: {'yes' if suggestion.security_review else 'no'}")
        for reason in suggestion.rationale:
            lines.append(f"- Rationale: {reason}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
