from oss_maintainer_flow.release_notes import PullRequest, render_release_checklist, render_release_notes


def test_release_notes_group_pull_requests() -> None:
    notes = render_release_notes(
        [
            PullRequest(number=1, title="Add export command", author="highsky21c", labels=("feature",)),
            PullRequest(number=2, title="Fix crash", author="highsky21c", labels=("bug",)),
        ],
        "0.1.0",
    )

    assert "# Release 0.1.0" in notes
    assert "## Features" in notes
    assert "## Fixes" in notes
    assert "Add export command (#1) by @highsky21c" in notes


def test_release_checklist_flags_missing_metadata() -> None:
    checklist = render_release_checklist(
        [
            PullRequest(number=1, title="Add export command", author="highsky21c", labels=("feature",)),
            PullRequest(number=2, title="Fix crash", author="highsky21c", merged_at="2026-06-24"),
        ],
        "0.2.0",
        changelog="- Add export command (#1)",
    )

    assert "# Release Checklist 0.2.0" in checklist
    assert "- [ ] Every pull request has at least one release label." in checklist
    assert "- [ ] Every pull request has a merged timestamp." in checklist
    assert "- [ ] Every pull request appears in the changelog." in checklist
    assert "## Pull requests missing release labels" in checklist
    assert "#2 Fix crash" in checklist


def test_release_checklist_marks_complete_metadata() -> None:
    checklist = render_release_checklist(
        [
            PullRequest(
                number=1,
                title="Add export command",
                author="highsky21c",
                labels=("feature",),
                merged_at="2026-06-24",
            )
        ],
        "0.2.0",
        changelog="- Add export command (#1)",
    )

    assert "- [x] Every pull request has at least one release label." in checklist
    assert "- [x] Every pull request has a merged timestamp." in checklist
    assert "- [x] Every pull request appears in the changelog." in checklist
