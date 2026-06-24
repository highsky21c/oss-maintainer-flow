# OSS Maintainer Flow

OSS Maintainer Flow is a small Python CLI for open source maintainers who need a repeatable way to triage issues, summarize pull request work, and draft release notes without moving project data into an ad hoc spreadsheet.

The project is intentionally plain text first. It reads GitHub issue exports or simple JSON files, applies transparent triage rules, and produces Markdown that maintainers can review before posting publicly.

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

- GitHub API import command
- Configurable project-specific triage rules
- Optional OpenAI API integration for maintainer-reviewed summaries
- Release checklist generation
- Security advisory draft templates

## Maintainer principles

- Suggestions should be explainable.
- Human maintainers make final decisions.
- Sensitive reports should be routed conservatively.
- Automation should reduce toil without hiding context from contributors.

## License

MIT
