# Implementation Plan: Sprint 053 — quality-instruments-and-seal-defects

**Canonical path**: `docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/053` · **Base**: `main` at `3c6d341`
**Status**: `APPROVED` (2026-09-27) → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

The human's 2026-09-25 programme decision queued two sprints: `053` (`KI-050-6`, a
JS/TS complexity instrument on `tree-sitter`) and `054` (pin `ruff`, track its
configuration, reach exit `0`, wire `ruff check .` into `make verify`). On
2026-09-27 the human merged both into **one sprint, `053`**, and added two open
defects to it: `KI-052-9` (nucleus deploy-unlock marker path) and `KI-052-2`
(two spellings of the sprint seal, flagged *"priority: before or with Sprint 053"*).
Sprint id `054` is released; the programme queue records the merge.

Four problems, measured on `main` at `3c6d341`:

| # | Problem | Measurement | Reproduce |
| :--- | :--- | :--- | :--- |
| P1 | `KI-052-2` — `session_probe.py:243` compares `current_sprint.status` to `"CLOSED"`; `session_state.release()` writes `CLOSED_SUCCESSFULLY` (`session_state.py:88`), so the hygiene check can never fire. `open_sprint()` (`session_state.py:546`) treats a legacy `"CLOSED"` as unsealed and refuses with exit `2` — every host upgrading its pin past `dc38968` is refused at its next `open-sprint`. Docstrings still name `CLOSED` (`session_state.py:40,58,297,498`). | 1 comparison against a literal the writer never emits; 1 refusal of a legacy seal | `grep -n '"CLOSED"' scripts/session_probe.py`; `grep -n '^CLOSED' scripts/session_state.py` |
| P2 | `KI-052-9` — `hooks/on_commit.py:677` hard-codes `DEPLOY_UNLOCK = Path(".agents/.deploy_unlock")`, the host layout. In nucleus mode the only way to satisfy `deployment_workflow.md` `deploy_unlock` is to create a stray `./.agents/` directory; the Sprint 052 seal push (`03bbc0b`) was unlocked that way. | 1 host-only path in a hook that runs in both modes | `grep -n 'DEPLOY_UNLOCK =' hooks/on_commit.py` |
| P3 | `KI-050-6` — `scripts/quality_audit.py` measures Python only. Files with `JS_SUFFIXES` (`quality_audit.py:94`) are emitted as not-measured units (`_not_measured_unit`, line 369). `agents.md §1` `max_indentation` / `max_lines_per_func` state *"JS/TS: no instrument"*. The Sprint 050 stdlib brace scanner was withdrawn after four `REJECTED`/`charter` verdicts; its five failure families (`docs/sprints/050-core-pipeline/SPRINT_LOG.md` lines 150-230) are this sprint's acceptance corpus. | 0 JS/TS units measured | `grep -n '_not_measured_unit' scripts/quality_audit.py` |
| P4 | `ruff` backlog (`T3` / `T-046-2` / `KI-047-5`) — no tracked `ruff` configuration, no pinned version, and `make verify` runs no `ruff check`. | **176 findings in 60 files** under `ruff 0.16.3` (the queue's figure of 190 is stale). 18 of them in 8 vendored `skills/skill-creator/` files. **158 first-party findings in 52 files.** 97 auto-fixable. | `venv_skillopt/bin/ruff check . --statistics` (the last line reads `Found 176 errors.`); `venv_skillopt/bin/ruff check . --output-format concise \| grep -vc skill-creator` → `158` |

**Done** means: P1 and P2 have paired regression tests that fail on `3c6d341` and pass on
the branch; `quality_audit.py` measures JS/TS functions correctly across the five failure
families and fails closed when it cannot parse; and `make verify` runs a pinned
`ruff check .` that exits `0`.

---

## Design

| ID | Decision | Chosen over, and why |
| :--- | :--- | :--- |
| `D1` | **Seal vocabulary lives in one place.** `scripts/session_state.py` exports `SEALED_STATUSES = frozenset({"CLOSED_SUCCESSFULLY", "CLOSED"})`, where `"CLOSED"` is the legacy alias. `_sprint_is_sealed()` and `session_probe.py`'s hygiene check both read it. A `current_sprint` with **no** `status` stays refused by `open_sprint()`, because it is genuinely unknown and may be a live sprint. The refusal message names the one-command remediation (`python3 scripts/session_state.py release`). | Rejected: rewriting legacy anchors on read. A write hidden in a read path gives the state anchor two writers (`agents.md §5 state_homologation`). Rejected: accepting a missing `status` as sealed, which fails open on a live sprint. |
| `D2` | **The deploy-unlock marker path is resolved through `scripts/_mode.py`.** In nucleus mode it is `<repo root>/.deploy_unlock`; in host mode it stays `.agents/.deploy_unlock`. It is resolved at call time, not at import, so tests can monkeypatch the mode. `.gitignore:77` already ignores `.deploy_unlock` at any depth. | Rejected: accepting either path in both modes. A host could then unlock with a root-level marker that the deployment workflow never names. |
| `D3` | **The JS/TS instrument uses `tree-sitter` with the `javascript` and `typescript`/`tsx` grammars.** A function unit is a `function_declaration`, `generator_function_declaration`, `function_expression`, `arrow_function` or `method_definition`. Its size is **executable lines**: rows covered by statement nodes of the body, excluding comment-only and blank rows, the same definition as Python `D1` of Sprint 050. An expression-bodied arrow counts as 1. Its depth is **block-nesting depth over ancestors** of type `function_*`, `arrow_function`, `method_definition`, `class_*`, `if_statement`, `for_*`, `while_statement`, `do_statement`, `try_statement` and `switch_statement`, counted from the program root, mirroring the Python ancestor set in `agents.md §1`. | Rejected: repairing the Sprint 050 brace scanner. The Sprint 050 Abort criterion 1 already proved that JS/TS lexing is context-sensitive (regex versus division, keyword versus identifier), and `agents.md §1` now prohibits crediting a heuristic scanner with a fail-closed guarantee. Rejected: calling Node/`eslint`. It is a second runtime inside a Python instrument, and `pnpm` is not a nucleus dependency. |
| `D4` | **The JS/TS path fails closed.** If any JS/TS file is in scope and `tree_sitter` cannot be imported, `quality_audit.py` exits `2` and names `pip install -r requirements-quality.txt`. A tree with parse errors (`root_node.has_error`) yields an `UNPARSED` unit, which counts as non-compliant and never as silently skipped. The Python path stays stdlib-only, so a tree with no JS/TS files never imports `tree_sitter`. | Rejected: skip with a warning, the exact silent-compliance class that withdrew the Sprint 050 scanner. |
| `D5` | **The dependencies go in a new `requirements-quality.txt`** (pinned `tree-sitter`, `tree-sitter-javascript`, `tree-sitter-typescript` and `ruff`). `requirements-core.txt` includes it with `-r requirements-quality.txt`, so every host venv built by `start_workflow.md` `pip_setup` gets the instruments. CI installs that one file, not the whole core set, because CI needs no `graphifyy`. | Rejected: listing the packages in `requirements-core.txt` directly. CI would then need `graphifyy` just to get the instruments. Rejected: a dev-only file that hosts never install, which would leave the `agents.md §1` linters host-unavailable. |
| `D6` | **`ruff` is pinned to `0.16.3`**, the version the baseline was measured under. `ruff.toml` carries `required-version = "==0.16.3"` and an explicit `select` that reproduces the current 176-finding rule set, so a later ruff release cannot silently widen or narrow the gate. | Rejected: pinning the newest `0.16.9` (released 2026-09-24). The baseline would have to be re-measured under an unexercised version inside the same sprint that remediates it. The bump is a later `chore(deps)` commit. |
| `D7` | **The vendored `skills/skill-creator/` files are excluded in `ruff.toml` `extend-exclude`**, with exactly the ten paths of `config/quality_audit_exclusions.json`. Their parity is pinned by a test (`C02`) rather than by memory. This was the human's decision on 2026-09-27. | Rejected: editing vendored code, which breaks upstream parity (`rules/skills_and_integrations.md §3`). Rejected: a directory glob, which would also silently exempt a future first-party file placed there. |
| `D8` | **Remediation preserves behaviour, one file per unit** (`jurisdictional_lock`). `PLW1510` is cleared with an explicit `check=False`, the current behaviour made visible, unless the call site already asserts success. `BLE001`/`S110`/`E722` are cleared by narrowing to the exceptions actually raised and logging them (`agents.md §1 exception_handling`). `# noqa: <code>` is allowed only with an inline reason, **at most 10 across the sprint**, each listed in `SPRINT_LOG.md`. A finding that proves to be a runtime defect turns its unit into `fix(` with a paired test. | Rejected: one repo-wide `ruff --fix` commit. It violates `jurisdictional_lock`, and a bulk unsafe fix changes behaviour in a diff nobody can review. |
| `D9` | **Order: Wave A (defects) → Wave B (JS/TS) → Wave C (ruff).** Lint units on files that Wave A also touches (`session_state.py`, `session_probe.py`, `on_commit.py`) run after the Wave A unit on the same file has landed. That is a sequential claim of the same subject, which `jurisdictional_lock` permits. The `Makefile` wiring (`C56`) lands last, when `ruff check .` already exits `0`, so `verify` never goes red on the branch. | Rejected: wiring first, as a red gate that forces remediation. It would leave every intermediate commit failing `make verify`. |

---

## Work

### Wave A — seal vocabulary and deploy-unlock (`KI-052-2`, `KI-052-9`)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `scripts/session_state.py` | modify — `fix(state)`: `SEALED_STATUSES` (legacy `"CLOSED"` accepted); `open_sprint` refusal names `release`; docstrings say `CLOSED_SUCCESSFULLY` (`D1`). Paired test: `tests/test_session_state.py` | medium | `implementer_agent` | ⏳ |
| A2 | `scripts/session_probe.py` | modify — `fix(probe)`: hygiene check compares against `SEALED_STATUSES` (`D1`). Paired test: `tests/test_session_probe.py` | low | `implementer_agent` | ⏳ |
| A3 | `hooks/on_commit.py` | modify — `fix(hooks)`: deploy-unlock marker resolved through `scripts/_mode.py` at call time; blocked-push message names the mode's path (`D2`). Paired test: `tests/test_on_commit.py` | medium | `implementer_agent` | ⏳ |
| A4 | `workflows/deployment_workflow.md` | modify — `docs(deploy)`: `deploy_unlock` names both paths (nucleus `./.deploy_unlock`, host `.agents/.deploy_unlock`) | low | `doc_orchestrator` | ⏳ |

### Wave B — JS/TS complexity instrument (`KI-050-6`)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `requirements-quality.txt` | create — `build(deps)`: four pins (Dependencies table) (`D5`) | low | `implementer_agent` | ⏳ |
| B2 | `requirements-core.txt` | modify — `build(deps)`: `-r requirements-quality.txt` (`D5`) | low | `implementer_agent` | ⏳ |
| B3 | `scripts/quality_audit.py` | modify — `feat(quality)`: tree-sitter JS/TS scanner, fail closed (`D3`, `D4`); the Python path unchanged and stdlib-only | high | `implementer_agent` | ⏳ |
| B4 | `tests/test_quality_audit.py` | modify — `test(quality)`: the five Sprint 050 failure families, the fail-closed import path, `UNPARSED` on parse error, `.ts`/`.tsx` grammar selection, and threshold boundaries (50/51 lines, depth 3/4) | high | `implementer_agent` | ⏳ |
| B5 | `.github/workflows/ci.yml` | modify — `ci`: `pip install -q pytest -r requirements-quality.txt` | low | `implementer_agent` | ⏳ |

### Wave C — ruff to exit `0` and into `make verify` (former Sprint 054)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C01 | `ruff.toml` | create — `build(lint)`: `required-version`, explicit `select`, `extend-exclude` = 10 vendored paths (`D6`, `D7`) | medium | `implementer_agent` | ⏳ |
| C02 | `tests/test_ruff_config.py` | create — `test(lint)`: `ruff.toml` `extend-exclude` equals the `config/quality_audit_exclusions.json` path set; `invoked_by:` docstring (`RA-16`) | low | `implementer_agent` | ⏳ |
| C03 | `workflows/repository_hardening_workflow.md` | modify — `docs(harden)`: restore the Phase 4 ordering note (*before any history decision*) that the `S045-19` reshape dropped (`KI-047-5` second half) | low | `doc_orchestrator` | ⏳ |
| C04 | `hooks/on_commit.py` | modify — `style(lint)`: clear 7 finding(s) — after A3 | low | `implementer_agent` | ⏳ |
| C05 | `hooks/on_commit_msg.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C06 | `hooks/telemetry.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C07 | `scripts/_mode.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C08 | `scripts/audit_cursor_era.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | ⏳ |
| C09 | `scripts/branch_sovereignty.py` | modify — `style(lint)`: clear 9 finding(s) | low | `implementer_agent` | ⏳ |
| C10 | `scripts/check_absolute_paths.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C11 | `scripts/check_forge_ladder.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C12 | `scripts/check_manifest_parity.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C13 | `scripts/check_model_tiers.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C14 | `scripts/check_task_scope.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C15 | `scripts/detect_drift.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C16 | `scripts/detect_new_models.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C17 | `scripts/docs_freshness_check.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C18 | `scripts/install.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | ⏳ |
| C19 | `scripts/loop_guard.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C20 | `scripts/model_ledger.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | ⏳ |
| C21 | `scripts/py_compile_tree.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C22 | `scripts/session_cost.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C23 | `scripts/session_probe.py` | modify — `style(lint)`: clear 8 finding(s) — after A2 | low | `implementer_agent` | ⏳ |
| C24 | `scripts/session_state.py` | modify — `style(lint)`: clear 4 finding(s) — after A1 | low | `implementer_agent` | ⏳ |
| C25 | `skills/compliance-checker/scripts/apply_rule_amendments.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | ⏳ |
| C26 | `skills/compliance-checker/scripts/distill.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | ⏳ |
| C27 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | ⏳ |
| C28 | `skills/js-standardizer/scripts/js_standardizer.py` | modify — `style(lint)`: clear 7 finding(s) (includes `E722` bare `except: pass`, `D8`) | low | `skill_architect` | ⏳ |
| C29 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | ⏳ |
| C30 | `skills/mass-standardizer/scripts/mass_standardizer.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | ⏳ |
| C31 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | ⏳ |
| C32 | `skills/python-quality-auditor/scripts/python_quality_auditor.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | ⏳ |
| C33 | `skills/skillopt/scripts/dataloader.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | ⏳ |
| C34 | `skills/skillopt/scripts/env.py` | modify — `style(lint)`: clear 7 finding(s) (includes `F821` on an annotation under `from __future__ import annotations`, cleared with a `TYPE_CHECKING` import) | low | `skill_architect` | ⏳ |
| C35 | `skills/skillopt/scripts/gemini_backend.py` | modify — `style(lint)`: clear 5 finding(s) | low | `skill_architect` | ⏳ |
| C36 | `skills/skillopt/scripts/train_runner.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | ⏳ |
| C37 | `skills/slash-commander/__init__.py` | modify — `style(lint)`: clear 1 finding(s) | low | `skill_architect` | ⏳ |
| C38 | `skills/slash-commander/scripts/__init__.py` | modify — `style(lint)`: clear 1 finding(s) | low | `skill_architect` | ⏳ |
| C39 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | ⏳ |
| C40 | `tests/test_artifact_registry.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C41 | `tests/test_audit_cursor_models.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C42 | `tests/test_check_forge_ladder.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C43 | `tests/test_ci_gate.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C44 | `tests/test_code_craft_gates.py` | modify — `style(lint)`: clear 3 finding(s) | low | `implementer_agent` | ⏳ |
| C45 | `tests/test_cursor_adapter.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C46 | `tests/test_docs_freshness_check.py` | modify — `style(lint)`: clear 3 finding(s) | low | `implementer_agent` | ⏳ |
| C47 | `tests/test_loop_guard.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C48 | `tests/test_mass_standardizer.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C49 | `tests/test_on_commit.py` | modify — `style(lint)`: clear 1 finding(s) — after A3 | low | `implementer_agent` | ⏳ |
| C50 | `tests/test_on_push.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C51 | `tests/test_root_resolution.py` | modify — `style(lint)`: clear 6 finding(s) | low | `implementer_agent` | ⏳ |
| C52 | `tests/test_session_protocol.py` | modify — `style(lint)`: clear 18 finding(s) | low | `implementer_agent` | ⏳ |
| C53 | `tests/test_session_start.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | ⏳ |
| C54 | `tests/test_session_state.py` | modify — `style(lint)`: clear 2 finding(s) — after A1 | low | `implementer_agent` | ⏳ |
| C55 | `tests/test_token_saver_auditor.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | ⏳ |
| C56 | `Makefile` | modify — `build(verify)`: `verify` runs `$(PY) -m ruff check .` and `$(PY) scripts/quality_audit.py .`; the comment at lines 19-22 (*"every other step is stdlib-only"*) restated (`D9`) | medium | `implementer_agent` | ⏳ |

C04-C55 cover 158 findings in 52 files: `venv_skillopt/bin/ruff check . --output-format concise | grep -v skill-creator | cut -d: -f1 | sort | uniq -c`. Per-file counts are the 2026-09-27 measurement. A unit is done when `ruff check <file>` exits `0`, not when its count reaches zero.

### Wave D — governance and records

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D01 | `agents.md` | modify — `docs(governance)`: `§1` Python `linter_command` → verified by `make verify`; JS/TS `linter_command`, `max_indentation`, `max_lines_per_func` → JS/TS instrument delivered (`D3`), prohibition clause kept and satisfied by a real lexer | medium | `rule_validator` | ⏳ |
| D02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — `docs(roadmap)`: Status bullet (054 merged into 053); `KI-050-6`, `KI-052-2`, `KI-052-9`, `KI-047-5`, `T3`/`T-046-2` marked delivered with commit citations; new rows for this sprint's routed findings | low | `doc_orchestrator` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| `tree-sitter` | `0.26.0` (uploaded 2026-06-30) | JS/TS lexing is context-sensitive, and the stdlib-only scanner failed on it four times (Sprint 050 Abort criterion 1). `agents.md §1` prohibits crediting a heuristic scanner without a real lexer. No existing dependency parses JS/TS. |
| `tree-sitter-javascript` | `0.25.0` (2025-09-01) | The JavaScript/JSX grammar for `tree-sitter`. |
| `tree-sitter-typescript` | `0.23.2` (2024-11-11) | The TypeScript and TSX grammars. `.ts` and `.tsx` are distinct grammars. |
| `ruff` | `0.16.3` | `agents.md §1` Python `linter_command`. It is already installed in `venv_skillopt` but unpinned and untracked. A pin makes the gate reproducible (`D6`). |

All four are older than `minimum-release-age=1440` (24 hours; `agents.md §8`, applied by analogy to PyPI). Upload dates come from `https://pypi.org/pypi/<name>/<version>/json`. Each adding commit carries `Dependency: <name> — <reason>` (`rules/code_craft.md §7`).

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `ruff check .` over the first-party tree | script (`make` target) | `Makefile` `verify` (`C56`) → `.github/workflows/ci.yml` |
| JS/TS complexity measurement | script (`scripts/quality_audit.py`) | `Makefile` `verify` / `quality-audit` (existing invoker) |
| `ruff.toml` ↔ `quality_audit_exclusions.json` parity | script (pytest) | `tests/test_ruff_config.py`, run by `Makefile` `test` |
| Seal-status comparison | script (`session_state.SEALED_STATUSES`) | `session_probe.py` (boot) and `session_state.py open-sprint` (Phase 3) |

No mechanism in this sprint relies on agent judgment.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 67 (A 4 · B 5 · C 56 · D 2) | Count of rows in Work tables |
| Subagents dispatched | ~12: 1 per wave per assignee batch, plus 2 fresh gates per gate round | Planned; actual count recorded in `PHASE_REGISTER.md` |
| Prior session ratio | **19.0× worst cycle** in session `5641e6fb` (4 cycles over the 15× hard bound; peak 433,800 tokens) — **hard threshold breached** | `python3 scripts/session_cost.py --session 5641e6fb-0acc-4ddf-90e2-e51fe6d08912` |

**Mitigation, required because the prior session breached the hard bound.** This sprint
is the largest by unit count since Sprint 052, so it is split along its waves. Each wave
is dispatched to subagents in batches, so the parent context holds verdicts, not diffs.
The parent session ends with `/agents:close` (non-sealing) after Wave B and again after
Wave C, and resumes with `/agents:start`. `session_cost.py` is read at each wave
boundary: a cycle past 15× ends the session at the next unit boundary.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `open_sprint(54)` on an anchor whose `current_sprint.status == "CLOSED"` returns `0` | **Yes** — returns `2` today (P1) |
| `open_sprint(54)` on an anchor whose `current_sprint` has no `status` returns `2` and the message names `release` | **Yes** — returns `2` without naming the remediation |
| `session_probe` hygiene fires for `current_sprint.status == "CLOSED_SUCCESSFULLY"` while the anchor is `IN_PROGRESS` | **Yes** — never fires today (P1) |
| In nucleus mode, `is_blocked_push("git push origin main")` is `False` with `./.deploy_unlock` present and `True` with only `./.agents/.deploy_unlock` present | **Yes** — inverted today (P2) |
| In host mode, `.agents/.deploy_unlock` still unlocks | **No** — regression to protect |
| Each of the five Sprint 050 failure families (arrow over-detection, unenclosed module-level callbacks, nested-arrow depth loss, control-keyword method names, regex-literal masking desync) yields the hand-computed lines and depth | **Yes** — JS/TS is not measured today (P3) |
| A `.js` file in scope with `tree_sitter` not importable → exit `2` naming `requirements-quality.txt` | **Yes** — today it yields a not-measured unit and exit `0` |
| A JS file with a syntax error → `UNPARSED`, non-compliant | **Yes** |
| Python units measured identically before and after B3 (`--report` output on `scripts/` unchanged) | **No** — regression to protect |
| `ruff.toml` `extend-exclude` equals the exclusions-file path set | **Yes** — no `ruff.toml` exists |
| `ruff check .` exits `0` | **Yes** — 176 findings today (P4) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `venv_skillopt/bin/python -m pytest tests/ -q; echo $?` | `0` |
| `venv_skillopt/bin/ruff check .; echo $?` | `All checks passed!`, `0` |
| `venv_skillopt/bin/ruff --version` | `ruff 0.16.3` |
| `venv_skillopt/bin/python scripts/quality_audit.py .; echo $?` | `0` |
| `venv_skillopt/bin/python -m pytest tests/test_quality_audit.py -q -k "family or js or ts"; echo $?` | `0` — every corpus unit measured, none `NOT_MEASURED` |
| `make verify; echo $?` | `0`, with the ruff and quality-audit lines present in its output |
| `grep -n '"CLOSED"' scripts/session_probe.py` | no match |
| `grep -n 'DEPLOY_UNLOCK = Path(".agents' hooks/on_commit.py` | no match |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/053-core-pipeline; echo $?` | `0` |
| `git -C . status --porcelain` after `make verify` | empty |

The corpus has no fixture directory: B4 (`4585778`, `04e96c8`) writes each family's source inline to pytest's `tmp_path` (`tests/test_quality_audit.py` module docstring), so the corpus row runs the family tests rather than `quality_audit.py --report` over a path. Fixed before Phase 7.

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§1` Python `linter_command` is instrumented in `make verify`. The JS/TS `linter_command` complexity clause, `max_indentation` and `max_lines_per_func` now name the tree-sitter instrument. `KI-050-6` is closed. (D01) |
| `workflows/deployment_workflow.md` | `deploy_unlock` names the marker path per mode (A4) |
| `workflows/repository_hardening_workflow.md` | Phase 4 ordering note restored (C03) |
| `Makefile` | `verify` gains `ruff check`, and quality-audit runs under `$(PY)`. The interpreter comment is restated (C56). |
| `.github/workflows/ci.yml` | installs `requirements-quality.txt` (B5) |
| `requirements-core.txt`, `requirements-quality.txt`, `ruff.toml` | new and changed dependency and config manifests (B1, B2, C01) |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | the merged-sprint status and five closed backlog rows (D02) |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerated by `scripts/map_workflows.py` if A4 or C03 changes a step. Never hand-edited. |
| `CHANGELOG.md` | `[Unreleased]` entry citing commit SHAs (Phase 8) |
| `docs/sprints/053-core-pipeline/` | `SPRINT_LOG.md`, `agent_assignment.md`, `skill_assignment.md`, `task_scope.md`, `PHASE_REGISTER.md`, each from its template in `docs/standards/templates/` where one exists |

**Measured figures.** 176, 158, 60, 52, 18 and 97 come from the `ruff` commands in Context
P4. The package dates come from the PyPI JSON API in Dependencies. 19.0× comes from the
`session_cost.py` command in Cost.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Host venvs that already hold `installed.lock` do not reinstall on a changed requirement set, so they never receive `requirements-quality.txt` | `start_workflow.md` `pip_setup` installs only when the lock is absent. `D4` makes the gap visible (exit `2` naming the command), not silent. Routed as a new `KI-053-*` row in the programme queue (D02): the lock compares the requirement-set hash. |
| `ruff format` / formatter adoption | A different instrument with a repo-wide diff. Not requested. Not routed. |
| `mypy`, `bandit`, `radon` and a general style score | `agents.md §1` states them uninstrumented. Unchanged by this sprint. |
| JS/TS `pnpm run lint` | A host concern. The nucleus ships no JS/TS. |
| Bumping `ruff` past `0.16.3` | A later `chore(deps)` commit that re-measures the baseline (`D6`) |
| The vendored `skills/skill-creator/` findings (18) | Excluded by the human's decision of 2026-09-27 (`D7`) |
| The other open `KI-052-*` rows (`KI-052-1`, `KI-052-3`..`KI-052-8`) | They stay in the programme queue with their current destinations |

---

## Abort criterion

Decided before execution:

1. **The five-family corpus cannot all pass under tree-sitter.** If any family still yields
   a wrong line or depth figure after B3 plus one remediation round, B3 and B4 are
   reverted and JS/TS stays instrument-less, with `agents.md §1` unchanged. Waves A and C
   still ship. A partially correct JS/TS instrument is worse than a declared absence
   (Sprint 050 `D4`).
2. **The pinned tree-sitter wheels do not install** on CI's Python 3.12 (Linux x86_64) or on
   the local Python 3.13 (macOS arm64). Wave B is aborted, with the same consequence as (1).
3. **Wave C needs more than 10 `# noqa` suppressions**, or more than 3 lint units turn out
   to change behaviour (`fix(`). Wave C stops before `C56` and the question goes to the
   human. A gate that can be reached only by suppression is not a gate (`D8`).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (`gst.mirabal@gmail.com`) |
| **Date** | 2026-09-27 |
| **Plan commit at approval** | `7eb80bd` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
