# Configuration

Projects can add repository-specific triage rules with a JSON config file. Built-in rules remain active, and custom rules are appended.

## Example

```json
{
  "rules": [
    {
      "label": "packaging",
      "terms": ["wheel", "sdist", "pip install"],
      "rationale": "packaging"
    }
  ],
  "security_terms": ["private key", "access token"],
  "security_label": "security-review"
}
```

Run triage with:

```bash
oss-maintainer-flow triage examples/issues.json --config examples/triage-config.json
```

## Fields

- `rules`: Additional label rules. Each rule needs a `label` and non-empty `terms` list.
- `terms`: Case-insensitive phrases matched against issue title and body.
- `rationale`: Short text included in the report so maintainers can understand why a label was suggested.
- `security_terms`: Additional security-sensitive phrases.
- `security_label`: Label used for security-sensitive reports. Defaults to `security-review`.

## Maintainer guidance

Keep project-specific rules conservative. Rules should make review easier, not silently decide project policy. If a term is broad or ambiguous, document why it belongs in the project config.
