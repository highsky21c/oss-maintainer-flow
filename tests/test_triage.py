from oss_maintainer_flow.triage import Issue, suggest_issue


def test_suggests_bug_label_for_crash() -> None:
    suggestion = suggest_issue(Issue(number=1, title="Crash on startup", body="Traceback shown"))

    assert "bug" in suggestion.labels
    assert not suggestion.security_review


def test_flags_security_sensitive_issue() -> None:
    suggestion = suggest_issue(Issue(number=2, title="Token leak in logs"))

    assert "security-review" in suggestion.labels
    assert suggestion.security_review
