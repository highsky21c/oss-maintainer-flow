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


def changelog_mentions_pr(changelog: str, pr: PullRequest) -> bool:
    if not changelog:
        return False
    return f"#{pr.number}" in changelog or pr.title.lower() in changelog.lower()


def render_release_checklist(pulls: list[PullRequest], version: str, changelog: str = "") -> str:
    missing_labels = [pr for pr in pulls if not pr.labels]
    missing_merge_dates = [pr for pr in pulls if not pr.merged_at]
    missing_changelog = [pr for pr in pulls if not changelog_mentions_pr(changelog, pr)]

    lines = [
        f"# Release Checklist {version}",
        "",
        "## Metadata checks",
        f"- [{'x' if not missing_labels else ' '}] Every pull request has at least one release label.",
        f"- [{'x' if not missing_merge_dates else ' '}] Every pull request has a merged timestamp.",
        f"- [{'x' if not missing_changelog else ' '}] Every pull request appears in the changelog.",
        "",
        "## Manual review",
        "- [ ] Confirm CI is passing on the release commit.",
        "- [ ] Review generated release notes against merged pull requests.",
        "- [ ] Confirm security-sensitive changes have appropriate disclosure notes.",
        "- [ ] Tag the release only after changelog and release notes are reviewed.",
    ]

    if missing_labels:
        lines.extend(["", "## Pull requests missing release labels"])
        lines.extend(f"- #{pr.number} {pr.title}" for pr in missing_labels)

    if missing_merge_dates:
        lines.extend(["", "## Pull requests missing merged timestamps"])
        lines.extend(f"- #{pr.number} {pr.title}" for pr in missing_merge_dates)

    if missing_changelog:
        lines.extend(["", "## Pull requests missing changelog references"])
        lines.extend(f"- #{pr.number} {pr.title}" for pr in missing_changelog)

    return "\n".join(lines).rstrip() + "\n"
