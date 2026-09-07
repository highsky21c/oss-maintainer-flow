# Reports

Markdown-producing commands print to stdout by default and can also write reviewable report files with `--output`.

## Triage report

```bash
oss-maintainer-flow triage examples/issues.json --output reports/triage.md
```

## Release notes

```bash
oss-maintainer-flow release-notes examples/pulls.json --version 0.2.0 --output reports/release-notes.md
```

## Release checklist

```bash
oss-maintainer-flow release-checklist examples/pulls.json --version 0.2.0 --changelog CHANGELOG.md --output reports/release-checklist.md
```

## Health report

```bash
oss-maintainer-flow health examples/issues.json examples/pulls.json --output reports/health.md
```

## GitHub exports

GitHub exports are JSON, but they use the same output behavior:

```bash
oss-maintainer-flow import-github highsky21c/oss-maintainer-flow --kind issues --output data/issues.json
```

Writing reports to files makes it easier to review generated output in pull requests before posting anything publicly.
