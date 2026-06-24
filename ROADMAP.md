# Roadmap

This roadmap focuses on maintenance work that is visible, reviewable, and useful for small open source projects before it grows into heavier automation.

## v0.1.0 - Maintainer workflow baseline

- Offline issue triage from JSON exports
- Security-sensitive issue detection
- Release-note drafting from merged pull request metadata
- Maintainer health report for triage and release metadata coverage
- CI, tests, issue templates, PR template, security policy, and contribution guide

## v0.2.0 - GitHub workflow import

- Import open issues and merged pull requests from the GitHub API
- Support repository-specific triage rule configuration
- Export reports as Markdown files for maintainers to review in pull requests
- Add fixture-based tests for GitHub API response normalization

## v0.3.0 - Maintainer-reviewed AI assistance

- Add optional OpenAI API integration for issue summaries and PR review summaries
- Keep all AI output in draft form until a maintainer approves it
- Add evaluation fixtures for hallucination-prone issue reports
- Add privacy controls for excluding sensitive issue bodies from API calls

## v0.4.0 - Release operations

- Generate release checklists from merged pull requests
- Draft GitHub Release notes from reviewed Markdown output
- Detect missing changelog entries
- Add advisory templates for coordinated security releases

## Success metrics

- Time from issue export to triage report under one minute for small projects
- Every generated suggestion includes a rationale
- Security-sensitive reports are conservatively flagged
- Release notes can be reproduced from versioned input data
