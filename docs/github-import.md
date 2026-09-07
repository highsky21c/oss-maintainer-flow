# GitHub Import

`import-github` exports GitHub issue or pull request metadata into the same JSON shapes used by the offline commands.

## Issues

```bash
oss-maintainer-flow import-github highsky21c/oss-maintainer-flow --kind issues --output issues.json
oss-maintainer-flow triage issues.json --config examples/triage-config.json
```

The issue export excludes pull requests returned by GitHub's issues API.

## Pull requests

```bash
oss-maintainer-flow import-github highsky21c/oss-maintainer-flow --kind pulls --state closed --output pulls.json
oss-maintainer-flow release-notes pulls.json --version 0.2.0
oss-maintainer-flow release-checklist pulls.json --version 0.2.0 --changelog CHANGELOG.md
```

## Authentication

Unauthenticated requests work for public repositories but are rate limited. Set `GITHUB_TOKEN` or pass `--token` for higher limits:

```bash
GITHUB_TOKEN=... oss-maintainer-flow import-github owner/repo --kind issues
```

The importer only reads repository metadata. It does not create labels, comments, issues, pull requests, or releases.
