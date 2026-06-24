from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    author: str
    labels: tuple[str, ...] = ()
    merged_at: str | None = None


SECTIONS = (
    ("Breaking Changes", ("breaking", "breaking-change")),
    ("Features", ("feature", "enhancement")),
    ("Fixes", ("bug", "fix")),
    ("Documentation", ("documentation", "docs")),
    ("Maintenance", ("chore", "maintenance", "ci")),
)


def section_for(pr: PullRequest) -> str:
    lower_labels = {label.lower() for label in pr.labels}
    for section, labels in SECTIONS:
        if lower_labels.intersection(labels):
            return section
    return "Other Changes"


def render_release_notes(pulls: list[PullRequest], version: str) -> str:
    grouped: dict[str, list[PullRequest]] = {}
    for pr in pulls:
        grouped.setdefault(section_for(pr), []).append(pr)

    lines = [f"# Release {version}", ""]
    for section, _labels in (*SECTIONS, ("Other Changes", ())):
        items = grouped.get(section, [])
        if not items:
            continue
        lines.append(f"## {section}")
        for pr in items:
            author = f" by @{pr.author}" if pr.author else ""
            lines.append(f"- {pr.title} (#{pr.number}){author}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
