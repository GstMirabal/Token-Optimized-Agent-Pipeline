# Task Scope — Sprint 050 (deterministic-quality-instrument)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap/Plan
against current `rules/`. `jurisdictional_lock` and `no_interference` are both
applied by reading this file; `scripts/loop_guard.py` measures progress from it;
`workflows/close_workflow.md` Phase 2.6 demands it as phase evidence.

**Provenance note.** The `rule_validator` subagent dispatched for this phase
was terminated mid-task by an account-level session rate limit (HTTP 429,
reset 11:30am Europe/Madrid) before writing this file. Before the
interruption it completed the `no_interference` check (confirmed: Sprint 049
is CLOSED/deployed, no other `IN_PROGRESS` sprint directory exists — the same
finding recorded below) and had not yet begun drafting the artifact. Per
`pipeline_workflow.md` Phase 4.1's contemplated case — "a session that cannot
dispatch subagents still writes the file, recording which profile's ruleset
governed each write" — the session completed this document directly, under
`agents/rule_validator.md`'s ruleset, reproducing the same structure and
precedent-citation standard as the sprint's other Phase 4 artifacts. No
content below was authored to a lower standard than a fresh dispatch would
have produced; this note exists so the substitution is visible rather than
implicit.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(`docs/active_state.json`). **Model/Effort columns are required regardless of
tool**: `scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` fires for any
sprint numbered ≥28 under every harness — Sprint 050 qualifies independently of
`session_tool`.

Model/Effort source: `config/model_tiers.json` `tiers.author.claude_code`
(`sonnet` / `medium`) for every row. All three assignees in this sprint
(`rule_validator`, `implementer_agent`, `doc_orchestrator`) are listed under
`tiers.author.profiles`; none is in `tiers.gate.profiles` or
`tiers.mechanical.profiles`. Every unit is a stdlib-only Python script, a
`Makefile`/JSON/workflow-prose edit, or a governance amendment — no new logic
class beyond what the plan already declares, no new dependency (`Dependencies:
None`), no mechanical-tier work. This role transcribes that flat verdict; no
`token_economy_agent` escalation was raised on the tier itself
(`tier_transcription`). No `Declared escalations`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/050-core-pipeline`

---

## Work

One row per unit U1–U10 (`IMPLEMENTATION_PLAN.md` `## Work`). `File` is the
single physical file that is the unit's structural subject
(`agents.md §2 jurisdictional_lock`). `U2` and `U6` each carry a paired test in
the same commit; that companion is a mandatory companion, not a second
claimable subject, and so does not appear as its own row. Assignees are the
Phase 4.1 binding staffing (`agent_assignment.md`), which corrected three units
from the plan's original proposal (`U1`, `U4`, `U5` — see that file's
`Disagreements with the plan`).

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `11186bb` |
| U2 | `scripts/quality_audit.py` (+ paired `tests/test_quality_audit.py`, same commit) | create | high | `implementer_agent` | sonnet | medium | ⏳ |
| U3 | `Makefile` | modify | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U4 | `config/invocation_exceptions.json` | modify | low | `rule_validator` | sonnet | medium | ⏳ |
| U5 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ⏳ |
| U6 | `scripts/session_state.py` (+ paired `tests/test_session_state.py`, same commit) | modify | high | `implementer_agent` | sonnet | medium | ⏳ |
| U7 | `workflows/close_workflow.md` | modify | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| U8 | `workflows/deployment_workflow.md` | modify | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| U9 | `tests/test_audit_cursor_models.py` | modify | low | `implementer_agent` | sonnet | medium | ⏳ |
| U10 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (generated, never hand-edited) | low | `implementer_agent` | sonnet | medium | ⏳ |

### `jurisdictional_lock` and `no_interference`

**`agents.md` is claimed twice (`U1`, `U5`) — not a violation, because the
claims are sequential, never concurrent** (`D8`, `agent_assignment.md`
Ordering constraints: "`U1` before `U5`, never concurrent" —
`jurisdictional_lock` caps *concurrent* claim scope, not lifetime touches,
Phase 014 `T21`/`T22` precedent). Wave 1 execution order
(`agent_assignment.md`): `U1` → `U2` → `{U3, U4, U5}`, with `U5` additionally
gated on `U1` having closed. No other subject is claimed twice in this table.

**`no_interference`**: checked `docs/sprints/` for any other `IN_PROGRESS`
sprint directory. `049-core-pipeline` carries a `PHASE_REGISTER.md` and the git
log shows it deployed (`753fbe1 docs(roadmap): mark Sprint 049 deployed as
v4.32.0 #049`) — CLOSED, not concurrent. `050-core-pipeline` is the only
sprint directory with an open `current_sprint` anchor
(`docs/active_state.json`: `{id: 50, status: IN_PROGRESS}`). No other
concurrently in-progress `task_scope.md` exists that could claim any of the 10
files above. Queried `graphify-out/graph.json` (nodes + links present) for
dependency edges touching the 10 target files against anything outside this
sprint's own unit set — no external in-flight claim found.

### Paired tests carried inside a unit

| Unit | Commit type | Paired test in the same commit |
| :--- | :--- | :--- |
| U2 | `feat(` | `tests/test_quality_audit.py` |
| U6 | `fix(` | `tests/test_session_state.py` |

`rules/code_craft.md §6` requires the test in the same commit and
`hooks/on_commit.py audit_regression_test` verifies it for `fix(`-typed
commits; `U2` is `feat(` (new file) and carries its test in the same commit by
plan design (`D6`), not by that hook's enforcement.

---

## Rule audit

| Rule | Bearing on this sprint | Verdict |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | `agents.md` claimed by `U1` and `U5`, sequentially, never concurrently | **Satisfied** — ordering constraint recorded above and in `agent_assignment.md` |
| `agents.md §2 no_interference` | No other in-progress task claims any subject in this table | **Satisfied** — Sprint 049 is CLOSED and deployed as `v4.32.0`; no other `IN_PROGRESS` sprint directory exists |
| `agents.md §2 token_saver` / `ast_skeleton` | `scripts/cursor_adapter.py` and other >200-line files are read-only reference for `U2`/`U6`, not edit targets; the two new/modified subjects (`quality_audit.py` new, `session_state.py` existing) are read via targeted sections, not full dumps | **Satisfied** — no full-file dump required by this sprint's own targets |
| `agents.md §3 strict_rule` / `jurisdiction` | Nucleus session: the framework is the work | **Satisfied** — `.git` is a real directory; sprint records belong in `.agents/docs/sprints/` |
| `agents.md §5 historical_log` | Commit suffix `#050`, Conventional Commits | **Satisfied** — Phase 1/3/4.1/4.2 commits (`5f1b174`, `532b508`, `7ef9c72`, `195eba9`) already carry it |
| `RA-08 COMMIT_SQUASH` | Atomic local commits; squash at Closeout | **Satisfied** — 10 atomic units planned |
| `RA-12 BRANCH_DISCIPLINE` | All work on `ai-sprint/050` | **Satisfied** — branch cut from `main`@`753fbe1` before the first commit |
| `RA-16 INVOCATION_COVERAGE` | `U2` and `U6` are new/modified scripts requiring a declared `invoked_by:`; `U4` corrects two exception notes | **Satisfied by design** — `U2`'s plan content states `invoked_by: Makefile \`quality-audit\` target`; `U6`'s subcommand is invoked from `close_workflow.md` (`U7`) and `deployment_workflow.md` (`U8`) in the same sprint, so the invoker lands before the sprint closes |
| `rules/code_craft.md §6` | One `fix(` unit (`U6`) | **Satisfied** — paired test tabled above |
| `rules/code_craft.md §7` | Dependencies | **Satisfied** — plan declares `None`; every unit is stdlib-only (`D4`) |
| `agents/token_economy_agent.md` `burden_of_proof` | Whether a recurring mechanism may be built as deterministic vs. agent judgment | **Satisfied** — `skill_assignment.md` Phase 4.2 discovery independently re-derived `D3`'s script-vs-skill split (no reusable skill found; `scripts/` is the correct jurisdiction for a deterministic, `Makefile`-invoked instrument) |
| `agents.md §1 code_logic` | English in code, logs, commits and artifacts | **Satisfied** — `IMPLEMENTATION_PLAN.md` is the only Spanish artifact, which `§1 user_chat` permits |
| `agents.md §1 unambiguous_action` | Every unit names its operation, its target by name and its done-criterion | **Satisfied** — plan `## Tests` and `## Verification` carry the criteria per unit |
| `agents.md §0 mandatory_topology` (generated-doc clause) | `U10` regenerates `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | **Satisfied** — never hand-edited; `U7`/`U8` must land first (`agent_assignment.md` Wave 3 ordering) |

### Findings raised against the plan

| # | Finding | Disposition |
| :--- | :--- | :--- |
| 1 | `D5` leaves the `verify`-wiring branch (A vs. B) undecided until `U2` is measured against the live repository | **Not a violation, sequencing recorded.** `U2` must land and be run over the tree before `U3` decides `.PHONY quality-audit`'s membership in `verify`; both branches are already declared in the plan so neither is renegotiated post-hoc |
| 2 | `U1` and `U5` amend `agents.md`, the always-loaded constitution, twice in one sprint | **Allowed, assignee constrained and sequenced.** `§6 rule_validator` is the only profile chartered to index amendments into `agents.md`; `agent_assignment.md` assigns both to it and orders them non-concurrently around `U2` |
| 3 | `U6` is a `fix(`-typed modification to an existing script (`session_state.py`) that currently has no dedicated test file (`grep -rln 'session_state' tests/` → 3 files, none its own) | **Intended, not a gap.** The plan's own unit content for `U6` calls this out and creates `tests/test_session_state.py` as the first direct-coverage file for that script, paired in the same commit per `rules/code_craft.md §6` |

---

## Verdict

**APPROVED for Phase 5.** Ten live units, three assignees, all author-tier. No
subject is claimed twice concurrently in this table (`agents.md` claimed
twice, sequentially, per `D8`). No rule in `rules/` is contradicted by the plan
as written, and the three findings above are dispositions, not blockers.

Phase 5 remains a single attended human authorization and is not satisfied by
this verdict.
