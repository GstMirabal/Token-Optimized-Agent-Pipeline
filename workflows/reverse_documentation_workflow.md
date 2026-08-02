---
description: "Reverse Documentation Protocol (Keyword: revdoc)"
version: 1.0.0
invoked_by: human:/agents:revdoc
---

# 📐 Workflow: Reverse Documentation

Produce documentation for an existing codebase that is **true**, and provably
so. Runs before any remediation work on a repository the pipeline has not
documented, and before any sprint that will restructure one.

> [!IMPORTANT]
> Reverse engineering produces convincing documentation whether or not it is
> correct — that is its characteristic failure, not an occasional one. Every
> phase below exists because a confident, false document survived the phase
> before it.

## Why this runs first

Documenting after fixing produces text that justifies what was done. Fixing
before documenting means fixing against a model of the system rather than the
system. Both fail quietly.

The order is also load-bearing in a way that is easy to miss: **writing a
contract forces reading each entry point end to end**, and that is where
defects invisible to a module-level reading surface. In the sprint that
produced this workflow, both capital-risk findings in a trading relay came out
of writing its API contract — neither was visible in a blueprint.

## Execution Flow

| Phase | Action | Gate |
| :--- | :--- | :--- |
| **1** | **Graph first.** `graphify update <path> --force`. | Node count and file coverage recorded. |
| **2** | **Measure coverage.** Every source file present in the graph. | Uncovered files listed and explained, not ignored. |
| **3** | **Read the existing documentation.** Every file under `docs/`, in full. | — |
| **4** | **Contrast each claim against the graph and the tree.** | Every path, symbol and route the documentation declares is confirmed to exist. |
| **5** | **Correct what is false**, in place, saying what it said before. | — |
| **6** | **Write the missing contracts**, one per exposed interface, using the `contract-writer` skill. | Every endpoint and public interface has one. |
| **7** | **Diátaxis classification.** Reference, Explanation, How-to, Tutorial. | No document does two jobs. |
| **8** | **Prose gate.** `vale docs/`. | Zero findings. |
| **9** | **Coverage closure.** Re-run phase 4 against the finished set. | Zero stale references. |
| **10** | **Freshness gate.** `docs_freshness_check.py . <sprint>` | Exit 0. |

## Phase 1 — Graph first, not graph afterwards

The graph is the **input** to reverse engineering, not a check applied to its
output. Writing first and validating later produces a document whose errors you
then go looking for, which is a worse method than not making them.

```bash
graphify update . --force        # --force is required after a refactor that deleted code
```

If `graphify` is not on `PATH`, it is usually installed inside the framework's
own environment:

```bash
.agents/venv_skillopt/bin/python -m graphify update . --force
```

## Phase 4 — What "contrast" means, concretely

Not reading the document and nodding. Extracting its claims and checking each
one:

```bash
# Every path the documentation declares, and whether it exists
grep -hoE '`[a-zA-Z0-9_/.-]+\.(py|toml|yml|sh|md)`' docs/**/*.md \
  | tr -d '`' | sort -u \
  | while read -r p; do [ -e "$p" ] || echo "STALE: $p"; done
```

Run this **for every path prefix the repository has ever used**, not only the
current one. A restructuring sprint leaves documentation citing the old tree,
and a grep scoped to the new prefix finds nothing wrong.

That is not hypothetical: a repository that moved `backend/apps/users/` to
`users/` shipped a customization guide whose first command was
`python backend/manage.py`. The check that would have caught it was scoped to
`users/` and reported clean.

## Phase 6 — Contracts are where the defects are

A contract states, per interface: inputs with types and constraints, every
status code, what the caller can and cannot infer, and what the host must
supply. Writing one honestly is impossible without following a request through
to its effect, which is why this phase finds what module-level reading does
not.

Use the `contract-writer` skill (`skills/contract-writer/`) rather than
improvising the shape. It exists for this phase and, until Phase 019, this
workflow did not name it once — the skill was built for the job and left
unwired, which is the pattern `RA-16` now blocks.

Record what is **absent** as explicitly as what is present. A blueprint stating
"no contract exists for this interface at this audit" is doing its job; one
that omits the interface is not.

## Phase 8 — Run the linter, do not merely configure it

`vale` requires `.vale.ini` and a styles directory. If a repository has the
configuration and no one has ever run the binary, the gate has never gated
anything.

Installing it globally is prohibited (`agents.md §2 no_globals`). Fetch the
binary into a scratch directory instead:

```bash
curl -sL "https://github.com/errata-ai/vale/releases/download/v${V}/vale_${V}_macOS_arm64.tar.gz" \
  | tar xz -C "$SCRATCH"
"$SCRATCH/vale" docs/
```

## What this protocol does not cover

- **Whether the documented behaviour is the wanted behaviour.** This verifies
  that the documentation matches the code. Whether the code should do that is
  the audit's question, and the human's.
- **Runtime behaviour.** A contract derived from reading is a claim about
  reading. `audit_workflow.md` is where claims get executed.

---
*Feeds `audit_workflow.md`: findings surfaced while writing contracts are
audit input, recorded and not fixed in this phase.*
