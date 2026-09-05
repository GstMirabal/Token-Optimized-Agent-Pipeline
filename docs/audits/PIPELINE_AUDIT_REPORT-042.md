# 🏛️ Structural Audit Report: `.agents` nucleus (core / pipeline)
**Audit ID**: #A042-TGP
**Auditor**: `rule_validator` coordinating, nucleus mode (`scripts/_mode.py`: `.git` is a real directory)

---

## 🚦 Executive Summary

Structural, topological and legal sweep of the pipeline environment, run at Sprint 042's
close because `scripts/docs_freshness_check.py` raised a `BLOCK`: the structural delta
since the last audited sprint exceeded the p90 threshold of recent deltas.

**Why this audit exists rather than a field being incremented.** The gate reads
`current_sprint.last_audit_sprint` in `docs/active_state.json`, and the remedy its
message names — refreshing `0_SYSTEM_OVERVIEW.md` / `0_SYSTEM_ARCHITECTURE.md` — is
**host-only by design**; neither file exists in the nucleus and `close_workflow.md`
Phase 2 says so explicitly. Bumping the field without an audit would have made it
assert something that had not happened. This report is what makes `last_audit_sprint: 42`
true.

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Architectural Purity** | 100/100 | ✅ |
| **Governance Compliance** | 100/100 | ✅ |
| **Unit Coverage** | 678 tests passing, 0 failing | ✅ |

### The measurement that triggered it

| Magnitude | Value |
| :--- | :--- |
| p90 threshold of recent node deltas | `2433` |
| Delta from sprint 041 to 042 | `2662` (9% over) |
| Window of deltas | `[0, 0, 866, 1591, 1764, 1899, 2385, 2433, 3546]` |
| Node counts, 041 → 042 | `8547` → `8845` |

Reproduce: `python3 scripts/docs_freshness_check.py . 42`, and the window with
`docs_freshness_check.graph_stats_snapshots(Path('.'))`.

The delta is genuine — Sprint 042 added two Python modules, a JSON registry, two ADRs
and five sprint records, and the graph indexes prose as well as code. Two of the nine
baseline deltas are **`0`** (sprints 035 and 039), which `close_workflow.md` Phase 5
identifies as a rebuild that no-opped and instructs be re-run. Recorded, not corrected
here: rewriting historical snapshots would be inventing measurements.

---

## 🔍 Structural Findings & Rule Amendments

| Found Violation | Root Cause | Atomic Rectification | Law Applied |
| :--- | :--- | :--- | :--- |
| *(none — every sweep below returned clean)* | — | — | — |

### Sweep results, each with the command that produced it

| Step | Command | Result |
| :--- | :--- | :--- |
| `rule_introspection` | Cross-reference of `rules/*.md` against `agents.md` citations | Clean both ways: no rule cited that is absent from disk, no rule on disk uncited by `agents.md`. 11 rule contexts |
| `skill_standard_check` | `python3 skills/topology-monitor/scripts/legacy_app_auditor.py` | `[AUDIT PASSED]`, exit `0` |
| `federation_audit` | `bridge_state.mirror_missing` / `content_stale` / `bridge_stale`, target `claude`, `nucleus=True` | All `False` — the nucleus bridge is present and current. Tag and lock checks correctly skipped: the nucleus deliberately floats on `main` and holds no `.claude_bridge.lock` (`git describe --exact-match` fails by design) |
| `nomenclature` | Naming sweep of `docs/decisions/` and `docs/hotfixes/` | Every ADR matches `ADR-NNNN-slug.md`; every hotfix matches `H-NNN-layer.md` (`RA-03` sanctioned exception to `RA-06`) |
| `link_audit` | `python3 skills/slash-commander/scripts/verify_commands.py` | 13 commands resolve; the slash-commands guide names every stem |
| Reference integrity | `python3 scripts/verify_references.py` | Exit `0` — rules reachable, templates exist, citations resolve, every mechanism has an invoker (`RA-16`), file:line citations in range |
| Framework self-check | `make verify` | Exit `0`, 18 checks |

`precision_audit` (`skills/skillopt/scripts/train_runner.py`) was **not run**: the
workflow requires explicit human authorization for it and none was given for this
audit. Stated rather than silently skipped.

---

## 🛠️ Three-File Skill Standard Verification
Status of the skill infrastructure. Sprint 042 forged no skill (`skill_assignment.md`
records the ladder terminating at P1), so this verifies the existing 34.

- [x] **README.md**: certified by `legacy_app_auditor.py`.
- [x] **SKILL.md**: procedural logic and YAML manifest verified; `check_manifest_parity.py` exit `0` inside `make verify`.
- [x] **scripts/**: executable logic and `__init__.py` present where the standard requires them (executable skills only — knowledge skills correctly carry no scaffolding, `agents.md §3 three_file_standard`).

---

## 🛡️ Certification

Sprint 042's own subject matter is documentary truth — a check that a template can
pass the gate consuming it — and this audit found the nucleus's structural
documentation consistent with its tree.

**One finding is recorded and routed rather than fixed here**, because it is a
framework defect and not a violation of the tree under audit: in nucleus mode the
`docs_freshness_check` `BLOCK` prescribes refreshing two anchors that do not exist,
and `current_sprint.last_audit_sprint` — the field the whole check pivots on — is
written by **no workflow and no script** (`grep -rn "last_audit_sprint" workflows/ commands/`
returns nothing). A gate whose input has no owner and whose remedy names host-only
files will keep stopping nucleus closes. Destination:
`docs/roadmaps/core/pipeline/021-030-program-queue.md`, *Still open for a later program*.

**Certified under Pipeline Methodology, nucleus mode.**
*Timestamp: 2026-09-02*
*Sealed at: `ai-sprint/042`*
