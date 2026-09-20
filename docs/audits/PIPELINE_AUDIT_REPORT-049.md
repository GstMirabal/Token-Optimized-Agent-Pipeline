# 🏛️ Structural Audit Report: `.agents` nucleus (core / pipeline)
**Audit ID**: #A049-DPR
**Auditor**: `principal_agent` coordinating, nucleus mode (`scripts/_mode.py`: `.git` is a real directory)

---

## 🚦 Executive Summary

Structural, topological and legal sweep of the pipeline environment, run at
Sprint 049's close because `scripts/docs_freshness_check.py` raised a `BLOCK`:
the structural delta since the last audited sprint exceeded the p90 threshold
of recent deltas.

**Why this audit exists rather than a field being incremented.** Same
reasoning as `PIPELINE_AUDIT_REPORT-042.md` and `PIPELINE_AUDIT_REPORT-047.md`:
bumping `current_sprint.last_audit_sprint` without doing the audit would
assert something that had not happened. This report is what makes
`last_audit_sprint: 49` true.

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Architectural Purity** | 100/100 | ✅ |
| **Governance Compliance** | 100/100 | ✅ |
| **Unit Coverage** | 780 tests passing, 0 failing | ✅ |

### The measurement that triggered it

| Magnitude | Value |
| :--- | :--- |
| p90 threshold of recent node deltas | `2461` |
| Delta from sprint 47 (last audit) to sprint 49 | `5661` (130% over) |
| Window of deltas (sprints 39→40…48→49) | `[1046, 1302, 1343, 1764, 2018, 2213, 2433, 2461, 3442]` |
| Node counts, 045 → 046 → 047 → 048 → 049 | `9415` → `9591` → `9920` → `10056` → `10371` |

Reproduce: `python3 scripts/docs_freshness_check.py . 49`, and the window with
`docs_freshness_check.graph_stats_snapshots(Path('.'))`.

The delta is genuine and spans **two** sprints, not one: `last_audit_sprint`
was last set at Sprint 047 and was not advanced by Sprint 048
(`jurisdictional-lock-reconciliation-and-047-residue`), so this measurement
accumulates 048's 13-unit rule restatement **and** 049's 11-unit Cursor-bridge
remediation in one delta — the same accumulation pattern
`PIPELINE_AUDIT_REPORT-047.md` recorded for 046+047. Both sprints added real
content: 048 one new test file plus behavioural changes to seven scripts; 049
one new fixture (`profiles/example-project/rule_triggers.json`), behavioural
changes to six scripts, and 32 new test cases. Recorded, not corrected here:
rewriting historical snapshots would be inventing measurements.

---

## 🔍 Structural Findings & Rule Amendments

| Found Violation | Root Cause | Atomic Rectification | Law Applied |
| :--- | :--- | :--- | :--- |
| *(none — every sweep below returned clean or carries a pre-existing, already-documented item)* | — | — | — |

### Sweep results, each with the command that produced it

| Step | Command | Result |
| :--- | :--- | :--- |
| `rule_introspection` | Full-corpus grep for the two style-score claims this sprint corrected (`F-049-7`), checking for a stray duplicate outside `agents.md`/`config/invocation_exceptions.json` | Clean: the corrected text (`"computes no numeric score"`) appears exactly where U10/U11 landed it — `agents.md` (the two `§1` rows) and `config/invocation_exceptions.json` (the two exception notes) — and nowhere else in `rules/*.md` or `workflows/*.md` |
| `skill_standard_check` | `python3 skills/topology-monitor/scripts/legacy_app_auditor.py` | `[AUDIT PASSED]`, exit `0` |
| `federation_audit` | Nucleus mode: tag/lock/submodule-cleanliness checks correctly skipped (the nucleus deliberately floats on `main`, no `.claude_bridge.lock`); the artifact-exists check already ran this session via `start_workflow.md bridge_check` at `/agents:start` | No drift reported this session |
| `nomenclature` | Naming sweep of `docs/sprints/*`, `docs/decisions/`, `docs/audits/` | Every sprint directory from `021` onward matches `[ID]-[Stack]-[Layer]/`; every ADR matches `ADR-NNNN-slug.md`; every audit report matches `[MODULE]_[TYPE]-[qualifier].md` (Option B). Zero rename candidates among sprint 021+ directories. One pre-existing, already-documented exception carried forward unchanged: `docs/sprints/core/pipeline/` — a Sprint-024-era relic from before Phase 019 standardized the `[ID]-[Stack]-[Layer]/` convention, explicitly named as a historical artifact in `agents.md §5 mandatory_topology` itself ("the nucleus's own `docs/sprints/core/pipeline/`" — one of four forms that circulated before Phase 019). Not this sprint's scope; no prior audit (042, 045, 047) remediated it either |
| `precision_audit` | `rules/skills_and_integrations.md §3` invocation, `--skill agents.md` | **Not run** — `venv_skillopt/bin/python -c "import skillopt"` confirms the stack is not provisioned (`ModuleNotFoundError`), and the Gemini backend it would call needs `GEMINI_API_KEY`, absent in this session (`RA-09` — no attempt made to read `.env` for it). Recorded per the canonical block's skip-string: `precision_audit skipped: skillopt stack absent`. Same skip as `PIPELINE_AUDIT_REPORT-047.md`; provisioning state unchanged since then |
| `link_audit` | `python3 skills/slash-commander/scripts/verify_commands.py` | 13 commands resolve; the slash-commands guide names every stem |
| Reference integrity | `python3 scripts/verify_references.py` | Exit `0` — rules reachable, templates exist, citations resolve, every mechanism has an invoker whose `invoked_by` anchor fragments resolve, file:line citations in range, profile model↔tier map |
| Framework self-check | `make verify` | Exit `0`, 780 tests pass |

---

## 🛠️ Three-File Skill Standard Verification
Status of the skill infrastructure. Sprint 049 forged no skill
(`skill_assignment.md` records the ladder terminating at P1 — every tool
needed, including the two skills *measured* rather than invoked to establish
`F-049-7`, was already registered), so this verifies the existing set.

- [x] **README.md**: certified by `legacy_app_auditor.py`.
- [x] **SKILL.md**: procedural logic and YAML manifest verified; `check_manifest_parity.py` exit `0` inside `make verify`.
- [x] **scripts/**: executable logic and `__init__.py` present where the standard requires them (executable skills only — knowledge skills correctly carry no scaffolding, `agents.md §3 three_file_standard`).

---

## 🛡️ Certification

Sprint 049's own subject matter was a human-requested audit of the Cursor
integration bridge, and this closeout audit found the nucleus's structural
documentation consistent with its tree afterward. No new violation surfaced.
The sprint's own Phase 7 Gate 1 caught two governance-file defects mid-sprint
(`agents.md` overstating `make verify`'s reach; a function past the 50-line
limit) — both confined to files this sprint itself introduced and remediated
in round 2 (`1a45dbd`); neither recurs here.

**One finding is carried, not fixed here**, because it is a framework
mechanism gap and not a violation of the tree under audit — identical to the
one `PIPELINE_AUDIT_REPORT-042.md` and `PIPELINE_AUDIT_REPORT-047.md` both
recorded and still open: `current_sprint.last_audit_sprint` is written by **no
workflow and no script** (`grep -rn "last_audit_sprint" workflows/ scripts/`
returns only its read site in `docs_freshness_check.py`), so a human/agent
must remember to advance it by hand at the end of every audit report — this
one included, and Sprint 048 is the second consecutive sprint to skip it,
which is exactly why this delta spans two sprints instead of one. Destination
unchanged: `docs/roadmaps/core/pipeline/021-030-program-queue.md`, *Still open
for a later program*.

**Certified under Pipeline Methodology, nucleus mode.**
*Timestamp: 2026-09-20*
*Sealed at: `ai-sprint/049`*
