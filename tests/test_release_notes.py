from oss_maintainer_flow.release_notes import PullRequest, render_release_notes


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
