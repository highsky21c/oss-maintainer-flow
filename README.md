# OSS Maintainer Flow

[![CI](https://github.com/highsky21c/oss-maintainer-flow/actions/workflows/ci.yml/badge.svg)](https://github.com/highsky21c/oss-maintainer-flow/actions/workflows/ci.yml)

OSS Maintainer Flow is a small Python CLI for open source maintainers who need a repeatable way to triage issues, summarize pull request work, and draft release notes without moving project data into an ad hoc spreadsheet.

The project is intentionally plain text first. It reads GitHub issue exports or simple JSON files, applies transparent triage rules, and produces Markdown that maintainers can review before posting publicly.

Current status: early-stage public maintainer tooling project. The repository is set up with tests, CI, issue templates, a security policy, a release process, and a public roadmap so maintenance work can happen in the open from the start.

## Why this exists

Maintainers spend a lot of time on work that is important but repetitive:

- identifying bug reports, security-sensitive issues, docs requests, and support questions
- turning merged pull requests into release notes
- preparing short status updates for contributors
- keeping review and release processes understandable for new maintainers

This project gives those workflows a small, auditable base that can later connect to LLM-assisted review and summarization.

## Features

- Suggests issue labels from title, body, and existing labels
- Flags likely security-sensitive reports for maintainer review
- Generates Markdown triage reports
- Drafts release notes from merged pull request metadata
- Produces a maintainer health report from issue and pull request exports
- Works offline with JSON input
- Keeps every suggestion reviewable before publication

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
oss-maintainer-flow triage examples/issues.json
oss-maintainer-flow release-notes examples/pulls.json --version 0.1.0
oss-maintainer-flow health examples/issues.json examples/pulls.json
```

## Input formats

Issue input:

```json
[
  {
    "number": 12,
    "title": "Crash when config file is missing",
    "body": "The CLI exits with a traceback if config.yaml is absent.",
    "labels": []
  }
]
```

Pull request input:

```json
[
  {
    "number": 31,
    "title": "Add JSON export command",
    "author": "contributor",
    "labels": ["feature"],
    "merged_at": "2026-06-24T00:00:00Z"
  }
]
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned milestones.

## Maintainer principles

- Suggestions should be explainable.
- Human maintainers make final decisions.
- Sensitive reports should be routed conservatively.
- Automation should reduce toil without hiding context from contributors.

## Maintainer workflow coverage

| Program signal | Repository evidence |
| --- | --- |
| Issue triage | `triage` command, issue templates, security-sensitive issue detection |
| Pull request review | PR template, maintainer checklist, planned review-summary command |
| Release management | `release-notes` command, changelog, release checklist |
| Active maintenance | Public roadmap issues, CI, contribution guide, security policy |
| Ecosystem value | Focused on reducing repeat maintainer toil for any GitHub-hosted OSS project |

## License

MIT
