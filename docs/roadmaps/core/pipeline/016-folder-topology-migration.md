---
description: "Folder Topology Migration & Phase 015 Follow-up Closure (Phase 16)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 16 - Folder Topology Migration & Phase 015 Follow-up Closure

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100%
- **Sprint ID:** `016` — next sequential number after Phase 15 (`015-terminology-and-nomenclature-hardening.md`, `COMPLETED`). Carries out the folder-path half of that Phase's rebrand, which was deliberately deferred because Phase 13 (`013-refined-telemetry-and-redundancy.md`) was `IN_PROGRESS` in the same `docs/roadmaps/core/matrix/` folder. Phase 13 is still `IN_PROGRESS` (`Strategy Lock: OPEN`, `Completion: 0%`) at the time of this Phase — the human explicitly authorized proceeding anyway rather than waiting further.

## Objective
Complete the deferred half of Phase 015: physically rename `docs/roadmaps/core/matrix/` → `docs/roadmaps/core/pipeline/` and `docs/sprints/core/matrix/` → `docs/sprints/core/pipeline/`, update `docs/active_state.json`'s `active_app` field to match, and close the three follow-up findings flagged at Phase 015's close (an orphaned skill directory, a hardcoded host name leak, and a stale topology doc).

## Work Breakdown

### Part A — Deferred folder rename
| Task | Action |
| :--- | :--- |
| `docs/roadmaps/core/matrix/` → `docs/roadmaps/core/pipeline/` | `git mv` of the whole directory — 15 tracked files (`000-master-blueprint.md` through `015-terminology-and-nomenclature-hardening.md`) renamed with history preserved. |
| `docs/sprints/core/matrix/` → `docs/sprints/core/pipeline/` | Plain `mv` (not `git mv`) — `031_implementation_plan.md` and `032_implementation_plan.md` were untracked, never committed to begin with (`git ls-files` confirmed empty for that path before the move). |
| `docs/active_state.json` | `active_app: "matrix"` → `"pipeline"`, per `docs/contracts/core/topology_mapper_contract.md §1` (`active_layer`/`active_app` resolve to `docs/roadmaps/{active_layer}/{active_app}/`). |
| `CHANGELOG.md` `[Unreleased]` | Phase 015 bullet's trailing pointer updated to the new path (a live "where to find more info" reference, not a historical claim); this Phase's own bullet added. |

**Historical phase files (`000-014`) are relocated but not content-edited** — same non-goal as Phase 015: rewriting their prose would falsify what existed when each was written. This includes Phase 12's own filename, `012-mcp-infrastructure-sentinel-gateway.md`, which keeps its `sentinel` naming as an accurate historical artifact even though the live vocabulary retired that word in Phase 015.

### Part B — Phase 015 follow-up closure
| Finding | Resolution |
| :--- | :--- |
| `skills/skill-creator-3rd/` orphan directory | Deleted entirely. Confirmed via `git ls-files` that it held zero tracked content — only stale `__pycache__/*.pyc` debris left over from the `v3.5.1` rename to `skills/skill-creator/` (untracked, gitignored, safe to remove). |
| `skills/compliance-checker/scripts/kill_switch.sh` host-name leak | Header comment `# 🛡️ CryptoBot Kill Switch (Rule 67)` → `# 🛡️ Kill Switch (Rule 67)`. Repo-wide grep confirmed `CryptoBot` appears nowhere else in framework code — only inside `profiles/crypto-django/` (correctly host-specific) and the Phase 014/015 roadmap prose describing the leak itself. |
| `skills/README.md` stale topology doc | Rewrote the "Triangle of Sovereignty" section, which documented a `core/`/`local/`/`3rd/` sub-layer structure that directly contradicts the current flat-`skills/` rule (`agents.md §3 topological_order` — confirmed via `ls -d skills/core skills/local skills/3rd`, none exist). Replaced with an accurate description of the real convention: flat directory, provenance encoded by the `-3rd` name suffix, project-family packs live under `profiles/[name]/skills/`. Also caught two more institutional-register strays in the same file that the Phase 015 case-insensitive sweep missed: "tactical tags" → "relevant tags", "the sanctioned 'Armory'" → "the sanctioned skill library". |

## Certification Checklist
- [x] `git ls-files` / `git status` confirmed clean rename tracking for `docs/roadmaps/core/matrix/` → `.../pipeline/` (15 files, `R` status); confirmed the sprints-side files were untracked before their plain `mv`.
- [x] Repo-wide grep for `docs/roadmaps/core/matrix`, `docs/sprints/core/matrix`, `skill-creator-3rd`, `CryptoBot` (outside declared non-goals), and `armory`/`tactical tags` returns zero hits in living files.
- [x] `skills/manifest_skills.json` regenerated via `generate_manifest.py` — parity check clean (`missing: []`, `unlisted: []`, `skill-creator-3rd` no longer flagged since the orphan directory is gone).
- [x] Full `pytest` suite (56 tests) green — no code under `hooks/`/`tests/` referenced the moved paths.
- [x] `docs/active_state.json` validated as well-formed JSON post-edit.

## Known follow-ups (still out of scope)
- Phase 13 (`013-refined-telemetry-and-redundancy.md`) remains `IN_PROGRESS`/0% — this Phase moved its file along with the rest of the folder but did not touch its content or advance its work. Whoever picks Phase 13 back up will find it at its new path, `docs/roadmaps/core/pipeline/013-refined-telemetry-and-redundancy.md`.
- `docs/roadmaps/core/pipeline/006-subagent-matrix-reform.md` and `012-mcp-infrastructure-sentinel-gateway.md` keep their historical `matrix`/`sentinel`-named filenames — consistent with the non-goal of not rewriting closed phase history, flagged here only so a future reader isn't confused by the mismatch between folder name (`pipeline/`) and file name.

---
*Closed 2026-07-26, branch `ai-sprint/015`, pending PR against `GstMirabal/.agents`.*
