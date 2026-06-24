# API Credit Usage Plan

The project can use API credits to build optional maintainer-reviewed assistance. The default CLI remains offline and deterministic.

## Planned API-backed features

- Draft issue summaries for long bug reports
- Draft pull request review summaries from changed-file metadata
- Suggest release-note categories from merged pull requests
- Identify likely security-sensitive reports for private maintainer review
- Generate maintainer status updates from reviewed project metadata

## Safety and privacy rules

- API-backed features must be opt-in.
- Generated output must be saved as a draft, not posted automatically.
- Every suggestion must include enough source context for review.
- Security-sensitive issues should be minimized or excluded from API calls unless the maintainer explicitly opts in.
- Project-specific redaction rules should run before any external API request.

## Evaluation plan

- Maintain fixture sets for bugs, feature requests, support questions, and security-sensitive reports.
- Compare generated labels against expected maintainer decisions.
- Track false negatives for security-sensitive issues as high-priority failures.
- Require tests for new prompt templates and output parsers.
