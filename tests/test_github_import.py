from oss_maintainer_flow.github_import import (
    label_names,
    normalize_issue,
    normalize_pull_request,
    parse_repository,
)


def test_parse_repository_accepts_owner_name() -> None:
    repo = parse_repository("highsky21c/oss-maintainer-flow")

    assert repo.owner == "highsky21c"
    assert repo.name == "oss-maintainer-flow"


def test_parse_repository_accepts_github_url() -> None:
    repo = parse_repository("https://github.com/highsky21c/oss-maintainer-flow")

    assert repo.owner == "highsky21c"
    assert repo.name == "oss-maintainer-flow"


def test_label_names_handles_api_and_string_labels() -> None:
    assert label_names([{"name": "bug"}, "triage", {"missing": "name"}]) == ["bug", "triage"]


def test_normalize_issue_matches_triage_input_shape() -> None:
    issue = normalize_issue(
        {
            "number": 3,
            "title": "Crash on startup",
            "body": None,
            "labels": [{"name": "bug"}],
        }
    )

    assert issue == {"number": 3, "title": "Crash on startup", "body": "", "labels": ["bug"]}


def test_normalize_pull_request_matches_release_input_shape() -> None:
    pull = normalize_pull_request(
        {
            "number": 8,
            "title": "Add importer",
            "user": {"login": "highsky21c"},
            "labels": [{"name": "enhancement"}],
            "merged_at": "2026-09-07T00:00:00Z",
        }
    )

    assert pull == {
        "number": 8,
        "title": "Add importer",
        "author": "highsky21c",
        "labels": ["enhancement"],
        "merged_at": "2026-09-07T00:00:00Z",
    }
