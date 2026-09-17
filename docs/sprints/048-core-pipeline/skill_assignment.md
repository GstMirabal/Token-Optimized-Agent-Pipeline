# Skill Assignment — Sprint 048 (jurisdictional-lock-reconciliation-and-047-residue)

Source: `docs/sprints/048-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from
`docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md`.

Mode: **claude-code** (nucleus), `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/048-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | HIT — existing deterministic tools cover every unit; no new capability required | `Read`/`Edit` for all 14 prose, JSON, and script edits; `omni-context-minimizer` (`omni_minimizer.py`) for the three Python targets over 200 lines (U8's subject and its paired test, U10, U13); `ruff`, `pytest`, `make verify`, `scripts/verify_references.py`, `scripts/map_workflows.py`, `scripts/check_task_scope.py`, `skills/token-saver-auditor/scripts/audit_plan.py` for verification |
| P2 | `autoskills-3rd` | not reached | P1 resolved every unit |
| P3 | `https://skills.sh/` (WebSearch/WebFetch) | reached — no applicable published skill | WebSearch on "rule reconciliation editor", "reference-anchor coverage checker", "Python AST function-length refactor tool" returned only generic linting/formatting skills (ESLint/Prettier/Black-style), none of which operate on this repo's internal governance corpus (`agents.md`, `rules/*.md`, `workflows/*.md`) or its internal `scripts/verify_references.py` check (d) — the sprint's own edit targets, not tools to import |
| P4 | Three-File Standard at Destination | not reached | ladder closed at P1; no skill is built this sprint |

This sprint **builds no new skill**. Every unit is a one-file (or one-file-plus-
paired-test, U8) edit — governance prose (U1, U3-U5, U7, U12, U14), a template
(U2), a JSON memory entry (U6), stdlib-only `scripts/` changes (U8 subject, U10),
and `pytest` fixture edits (U8 test, U11, U13) — verified by tools already present
in the tree. U9 is a contingency slot whose file set is unknown until U8's first
run; its resolution is recorded as "P1 HIT, tool deferred to discovery" rather
than invented in advance (`agents.md §1 unambiguous_action` — no claim without
evidence).

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U1 (`agents.md`, 176 lines) | `Read` with `offset`/`limit` on `§2 Isolation`; `grep -nE '^\| \`jurisdictional_lock\`' agents.md` to locate the row; `Edit`. Verify: `make verify`, `scripts/verify_references.py`, `grep -rn "physical file" --include=*.md --include=*.json .` (Verification table row), `scripts/check_task_scope.py --sprint-dir docs/sprints/048-core-pipeline` | N/A | P1 HIT; P3 checked, no applicable skill |
| U2 (`docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`, 184) | `Read`/`Edit` — `## Work` gloss line 39-40. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U3 (`workflows/pipeline_workflow.md`, 42) | `Read`/`Edit` — Phase 6 Done-criterion. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U4 (`agents/implementer_agent.md`, 32) | `Read`/`Edit` — two spots (frontmatter `description` line 3, `write_scope` line 20). Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U5 (`rules/code_craft.md`, 80) | `Read`/`Edit` — §2 line 21. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U6 (`memory_index.json`, 98) | `Read`/`Edit` — remove the superseded entry at line 89; `python3 -c "import json;json.load(open('memory_index.json'))"` to confirm valid JSON after the edit (`§4 single_line_breakdown`). Verify: `make verify` | N/A | P1 HIT |
| U7 (`agents/rule_validator.md`, 21) | `Read`/`Edit` — line 19 Model/Effort shape. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U8 (`scripts/verify_references.py`, 552 — over 200; paired `tests/test_verify_references.py`, 212 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton on both files (`agents.md §2 ast_skeleton`), then targeted `Read` of `check_invoked_by_anchors` (~line 390) and the corresponding test; `Edit` both as one paired unit (`agents.md §2 jurisdictional_lock`, as restated by U1). **Landed narrower than planned**: only the anchor-resolution half was extended — `check_invocation_coverage` (lines 234-236) was deliberately left untouched after a human mid-execution decision, since extending it too surfaced 59 findings, over Abort criterion 2's threshold. Verify: `ruff check scripts/verify_references.py tests/test_verify_references.py`, `python3 -m pytest tests/test_verify_references.py -q`, `python3 scripts/verify_references.py`, `make verify` | N/A | P1 HIT; P3 checked, no applicable skill |
| U9 (*contingency* — files named by U8's first run) | Tool deferred to discovery: `Read`/`Edit` per surfaced file; if any surfaced file exceeds 200 lines, run `skills/omni-context-minimizer/scripts/omni_minimizer.py` on it first (`ast_skeleton`) before any partial read. Abort per the plan's Abort criterion 2 if more than 10 defects surface. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT (same ladder as every prose/script edit; no new capability class expected) |
| U10 (`scripts/map_workflows.py`, 325 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton (`agents.md §2 ast_skeleton`), then targeted `Read` of `build()` (lines 239-296) and the two trailing legend blocks (lines 266, 282); `Edit` to hoist them to module-level constants. Verify: `ruff check scripts/map_workflows.py`, `python3 -m pytest tests/test_map_workflows.py -q`, `python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('scripts/map_workflows.py').read_text()); print(max(n.end_lineno-n.lineno+1 for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='build'))"` (≤50), `python3 scripts/map_workflows.py; git diff --exit-code docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (byte-identical) | N/A | P1 HIT; P3 checked, no applicable skill |
| U11 (`tests/test_mode.py`, 139) | `Read`/`Edit` — remove the unused `# noqa: E402` at line 30. Verify: `ruff check --select RUF100 tests/test_mode.py`, `python3 -m pytest tests/test_mode.py -q` | N/A | P1 HIT |
| U12 (`workflows/repository_hardening_workflow.md`, 165) | `Read`/`Edit` — restore the Phase 4 ordering note under the table. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |
| U13 (`tests/test_session_start.py`, 619 — over 200) | `skills/omni-context-minimizer/scripts/omni_minimizer.py` for the skeleton (`agents.md §2 ast_skeleton`), then targeted `Read` of `test_main_exits_zero_and_respects_line_cap`; `Edit` to add `monkeypatch.setattr(session_start, "is_nucleus", lambda: True)`. Verify: `python3 -m pytest tests/test_session_start.py -q`, `ruff check tests/test_session_start.py` | N/A | P1 HIT; P3 checked, no applicable skill |
| U14 (`docs/roadmaps/core/pipeline/021-030-program-queue.md`, 1666 — over 200 but Markdown, not code; `omni-context-minimizer` covers `.js/.py/.go/.ts`-class code, not prose, so the applicable token-economy instrument is targeted partial `Read`, not the AST skeleton tool) | `grep -n "Six findings\|KI-047-3" docs/roadmaps/core/pipeline/021-030-program-queue.md` to locate rows, then `Read` with `offset`/`limit` around line 256 (`agents.md §2 token_saver`); `Edit`. Verify: `scripts/verify_references.py`, `make verify` | N/A | P1 HIT |

Full-suite regression, run after every unit and finally after all 14 (plus any
U9 contingency rows) land: `python3 -m pytest tests/ -q` (Verification table,
exit `0`, zero failures).

`Destination` is `N/A` on every row: no skill is built, so there is no forge
destination to validate. Writing under `.agents/skills/` from any session is
prohibited (`agents.md §3 strict_rule`); it is not attempted here.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` (`audit_plan.py`) | Phase 1 / Phase 5 gate on `IMPLEMENTATION_PLAN.md` — already run at Phase 1 (`IMPLEMENTATION_PLAN.md` Verification table). |
| `omni-context-minimizer` (`omni_minimizer.py`) | `agents.md §2 ast_skeleton`: skeleton extraction before any partial read of the three Python targets over 200 lines — `scripts/verify_references.py` (552, U8), `tests/test_verify_references.py` (212, U8), `scripts/map_workflows.py` (325, U10), `tests/test_session_start.py` (619, U13). Not invoked for `docs/roadmaps/core/pipeline/021-030-program-queue.md` (1666, U14) — that file is Markdown prose, outside the tool's supported language set (NodeJS/Python/Go/Rust/Java); `agents.md §2 token_saver` (targeted `offset`/`limit` `Read`) is the applicable instrument there instead. |
| `graphify` | Phase 8 `venv_skillopt/bin/python -m graphify update . --force` post-change (`agents.md §2 graph_sync`; `IMPLEMENTATION_PLAN.md` Verification table). |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `omni-context-minimizer` for U1, U3-U7, U12, U14 | All below (agents.md, pipeline_workflow.md, implementer_agent.md, code_craft.md, rule_validator.md, repository_hardening_workflow.md) or Markdown-excluded (U14) — none clear the >200-line, code-file trigger (`agents.md §2 ast_skeleton`). Targeted `grep`/`offset`/`limit` `Read` suffice. |
| `python-quality-auditor` | Model-invoked style-score gate under `config/invocation_exceptions.json`, not a Phase 4.2 tool assignment — it runs automatically over `scripts/verify_references.py` (U8) and `scripts/map_workflows.py` (U10) as part of QA judgment, not as a skill this plan needs to schedule. No unit here is a Python refactor large enough to need a dedicated pre-audit beyond the standard `ruff` check already listed per row. |
| `sprint-architect` | The Work Breakdown (U1-U14) was produced at Phase 1 and is fixed in `IMPLEMENTATION_PLAN.md`. Phase 4.2 does not re-derive it. |
| `skill-creator` / `skill_forge_workflow` | No new skill is built: every unit maps to `Read`/`Edit` plus an existing deterministic gate. `rules/skills_and_integrations.md §1` — build only when the ladder finds no existing capability. |
| A new "rule-reconciliation" or "line-count refactor" skill | Over-engineering. U1-U7/U12/U14 are one-file prose/JSON edits with no repeatable transformation to encode; U10's line-count reduction is a one-time mechanical hoist verified by an existing AST one-liner, not a recurring operation that earns a forged tool (`rules/skills_and_integrations.md §1`). |
| `autoskills-3rd` (P2 rung) | Not reached — P1 resolved every unit, including the U9 contingency slot. |

## 5. Gaps

None. Every unit U1-U14 (and the U9 contingency, whose concrete file set is not
yet known) resolves to `Read`/`Edit` plus an existing verification tool (`ruff`,
`pytest`, `make verify`, `scripts/verify_references.py`,
`scripts/check_task_scope.py`, and AST-based line counting via the standard
library). No capability is missing; no skill is built.
