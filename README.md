# rulespec-ca

Canada RuleSpec encodings and source registry metadata.

## Layout

- `statutes/`: Canadian statute RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `regulations/`: Canadian regulation RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `policies/`: Canadian policy RuleSpec YAML, with tests beside each encoding as `.test.yaml`.
- `sources/`: source registry or manifest metadata when needed.

Do not add singular rule roots, separate parameter/test fixture files, or
generated formula artifacts.
