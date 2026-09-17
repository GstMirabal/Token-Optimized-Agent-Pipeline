# Task Scope — Sprint 048 (jurisdictional-lock-reconciliation-and-047-residue)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap/Plan
against current `rules/`. `jurisdictional_lock` and `no_interference` are both
applied by reading this file; `scripts/loop_guard.py` measures progress from it;
`workflows/close_workflow.md` Phase 2.6 demands it as phase evidence.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(`docs/active_state.json`). **Model/Effort columns are required regardless of
tool**: `scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` fires for any
sprint numbered ≥28 under every harness — Sprint 48 qualifies independently of
`session_tool`. `agents/rule_validator.md:19`'s "when `session_tool` is
`cursor` … otherwise" wording *was* the stale statement U7 in this sprint's plan
corrects — already landed at `f818ff0`, so line 19 now carries the corrected
`MODEL_FROM_SPRINT = 28` text itself (`workflows/pipeline_workflow.md:20` carried
the correct version from the start); it was not read as authority on this point
while drafting this table, back when it was still stale.

Model/Effort source: `config/model_tiers.json` `tiers.author.claude_code`
(`sonnet` / `medium`) for every row. All four assignees in this sprint
(`rule_validator`, `governance_learner`, `implementer_agent`, `orchestrator`) are
listed under `tiers.author.profiles`; none is in `tiers.gate.profiles` or
`tiers.mechanical.profiles`. Every unit is a prose amendment to governance
documents or a stdlib-only Python script/test edit — no new logic class, no new
dependency, no mechanical-tier work. This role transcribes that flat verdict; no
`token_economy_agent` escalation was raised and none applies (`tier_transcription`).
No `Declared escalations`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/048-core-pipeline`

---

## Work

One row per unit U1–U14 (`IMPLEMENTATION_PLAN.md` `## Work`). `File` is the
single physical file that is the unit's structural subject
(`agents.md §2 jurisdictional_lock`, **as restated by this sprint's own U1** —
U8 is the first unit written under the restated invariant and is deliberately
scoped to one structural subject plus its mandatory companion test, not a second
subject; see `jurisdictional_lock` below).

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | high | `rule_validator` | sonnet | medium | ✅ `9be872d` |
| U2 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `e4afc40` |
| U3 | `workflows/pipeline_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `aaefdfd` |
| U4 | `agents/implementer_agent.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `ea33343` |
| U5 | `rules/code_craft.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `81345d8` |
| U6 | `memory_index.json` | modify | low | `governance_learner` | sonnet | medium | ✅ `8037213` |
| U7 | `agents/rule_validator.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `f818ff0` |
| U8 | `scripts/verify_references.py` (subject) + paired test `tests/test_verify_references.py` — **landed narrower than planned**: only `check_invoked_by_anchors` (anchor-resolution half of check (d)) was extended to `skills/*/scripts/*.py` and `tests/*.py`. `check_invocation_coverage` (the sibling half) was deliberately left untouched — extending it too produced 59 findings, over Abort criterion 2's threshold of 10, confirmed by a human scoping decision mid-execution. The 59-finding remainder is routed to a new roadmap entry (see U14/roadmap) | modify | high | `implementer_agent` | sonnet | medium | ✅ `ffcb874` |
| U9 | *contingency* — not triggered. U8's landed (scoped) extension surfaced 0 new anchor-resolution findings, so no contingency repair was needed | n/a | medium | `implementer_agent` | sonnet | medium | n/a — not needed |
| U10 | `scripts/map_workflows.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `f1c323b` |
| U11 | `tests/test_mode.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `a9ab722` |
| U12 | `workflows/repository_hardening_workflow.md` | modify | low | `rule_validator` | sonnet | medium | ✅ `73ef5df` |
| U13 | `tests/test_session_start.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `b80063c` |
| U14 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | sonnet | medium | ✅ `c6b61d1` (plus a remediation-pass follow-up correcting the U8 description and adding the deferred-sweep entry) |

**Ordering** (`IMPLEMENTATION_PLAN.md` "Ordering", unchanged here): U1 before
U2–U6 (they cite the restated rule). U1 before U7 (D6 is a distinct `RA-14`
defect but shares the corrected-rule dependency in spirit; no hard order stated
beyond U1's precedence over the propagation set). U1 before U8 (`D4`). U8 before
U9. U10–U14 independent of the above and of each other.

**14 units, at most 15 distinct physical files** (U8 names two: its structural
subject plus one mandatory companion test, permitted under the restated
`jurisdictional_lock` — see below; U9's file(s) are unknown until U8 runs and are
bounded by Abort criterion 2). No file is claimed by two units of this sprint.

---

## Rule audit

### Rules consulted

| Rule file | Bearing on this sprint |
| :--- | :--- |
| `rules/code_craft.md` | U8–U11, U13 touch Python (`scripts/verify_references.py`, `scripts/map_workflows.py`, `tests/test_mode.py`, `tests/test_session_start.py`, and U9's contingency file(s)). Type hints, ≤50-line functions (U10's whole purpose is bringing `build()` to ≤50 lines), ≤3 indentation levels, no `TODO`/`FIXME`, English only. §6 (`fix(` commits must stage their proving test) is the exact rule U1 reconciles `jurisdictional_lock` against — U8 is this sprint's own first compliant instance (`D4`). |
| `rules/token_economy.md` | Plan carries `## Cost` (work units 14, `delegation_mode: native`, prior-session ratio 4.6× — `scripts/session_cost.py --from-anchor --json`), under the 5× soft threshold. Model/Effort here transcribe the flat author-tier verdict; no escalation. |
| `rules/documentation_standard.md` | U1–U7, U12, U14 edit `agents.md` / templates / `workflows/*.md` / a roadmap document. U10 regenerates no documentation directly but must leave `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` byte-identical (plan `## Verification`) — it is not a documentation edit, it is a refactor with a documented no-diff invariant. |
| `rules/qa_and_testing.md` | `tester_agent` executes the suite; it does not author test files. U8, U11, U13 (test edits) are `implementer_agent`, consistent with `F-026-A1`. |
| `rules/loop_governance.md` | No `/loop` planned for Execution by default; any `/loop` for Phases 6–8 is governed by `scripts/loop_guard.py start` (named in the plan footer alongside `/loop`, satisfying `audit_plan.py` Filter 6). |
| `rules/project_topology.md` | U8–U11, U13 run under the framework root; tests via `venv_skillopt/bin/python -m pytest`. `graphify update .` via `venv_skillopt/bin/python -m graphify` (never the bare console-script) at the quality/commit phase. |

### Rule conflict audit — U1–U6 against the currently-active corpus (Phase 4.3 charter)

Full-corpus grep (`jurisdictional_lock`, `no_interference`, `physical file`,
`one file per`, `single file per`), excluding `docs/sprints/`, `docs/roadmaps/`,
`docs/plans/`, `docs/audits/`, `CHANGELOG.md` (history, not always-loaded rule
text):

- `agents.md:70` — the statement U1 restates.
- `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md:40` — the statement
  U2 restates ("touching" → structural-subject language).
- `workflows/pipeline_workflow.md:20,22,27` — line 20 (Phase 4.3 row) already
  carries the *corrected* Model/Effort text (D6's target for U7); line 22 (Phase
  6 Done-criterion, "one physical file per commit where `jurisdictional_lock`
  applies") is the statement U3 restates; line 27 is a historical-precedent note
  about a host that skipped Phase 4/7, not a count claim — no conflict, no
  change needed.
- `agents/implementer_agent.md:3,20` — the two statements U4 restates
  (frontmatter `description`, `write_scope`).
- `rules/code_craft.md:21` — read directly: *"`jurisdictional_lock` bounds how
  many **files** a subagent touches; nothing bounded how much of one file it
  rewrites."* Confirmed as U5's target — the file-count framing U5 corrects to
  "bounds **which file** a subagent claims as its subject."
- `memory_index.json:89` — the void "sanctioned exception" entry U6 replaces.
- `config/artifact_registry.json:81` and `scripts/docs_freshness_check.py:428` —
  both say the two Isolation rules are "enforced by READING this file"; neither
  states a file **count**. No restatement needed, no conflict with U1's
  invariant.
- `.gitignore:68` — a comment referencing the same "applied by reading" idea, not
  a rule statement. No change needed.
- `docs/decisions/ADR-0001-no-parallel-fan-out.md:18,37` — carries the stale
  gloss "(one file per subagent)" at line 37. **Deliberately not patched**
  (plan `D2`): an ADR records a decision as reasoned at the time; its argument
  (disjointness of structural subjects is as trivial as disjointness of files)
  is unaffected by the restatement. Not a live conflict — a historical record,
  correctly excluded from the propagation set.
- `rules/qa_and_testing.md`, `rules/loop_governance.md`, `rules/django_backend_standard.md` —
  grepped for "one file"/"per commit"/"atomic commit"/"structural subject":
  no hits bearing on file-count semantics. No conflict.

**Verdict: no conflict found.** The propagation set U1–U7 (U1 root + U2–U6
derived statements + U7's distinct `RA-14` defect) is closed against the
always-loaded and machine-enforced corpus as measured at `cb0b6bb`. The one
statement left unpatched (`ADR-0001:37`) is a deliberate, reasoned exclusion
recorded in the plan, not an oversight this audit is flagging. `hooks/on_commit.py`
`audit_regression_test` (lines 712–741, read directly) confirms the mechanism
the plan cites: it requires a `fix(` commit touching a source file to also stage
a test file, which is precisely the two-physical-file case the *old*
`jurisdictional_lock` wording made ambiguous and U1's restatement resolves by
naming the companion test as not a second structural subject.

### `jurisdictional_lock` (one structural subject per unit)

Every unit U1–U14 names exactly one physical file as its structural subject,
except:

1. **U8's mandatory companion test** — `tests/test_verify_references.py` rides
   with `scripts/verify_references.py` in the same commit under
   `rules/code_craft.md §6`. Not a second structural subject under the
   restatement U1 itself lands in this sprint (`D4`): the companion is a
   mandatory pairing, not an independent claim.
2. **U9 is a contingency slot**, not a named file — its subject(s) are
   discovered by U8's own first run and bounded by Abort criterion 2 (≤10
   defects, else route to a dedicated sweep rather than expanding this sprint).

No other file is named twice across U1–U14.

### `no_interference` (no target claimed by another active subtask)

`docs/active_state.json` `current_sprint.id` = 48 is the only sprint
`IN_PROGRESS`. Sprints 021–047 are closed and deployed (`last_close_commit`
`cb0b6bb`); their `task_scope.md` rows are all terminal. No U1–U14 target file
is listed by an in-progress subtask in any other `task_scope.md`.

### Missing rules

None. No new `rules/` file is required. This sprint applies five findings routed
from Sprint 047 (`docs/roadmaps/core/pipeline/021-030-program-queue.md` — the
routed section named six `KI-047-*` numbers, but `KI-047-2` was already absorbed
into the `RA-14` amendment Sprint 047 applied and correctly carries no row) against
**existing** rules, workflows, agent profiles and scripts, plus U7's independent
`RA-14` defect in `agents/rule_validator.md`. No rule category is unaddressed by
the current `rules/` corpus.

---

## Verdict

`task_scope.md` shape: `# | File | Operation | Risk | Assignee | Model | Effort |
Status` — Model/Effort required under every harness for sprint ≥28
(`scripts/check_task_scope.py:38`), independent of `session_tool`. 14 rows, one
per U1–U14. `jurisdictional_lock` and `no_interference` both hold, with two
narrow, plan-declared conditions on U8 (mandatory companion test, not a second
subject) and U9 (contingency slot, subject unknown until U8 runs, bounded by
Abort criterion 2). **Rule conflict audit of U1–U6 against the currently-active,
always-loaded corpus: no conflict found** — the propagation set is closed per
`RA-14`, and the one intentionally-unpatched reference (`ADR-0001-no-parallel-fan-out.md:37`)
is a recorded historical decision, not a live inconsistency. No missing `rules/`
file.
