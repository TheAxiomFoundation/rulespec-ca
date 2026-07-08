# Bulk encode (CA)

A durable queue for bulk RuleSpec encoding of already-ingested Canadian
provisions. Each entry is encoded with `axiom-encode encode <citation> --apply`
(local `codex` backend), pre-checked with the same gate battery the PR CI runs,
and opened as one PR per module that auto-merges on green.

This is the `rulespec-ca` adaptation of the `rulespec-be`/`rulespec-uk`
dispatcher. The encoder and the CI gates own correctness. This system is
**plumbing**: it never edits or invents generated values. Its only judgement is
*which* provisions to queue.

## rulespec-ca is different in two ways

### 1. Generation is LOCAL (codex), not an OpenAI GitHub runner

Unlike `rulespec-be` (headless `--backend openai` on GitHub-hosted runners),
`rulespec-ca` is drained by a **local codex worker**: it selects `pending`
entries with `bulk/compute_matrix.py`, runs
`axiom-encode encode <citation> --apply --backend codex`, runs the gate battery,
pushes `bulk/<slug>`, and enables auto-merge. Consequently there is **no
`OPENAI_API_KEY` secret** on this repo — only the two secrets the apply + PR
path needs:

| Secret | Why |
| --- | --- |
| `AXIOM_ENCODE_APPLY_SIGNING_KEY` | Signs the apply manifest so `guard-generated` accepts the new files. Org-canonical key (`key_id: axiom-encode-apply-v1`), the same key the existing `policies/**` manifests carry. |
| `BULK_ENCODE_TOKEN` | A `repo`+`workflow`-scoped token used to push the branch and open the PR so the required `validate / validate` check actually runs (a PR opened by the default `GITHUB_TOKEN` does not trigger the `pull_request` event, so auto-merge would hang). |

### 2. FLAT layout — no `ca/` jurisdiction directory

Modules live at the repository root: `policies/…`, `statutes/…`,
`regulations/…`. There is **no `ca/` directory**. No encoder change is needed:
`axiom-encode`'s source-root token map (`policy`/`policies` → `policies`,
`statute[s]` → `statutes`, `regulation[s]` → `regulations`) resolves a corpus
citation to the flat path directly:

| corpus citation (`citation` in worklist) | applied module path |
| --- | --- |
| `ca/policy/cra/t1-2025/<x>` | `policies/cra/t1-2025/<x>.yaml` |
| `ca/statute/<x>` | `statutes/<x>.yaml` |
| `ca/regulation/<x>` | `regulations/<x>.yaml` |

`bulk/roots_for.py` returns the module's top-level content root
(`policies`/`statutes`/`regulations`) for `guard-generated --roots`, matching the
org validate scope (`validate-roots: statutes regulations policies`).

## Pieces

| File | Role |
| --- | --- |
| `bulk/worklist.yaml` | The durable queue. One entry per module. Committed. |
| `bulk/compute_matrix.py` | Turns the worklist into a job matrix / status lookups; single source of truth for selection. |
| `bulk/roots_for.py` | Maps an applied module path to `guard-generated --roots` (its flat content root). |

## Corpus source

The 241 Canadian provisions (`jurisdiction=ca`, all `doc_type=policy`: CRA
T1-2025 / T4127-2026 / TD1-2026 forms and schedules, benefits, Revenu-Québec
TP1-2025, ESDC) live in the Supabase `corpus.current_provisions` view. They are
**not** committed as `provisions/ca/` blobs in any pinned `axiom-corpus` ref, so
the encoder resolves each citation's source text from Supabase
`current_provisions` (its built-in fallback). Every worklist `citation` was
verified to exist there by exact `citation_path` before listing — the encoder
never invents Canadian numbers.

Policy-class sources are **guidance-grade** (CRA/Revenu-Québec forms and
worksheets, not the Income Tax Act itself); the worklist prefers provisions with
clear standalone amounts/rates/formulas and skips aggregation/rollup forms and
cross-reference-heavy ones.

## Branch protection (required for the safety model)

Auto-merge is only safe when a required check gates the merge. `main` protection
is configured as: required check **`validate / validate`**, **`strict: false`**,
repo-level "Allow auto-merge" enabled — the same shape as `rulespec-be`. Without
it, `gh pr merge --auto` could merge before or over a red validate. The
`validate / validate` roll-up runs on every `rulespec-ca` PR, so requiring it
never deadlocks. The drain **never** uses `--admin`, never bypasses a red check,
and never merges directly.

## Statuses

| Status | Meaning |
| --- | --- |
| `pending` | Queued. The next drain may pick it up. |
| `in-progress` | A run is encoding it (transient). |
| `needs-fixtures` | Encoded + applied, but companion fixtures hit the #1060 ceiling. The PR opens; auto-merge holds on the red required check until fixtures land. |
| `pr-open` | A PR exists and is set to auto-merge on green. |
| `merged` | The PR merged to main. Terminal success. |
| `failed` | Encode or a non-fixture gate failed. Needs human triage. Never auto-retried, never merged. |

## Oracle-coverage held state

A freshly encoded output is `unmapped` until `axiom-oracles` gains a mapping, so
its PR HOLDS at the `validate / validate` oracle-coverage gate — the expected,
accountable held state, never a weakened gate. Do **not** hand-edit
`axiom-oracles` concept mappings to force a canary green.
