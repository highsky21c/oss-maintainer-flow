from __future__ import annotations

import argparse
import json
from pathlib import Path

from .github_import import fetch_github_export
from .health import render_health_report
from .release_notes import PullRequest, render_release_checklist, render_release_notes
from .triage import Issue, load_triage_config, render_triage_report, suggest_issue


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise SystemExit("Input JSON must be a list of objects.")
    return data


def build_issue(item: dict) -> Issue:
    return Issue(
        number=int(item.get("number", 0)),
        title=str(item.get("title", "")).strip(),
        body=str(item.get("body", "") or ""),
        labels=tuple(str(label) for label in item.get("labels", [])),
    )


def build_pull_request(item: dict) -> PullRequest:
    return PullRequest(
        number=int(item.get("number", 0)),
        title=str(item.get("title", "")).strip(),
        author=str(item.get("author", "") or ""),
        labels=tuple(str(label) for label in item.get("labels", [])),
        merged_at=item.get("merged_at"),
    )


def run_triage(args: argparse.Namespace) -> None:
    issues = [build_issue(item) for item in load_json(args.input)]
    config = load_triage_config(args.config) if args.config else None
    suggestions = [suggest_issue(issue, config) if config else suggest_issue(issue) for issue in issues]
    print(render_triage_report(suggestions), end="")


def run_release_notes(args: argparse.Namespace) -> None:
    pulls = [build_pull_request(item) for item in load_json(args.input)]
    print(render_release_notes(pulls, args.version), end="")


def run_release_checklist(args: argparse.Namespace) -> None:
    pulls = [build_pull_request(item) for item in load_json(args.input)]
    changelog = args.changelog.read_text(encoding="utf-8") if args.changelog else ""
    print(render_release_checklist(pulls, args.version, changelog), end="")


def run_health(args: argparse.Namespace) -> None:
    issues = [build_issue(item) for item in load_json(args.issues)]
    pulls = [build_pull_request(item) for item in load_json(args.pulls)]
    print(render_health_report(issues, pulls), end="")


def run_import_github(args: argparse.Namespace) -> None:
    items = fetch_github_export(args.repository, args.kind, args.state, args.token)
    print(json.dumps(items, ensure_ascii=False, indent=2), end="\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oss-maintainer-flow")
    subcommands = parser.add_subparsers(dest="command", required=True)

    triage = subcommands.add_parser("triage", help="Suggest labels for issue JSON.")
    triage.add_argument("input", type=Path)
    triage.add_argument("--config", type=Path, help="Optional JSON file with project-specific triage rules.")
    triage.set_defaults(func=run_triage)

    release_notes = subcommands.add_parser("release-notes", help="Draft release notes from pull request JSON.")
    release_notes.add_argument("input", type=Path)
    release_notes.add_argument("--version", required=True)
    release_notes.set_defaults(func=run_release_notes)

    release_checklist = subcommands.add_parser(
        "release-checklist",
        help="Draft a release readiness checklist from pull request JSON.",
    )
    release_checklist.add_argument("input", type=Path)
    release_checklist.add_argument("--version", required=True)
    release_checklist.add_argument("--changelog", type=Path, help="Optional changelog file to check for PR references.")
    release_checklist.set_defaults(func=run_release_checklist)

    health = subcommands.add_parser("health", help="Report maintainer workflow health from issue and PR JSON.")
    health.add_argument("issues", type=Path)
    health.add_argument("pulls", type=Path)
    health.set_defaults(func=run_health)

    import_github = subcommands.add_parser(
        "import-github",
        help="Export GitHub issues or pull requests as local JSON.",
    )
    import_github.add_argument("repository", help="Repository in owner/name form or a GitHub repository URL.")
    import_github.add_argument("--kind", choices=("issues", "pulls"), required=True)
    import_github.add_argument("--state", default="open", choices=("open", "closed", "all"))
    import_github.add_argument("--token", help="Optional GitHub token. Defaults to GITHUB_TOKEN.")
    import_github.set_defaults(func=run_import_github)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
