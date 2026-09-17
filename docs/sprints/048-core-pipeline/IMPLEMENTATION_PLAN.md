# Implementation Plan: Sprint 048 — jurisdictional-lock-reconciliation-and-047-residue

**Canonical path**: `docs/sprints/048-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/048` · **Base**: `main` at `cb0b6bb`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.

---

## Context

Sprint 047 closed (`v4.30.0`, `cb0b6bb`) leaving five findings (the routed section
names six `KI-047-*` numbers, but `KI-047-2` was already absorbed into the `RA-14`
amendment Sprint 047 itself applied and correctly carries no row) routed to a later
program in `docs/roadmaps/core/pipeline/021-030-program-queue.md` under
*"Still open for a later program — routed out of Sprint 047"*. This sprint applies
them. Two of the five changed shape during Phase 1 re-measurement, and both changes
are recorded in Design rather than silently absorbed.

**`KI-047-1` is not a template tweak.** Its friction recurred in 046 and 047 because
two rule statements genuinely contradicted: `agents.md §2 jurisdictional_lock`
("`1` single physical file per instantiated subagent task") against
`rules/code_craft.md §6`, which is machine-enforced by
`hooks/on_commit.py audit_regression_test` (lines 712-741) and requires a `fix(`
commit to stage a test file — i.e. two files. Sprint 046 escaped by mislabelling a
`fix(` commit `refactor(`; Sprint 047 re-paired 7 units mid-execution.

**`KI-047-3`'s stated premise is stale.** The roadmap says check (d) found 2
pre-existing broken anchors and "the rest of the corpus was not swept". Both were
fixed inside 047: `SPRINT_LOG.md:51-52` records U25 (`#loop_guard` in
`pipeline_workflow.md`) and U26 (`#session_bound` in `rules/token_economy.md`) as
landed. There is no anchor backlog. What remains is **checker coverage**.

**Measured against the tree at `cb0b6bb`:**

| Fact | Command that reproduces it |
| :--- | :--- |
| `scripts/map_workflows.py` `build()` spans lines 239-296 (57 > 50) | `python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('scripts/map_workflows.py').read_text()); print([(n.name,n.end_lineno-n.lineno+1) for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='build'])"` |
| `tests/test_mode.py:30` carries `# noqa: E402` | `sed -n '30p' tests/test_mode.py` |
| `tests/test_session_start.py:56-61` patches `repo_root`, not `is_nucleus` | `sed -n '56,61p' tests/test_session_start.py` |
| check (d) scans only three non-recursive trees | `sed -n '386,391p' scripts/verify_references.py` |
| Nothing enforces a per-commit file count | `grep -rn "jurisdictional_lock" hooks/` → no matches |
| Roadmap says "Six findings" over a five-row table | `sed -n '256p' docs/roadmaps/core/pipeline/021-030-program-queue.md` |

**True when done**: no statement in the always-loaded corpus asserts a per-commit
file count; a `fix(`-typed unit with its paired test is compliant by construction
rather than by exception; check (d) reaches every tree that declares `invoked_by:`;
and the four mechanical items from 047 are closed.

---

## Design

### D1 — The contradiction is removed at the root, not excepted at the edge

An exception clause bolted onto `jurisdictional_lock` was drafted and **rejected**.
If two rules contradict, the imprecise one is corrected so the two are consistent by
construction. Determination: `agents.md §2 jurisdictional_lock` is the imprecise
statement. It states a **proxy metric** (a count of files) and omits its
**invariant** (disjoint exclusive claims between concurrently in-progress tasks), so
every downstream paraphrase had to guess the invariant and two guessed "commit
content".

Evidence the invariant is concurrency-isolation, not commit composition:

| # | Evidence |
| :--- | :--- |
| 1 | Its category is `Isolation`, shared with `no_interference` (`agents.md:70-71`). The pair is a claim protocol: `no_interference` governs another task's claim, `jurisdictional_lock` the size of one's own |
| 2 | It quantifies "per instantiated subagent **task**", never per commit. `agents.md` has never said "one file per commit" |
| 3 | `ADR-0001:18`: "Since `jurisdictional_lock` gives each subtask exactly one file, **disjointness is trivial**" — guaranteeing disjointness *is* the concurrency invariant |
| 4 | `docs/roadmaps/core/pipeline/014-identity-branding-hardening.md:95` already rescued the rule from a count-based misreading on a different axis: "caps concurrent/instantiated scope per task at 1 file, **not lifetime touches per file**" |
| 5 | Nothing enforces a per-commit file count. The only machine-enforced side is `audit_regression_test`, which *requires* two files. Both Isolation rules are applied by *reading* `task_scope.md` (`config/artifact_registry.json:81`) |

`IMPLEMENTATION_PLAN_TEMPLATE.md:39-40` is a symptom, not the root: it already
contains the correct concept and undercuts it — "one atomic commit **touching** one
physical file **as its structural subject**". "Structural subject" is right;
"touching" is wrong. The sentence carries both readings and executors picked the
strict one. Correcting the template alone would leave the root stating a proxy and
the next paraphrase would drift again.

### D2 — Propagation is mandatory and its set is closed (`RA-14`)

The root restatement (U1) obliges correcting every derived statement in the same
patch. The set was established by full-corpus grep of `jurisdictional_lock`,
`no_interference`, `physical file`, `one file per` and `single file per`:
U2 (template), U3 (`pipeline_workflow.md` Phase 6), U4 (`implementer_agent.md`,
**two** places — frontmatter `description` line 3 and `write_scope` line 20),
U5 (`code_craft.md §2`), U6 (`memory_index.json`).

`docs/decisions/ADR-0001-no-parallel-fan-out.md:37` carries the stale gloss
"(one file per subagent)" and is **deliberately not patched**: an ADR records a
decision as reasoned at the time, and its argument is unaffected — disjointness of
*subjects* is as trivial as disjointness of files. Recorded as a decision, not a miss.

### D3 — `memory_index.json:89` must be replaced, not merely left

That entry encodes the rejected framing verbatim: *"the **sanctioned exception** is
the code file plus its one test together (Sprint 043 `96e3303` precedent)"*. After
U1 there is no exception to sanction, so the entry becomes false and would re-teach
the discarded model to the next fresh-context agent. `agents.md §4
definitive_amnesia` / `extract_workflow.md redundant_ki_purge` require its removal.

### D4 — U1 must land before U8, and U8 then validates U1

U8 is a `fix(`-typed change to `scripts/verify_references.py` whose paired test is
`tests/test_verify_references.py`. Under the *old* wording that commit is a
violation; under U1's restatement it is ordinary compliance. Sequencing U1 first
makes this sprint the first consumer of its own rule change, which is the cheapest
available validation of the restatement.

### D5 — `KI-047-3` is a bounded coverage extension, not a corpus sweep

`scripts/verify_references.py:386-391` globs `workflows/*.md`, `scripts/*.py`,
`hooks/*.py`, non-recursively. Files declaring `invoked_by:` that are never
anchor-checked: `skills/token-saver-auditor/scripts/audit_plan.py`,
`skills/slash-commander/scripts/verify_commands.py`,
`skills/mass-standardizer/scripts/mass_standardizer.py`, plus seven under `tests/`.
Lines 234-236 use the same three globs for the sibling half of check (d), so one
shared helper corrects both halves. Fallout is unknown until the checker runs, hence
the U9 contingency slot with a bounded abort.

### D6 — `agents/rule_validator.md:19` is a distinct `RA-14` defect, admitted on its own merits

It still says Model/Effort apply "when `session_tool` is `cursor`… otherwise" the
short shape. `pipeline_workflow.md:20` corrected exactly this in Sprint 041
(`scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` applies under every
harness) and the fix never propagated here. Unrelated to `KI-047-1`; included as U7.

### Rejected alternatives

| Alternative | Why rejected |
| :--- | :--- |
| Amend only `IMPLEMENTATION_PLAN_TEMPLATE.md §Work` (the roadmap's original proposal) | Leaves the root stating a proxy metric; the contradiction survives and recurs a third time |
| Add an exception clause to `jurisdictional_lock` sanctioning the impl+test pair | A contrived special case layered on a rule whose general statement is the actual defect |
| A deterministic Phase-1 gate rejecting an unpaired `fix(` Work row | Needs a machine-readable "this unit will be `fix(`" signal — a new Work/`task_scope` column rippling into `check_task_scope.py`, `check_template_gates.py` and every consumer. A sprint of its own. Routed to *Out of scope* |
| Fix `scripts/_mode.py`'s sibling `RUF100` alongside `tests/test_mode.py` | Belongs to the pre-existing `S045-02` batch; folding one file out of a 188-finding batch creates a partial state nobody can audit |

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) with one physical file as
its structural subject (`agents.md §2 jurisdictional_lock`, as restated by U1).
U8 is planned as one paired row per that restatement — it is the first unit written
under it.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify — restate `§2 Isolation jurisdictional_lock` as its invariant (exactly one file as structural subject; subject is the unit of isolation, not a count of files in a commit; caps concurrent claim scope, not lifetime touches) | high | `rule_validator` | ✅ `9be872d` |
| U2 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify — `## Work` gloss drops "touching", names the structural subject, and requires a `fix(`-typed unit to name its paired test in the same row (`KI-047-1`) | medium | `rule_validator` | ✅ `e4afc40` |
| U3 | `workflows/pipeline_workflow.md` | modify — Phase 6 Done-criterion reads "one structural subject per commit"; a mandatory companion is not a second subject | medium | `rule_validator` | ✅ `aaefdfd` |
| U4 | `agents/implementer_agent.md` | modify — frontmatter `description` (line 3) and `write_scope` (line 20) both restated to "one structural subject per task" | low | `rule_validator` | ✅ `ea33343` |
| U5 | `rules/code_craft.md` | modify — §2 line 21 reads "bounds **which file** a subagent claims as its subject" | low | `rule_validator` | ✅ `81345d8` |
| U6 | `memory_index.json` | modify — replace the superseded entry at line 89 encoding the void "sanctioned exception" framing (`redundant_ki_purge`) | low | `governance_learner` | ✅ `8037213` |
| U7 | `agents/rule_validator.md` | modify — line 19 Model/Effort shape aligned to `check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` under every harness (`D6`) | low | `rule_validator` | ✅ `f818ff0` |
| U8 | `scripts/verify_references.py` (subject) **+ paired test** `tests/test_verify_references.py` | modify — **landed scope, corrected at Gate 1 remediation**: only `check_invoked_by_anchors` (the anchor-resolution half of check (d), line ~390) was extended to `skills/*/scripts/*.py` and `tests/*.py`; `check_invocation_coverage` (the sibling half, lines 234-236) was deliberately left at its original three trees. Extending both surfaced 59 findings, over Abort criterion 2's 10-item threshold; a human mid-execution decision scoped the unit down to the anchor-resolution half alone (0 new findings), leaving the coverage-half question for a dedicated future sweep (`KI-047-3`) | high | `implementer_agent` | ✅ `ffcb874` |
| U9 | *contingency* — files named by U8's first run | modify — repair `invoked_by:#anchor` defects surfaced in newly covered trees; one commit per subject. **Abort if more than 10 defects surface** (see Abort criterion 2) | medium | `implementer_agent` | n/a — not triggered (0 fallout) |
| U10 | `scripts/map_workflows.py` | modify — hoist the two trailing legend blocks (lines 266, 282) to module-level constants so `build()` is at or under 50 lines; output must be byte-identical (`KI-047-4`) | medium | `implementer_agent` | ✅ `f1c323b` |
| U11 | `tests/test_mode.py` | modify — remove the unused `# noqa: E402` at line 30 after measuring with `ruff` (`KI-047-5a`) | low | `implementer_agent` | ✅ `a9ab722` |
| U12 | `workflows/repository_hardening_workflow.md` | modify — restore Phase 4's "before any history decision" ordering constraint as a one-line note under the table, lost in the `S045-19` reshape (`KI-047-5b`) | low | `rule_validator` | ✅ `73ef5df` |
| U13 | `tests/test_session_start.py` | modify — add `monkeypatch.setattr(session_start, "is_nucleus", lambda: True)` to `test_main_exits_zero_and_respects_line_cap` (`KI-047-6`) | low | `implementer_agent` | ✅ `b80063c` |
| U14 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — "Six findings" to five with `KI-047-2` recorded as absorbed into `RA-14`; rewrite `KI-047-3`'s stale premise; mark the bucket applied | low | `orchestrator` | ✅ `c6b61d1` |

**Ordering**: U1 before U2-U6 (they cite the restated rule). U1 before U8 (`D4`).
U8 before U9. U10-U14 independent.

---

## Dependencies

`rules/code_craft.md §7` — every dependency is permanent code you do not control.
Before adding one, check the standard library, then what is already present. The
commit that adds it must also carry `Dependency: <name> — <reason>`.

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | This sprint adds no dependency. U8 uses `pathlib.Path.glob` already imported in `scripts/verify_references.py` |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| check (d) `invoked_by:#anchor` resolution over the extended tree set (U8) | deterministic — widens an existing `make verify` check, adds no new entry point | `Makefile#verify` (unchanged) |
| Phase-1 obligation to plan a `fix(`-typed unit as one paired row (U2) | **agent judgment** — the deterministic alternative is named below and is not built here | `workflows/pipeline_workflow.md` Phase 1 via `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` |

**Filter 5 disclosure.** The second mechanism is agent judgment while a deterministic
alternative exists: a `check_task_scope.py` gate rejecting an unpaired `fix(` Work
row. It is **named, costed and routed** rather than silently preferred — it requires
a new machine-readable commit-type column on the Work and `task_scope.md` tables,
rippling into `scripts/check_task_scope.py`, `scripts/check_template_gates.py` and
every consumer, which is a sprint of its own. Destination: *Out of scope*, row 1.
This sprint removes the rule contradiction that made the judgment call ambiguous;
mechanising the call is separable and deferred deliberately.

`RA-16 INVOCATION_COVERAGE`: no workflow, script, executable skill, hook or gate
merges without a declared, verifiable invoker, or a typed exception in
`config/invocation_exceptions.json` stating why it has none.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 14 | Count of rows in Work tables |
| Subagents dispatched | 1 (Phase 1, `principal_agent`; updated at close with the full pipeline count) | Native delegation; count dispatched at close |
| Prior session ratio | 4.6 | `python3 scripts/session_cost.py --from-anchor --json` → `cycles[0].ratio` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

---

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it.

| Check | Fails against the current tree? |
| :--- | :--- |
| `scripts/verify_references.py` check (d) rejects an unresolvable `#anchor` declared in `skills/*/scripts/*.py` or `tests/*.py` | **Yes** — this is the defect (`D5`; those trees are outside the glob at lines 386-391) |
| `build()` in `scripts/map_workflows.py` is at or under 50 lines (AST-measured) | **Yes** — this is the defect (57 lines, `KI-047-4`) |
| `ruff check --select RUF100 tests/test_mode.py` reports no finding | **Yes** — this is the defect (`KI-047-5a`) |
| `python3 -m pytest tests/test_session_start.py` passes with `is_nucleus()` returning False | **Yes** — this is the defect (`KI-047-6`), though it is green in every sanctioned context (nucleus clone, CI, separate clone, worktree); the guard protects the test from ambient checkout shape rather than repairing a live red |
| `python3 scripts/map_workflows.py` leaves `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` byte-identical | **No** — regression to protect; U10 is a refactor and must not alter generated output |
| No statement outside `docs/` history asserts a per-commit file count | **Yes** — this is the defect (U1-U6); no executable test exists, verified by the grep in Verification |

---

## Verification

The exact commands, and what each must return. Read exit codes with `$?` directly;
**never through a pipe**, which reports the exit code of the last command in it.

| Command | Expected |
| :--- | :--- |
| `make verify` | exit `0` |
| `python3 -m pytest tests/ -q` | exit `0`, zero failures |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/048-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/048-core-pipeline` | exit `0` |
| `grep -rn "physical file" --include=*.md --include=*.json . \| grep -v docs/sprints/ \| grep -v CHANGELOG.md \| grep -v docs/audits/ \| grep -v docs/roadmaps/ \| grep -v docs/plans/` | only `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md:39` (U2's own corrected text, "one physical file **as its structural subject**" — benign, not a stale count claim) remains. `ADR-0001-no-parallel-fan-out.md:37` uses the phrase "one file per subagent", which this grep pattern does not match — the file is deliberately unpatched (`D2`) but is not itself proof of this check passing (`F-048-QA6`, corrected at Gate 1 remediation) |
| `python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('scripts/map_workflows.py').read_text()); print(max(n.end_lineno-n.lineno+1 for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='build'))"` | `50` or less |
| `python3 scripts/map_workflows.py; git diff --exit-code docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | exit `0`, empty diff (U10 output-identical) |
| `ruff check --select RUF100 tests/test_mode.py` | exit `0` |
| `python3 scripts/verify_references.py` | exit `0` after U9 fallout is cleared |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§2 Isolation jurisdictional_lock` restated as its invariant, with the 046/047 precedent recorded |
| `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | `## Work` gloss corrected; `fix(`-pairing obligation added |
| `workflows/pipeline_workflow.md` | Phase 6 Done-criterion restated |
| `workflows/repository_hardening_workflow.md` | Phase 4 ordering constraint restored as a note |
| `agents/implementer_agent.md` | Two statements restated (description, `write_scope`) |
| `agents/rule_validator.md` | Model/Effort shape aligned to `check_task_scope.py` |
| `rules/code_craft.md` | §2 opening sentence restated |
| `memory_index.json` | Superseded "sanctioned exception" entry replaced |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 047 bucket marked applied; count and `KI-047-3` premise corrected |
| `CHANGELOG.md` | `[Unreleased]` entry at closeout (`RA-05`) |
| `docs/sprints/048-core-pipeline/` | Plan, `SPRINT_LOG.md`, `agent_assignment.md`, `skill_assignment.md`, `task_scope.md`, `PHASE_REGISTER.md` |

**Measured figures.** Every number in Context / Design / Verification carries
the command that reproduces it. A figure without its command is memory, not
evidence (`021-030-program-queue.md` J6 / T5).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| A deterministic Phase-1 gate rejecting an unpaired `fix(` Work row | Requires a new commit-type column on Work and `task_scope.md` plus changes to `check_task_scope.py` and `check_template_gates.py`. Sprint-sized. → new row under *Still open for a later program* in `docs/roadmaps/core/pipeline/021-030-program-queue.md` |
| `scripts/_mode.py` sibling `RUF100` | Belongs to the pre-existing repo-wide `ruff` batch (`S045-02` / roadmap T3, 188 findings) |
| `docs/decisions/ADR-0001-no-parallel-fan-out.md:37` stale gloss | Deliberately untouched: historical decision record, argument unaffected (`D2`) |
| `S045-29` | Deferred human policy call, unchanged by this sprint |
| `last_harden_run` anchor field | Routed out of 047 as a new mechanism; still unowned |
| Recursive descent into `skills/**/scripts/` beyond one level | U8 covers `skills/*/scripts/*.py`; deeper nesting does not exist today and `code_craft.md §1` forbids building for a case with no instance |

---

## Abort criterion

Stop and revert if any of these is observed:

1. U1's restatement cannot be written such that `make verify` and
   `scripts/check_template_gates.py` both exit `0` without weakening the invariant —
   i.e. if passing the gates requires reintroducing a file count. Re-open the
   reconciliation with the human rather than patching around it.
2. U8's first run surfaces more than 10 broken `invoked_by:#anchor` defects in newly
   covered trees. That is a corpus-wide defect, not a contingency slot: land U8 with
   the extension gated off or the fallout accepted as a tracked red, and route the
   remainder to a dedicated sweep rather than expanding this sprint mid-execution.
   Threshold confirmed by the human at Phase 1 (10, unchanged from draft).
3. U10 cannot be made byte-identical in generated output. A refactor that changes
   `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` is not a refactor; drop U10 and return
   `KI-047-4` to the roadmap.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (`gst.mirabal@gmail.com`) — Phase 5, attended, not in a `/loop` |
| **Date** | 2026-09-17 |
| **Plan commit at approval** | `1bde7d9` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both. Until Sprint 041 it named only `/loop`, so **every plan written faithfully
> from this template was rejected by the mandatory Phase 1 gate** — the template
> failed the check that consumes it, and the only passing plans were the ones that
> had dropped this footer. Replace `{{…}}` placeholders; leave this pairing intact.
