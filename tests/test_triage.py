from oss_maintainer_flow.triage import Issue, config_from_dict, suggest_issue


def test_suggests_bug_label_for_crash() -> None:
    suggestion = suggest_issue(Issue(number=1, title="Crash on startup", body="Traceback shown"))

    assert "bug" in suggestion.labels
    assert not suggestion.security_review


def test_flags_security_sensitive_issue() -> None:
    suggestion = suggest_issue(Issue(number=2, title="Token leak in logs"))

    assert "security-review" in suggestion.labels
    assert suggestion.security_review


def test_custom_rule_adds_project_specific_label() -> None:
    config = config_from_dict(
        {
            "rules": [
                {
                    "label": "packaging",
                    "terms": ["wheel", "sdist"],
                    "rationale": "packaging",
                }
            ]
        }
    )

    suggestion = suggest_issue(Issue(number=3, title="Wheel build fails"), config)

    assert "bug" in suggestion.labels
    assert "packaging" in suggestion.labels


def test_custom_security_terms_extend_defaults() -> None:
    config = config_from_dict({"security_terms": ["private key"]})

    suggestion = suggest_issue(Issue(number=4, title="Private key appears in logs"), config)

    assert "security-review" in suggestion.labels
    assert suggestion.security_review
