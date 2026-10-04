# 🏛️ Structural Audit Report: `.agents` nucleus (core / pipeline)
**Audit ID**: #A053-RVX
**Auditor**: `rule_validator` coordinating (`agents.md §6 rule_validator`), nucleus mode (`scripts/_mode.py`: `.git` is a real directory)

---

## 🚦 Executive Summary

Structural, topological and legal sweep of the pipeline environment, run at
Sprint 053's close because `make docs-freshness-check SPRINT_ID=053` raised
`[BLOCK] Structural change since last audit exceeds the p90 delta threshold`
(`close_workflow.md` Phase 1 `docs_freshness_gate`): the structural delta since
the last audited sprint (`last_audit_sprint: 52`) exceeded the 90th-percentile
threshold of recent snapshot deltas.

**Why this audit exists rather than a field being incremented.** Same
reasoning as `PIPELINE_AUDIT_REPORT-042.md`, `-047.md`, `-049.md` and
`-052.md`: bumping `docs/active_state.json` `current_sprint.last_audit_sprint`
from `52` to `53` without doing the audit would assert something that had not
happened. This report is what makes `last_audit_sprint: 53` true.

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Architectural Purity** | 100/100 — `legacy_app_auditor.py` and `verify_references.py` both exit `0`; no structural violation found | ✅ |
| **Governance Compliance** | 94/100 — two stale statements contradicting the Sprint 053 change (`config/invocation_exceptions.json:60`, `README.md:91`) and two open wording observations (`O6`, `O1`) recorded, none remediated here (§ Findings) | ⚠️ |
| **Unit Coverage** | 946 tests passing, 0 failing (`make verify` exit `0`; `SPRINT_LOG.md` Quality Gate table: Gate 1 QA R2 `APPROVED`, Gate 2 Tester R1 `RECORD`/`testifying`) | ✅ |

Score justification: Purity is 100 because every mechanical structural check
passed and no file sits outside the topology `agents.md §5` requires.
Compliance loses 6 points: 3 for a live configuration note that now asserts the
opposite of the shipped fact (`invocation_exceptions.json:60`), 1 for a README
dependency claim the sprint made partly false (`README.md:91`), and 2 for the
two Gate 1 R2 observations that leave `agents.md §1` wording wider than the
instrument's behavior. Coverage is the measured test count; this audit does not
compute a percentage.

### The measurement that triggered it

| Magnitude | Value |
| :--- | :--- |
| p90 threshold of snapshot deltas (`percentile`, window `GRAPH_STATS_WINDOW` = 10) | `3643` |
| `node_delta` Sprint 052 → 053 | `5864` (61% over) |
| Window of deltas, sorted | `[1046, 1302, 1343, 1873, 2018, 2461, 3442, 3643, 7937]` |
| Snapshots (nodes / edges / communities), 052 → 053 | `11761 / 15788 / 950` → `12375 / 16638 / 994` |

`node_delta` (`scripts/docs_freshness_check.py:422`) is not the raw node
difference: it is `|Δnodes| + |Δedges| + 100 × max(0, Δcommunities)`, i.e.
`614 + 850 + 44 × 100 = 5864`. The `44` new communities contribute `4400` of
the `5864`, so the breach is driven by community count, not by node growth
(`+614`, 5% of 11761).

Reproduce: `make docs-freshness-check SPRINT_ID=053`, and the window with
`docs_freshness_check.graph_stats_snapshots(Path('.'))`. The 053 snapshot is
`docs/sprints/053-core-pipeline/graph_stats.json` (`nodes: 12375`,
`edges: 16638`, `communities: 994`, built at `0e854e1`; untracked at audit
time, `git status --porcelain` lists it).

Unlike `PIPELINE_AUDIT_REPORT-052.md`, the delta here spans **one** sprint
transition (052 → 053), both ends snapshotted. The content behind it is real:
Sprint 053 touched 67 task-scope rows (`task_scope.md`: Wave A 4, B 5, C 56,
D 2) — a tree-sitter JS/TS scanner in `scripts/quality_audit.py`, a pinned
`ruff` gate wired into `make verify`, 56 `style(lint)` units clearing a
176-finding baseline across scripts, hooks, skills and tests, and the marker
path fix in `hooks/on_commit.py`. Recorded, not corrected here: a threshold
breach caused by a lint sweep is a legitimate structural change, and rewriting
snapshots would be inventing measurements.

The same `docs-freshness-check` run also emitted two `WARN` classes, recorded
and not remediated: `graph_stats.json` missing for sprints `024`, `025`, `051`
(inside the populated range, `check_graph_stats_gaps`), and `code_containers`
not declared in `docs/active_state.json` (C4 Level 3 runs advisory-only —
`rules/documentation_standard.md §2.1`, which calls this the correct default).

---

## 🔍 Structural Findings & Rule Amendments

| Found Violation | Root Cause | Atomic Rectification | Law Applied |
| :--- | :--- | :--- | :--- |
| `config/invocation_exceptions.json:60` (note on `skills/js-standardizer`) states "no deterministic instrument currently exists for JS/TS complexity" and that Sprint 050 "withdrew" its instrument. `agents.md §1` (`:43`, `:47`, `:48`) now states the opposite: `scripts/quality_audit.py` measures JS/TS since `0ec6616`, closing `KI-050-6`. | Sprint 053 unit `D01` rewrote the `agents.md §1` rows and `D02` marked `KI-050-6` delivered in the roadmap, but the `RA-14` corpus grep for `KI-050-6` was not extended to `config/invocation_exceptions.json`, whose note was written at Sprint 049/050 and quotes the pre-053 state. | Recorded here; the audit edits no file. Fix owed (separate decision): annotate the note in place — it is a live configuration note, not a historical record. | `RA-14: PATCH_PROPAGATION` |
| `README.md:91` states the governance scripts are "stdlib only — no runtime dependencies". Since Sprint 053, `make verify` runs `$(PY) -m ruff check .` (`Makefile:75`) and `scripts/quality_audit.py`, whose JS/TS path exits `2` without `tree_sitter` (`Makefile:19-25`, already restated by `ce80b0d`); both are pinned in `requirements-quality.txt` and installed by `.github/workflows/ci.yml:30`. | The Makefile comment was restated by unit `C56`; the README sentence making the same claim was not in any unit's file list. | Recorded here, not remediated. The README sentence scopes itself to "Python 3.10+ … governance scripts"; the Python path of `quality_audit.py` and every other script stay stdlib-only, so the claim is partly true. The `verify` gate is the part that is not. Fix owed (separate decision). | `RA-14: PATCH_PROPAGATION` |
| `O6` (Gate 1 R2): `agents.md §1` `max_lines_per_func` (`:48`) says executable lines exclude "comment-only lines". Both paths count a comment row that sits inside a multi-row statement, because executable rows are the rows covered by statement nodes (`scripts/quality_audit.py:13-15`, `:559`). | Wording written for the common case; the instrument's definition is "rows covered by statement nodes", which is narrower than "comment-only lines are excluded". | Recorded, not corrected. Candidate routing: `/agents:extract`. | `unambiguous_action` (`agents.md §1 Language`) |
| `O1` (Gate 1 R2): nested function rows are counted in the enclosing JS/TS unit as well as in their own (`SPRINT_LOG.md:65`); the Python path treats a nested def as a boundary (`scripts/quality_audit.py:29-34`). `IMPLEMENTATION_PLAN.md` `D3` does not decide it. | Python/JS-TS asymmetry left undecided in the plan; behavior pinned by neither text nor test. | Recorded, not corrected. Candidate routing: `/agents:extract`; a decision belongs to the next sprint touching `scripts/quality_audit.py`. | `unambiguous_action` |

### Rule cross-reference performed (`rule_introspection`), scoped to this sprint's changes

Changed-file list taken from `docs/sprints/053-core-pipeline/task_scope.md`.
Commits audited: `agents.md §1` Python `linter_command`, JS/TS `linter_command`,
`max_indentation`, `max_lines_per_func` (`ce4d31e`, `31a0cad`),
`workflows/deployment_workflow.md` `deploy_unlock` (`bdf64ca`), `Makefile`
(`ce80b0d`), against `rules/`, `workflows/`, `docs/guides/`, `skills/*/SKILL.md`,
`agents/`, `commands/`, `config/`, `README.md`.

Searches run (ripgrep): `KI-050-6|no instrument|Python only|Python-only|NOT .make verify.|ruff check|stdlib-only|stdlib only` over `rules/ workflows/ docs/guides/ skills/*/SKILL.md agents/ commands/ Makefile README.md`; `deploy_unlock` and `\.deploy_unlock` over the whole tree excluding `docs/sprints/`; `comment-only` over `agents.md rules/ scripts/quality_audit.py docs/guides/ workflows/`; `ruff|quality[-_]audit|linter_command|max_indentation|max_lines_per_func|js-standardizer|python-quality-auditor|tree-sitter` over `rules/ workflows/ docs/guides/ skills/*/SKILL.md agents/ commands/`; `KI-050-6` over the tree excluding `docs/sprints/`.

| # | Location | What it says | Contradiction? |
| :--- | :--- | :--- | :--- |
| 1 | `agents.md:41` (Python `linter_command`) | `make verify` runs pinned `ruff check .`; `quality_audit.py` "does not run `ruff`" | No. Internally consistent with `Makefile:75-76`, which are two separate steps. |
| 2 | `agents.md:43` (JS/TS `linter_command`) | `pnpm run lint` verified by QA-gate judgment, "NOT `make verify` — `verify` runs no `pnpm run lint` step" | No. Still true: `Makefile:56-78` has no `pnpm` step. The adjacent "no instrument" prohibition text now describes history and says the Sprint 053 instrument satisfies it. |
| 3 | `agents.md:47`, `agents.md:48` (`max_indentation`, `max_lines_per_func`) | Measured for Python and JS/TS by `quality_audit.py`; `make verify` runs it | No against `Makefile:76`. Wording observation `O6` applies to `:48` ("comment-only lines") — see Findings. |
| 4 | `rules/code_craft.md:3` | `agents.md §1` governs style, typing and size; this rule governs what metrics cannot see | No. Deference clause unaffected by the row edits. |
| 5 | `rules/qa_and_testing.md:22` | Sprint 042 narrative: a green build with "`ruff` clean" hid a security defect | No. Historical example; it does not claim ruff is outside or inside `make verify`. |
| 6 | `rules/LEGACY_RULE_CONCORDANCE.md:12` | `Rule 35` → `agents.md §1 linter_command` "Linter gates (ruff / pnpm run lint)" | No. Pointer only. |
| 7 | `agents/qa_agent.md:3` | QA validates structural adherence "(ruff, npm run lint)" | No. Consistent with ruff now gated. |
| 8 | `skills/python-quality-auditor/SKILL.md`, `skills/js-standardizer/SKILL.md` | Matched only on the skill name; neither carries a "no instrument" or "NOT `make verify`" statement | No. |
| 9 | `skills/django-verification-3rd/SKILL.md:42`, `:432`, `:460` | Generic `ruff check .` usage for Django hosts | No. Host-facing guidance, not a statement about this repository's gate. |
| 10 | `Makefile:19-25` | Pytest, ruff and tree-sitter-backed JS/TS audit need third-party packages; every other step is stdlib-only | No. This is the restated, current text (`ce80b0d`). |
| 11 | `config/invocation_exceptions.json:60` | "no deterministic instrument currently exists for JS/TS complexity"; "withdrew it (Abort criterion 1)"; "Re-planned as its own sprint: `KI-050-6`" | **Yes.** Contradicts `agents.md:43` and the delivered instrument (`scripts/quality_audit.py:2`, `:58`). See Findings row 1. |
| 12 | `README.md:91` | "stdlib only — no runtime dependencies" | **Yes, partial.** The `make verify` ruff step and the JS/TS audit path require `requirements-quality.txt`. See Findings row 2. |
| 13 | `docs/roadmaps/core/pipeline/021-030-program-queue.md:13` | Sprint 050 narrative: "`agents.md §1` now states plainly that no JS/TS instrument exists" | No. Historical sentence inside the Sprint 050 account; `:13` also carries the Sprint 053 in-flight account and `:298`-`:299` mark `KI-050-6` "Delivered, Sprint 053" with the original text kept (`documentation_standard.md §6`: annotate in place, never delete). |
| 14 | `docs/roadmaps/core/pipeline/021-030-program-queue.md:298`, `:299` | `KI-049-4` points to `KI-050-6`; `KI-050-6` marked `Delivered, Sprint 053` | No. |
| 15 | `CHANGELOG.md:60` | Earlier entry citing `KI-050-6` | No. Historical ledger. |
| 16 | `tests/test_quality_audit.py:2`, `:229`; `scripts/quality_audit.py:2`, `:58` | Cite `KI-050-6` as delivered | No. |
| 17 | `workflows/deployment_workflow.md:19` (`deploy_unlock`) vs `hooks/on_commit.py:682-695`, `:722-727`, `:1069` | Workflow: nucleus `touch .deploy_unlock`, host `touch .agents/.deploy_unlock`, resolved by `deploy_unlock_path()` / `is_nucleus()` | No. Workflow text and implementation agree on both paths and on the mode switch. |
| 18 | `tests/test_on_commit.py:49`, `:55`, `:60`, `:71` | Host marker `.agents/.deploy_unlock` and nucleus marker `.deploy_unlock` both exercised | No. |
| 19 | `.gitignore:77` | Pattern `.deploy_unlock` (no leading slash) | No. Matches the marker at repository root and under `.agents/`. |
| 20 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md:95` | Step name `deploy_unlock`, action `write` | No. Generated by `scripts/map_workflows.py`; the step name is unchanged. |
| 21 | `docs/roadmaps/core/pipeline/021-030-program-queue.md:325` | `KI-052-9` marked `Delivered, Sprint 053` with both paths and the re-measure command; original text kept | No. |
| 22 | `CHANGELOG.md:638` | Historical entry for the `.deploy_unlock` marker | No. Ledger record of the earlier state. |

### Sweep results, each with the command that produced it

| Step | Command | Result |
| :--- | :--- | :--- |
| `rule_introspection` | See cross-reference table above | Two contradictions (entries 11, 12) and two open wording observations (`O6`, `O1`); no other contradiction |
| `skill_standard_check` | `python3 skills/topology-monitor/scripts/legacy_app_auditor.py` | Exit `0` — `AUDIT PASSED: Pipeline Structure is Valid` |
| `federation_audit` | Nucleus mode: tag/lock/submodule-cleanliness checks skipped by the workflow's own nucleus clause (no `.claude_bridge.lock`; the nucleus floats on `main`); the artifact-exists check belongs to `start_workflow.md bridge_check` | No drift reported |
| `nomenclature` | Naming sweep of files ADDED this sprint outside `docs/sprints/053-core-pipeline/` | Zero rename candidates — see verdict table below |
| `precision_audit` | `venv_skillopt` cannot import `skillopt` or `scripts.train` | `precision_audit skipped: skillopt stack absent`. Same skip as `-047.md`/`-049.md`/`-052.md`; provisioning state unchanged |
| `link_audit` | `python3 skills/slash-commander/scripts/verify_commands.py` | Exit `0` — 13 commands resolve; `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` §3.2 names all 13 stems |
| Reference integrity | `python3 scripts/verify_references.py` | Exit `0` — `Reference integrity OK` |
| Framework self-check | `make verify` (Sprint 053 Quality Gate) | Exit `0`; 946 passed; Gate 1 QA R1 `REJECTED`/`charter` → R2 `APPROVED`; Gate 2 Tester R1 `RECORD`/`testifying` (`SPRINT_LOG.md`) |

### Nomenclature verdicts

Candidates: every file ADDED this sprint outside
`docs/sprints/053-core-pipeline/` (`agents.md §5 mandatory_topology`), judged
against `RA-06: IDENTITY_NAMING` Option B. As in `PIPELINE_AUDIT_REPORT-052.md`,
tool-mandated names (configuration files a tool discovers by name, test modules
pytest discovers by pattern) are exempt from `[MODULE]_[TYPE].md`.

| File | Convention checked | Verdict |
| :--- | :--- | :--- |
| `requirements-quality.txt` | Sibling of the existing `requirements-core.txt`; `pip install -r` target, name chosen by the requirements-file convention, `kebab-case` descriptive | Compliant (tool-convention name). No rename. |
| `ruff.toml` | Name is fixed by `ruff`, which discovers it by exact filename at the repository root | Exempt (tool-mandated). No rename. |
| `tests/test_ruff_config.py` | `tests/test_*.py` pytest discovery pattern, mirrors its subject (`ruff.toml`) like `tests/test_graph_reconcile.py` in `-052.md` | Compliant (tool-mandated pattern). No rename. |

Zero rename candidates.

---

## 🛠️ Three-File Skill Standard Verification
Sprint 053 forged no new skill. Its `skill_architect` units (`C25`–`C39`) are
`style(lint)` edits to existing skill scripts, and `C37`/`C38` touch two
`__init__.py` files without changing the layout. The existing set is verified.

- [x] **README.md**: certified by `legacy_app_auditor.py` (`AUDIT PASSED`).
- [x] **SKILL.md**: procedural logic and YAML manifest verified; `check_manifest_parity.py` and the `generate_manifest.py` diff gate run inside `make verify` (exit `0`).
- [x] **scripts/**: executable logic and `__init__.py` present where the standard requires them (executable skills only; knowledge skills correctly carry no scaffolding, `agents.md §3 three_file_standard`).

---

## 🛡️ Certification

Sprint 053's subject matter was seal-vocabulary and deploy-marker fixes
(Wave A), the tree-sitter JS/TS complexity instrument closing `KI-050-6`
(Wave B), and a pinned, gated `ruff` baseline taken from 176 findings to 0
(Wave C). This closeout audit found the nucleus's structural documentation
consistent with its tree except for two propagation gaps (`config/invocation_exceptions.json:60`,
`README.md:91`) and two open observations on the `agents.md §1` complexity
wording (`O6`, `O1`). None is a functional defect: each is a documentation
statement that lags the instrument. Remediation is a separate decision and no
rule, workflow, configuration or README file was edited by this audit.

**Findings carried, not fixed here:**

| Finding | Destination |
| :--- | :--- |
| `config/invocation_exceptions.json:60` stale note on JS/TS instrument | Next sprint touching `config/invocation_exceptions.json`, or `/agents:extract` |
| `README.md:91` "stdlib only — no runtime dependencies" | Same |
| `O6` comment-row wording in `agents.md §1` | `/agents:extract`, candidate nucleus rule-amendment |
| `O1` nested-function rows in enclosing JS/TS unit (`D3` undecided) | `/agents:extract`; decided with the next change to `scripts/quality_audit.py` |
| `graph_stats.json` absent for sprints `024`, `025`, `051` | Still open: `docs/roadmaps/core/pipeline/021-030-program-queue.md`, *Still open for a later program* |
| `code_containers` not declared (C4 L3 advisory) | Correct default per `documentation_standard.md §2.1` |

**Remediated after this report, before the seal.** The two propagation gaps
were closed inside the Sprint 053 close rather than carried, because both
were left by this sprint's own change (`RA-14`): `config/invocation_exceptions.json`
`skills/js-standardizer` note (`926de1c`) and `README.md:91` (`df21f8d`).
`verify_references.py` and `check_readme_counts.py` exit `0` after both. The
first two rows of the table above are therefore closed; the scores above are
left as measured at the time of the sweep.

`current_sprint.last_audit_sprint` remains written by no workflow and no
script (the gap `-042.md`, `-047.md`, `-049.md` and `-052.md` recorded and
still open).

This report makes `last_audit_sprint: 53` true. Advancing
`docs/active_state.json` `current_sprint.last_audit_sprint` from `52` to `53`
is a separate write, owed to whoever closes Sprint 053, not performed by this
report itself (this audit's scope is limited to the artifact at
`docs/audits/PIPELINE_AUDIT_REPORT-053.md`; no other file was edited).

**Certified under Pipeline Methodology, nucleus mode.**
*Timestamp: 2026-10-04*
*Sealed at: `ai-sprint/053`*
