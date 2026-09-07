from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityAdvisory:
    title: str
    affected_versions: str
    patched_versions: str
    severity: str = "unknown"
    summary: str = ""
    impact: str = ""
    remediation: str = ""
    disclosure_status: str = "draft"


def build_advisory(item: dict) -> SecurityAdvisory:
    return SecurityAdvisory(
        title=str(item.get("title", "Security advisory draft")).strip(),
        affected_versions=str(item.get("affected_versions", "unknown")).strip(),
        patched_versions=str(item.get("patched_versions", "unreleased")).strip(),
        severity=str(item.get("severity", "unknown")).strip(),
        summary=str(item.get("summary", "") or "").strip(),
        impact=str(item.get("impact", "") or "").strip(),
        remediation=str(item.get("remediation", "") or "").strip(),
        disclosure_status=str(item.get("disclosure_status", "draft")).strip(),
    )


def fallback(value: str, placeholder: str) -> str:
    return value if value else placeholder


def render_security_advisory(advisory: SecurityAdvisory) -> str:
    lines = [
        f"# {advisory.title}",
        "",
        f"- Disclosure status: {advisory.disclosure_status}",
        f"- Severity: {advisory.severity}",
        f"- Affected versions: {advisory.affected_versions}",
        f"- Patched versions: {advisory.patched_versions}",
        "",
        "## Summary",
        "",
        fallback(advisory.summary, "Draft summary pending maintainer review."),
        "",
        "## Impact",
        "",
        fallback(advisory.impact, "Impact assessment pending maintainer review."),
        "",
        "## Remediation",
        "",
        fallback(advisory.remediation, "Remediation steps pending maintainer review."),
        "",
        "## Maintainer checklist",
        "",
        "- [ ] Confirm the report is not being discussed in a public issue before disclosure.",
        "- [ ] Confirm affected and patched versions are accurate.",
        "- [ ] Confirm reproduction details are stored privately.",
        "- [ ] Confirm public language avoids exposing exploit details prematurely.",
        "- [ ] Publish only after the fix and disclosure timing are approved.",
    ]
    return "\n".join(lines).rstrip() + "\n"
