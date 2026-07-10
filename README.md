# rulespec-ca

Canada RuleSpec encodings and source registry metadata.

## Layout

- `ca/statutes/`: Canadian statute RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `ca/regulations/`: Canadian regulation RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `ca/policies/`: Canadian policy RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `data/corpus/provisions/ca/`: release-pinned Canadian source provisions used for deterministic validation.
- `manifests/releases/current.json`: exact active scopes for the local Canadian corpus release.
- `sources/`: source registry or manifest metadata when needed.

The Canadian release has one active corpus record per module citation. When a
module uses multiple official documents, their source text is consolidated in
that record rather than represented as ambiguous parallel rows.

`ca/` is the only RuleSpec jurisdiction root. Canonical IDs remain
`ca:statutes/...`, `ca:regulations/...`, and `ca:policies/...`; the directory
prefix is repository layout, not part of the ID path after the colon.

Do not add flat compatibility roots, singular rule roots, separate
parameter/test fixture files, or generated formula artifacts.
