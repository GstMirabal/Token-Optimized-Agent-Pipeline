# Task Scope — Sprint 049 (cursor-bridge-100)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap/Plan
against current `rules/`. `jurisdictional_lock` and `no_interference` are both
applied by reading this file; `scripts/loop_guard.py` measures progress from it;
`workflows/close_workflow.md` Phase 2.6 demands it as phase evidence.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(`docs/active_state.json`). **Model/Effort columns are required regardless of
tool**: `scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` fires for any
sprint numbered ≥28 under every harness — Sprint 49 qualifies independently of
`session_tool`.

Model/Effort source: `config/model_tiers.json` `tiers.author.claude_code`
(`sonnet` / `medium`) for every row. Both assignees in this sprint
(`implementer_agent`, `rule_validator`) are listed under `tiers.author.profiles`;
neither is in `tiers.gate.profiles` or `tiers.mechanical.profiles`. Every unit is
a stdlib-only Python edit, a `Makefile` target, a JSON data file, or a governance
prose amendment — no new logic class, no new dependency, no mechanical-tier work.
This role transcribes that flat verdict; no `token_economy_agent` escalation was
raised on the tier itself (`tier_transcription`). No `Declared escalations`.

`token_economy_agent` **delivered** its pre-approval judgment on the proposed
reclassification and returned **HOLD**: the named deterministic alternative does not
perform the displaced check (`F-049-7`, transcribed in `SPRINT_LOG.md`). `U9` is
withdrawn as a result and no live unit proposes a reclassification. The governing
text is `agents/token_economy_agent.md` `burden_of_proof` — **not**
`rules/token_economy.md`, which contains zero occurrences of the word `Filter`
(`grep -c -i filter rules/token_economy.md` → `0`). That mis-citation was this
plan's own and is corrected here and in `IMPLEMENTATION_PLAN.md` `D1`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/049-core-pipeline`

---

## Work

One row per unit U1–U12 (`IMPLEMENTATION_PLAN.md` `## Work`). `File` is the
single physical file that is the unit's structural subject
(`agents.md §2 jurisdictional_lock`). A `fix(`-typed unit carries its paired test
in the same commit; that companion is a mandatory companion, not a second
claimable subject, and so does not appear as its own row.

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/cursor_adapter.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ `b5df5bd` |
| U2 | `scripts/install.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ `b247a27` |
| U3 | `profiles/example-project/rule_triggers.json` | create | low | `implementer_agent` | sonnet | medium | ✅ `9daca5d` |
| U4 | `scripts/bridge_state.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ `258ac26` |
| U5 | `scripts/audit_cursor_era.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `e72eb6f` |
| U6 | `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | modify | low | `implementer_agent` | sonnet | medium | ✅ `80f1ef7` |
| U7 | `scripts/audit_cursor_models.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `b38cd1d` |
| U8 | `tests/test_cursor_phase1.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `591e047` |
| ~~U9~~ | ~~`Makefile`~~ | **withdrawn** | — | — | — | — | 🚫 |
| U10 | `config/invocation_exceptions.json` | modify | medium | `rule_validator` | sonnet | medium | ✅ `8fd2662` |
| U11 | `agents.md` | modify | high | `rule_validator` | sonnet | medium | ✅ `dbd5b15` |
| U12 | `Makefile` | modify | low | `implementer_agent` | sonnet | medium | ✅ `d112407` |

### `jurisdictional_lock` and `no_interference`

With `U9` withdrawn, `U12` is the only unit claiming `Makefile`: the shared-subject
constraint recorded in the first revision no longer applies. **No subject is claimed
twice in this table.** The single remaining ordering constraint is `U1` before `U2`,
which is a call-signature dependency, not a `jurisdictional_lock` matter.

### Paired tests carried inside a unit

| Unit | Commit type | Paired test in the same commit |
| :--- | :--- | :--- |
| U1 | `fix(` | `tests/test_cursor_adapter.py` |
| U2 | `fix(` | `tests/test_installer.sh` |
| U4 | `fix(` | `tests/test_bridge_state.py` |
| U5 | `fix(` | `tests/test_audit_cursor_era.py` |
| U7 | `fix(` | `tests/test_audit_cursor_models.py` |

`rules/code_craft.md §6` requires the test in the same commit and
`hooks/on_commit.py audit_regression_test` verifies it. Planning the pair at
Phase 1 is what Sprint 047 had to do mid-execution for 7 units.

---

## Rule audit

| Rule | Bearing on this sprint | Verdict |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | No subject is claimed twice since `U9` was withdrawn | **Satisfied** — every live unit names a distinct structural subject |
| `agents.md §2 no_interference` | No other in-progress task claims any subject in this table | **Satisfied** — Sprint 048 is CLOSED and deployed as `v4.31.0` |
| `agents.md §2 token_saver` / `ast_skeleton` | Three subjects exceed 200 lines (`cursor_adapter.py` 368, `install.py`, `audit_cursor_models.py`) | **Satisfied** — `omni-context-minimizer` assigned to `U1`, `U2`, `U7` in `skill_assignment.md` |
| `agents.md §3 strict_rule` / `jurisdiction` | Nucleus session: the framework is the work | **Satisfied** — `.git` is a real directory; sprint records belong in `.agents/docs/sprints/` |
| `agents.md §5 historical_log` | Commit suffix `#049`, Conventional Commits | **Satisfied** — Phase 3 commit `e2ec1ac` already carries it |
| `RA-08 COMMIT_SQUASH` | Atomic local commits; squash at Closeout | **Satisfied** — 12 atomic units planned |
| `RA-12 BRANCH_DISCIPLINE` | All work on `ai-sprint/049` | **Satisfied** — branch cut from `c0f5904` before the first commit |
| `RA-16 INVOCATION_COVERAGE` | `U10` **corrects** two exception notes and keeps both exceptions; `U12` adds one `Makefile` target | **Satisfied by string retention, not by sequencing** — `verify_references.py check_invocation_coverage` builds its corpus from `agents.md`, `workflows/`, `commands/`, `rules/*.md` and `agents/*.md`; the `Makefile` is **not** in it. The first revision's sequencing claim named the wrong mechanism. `U11` must keep the literal strings `python-quality-auditor` and `js-standardizer` in the rewritten rows |
| `rules/code_craft.md §6` | Five `fix(` units | **Satisfied** — paired tests tabled above |
| `rules/code_craft.md §7` | Dependencies | **Satisfied** — plan declares `None`; every unit is stdlib-only |
| `agents/token_economy_agent.md` `burden_of_proof` | Whether a recurring mechanism may be reclassified to deterministic | **Satisfied by withdrawal** — the audit ruled the named alternative does not perform the displaced check, so nothing is reclassified. Building the real instrument is Sprint 050 (`IMPLEMENTATION_PLAN.md` `## Out of scope`) |
| `agents.md §1 code_logic` | English in code, logs, commits and artifacts | **Satisfied** — `IMPLEMENTATION_PLAN.md` is the only Spanish artifact, which `§1 user_chat` permits |
| `agents.md §1 unambiguous_action` | Every unit names its operation, its target by name and its done-criterion | **Satisfied** — plan `## Tests` and `## Verification` carry the criteria per unit |

### Findings raised against the plan

| # | Finding | Disposition |
| :--- | :--- | :--- |
| 1 | `U6` modifies a file whose own header reads *"Derived by `scripts/audit_cursor_era.py`. Do not edit by hand."* | **Not a violation, sequencing recorded.** `U6` is the committed output of running `make cursor-era-audit` after `U5`, not a hand edit. The Quality Gate should reject `U6` if its diff is not byte-identical to a fresh regeneration |
| 2 | `U11` amends `agents.md`, the always-loaded constitution | **Allowed, assignee constrained.** `§6 rule_validator` is the only profile chartered to index amendments into `agents.md`; `agent_assignment.md` assigns it there and nowhere else |
| 3 | The plan's expected `make cursor-tiers` result after `U7` is **exit 2** | **Intended.** Recorded in the plan's `## Out of scope`: the gate going red on a real drift is the unit working. Reconciling which model wins is a tier trial, not this sprint |

---

## Verdict

**APPROVED for Phase 5.** Twelve units, two assignees, both author-tier. One
shared structural subject (`Makefile`) with its sequencing constraint recorded and
binding. No rule in `rules/` is contradicted by the plan as written, and the three
findings above are dispositions, not blockers.

Phase 5 remains a single attended human authorization and is not satisfied by this
verdict.
