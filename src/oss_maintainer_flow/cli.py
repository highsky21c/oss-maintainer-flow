from __future__ import annotations

import argparse
import json
from pathlib import Path

from .health import render_health_report
from .release_notes import PullRequest, render_release_notes
from .triage import Issue, render_triage_report, suggest_issue


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
    suggestions = [suggest_issue(issue) for issue in issues]
    print(render_triage_report(suggestions), end="")


def run_release_notes(args: argparse.Namespace) -> None:
    pulls = [build_pull_request(item) for item in load_json(args.input)]
    print(render_release_notes(pulls, args.version), end="")


def run_health(args: argparse.Namespace) -> None:
    issues = [build_issue(item) for item in load_json(args.issues)]
    pulls = [build_pull_request(item) for item in load_json(args.pulls)]
    print(render_health_report(issues, pulls), end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oss-maintainer-flow")
    subcommands = parser.add_subparsers(dest="command", required=True)

    triage = subcommands.add_parser("triage", help="Suggest labels for issue JSON.")
    triage.add_argument("input", type=Path)
    triage.set_defaults(func=run_triage)

    release_notes = subcommands.add_parser("release-notes", help="Draft release notes from pull request JSON.")
    release_notes.add_argument("input", type=Path)
    release_notes.add_argument("--version", required=True)
    release_notes.set_defaults(func=run_release_notes)

    health = subcommands.add_parser("health", help="Report maintainer workflow health from issue and PR JSON.")
    health.add_argument("issues", type=Path)
    health.add_argument("pulls", type=Path)
    health.set_defaults(func=run_health)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
