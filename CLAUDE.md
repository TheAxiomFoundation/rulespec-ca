# rulespec-ca Agent Notes

This repo stores Canada RuleSpec encodings and source registry metadata.

## Do

- Put RuleSpec encodings under `ca/statutes/`, `ca/regulations/`, or `ca/policies/`.
- Put tests beside each encoding as `.test.yaml`.
- Keep only source registry or manifest metadata under `sources/` when needed.
- Keep committed Canadian corpus provisions release-pinned by
  `manifests/releases/current.json`.
- Keep canonical RuleSpec IDs in the `ca:statutes/...`, `ca:regulations/...`,
  and `ca:policies/...` namespaces.

## Do Not

- Add flat `statutes/`, `regulations/`, or `policies/` compatibility roots.
- Add singular rule roots, separate parameter/test fixture files, or generated formula artifacts.
- Put unrelated jurisdiction materials here.
- Add unversioned source payloads or corpus files outside the active release.
