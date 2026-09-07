# Maintainer Playbook

This playbook describes how the repository is intended to be maintained in public.

## Weekly issue triage

1. Export or collect new issue metadata.
2. Run `oss-maintainer-flow triage --output reports/triage.md`.
3. Apply labels only after reviewing the rationale.
4. Move security-sensitive reports to the private disclosure process.
5. Link follow-up work to public roadmap issues when appropriate.

## Pull request review

1. Check that the pull request explains the maintainer workflow being improved.
2. Confirm tests or fixtures cover behavior changes.
3. Confirm user-facing output remains reviewable and avoids automatic publication.
4. Request changes when generated text could hide important context from maintainers.

## Release management

1. Verify CI is passing on `main`.
2. Run `oss-maintainer-flow release-notes --output reports/release-notes.md`.
3. Run `oss-maintainer-flow release-checklist --output reports/release-checklist.md`.
4. Review generated notes against merged pull requests.
5. Update `CHANGELOG.md`.
6. Tag the release and publish reviewed notes.

## Security handling

1. Do not discuss unreleased vulnerabilities in public issues.
2. Acknowledge reports by email.
3. Prepare a private fix branch if needed.
4. Publish an advisory or changelog note after coordinated disclosure.
