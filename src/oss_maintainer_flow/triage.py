from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


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


@dataclass(frozen=True)
class TriageRule:
    label: str
    terms: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class TriageConfig:
    rules: tuple[TriageRule, ...]
    security_terms: tuple[str, ...]
    security_label: str = "security-review"


RULES: tuple[TriageRule, ...] = (
    TriageRule("bug", ("crash", "traceback", "exception", "broken", "error", "fails"), "bug"),
    TriageRule("documentation", ("docs", "documentation", "readme", "tutorial"), "documentation"),
    TriageRule("enhancement", ("feature", "support", "add", "improve"), "enhancement"),
    TriageRule("question", ("how do i", "how to", "question", "help"), "question"),
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

DEFAULT_CONFIG = TriageConfig(RULES, SECURITY_TERMS)


def config_from_dict(data: dict) -> TriageConfig:
    custom_rules: list[TriageRule] = []
    for item in data.get("rules", []):
        label = str(item["label"]).strip()
        terms = tuple(str(term).lower() for term in item.get("terms", []))
        rationale = str(item.get("rationale", label)).strip()
        if label and terms:
            custom_rules.append(TriageRule(label, terms, rationale))

    custom_security_terms = tuple(str(term).lower() for term in data.get("security_terms", []))
    security_label = str(data.get("security_label", DEFAULT_CONFIG.security_label)).strip()

    return TriageConfig(
        rules=(*DEFAULT_CONFIG.rules, *custom_rules),
        security_terms=(*DEFAULT_CONFIG.security_terms, *custom_security_terms),
        security_label=security_label or DEFAULT_CONFIG.security_label,
    )


def load_triage_config(path: Path) -> TriageConfig:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise SystemExit("Triage config JSON must be an object.")
    return config_from_dict(data)


def suggest_issue(issue: Issue, config: TriageConfig = DEFAULT_CONFIG) -> TriageSuggestion:
    text = f"{issue.title}\n{issue.body}".lower()
    existing = {label.lower() for label in issue.labels}
    labels: list[str] = []
    rationale: list[str] = []

    for rule in config.rules:
        if rule.label.lower() in existing:
            continue
        if any(term in text for term in rule.terms):
            labels.append(rule.label)
            rationale.append(f"Matched {rule.rationale} language in the issue text.")

    security_review = any(term in text for term in config.security_terms)
    if security_review and config.security_label.lower() not in existing:
        labels.append(config.security_label)
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
