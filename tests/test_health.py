from oss_maintainer_flow.health import render_health_report
from oss_maintainer_flow.release_notes import PullRequest
from oss_maintainer_flow.triage import Issue


def test_health_report_includes_coverage() -> None:
    report = render_health_report(
        [Issue(number=1, title="Crash", labels=("bug",))],
        [PullRequest(number=2, title="Fix crash", author="highsky21c", labels=("bug",), merged_at="2026-06-24")],
    )

    assert "Issue triage coverage: 100%" in report
    assert "Release-note coverage: 100%" in report


def test_health_report_routes_security_issues() -> None:
    report = render_health_report(
        [Issue(number=1, title="Token leak in debug logs")],
        [],
    )

    assert "Security-sensitive issues needing review: 1" in report
    assert "private disclosure process" in report
