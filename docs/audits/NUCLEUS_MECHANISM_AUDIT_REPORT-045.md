# Nucleus Mechanism Audit Report: Executable Mechanism Layer

**Audit ID**: #A045-a1d7
**Auditor**: rule_validator
**Date**: 2026-09-07
**Sprint**: 045 (nucleus-ruleset-mechanism-audit) — Phase 6, Unit 3
**Mode**: NUCLEUS
**Branch**: ai-sprint/045
**Scope**: `scripts/*.py` (39), `hooks/*.py` (7, one is a package marker), `skills/` (34 skill directories; 23 executable, 11 knowledge)
**Classification legend**: VIGENTE = compliant, keep as-is · MEJORAR = keep but amend · OBSOLETA = superseded / dead

> This unit **classifies and drafts** only (`IMPLEMENTATION_PLAN.md` decision D1). No script, hook, skill, `agents.md` or `rules/*.md` is modified. Every proposed amendment below is drafted text, not an applied change.

---

## Executive Summary

| Metric | Value | Status |
| :--- | :--- | :--- |
| Mechanisms audited | 39 scripts + 6 hooks + 34 skills | — |
| VIGENTE | 41 scripts/hooks + 34 skills (three-file) | GREEN |
| MEJORAR | 6 (4 scripts, 2 hooks) + 2 skill annotations | YELLOW |
| OBSOLETA | 0 | GREEN |
| Mechanisms with NO declared/derivable invoker | 0 | GREEN |
| Blocking hook paths using `sys.exit(1)` / `exit(1)` / `raise SystemExit(1)` | 0 | GREEN |
| Stale `config/invocation_exceptions.json` entries | 0 (all 12 paths exist) | GREEN |
| `RA-16` hard violations | 0 | GREEN |
| `RA-11` hard violations | 0 | GREEN |
| `RA-17` vocabulary drift vs `rules/qa_and_testing.md §4` | 0 (1 doc-string mis-citation) | GREEN |
| Three-File Skill Standard violations | 0 | GREEN |

Deterministic evidence relied upon (provided, spot-checked against source in this unit):
`scripts/verify_references.py` GREEN incl. check (d) "every mechanism has an invoker";
`skills/topology-monitor/scripts/legacy_app_auditor.py` "AUDIT PASSED";
`scripts/scan_workflow_determinism.py` no candidates.

---

## Table 1 — Mechanism verdict register

| Mechanism (path) | Kind | Invoker found | Verdict | Evidence | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scripts/_mode.py` | lib | `invoked_by:` submodule_purity / session_probe (also imported) | VIGENTE | `grep -n invoked_by scripts/_mode.py` → line 25 | — |
| `scripts/_root.py` | lib | `invoked_by:` _mode / branch_sovereignty (imported everywhere) | VIGENTE | `scripts/_root.py:53` | — |
| `scripts/install.py` | executable | `invoked_by:` install.sh, start_workflow.md#bridge_check, hooks/on_init.py | VIGENTE | `scripts/install.py:3` | — |
| `scripts/merge_json.py` | lib (import-only) | AST import by `scripts/install.py` (RA-16 precedent) | MEJORAR | `grep -n 'from merge_json\|import merge_json' scripts/install.py`; no literal `invoked_by:` token in module docstring | Add module-docstring line: `invoked_by: scripts/install.py (import; non-destructive settings/mcp merge).` |
| `scripts/cursor_adapter.py` | lib (import-only) | AST import by `scripts/install.py` when `--target cursor\|both` | MEJORAR | `scripts/cursor_adapter.py:3` prose "Imported by scripts/install.py" but no `invoked_by:` token | Add: `invoked_by: scripts/install.py (import; --target cursor\|both).` for parity with the other 37 scripts. |
| `scripts/install` bridge (`scripts/install.sh`) | shell wrapper | `agents.md §3 federation` sanctioned bridge | VIGENTE | `agents.md` federation row | — (shell, out of `*.py` scope; noted for completeness) |
| `scripts/verify_references.py` | gate | `invoked_by:` Makefile `verify` (→ ci.yml) | VIGENTE | `scripts/verify_references.py:24`; `Makefile:62` | — |
| `scripts/map_workflows.py` | generator/gate | `invoked_by:` Makefile `verify` (regenerate-and-compare) | VIGENTE | `scripts/map_workflows.py:21`; `Makefile:65` | — |
| `scripts/scan_workflow_determinism.py` | gate | `invoked_by:` Makefile `verify` | VIGENTE | `scripts/scan_workflow_determinism.py:1`; `Makefile:57` | — |
| `scripts/py_compile_tree.py` | gate | `invoked_by:` Makefile `verify` | VIGENTE | `scripts/py_compile_tree.py:6`; `Makefile:53` | — |
| `scripts/check_task_scope.py` | gate | `invoked_by:` close_workflow Phase 2.6, pipeline_workflow, Makefile `verify` | VIGENTE | `scripts/check_task_scope.py:10`; `Makefile:59` | — |
| `scripts/check_gate_log.py` | gate (RA-17) | `invoked_by:` close_workflow Phase 2.6, pipeline_workflow Phase 7, Makefile `verify` | MEJORAR | `scripts/check_gate_log.py:8`; vocabulary matches `rules/qa_and_testing.md §4` exactly (`check_gate_log.py:31-33,89-94`) | Docstring line 17 says `2 — vocabulary or class mismatch (RA-11)`; the detected condition is an **RA-17** vocabulary/class mismatch. Change parenthetical to `(RA-17; blocking exit-code 2 per RA-11 semantics)`. |
| `scripts/check_role_artifact.py` | gate | `invoked_by:` Makefile `role-artifacts`; `claude/settings.hooks.json` SubagentStop | VIGENTE | `scripts/check_role_artifact.py:14`; blocking path `return 2` (`:200,211,281`); `--from-hook` intentionally advisory `return 0` | — |
| `scripts/check_template_gates.py` | gate | `invoked_by:` Makefile `verify` | VIGENTE | `scripts/check_template_gates.py:30`; `Makefile:61` | — |
| `scripts/check_manifest_parity.py` | gate | `invoked_by:` Makefile `verify` (→ ci.yml) | VIGENTE | `scripts/check_manifest_parity.py:8`; `Makefile:67` | — |
| `scripts/check_absolute_paths.py` | gate | `invoked_by:` Makefile `verify` (→ ci.yml) | VIGENTE | `scripts/check_absolute_paths.py:14`; `Makefile:68` | — |
| `scripts/check_readme_counts.py` | gate | `invoked_by:` Makefile `verify`, close_workflow#readme_counts | VIGENTE | `scripts/check_readme_counts.py:28`; `Makefile:66` | — |
| `scripts/check_model_tiers.py` | gate | `invoked_by:` Makefile#verify | VIGENTE | `scripts/check_model_tiers.py:20`; `Makefile:63` | — |
| `scripts/detect_new_models.py` | gate | `invoked_by:` scripts/session_probe.py, Makefile#verify | VIGENTE | `scripts/detect_new_models.py:54`; `Makefile:64` | — |
| `scripts/check_forge_ladder.py` | gate | `invoked_by:` pipeline_workflow.md Phases 4.1, 4.2 | VIGENTE | `scripts/check_forge_ladder.py:10` | — |
| `scripts/check_venv_relocatable.py` | check | `invoked_by:` start_workflow.md#pip_setup | VIGENTE | `scripts/check_venv_relocatable.py:24` | — |
| `scripts/branch_sovereignty.py` | audit | `invoked_by:` close_workflow.md#branch_audit / #local_prune | VIGENTE | `scripts/branch_sovereignty.py:41` | — |
| `scripts/submodule_purity.py` | gate | `invoked_by:` close_workflow.md#submodule_purity, hooks/on_commit.py | VIGENTE | `scripts/submodule_purity.py:33`; called from `hooks/on_commit.py:812-821` | — |
| `scripts/ci_gate.py` | gate | `invoked_by:` deployment_workflow.md#pr_flow | VIGENTE | `scripts/ci_gate.py:64` | — |
| `scripts/detect_drift.py` | gate | `invoked_by:` start_workflow.md#drift_check | VIGENTE | `scripts/detect_drift.py:51` | — |
| `scripts/publish_github_release.py` | executable | `invoked_by:` deployment_workflow.md#github_release | VIGENTE | `scripts/publish_github_release.py:19` | — |
| `scripts/docs_freshness_check.py` | gate | `invoked_by:` close_workflow.md#docs_freshness_gate, Makefile `docs-freshness-check` | VIGENTE | `scripts/docs_freshness_check.py:8`; `Makefile:100` | — |
| `scripts/loop_guard.py` | guard | `invoked_by:` pipeline_workflow.md#loop_guard | VIGENTE | `scripts/loop_guard.py:22` | — |
| `scripts/session_start.py` | executable | `invoked_by:` start_workflow.md, `make session-start`, commands/start.md | VIGENTE | `scripts/session_start.py:17`; `Makefile:104` | — |
| `scripts/session_probe.py` | executable | `invoked_by:` start_workflow.md#readiness_probe / #platform_probe | VIGENTE | `scripts/session_probe.py:23` | — |
| `scripts/session_state.py` | executable | `invoked_by:` start_workflow.md#state_claim, close_workflow.md#state_sync | VIGENTE | `scripts/session_state.py:17` | — |
| `scripts/session_cost.py` | lib | `invoked_by:` scripts/session_probe.py, rules/token_economy.md#session_bound | VIGENTE | `scripts/session_cost.py:33` | — |
| `scripts/session_end_hook.py` | hook wrapper | `invoked_by:` `claude/settings.hooks.json` SessionEnd | VIGENTE | `scripts/session_end_hook.py:7`; `claude/settings.hooks.json:120-129`; calls `session_state.py suspend` only, never `release` (`:26-31`); propagates 0/2 | — (SessionEnd cannot block a closing session; suspend-not-release is deliberate per Sprint 027 D4) |
| `scripts/persist_session_context.py` | hook | `invoked_by:` `claude/settings.hooks.json` PreCompact; manual under Cursor | VIGENTE | `scripts/persist_session_context.py:7`; `claude/settings.hooks.json:90-98` | — |
| `scripts/bridge_state.py` | lib | `invoked_by:` scripts/session_start.py, hooks/on_init.py | VIGENTE | `scripts/bridge_state.py:27`; imported at `hooks/on_init.py:30` | — |
| `scripts/sync_agents_pin.py` | executable | `invoked_by:` start_workflow.md#lightweight_sync | VIGENTE | `scripts/sync_agents_pin.py:11` | — |
| `scripts/model_ledger.py` | generator | `invoked_by:` Makefile `model-ledger`, close_workflow.md | VIGENTE | `scripts/model_ledger.py:5`; `Makefile:108` | — |
| `scripts/render_readme.py` | generator | `invoked_by:` human, during host onboarding (printed by install.py) | VIGENTE | `scripts/render_readme.py:3` (typed human-entry-point rationale in docstring) | — |
| `scripts/audit_cursor_models.py` | gate/proposer | `invoked_by:` Makefile `cursor-tiers` (`--check` in `verify` path) | VIGENTE | `scripts/audit_cursor_models.py:28`; `Makefile:114-115` | — (still binding for Cursor sprints even though `session_tool: claude-code` now) |
| `scripts/audit_cursor_era.py` | historical census | `invoked_by:` Makefile `cursor-era-audit` | MEJORAR | `scripts/audit_cursor_era.py:7`; `Makefile:119-120`; sprint range frozen 026–033 (`:28-29`); output `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` is a one-shot census, deliberately not in `verify` | REFUTES "OBSOLETA": a standing Make target invokes it. Add one docstring line: `Scope frozen to sprints 026-033 (Cursor era). Not stale — a bounded historical census, re-runnable but not expected to change.` so a future auditor does not read the frozen range as rot. |
| `hooks/__init__.py` | package marker | n/a (excluded by RA-16 check `:232`) | VIGENTE | `scripts/verify_references.py:232` | — |
| `hooks/on_init.py` | Claude Code SessionStart hook | `invoked_by:` `claude/settings.hooks.json` SessionStart | VIGENTE | `hooks/on_init.py:9`; `claude/settings.hooks.json:59-67`; non-blocking by design, exit 0 only (`:14-16,135-151`) | — |
| `hooks/on_commit.py` | dual: `.git/hooks/pre-commit` **and** Claude Code `PreToolUse` Bash | `invoked_by:` `.git/hooks/pre-commit`; also `claude/settings.hooks.json` PreToolUse (`:69-79`) | MEJORAR | blocking path `block()` → `sys.exit(2)` (`hooks/on_commit.py:824-828`), correct for both wirings; `sys.exit(0)` on pass (`:843,895`); no `exit(1)` anywhere | Docstring "Exit codes: 0 — allowed / 1 — rejected" (`:12-14`) predates the PreToolUse wiring and understates it. Amend to: `2 — rejected (blocks git commit AND the Claude Code PreToolUse Bash call; RA-11 requires 2, not 1)`. |
| `hooks/on_commit_msg.py` | `.git/hooks/commit-msg` (native git only) | `invoked_by:` `.git/hooks/commit-msg` | VIGENTE | `hooks/on_commit_msg.py:14`; `return 1` at `:73` then `sys.exit(main())` at `:79`. RA-11 is scoped to **Claude Code PreToolUse** hooks; this is a git hook where any non-zero aborts. `exit 1` is correct. | — |
| `hooks/on_push.py` | `.git/hooks/pre-push` (native git only) | `invoked_by:` `.git/hooks/pre-push` | VIGENTE | `hooks/on_push.py:10`; `return 1` at `:55`. Git hook, not a Claude Code hook — RA-11 does not bind it; `exit 1` blocks `git push` correctly. | — |
| `hooks/state_mirror.py` | Claude Code Stop hook | `invoked_by:` `claude/settings.hooks.json` Stop; close_workflow.md#state_sync | MEJORAR | `hooks/state_mirror.py:9`; `claude/settings.hooks.json:80-89`; no blocking path (silent shadow copy). **Code-craft**: `except json.JSONDecodeError: pass` at `:27-28` with a comment but no logging — violates `agents.md §1 exception_handling` "No `pass` in except. Explicit logging required." | Replace the bare `pass` with `print("[state_mirror] active_state.json is not valid JSON; mirror skipped", file=sys.stderr)`. A single stderr line satisfies §1 without noise on the Stop path. |
| `hooks/telemetry.py` | lib (not a hook despite folder) | `invoked_by:` hooks/on_commit.py, hooks/on_init.py | VIGENTE | `hooks/telemetry.py:8`; broad `except Exception as e` at `:37` **does** log (`print`), so §1-compliant | — |
| `skills/` — 23 executable skills | executable skills | RA-16 check (d) `:244-248`: in `config/invocation_exceptions.json` OR name in governance corpus | VIGENTE | `verify_references.py` GREEN; each carries `README.md` + `SKILL.md` + `scripts/__init__.py` (`Glob skills/*/scripts/__init__.py` → 23 hits incl. all executable dirs) | — (two annotations below) |
| `skills/autoskills-3rd` | executable vendored (`-3rd`) | name "autoskills-3rd" in `rules/skills_and_integrations.md:8`, `agents/skill_architect.md:3,17` | MEJORAR | `grep -rn autoskills-3rd rules/ agents/`; NOT in `config/invocation_exceptions.json` while its four `django-*-3rd` siblings are | Add to `config/invocation_exceptions.json`: `{"path": "skills/autoskills-3rd", "reason": "vendored-reference", "note": "Local Arsenal Bridge (skills_and_integrations.md §Priority 2). Not a scripted workflow step."}` so coverage does not depend on a rule sentence's wording. |
| `skills/django-expert-3rd` | executable vendored (`-3rd`) | name "django-expert-3rd" in `rules/django_backend_standard.md:7,33,44` | MEJORAR | `grep -rn django-expert-3rd rules/`; NOT in exceptions file; **also** ships a nested `skills/django-expert-3rd/skills/SKILL.md` (sub-layer) alongside the top-level pointer `SKILL.md` | (1) Add `vendored-reference` exception entry as for autoskills-3rd. (2) The nested `skills/` sub-layer contradicts `agents.md §3 topological_order` literally, but is an **accepted** vendored-upstream shape documented in `rules/django_backend_standard.md:33,44`; keep, and keep that cross-reference intact (`RA-14`). Flagged for Unit 1. |
| `skills/` — 11 knowledge skills (`accessibility`, `frontend-design`, `seo`, `vite`, `graphify`, `nodejs-*`, `tailwind-css-patterns`, `typescript-advanced-types`, `vercel-*`) | knowledge skills | n/a — no `scripts/`, only `SKILL.md` required | VIGENTE | `Glob skills/*/SKILL.md`; none has a `scripts/` dir; `agents.md §3 three_file_standard` requires only `SKILL.md` for knowledge skills | — |
| `skills/omni-context-minimizer/scripts/omni_minimizer.py` | executable skill script | skill dir name in `rules/token_economy.md:3,11`, `workflows/pipeline_workflow.md`, `agents.md` | MEJORAR | `grep -rn omni_minimizer .` → `agents.md:64` and `rules/token_economy.md:11` cite the bare filename `omni_minimizer.py` with **no path** | See RA-16 finding F-3 — bare-script citation breaks the resolvability convention (`rules/qa_and_testing.md:5`). Draft amendment in Table 2. Flagged for Unit 1 cross-reference. |

---

## Table 2 — Rule-compliance findings

| ID | Rule | Mechanism(s) | Finding | Severity | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F-1 | RA-16 INVOCATION_COVERAGE | `scripts/merge_json.py`, `scripts/cursor_adapter.py` | Both pass check (d) only via AST **import** resolution (`verify_references.py:184-203,234`). Neither carries the literal `invoked_by:` token that the other 37 scripts and 5 real hooks carry. Coverage is real but the declaration is implicit. | LOW (no check failure) | `merge_json.py` docstring: add `invoked_by: scripts/install.py (import).` · `cursor_adapter.py` docstring: add `invoked_by: scripts/install.py (import; --target cursor\|both).` |
| F-2 | RA-16 INVOCATION_COVERAGE | `skills/autoskills-3rd`, `skills/django-expert-3rd` | Executable vendored `-3rd` skills that satisfy check (d) branch `skill.name in governance` (`verify_references.py:246`) purely because their directory name appears in a rule sentence. Their four `django-*-3rd` siblings instead carry explicit `vendored-reference` exceptions. Asymmetric and fragile: reword the rule sentence and the skill silently loses coverage. | LOW | Add two entries to `config/invocation_exceptions.json` `exceptions[]` with `reason: "vendored-reference"` (text drafted in Table 1). No stale entries to remove — all 12 current paths exist. |
| F-3 | RA-16 / citation-resolvability (`rules/qa_and_testing.md:5`) | `agents.md:64` (`§2 ast_skeleton`), `rules/token_economy.md:11` | The always-loaded ruleset mandates the AST-skeleton step by citing the **bare script** `omni_minimizer.py`, which lives in `skills/omni-context-minimizer/scripts/` — a directory the resolvability convention says must never be cited bare. `agents.md §2 ast_skeleton` also names no skill and no path. | MEDIUM (docs) | `agents.md §2 ast_skeleton` value → `invoke skills/omni-context-minimizer/scripts/omni_minimizer.py (skill: omni-context-minimizer) to extract the skeleton before any partial read.` `rules/token_economy.md:11` ladder cell → `skills/omni-context-minimizer/scripts/omni_minimizer.py <file>`. Apply under `RA-14` (grep both files + `workflows/pipeline_workflow.md` on the same patch). Owner: Unit 1. |
| F-4 | RA-11 HOOK_BLOCKING_SEMANTICS | `hooks/on_commit.py` | No violation in code — the blocking `block()` correctly `sys.exit(2)` (`:828`) and is dual-wired (native `pre-commit` + Claude Code `PreToolUse`, `claude/settings.hooks.json:69-79`). The **docstring** (`:12-14`) still advertises `1 — commit rejected`, which is wrong for the PreToolUse path and invites a future edit to "simplify" back to `exit(1)`. | LOW (doc) | Rewrite the docstring "Exit codes" block to state `2` is the blocking code and cite `RA-11` (text in Table 1). |
| F-5 | RA-11 scope clarification (no violation) | `hooks/on_commit_msg.py:73`, `hooks/on_push.py:55` | Both use `return 1` → `sys.exit(main())`. These are **native git hooks** (`commit-msg`, `pre-push`), not Claude Code `PreToolUse` hooks; RA-11 is explicitly scoped to Claude Code `PreToolUse`. For git hooks any non-zero exit aborts, so `exit 1` is correct. Recorded so a future audit does not misfile it as an RA-11 breach. | INFO | None. Optionally add one line to each docstring: `Native git hook — any non-zero aborts; RA-11 (Claude Code PreToolUse exit-2 rule) does not apply here.` |
| F-6 | RA-17 GATE_VERDICT_CLASSES | `scripts/check_gate_log.py` | Verdict vocabulary is an **exact** match to `rules/qa_and_testing.md §4`: `VERDICTS = {APPROVED, REJECTED, RECORD}` (`:31`), `REJECTED_CLASSES = {charter, instructing}` (`:32`), `RECORD_CLASS = testifying` (`:33`), `APPROVED` must have empty Class (`:93-94`). `scripts/check_role_artifact.py` reuses `check_gate_log.gate_tables` for gate-row detection (`:184`). No drift. Only defect: docstring `:17` attributes the blocking exit-2 to `(RA-11)` where the condition detected is an `RA-17` mismatch. | LOW (doc) | Docstring `:17` → `2 — vocabulary or class mismatch (RA-17; exit-code-2 blocking per RA-11 semantics)`. |
| F-7 | code_craft `exception_handling` (`agents.md §1`) | `hooks/state_mirror.py:27-28` | `except json.JSONDecodeError: pass` with an explanatory comment but **no logging**. `agents.md §1` is categorical: "No `pass` in except. Explicit logging required." | LOW | Replace `pass` with `print("[state_mirror] active_state.json not valid JSON; mirror skipped", file=sys.stderr)`. Non-fatal, one line, keeps the Stop hook quiet on the happy path. |
| F-8 | Dead/superseded scan | all 39 scripts, 7 hooks | No script is referenced by an obsolete name; no script is superseded-and-unremoved. `merge_json.py` / `cursor_adapter.py` looked orphaned to a filename-only scan but are live imports (F-1). `audit_cursor_era.py` is bounded-historical, not dead (standing `make cursor-era-audit`). `session_end_hook.py` is correctly wired to SessionEnd. | INFO | None. `audit_cursor_era.py` gets the clarifying docstring line from Table 1. |

---

## Three-File Skill Standard Verification (`agents.md §3 three_file_standard`)

- [x] **README.md** — present for every executable skill (`Glob skills/*/README.md` → 25 hits covering all 23 executable dirs plus `skills/skillopt`, `skills/django-expert-3rd`).
- [x] **SKILL.md** — present for all 34 skill directories (`Glob skills/**/SKILL.md`). Every one spot-checked carries `name`/`description` frontmatter (e.g. `skills/omni-context-minimizer/SKILL.md:1-4`).
- [x] **scripts/ with `__init__.py`** — present for all 23 executable skills (`Glob skills/*/scripts/__init__.py` → 23 hits: autoskills-3rd, django-patterns/security/tdd/verification/expert-3rd, skills-samples-3rd, env-shielding-auditor, mass-standardizer, js-standardizer, mcp-registry, omni-context-minimizer, readme-standardizer, python-quality-auditor, sprint-architect, contract-writer, topology-scaffolder, skillopt, slash-commander, skill-creator, compliance-checker, topology-monitor, token-saver-auditor).
- [x] **Knowledge skills** — 11 skills ship only `SKILL.md` and no `scripts/` dir; padding them would be prohibited noise per the rule. Compliant.
- [x] **`legacy_app_auditor.py`** — "AUDIT PASSED: Pipeline Structure is Valid" (provided evidence, consistent with the above).
- [!] **Structural note (accepted deviation, not a violation)** — `skills/django-expert-3rd/` contains a nested `skills/` sub-layer (`skills/django-expert-3rd/skills/SKILL.md`) alongside its top-level pointer `SKILL.md`. `agents.md §3 topological_order` forbids sub-layers literally; this instance is a vendored-upstream shape explicitly documented and accepted in `rules/django_backend_standard.md:33,44`. Keep, keep the cross-reference (F-2 / Unit 1).

---

## Consolidated proposed amendments (drafted, applied by later units / sprints — NOT here)

| # | Target file | Change | Applying authority |
| :--- | :--- | :--- | :--- |
| A-1 | `agents.md` `§2 ast_skeleton` | Cite `skills/omni-context-minimizer/scripts/omni_minimizer.py` with full path + skill name (F-3) | Unit 1 (ruleset), under `RA-14` |
| A-2 | `rules/token_economy.md:11` | Same full-path citation in the AST-skeleton ladder cell (F-3) | Unit 1, same patch as A-1 |
| A-3 | `config/invocation_exceptions.json` | Add `vendored-reference` entries for `skills/autoskills-3rd` and `skills/django-expert-3rd` (F-2) | mechanism-layer sprint |
| A-4 | `scripts/merge_json.py`, `scripts/cursor_adapter.py` | Add explicit `invoked_by: scripts/install.py (import…)` docstring line (F-1) | mechanism-layer sprint |
| A-5 | `scripts/check_gate_log.py:17` | Fix `(RA-11)` → `(RA-17; …)` in the exit-code docstring (F-6) | mechanism-layer sprint |
| A-6 | `hooks/on_commit.py:12-14` | Rewrite "Exit codes" block to state exit 2 blocks both wirings, cite RA-11 (F-4) | mechanism-layer sprint |
| A-7 | `hooks/state_mirror.py:27-28` | Replace bare `except … pass` with a stderr warning (F-7) | mechanism-layer sprint |
| A-8 | `scripts/audit_cursor_era.py` docstring | Add "scope frozen 026-033, bounded historical census, not stale" line (F-8) | mechanism-layer sprint |
| A-9 | `hooks/on_commit_msg.py`, `hooks/on_push.py` docstrings | Optional: note these are native git hooks outside RA-11 scope (F-5) | mechanism-layer sprint (optional) |

---

## Certification

**Certified by rule_validator under Pipeline Methodology v4.0 (Sprint 045, Phase 6, Unit 3).**
Method: static classification only. `Glob`/`Grep`/`Read` over `scripts/`, `hooks/`, `skills/`, `Makefile`, `claude/settings.hooks.json`, `config/invocation_exceptions.json`, `rules/qa_and_testing.md`. Runtime GREEN status of `make verify` / `verify_references.py` / `legacy_app_auditor.py` / `scan_workflow_determinism.py` taken from the sprint's provided deterministic evidence and cross-checked against source.
No mechanism was modified. No rule was amended. All amendments above are drafted text only (`IMPLEMENTATION_PLAN.md` D1).

*Timestamp: 2026-09-07*
*Audit ID: #A045-a1d7*
