# Security Advisories

`security-advisory` creates a Markdown draft from local JSON metadata. It is intentionally draft-only and does not publish an advisory, create a GitHub security advisory, or comment on public issues.

## Usage

```bash
oss-maintainer-flow security-advisory examples/security-advisory.json --output reports/security-advisory.md
```

## Input

```json
{
  "title": "Token exposure in verbose logs",
  "affected_versions": "<0.2.0",
  "patched_versions": "0.2.0",
  "severity": "medium",
  "summary": "Verbose logs may include access tokens when debug output is enabled.",
  "impact": "Local logs could disclose credentials to anyone with access to the log files.",
  "remediation": "Upgrade to the patched release, delete affected logs, and rotate exposed tokens.",
  "disclosure_status": "draft"
}
```

## Maintainer guidance

- Keep reproduction details outside public drafts until disclosure is approved.
- Treat missing impact or remediation text as a blocker for publication.
- Confirm affected and patched versions before tagging a release.
- Use the generated checklist as a review aid, not as publication approval.
