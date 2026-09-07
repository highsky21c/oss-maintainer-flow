from oss_maintainer_flow.security_advisory import build_advisory, render_security_advisory


def test_security_advisory_renders_review_checklist() -> None:
    advisory = build_advisory(
        {
            "title": "Token exposure in verbose logs",
            "affected_versions": "<0.2.0",
            "patched_versions": "0.2.0",
            "severity": "medium",
            "summary": "Verbose logs may include tokens.",
            "impact": "Local logs could disclose credentials.",
            "remediation": "Upgrade and rotate exposed tokens.",
        }
    )

    rendered = render_security_advisory(advisory)

    assert "# Token exposure in verbose logs" in rendered
    assert "- Severity: medium" in rendered
    assert "- [ ] Confirm public language avoids exposing exploit details prematurely." in rendered


def test_security_advisory_uses_placeholders_for_missing_review_text() -> None:
    rendered = render_security_advisory(build_advisory({"title": "Draft"}))

    assert "Draft summary pending maintainer review." in rendered
    assert "Impact assessment pending maintainer review." in rendered
    assert "Remediation steps pending maintainer review." in rendered
