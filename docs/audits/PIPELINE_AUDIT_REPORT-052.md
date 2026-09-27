# 🏛️ Structural Audit Report: `.agents` nucleus (core / pipeline)
**Audit ID**: #A052-RVX
**Auditor**: `rule_validator` coordinating (`agents.md §6 rule_validator`), nucleus mode (`scripts/_mode.py`: `.git` is a real directory)

---

## 🚦 Executive Summary

Structural, topological and legal sweep of the pipeline environment, run at
Sprint 052's close because `scripts/docs_freshness_check.py . 52` raised
`BLOCK`: the structural delta since the last audited sprint (`last_audit_sprint:
49`) exceeded the 90th-percentile threshold of recent node-count deltas.

**Why this audit exists rather than a field being incremented.** Same
reasoning as `PIPELINE_AUDIT_REPORT-042.md`, `-047.md` and `-049.md`: bumping
`docs/active_state.json` `current_sprint.last_audit_sprint` from `49` to `52`
without doing the audit would assert something that had not happened. This
report is what makes `last_audit_sprint: 52` true.

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Architectural Purity** | 100/100 | ✅ |
| **Governance Compliance** | 99/100 — one propagation gap recorded, not remediated here (§ Findings) | ⚠️ |
| **Unit Coverage** | 917 tests passing, 0 failing (Tester Gate 2, round 1, on the `34d685b` lineage) | ✅ |

### The measurement that triggered it

| Magnitude | Value |
| :--- | :--- |
| p90 threshold of recent node deltas | `3442` |
| Delta from sprint 49 (last audit) to sprint 52 | `9810` (185% over) |
| Window of deltas (10 most recent sprint-to-sprint transitions) | `[1046, 1302, 1343, 1873, 2018, 2213, 2461, 3442, 3643]` |
| Node counts, 049 → 050 → 052 | `10371` → `10586` → `11761` |

Reproduce: `python3 scripts/docs_freshness_check.py . 52`, and the window with
`docs_freshness_check.graph_stats_snapshots(Path('.'))`. Node count 052 confirmed
against `docs/sprints/052-core-pipeline/graph_stats.json` (`nodes: 11761`,
`built_at_commit: 34d685b`, uncommitted at audit time — `git status --porcelain`
lists it untracked).

The delta is genuine and spans **three** sprints, not one, for a second reason
beyond the usual accumulation pattern `PIPELINE_AUDIT_REPORT-047.md` and
`-049.md` already recorded: **Sprint 051 persisted no
`docs/sprints/051-core-pipeline/graph_stats.json`** (confirmed —
`docs_freshness_check` reports `WARN graph_stats missing for … 051` among its
other output), so there is no 049→050→051→052 chain of snapshots to measure
sprint-by-sprint; the only comparable data points are 049, 050 and 052, and the
delta this audit measures is necessarily the full 049→052 span. This is this
sprint's own addition to the still-open framework gap below — not a new
mechanism failure, a second instance of the same one. Sprint 052 itself carries
real, extensive structural content across the span: Wave 6 refactored 42 files
to zero quality-audit violations, three orphan scripts were deleted, `ADR-0015`/
`ADR-0016`/`ADR-0017` were created, `scripts/graph_reconcile.py` was added with
its test, and the sprint's own directory artifacts were created. Recorded, not
corrected here: rewriting historical snapshots would be inventing measurements.

---

## 🔍 Structural Findings & Rule Amendments

| Found Violation | Root Cause | Atomic Rectification | Law Applied |
| :--- | :--- | :--- | :--- |
| `rules/project_topology.md:14` ("Testing Purity") states an unconditional prohibition — local/dev database use for tests forbidden, ephemeral instantiation mandatory — with no cross-reference to the declared-deviation path `agents.md §3 local_testing` now grants via `ADR-0016` (`bbd8d0c`, this sprint). A reader who loads `rules/project_topology.md` alone (its own lazy-load trigger: "touching DB containers") sees only the flat rule and has no visible path to a host's sanctioned SQLite-fidelity deviation, or to the mandatory-ADR-declaration requirement that makes an undeclared deviation a violation. | `ADR-0016`/`U15` restated `agents.md §3 local_testing` (companion unit scope, per the ADR's own closing line: "Companion unit `U15` applies the replacement row text to `agents.md §3`") but the `RA-14` corpus-wide propagation grep was not extended to `rules/project_topology.md`, which states the same substantive constraint in a second location. | Recorded here; the audit edits no rule. **Remediated in the same close at `9f20149`**: the Testing Purity bullet now names the `agents.md §3 local_testing` / `ADR-0016` declared-deviation path and its condition (`RA-14: PATCH_PROPAGATION`). |
| *(no other contradiction found — see sweep table below)* | — | — | — |

### Rule cross-reference performed (`rule_introspection`), scoped to this sprint's changes

Commits audited: `agents.md §1` complexity rows (`ac33d04`, `U65`) and `agents.md
§3 local_testing` (`bbd8d0c`, `U15`), against `rules/qa_and_testing.md`,
`rules/project_topology.md`, `rules/code_craft.md`,
`rules/documentation_standard.md`, `rules/token_economy.md`.

| Check | Command / method | Result |
| :--- | :--- | :--- |
| Stale duplicate of the pre-`U65` claim ("`make verify` does NOT run `make quality-audit`" / "deliberately withheld") anywhere still authoritative | `grep -rn "does NOT run .make quality-audit.\|deliberately withheld" .` | Found only in `docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md`, `docs/sprints/052-core-pipeline/task_scope.md` and `docs/sprints/050-core-pipeline/SPRINT_LOG.md` — all three are historical sprint records narrating the *prior* state before `U65`, not live governance text. No rule file or `agents.md` itself carries the stale claim. **Clean.** |
| `agents.md §1 max_indentation`/`max_lines_per_func` (post-`ac33d04`) claim that `make verify` runs `make quality-audit` | Read `Makefile:53-74` | Confirmed: `verify:` target line 72 runs `python3 scripts/quality_audit.py .` (the same script `make quality-audit` invokes). Claim is accurate, not contradicted by any rule file. |
| `rules/code_craft.md:3` deference clause ("`agents.md §1` already governs style, typing and size; this governs the decisions those metrics cannot see") against the updated complexity rows | Read in full | Still accurate — the row was not restructured, only its wiring-status narrative updated. No update needed, no contradiction. |
| `rules/qa_and_testing.md §1` "100% Code Coverage" mandate against `config/quality_audit_exclusions.json` (complexity exemption for 10 vendored files) | Read both | Distinct instruments — one gates coverage, the other gates complexity/length. The exclusions file only exempts vendored files from `scripts/quality_audit.py`'s complexity scan; it does not touch the coverage mandate. No overlap, no contradiction. |
| `agents.md §3 local_testing` (post-`bbd8d0c`) against `rules/project_topology.md §2` "Testing Purity" | Read both, `ADR-0016` | **Propagation gap — see Findings table above.** Not a logical contradiction (the ADR-0016 deviation is a form of "purely ephemeral DB layer" and would satisfy `project_topology.md`'s literal text), but `project_topology.md` names no deviation path and no ADR-declaration requirement, so a session relying on it alone cannot know the escape hatch or its condition exists. |
| `rules/documentation_standard.md §3` ADR immutability against the `ADR-0015` → `ADR-0017` supersession this sprint performed | Read `ADR-0015`, `ADR-0017`, `documentation_standard.md:50` | Compliant: `ADR-0015` was annotated "Superseded by `ADR-0017`" in place rather than edited; `ADR-0017` is a new numbered file. No contradiction. |
| `rules/token_economy.md` against this sprint's changes | Full read | No reference to `quality_audit`, `local_testing`, or either changed row; no overlap surfaces. |

### Sweep results, each with the command that produced it

| Step | Command | Result |
| :--- | :--- | :--- |
| `rule_introspection` | See cross-reference table above | One propagation gap recorded (`rules/project_topology.md:14`); no other contradiction |
| `skill_standard_check` | `python3 skills/topology-monitor/scripts/legacy_app_auditor.py` | Exit `0` — `AUDIT PASSED: Pipeline Structure is Valid.` |
| `federation_audit` | Nucleus mode: tag/lock/submodule-cleanliness checks correctly skipped (`workflows/audit_workflow.md` row's own rule — the nucleus deliberately floats on `main`, no `.claude_bridge.lock`); the artifact-exists check belongs to `start_workflow.md bridge_check`, clean at this session's boot | No drift reported this session |
| `nomenclature` | Naming sweep of every file ADDED this sprint outside `docs/sprints/052-core-pipeline/` | Zero rename candidates — see verdict table below |
| `precision_audit` | `venv_skillopt/bin/python -c "import skillopt"` | `ModuleNotFoundError` — stack not provisioned. Recorded per the canonical skip-string: `precision_audit skipped: skillopt stack absent`. Same skip as `-047.md`/`-049.md`; provisioning state unchanged |
| `link_audit` | `python3 skills/slash-commander/scripts/verify_commands.py` | All 13 command references resolve; `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` §3.2 names every stem |
| Reference integrity | `python3 scripts/verify_references.py` | Exit `0` — rules reachable, templates exist, citations resolve, every mechanism has an invoker, file:line citations in range |
| Framework self-check (last recorded, this sprint's own Tester Gate 2) | `make verify` | Exit `0`; 917 passed, 0 failing (`SPRINT_LOG.md` Tester Gate 2 round 1, `34d685b` lineage) |

### Nomenclature verdicts

Candidates: every file ADDED this sprint outside
`docs/sprints/052-core-pipeline/` (per `agents.md §5 mandatory_topology`), judged
against `RA-06: IDENTITY_NAMING` Option B and, for ADRs, the
`docs/decisions/ADR-XXXX-[slug].md` convention (`rules/documentation_standard.md
§3`).

| File | Convention checked | Verdict |
| :--- | :--- | :--- |
| `config/quality_audit_exclusions.json` | `config/*.json`, `snake_case` descriptive name — matches `config/model_tiers.json`, `config/rule_triggers.json`, `config/invocation_exceptions.json`, `config/template_gates.json` | Compliant. No rename. |
| `docs/decisions/ADR-0015-artifact-owner-writer-separation.md` | `ADR-XXXX-[slug].md`, four-digit zero-padded, English slug | Compliant. No rename. |
| `docs/decisions/ADR-0016-test-database-isolation.md` | Same | Compliant. No rename. |
| `docs/decisions/ADR-0017-typed-artifact-writer.md` | Same | Compliant. No rename. |
| `scripts/graph_reconcile.py` | `scripts/*.py`, `snake_case` — matches `scripts/detect_drift.py`, `scripts/session_state.py` | Compliant. No rename. |
| `tests/test_graph_reconcile.py` | `tests/test_*.py` pytest convention, mirrors its subject's name | Compliant. No rename. |

Zero rename candidates. Same outcome as `PIPELINE_AUDIT_REPORT-049.md`'s sweep.

---

## 🛠️ Three-File Skill Standard Verification
Sprint 052 forged no new skill (its skill-touching units, `U49`–`U61`, are
complexity refactors of existing skill scripts, not new skills) and deleted
three orphaned scripts (`context_refresher.py`, `coverage_auditor.py`,
`task_auditor.py`) after `RA-16` check (d) found no invoker — a human decision,
not a standard defect. This verifies the existing, now-reduced set.

- [x] **README.md**: certified by `legacy_app_auditor.py` (`[AUDIT PASSED]`).
- [x] **SKILL.md**: procedural logic and YAML manifest verified; `check_manifest_parity.py` exit `0` inside `make verify`.
- [x] **scripts/**: executable logic and `__init__.py` present where the standard requires them (executable skills only — knowledge skills correctly carry no scaffolding, `agents.md §3 three_file_standard`).

---

## 🛡️ Certification

Sprint 052's own subject matter was the Python quality gate (baseline
remediation and `make verify` wiring), invocation-coverage extension, and the
open upstream register — all six now closed
(`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` Sprint 052 status block, all
`ac33d04`-measured entries closed). This closeout audit found the nucleus's
structural documentation consistent with its tree, with one recorded exception:
the `rules/project_topology.md` propagation gap above, which is a documentation
completeness defect, not a functional contradiction — the underlying
constraint (ephemeral test database) is not violated by either text, only
under-cross-referenced in one of the two places it is stated.

**One finding is carried, not fixed here**, because it is a framework mechanism
gap and not a violation of the tree under audit — identical to the one
`PIPELINE_AUDIT_REPORT-042.md`, `-047.md`, and `-049.md` all recorded and still
open: `current_sprint.last_audit_sprint` is written by **no workflow and no
script** (`grep -rn "last_audit_sprint" workflows/ scripts/` returns only its
read site in `docs_freshness_check.py`), so a human/agent must remember to
advance it by hand at the end of every audit report — this one included. This
sprint adds its own instance of the adjacent, related gap `-049.md` first
named for a different mechanism (persisting `graph_stats.json` every close):
**Sprint 051 is the second sprint on record to skip persisting
`docs/sprints/[ID]-core-pipeline/graph_stats.json`** (048 was the first,
per `-049.md`), which is exactly why this audit's delta spans three sprints
(049→050→052) instead of one. Destination unchanged:
`docs/roadmaps/core/pipeline/021-030-program-queue.md`, *Still open for a later
program*.

This report makes `last_audit_sprint: 52` true. Advancing
`docs/active_state.json` `current_sprint.last_audit_sprint` from `49` to `52`
is a separate write, owed to whoever closes Sprint 052, not performed by this
report itself (this audit's scope is limited to the artifact at
`docs/audits/PIPELINE_AUDIT_REPORT-052.md`; no other file was edited).

**Certified under Pipeline Methodology, nucleus mode.**
*Timestamp: 2026-09-27*
*Sealed at: `ai-sprint/052`*
