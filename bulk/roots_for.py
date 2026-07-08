#!/usr/bin/env python3
"""Print the guard-generated `--roots` for an applied module path.

`axiom-encode guard-generated --roots` wants the space-separated content roots
that the changed files live under. rulespec-ca uses a FLAT layout: encoded
modules live at the repository root under `policies/`, `statutes/`, or
`regulations/` (there is no `ca/` jurisdiction directory — the encoder maps a
corpus citation `ca/policy/<rest>` to the module `policies/<rest>.yaml`, and
`ca/statute/<rest>` / `ca/regulation/<rest>` to `statutes/`/`regulations/`
respectively, via the source-root token mapping in axiom-encode). A bulk job
touches exactly one module, so the root is that module's own top-level content
directory — matching how the org validate workflow scopes a single change
(`validate-roots: statutes regulations policies`).

Usage:
  python bulk/roots_for.py policies/cra/t1-2025/canada-workers-benefit.yaml  # -> "policies"
  python bulk/roots_for.py statutes/ita/2007/section/BC1.yaml                # -> "statutes"
"""

from __future__ import annotations

import sys
from pathlib import PurePosixPath

CONTENT_ROOTS = ("policies", "statutes", "regulations")


def roots_for(module_path: str) -> str:
    parts = PurePosixPath(module_path).parts
    if not parts:
        return "policies"
    top = parts[0]
    # Only the three content roots are valid guard roots for this flat repo.
    # Anything else (a stray path) falls back to `policies` so the guard still
    # runs against a real root rather than an invalid one.
    return top if top in CONTENT_ROOTS else "policies"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: roots_for.py <module-path>", file=sys.stderr)
        raise SystemExit(2)
    print(roots_for(sys.argv[1]))
