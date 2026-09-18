# 📝 Sprint Log: #048
**Session Tracker**: 20260916T210722Z-20684
**Role Active**: Orchestrator

---

## 🚦 Session Metadata
| Parameter | Value |
| :--- | :--- |
| **Active Layer** | core / pipeline |
| **Sprint Slug** | jurisdictional-lock-reconciliation-and-047-residue |
| **Stack / Layer** | core / pipeline |
| **Branch** | `ai-sprint/048` |
| **Base** | `main` at `cb0b6bb` |
| **Strategic Goal** | Apply the five findings routed out of Sprint 047 (`KI-047-1`, `KI-047-3`, `KI-047-4`, `KI-047-5`, `KI-047-6` — `KI-047-2` was absorbed into the `RA-14` amendment Sprint 047 itself applied and correctly carries no row) across 14 planned one-file units (U1–U14), plus U7's independent `RA-14` defect in `agents/rule_validator.md`. The sprint's centre of gravity is `KI-047-1`, which is not a template tweak: `agents.md §2 jurisdictional_lock` stated a **proxy metric** (a count of files) and omitted its **invariant** (disjoint exclusive claims between concurrently in-progress tasks), so it genuinely contradicted `rules/code_craft.md §6` — machine-enforced by `hooks/on_commit.py audit_regression_test`, which *requires* a `fix(` commit to stage two files. Sprint 046 escaped the contradiction by mislabelling a `fix(` commit `refactor(`; Sprint 047 re-paired 7 units mid-execution. An exception clause sanctioning the impl+test pair was drafted and **rejected** by the human: when two rules contradict, the imprecise one is corrected at its root, not excepted at its edge. U1 corrects the root; U2–U6 are the closed propagation set established by full-corpus grep (`RA-14`); U8 is the first unit written under the restated rule and validates it. |
| **Intelligence State** | CERTIFIED (`docs/active_state.json` `intelligence_certified: YES`) |
| **Start Time** | 2026-09-16T21:07:22Z |

---

## 🏁 Sprint Progression

Four waves. Each unit is one atomic commit (`RA-08`) with **one structural
subject** — the rule this sprint restates (`agents.md §2 jurisdictional_lock`,
landed by U1). U8 is the sprint's one paired row (subject + its mandatory
companion test); under the restatement that companion is not a second subject,
which is the point of sequencing U1 before it (`IMPLEMENTATION_PLAN.md` `D4`).
14 units, at most 15 distinct physical files, no file claimed twice.

### Wave 1 — U1–U5, U7, U12: root restatement + propagation (gate: `make verify`)

- [x] **Objective 1**: Restate `jurisdictional_lock` at its root and propagate to every derived statement in the same patch (`RA-14`).
    - `[x]` U1 — `agents.md` (`9be872d`): `§2 Isolation jurisdictional_lock` restated as its invariant — exactly one file as **structural subject**, declared in `task_scope.md`, no concurrently in-progress task may claim it; the subject is the unit of isolation, **not a count of files in a commit**; caps concurrent claim scope, never lifetime touches (Phase 014 `T21`/`T22` precedent).
    - `[x]` U2 — `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` (`e4afc40`): `## Work` gloss drops "touching", names the structural subject, requires a `fix(`-typed unit to name its paired test in the same row.
    - `[x]` U3 — `workflows/pipeline_workflow.md` (`aaefdfd`): Phase 6 Done-criterion reads "one structural subject per commit — a mandatory companion is not a second subject".
    - `[x]` U4 — `agents/implementer_agent.md` (`ea33343`): two statements in one file — frontmatter `description` (line 3) and `write_scope` (line 20).
    - `[x]` U5 — `rules/code_craft.md` (`81345d8`): §2 line 21 reads "bounds **which file** a subagent claims as its subject".
    - `[x]` U7 — `agents/rule_validator.md` (`f818ff0`): line 19 Model/Effort shape aligned to `scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` under every harness (`D6`) — an independent `RA-14` defect; `pipeline_workflow.md:20` corrected this in Sprint 041 and it never propagated here.
    - `[x]` U12 — `workflows/repository_hardening_workflow.md` (`73ef5df`): Phase 4's "before any history decision" ordering constraint restored as a note, lost in the `S045-19` reshape.

### Wave 2 — U6: `memory_index.json`

- [x] **Objective 2**: Remove, not merely leave, the entry encoding the rejected framing.
    - `[x]` U6 — `memory_index.json` (`8037213`): the entry at line 89 read *"the **sanctioned exception** is the code file plus its one test together"*. After U1 there is no exception to sanction; replaced before it could re-teach the discarded model to the next fresh-context agent (`D3`; `agents.md §4 definitive_amnesia`).

### Wave 3 — U8–U11, U13: framework-root `scripts/` and `tests/` (`implementer-agent`, `F-026-A1`)

- [x] **Objective 3**: Close the four mechanical items from 047 and extend check (d)'s coverage; zero regression.
    - `[x]` U8 — `scripts/verify_references.py` + paired `tests/test_verify_references.py` (`ffcb874`, 2 files, 37 insertions): `check_invoked_by_anchors` extended to `skills/*/scripts/*.py` and `tests/*.py`. **Landed narrower than planned** — see *Deviations*. 0 new anchor findings; U9 not triggered. This sprint's own first `fix(` commit written under U1's restatement, compliant by construction rather than by exception.
    - `[x]` U9 — *contingency, not triggered*: 0 broken `invoked_by:#anchor` defects surfaced in the newly covered trees.
    - `[x]` U10 — `scripts/map_workflows.py` (`f1c323b`): two trailing legend blocks hoisted to module-level constants; `build()` measured at **39 lines** (was 57, cap is 50). Generated output byte-identical (`git diff --exit-code docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` exit 0). Abort criterion 3 not reached.
    - `[x]` U11 — `tests/test_mode.py` (`a9ab722`): unused `# noqa: E402` removed at line 30, measured with `ruff check --select RUF100` first. Sibling `RUF100` in `scripts/_mode.py` deliberately untouched (`S045-02` batch, Out of scope row 2).
    - `[x]` U13 — `tests/test_session_start.py` (`b80063c`): `monkeypatch.setattr(session_start, "is_nucleus", lambda: True)` added to `test_main_exits_zero_and_respects_line_cap`, mirroring Sprint 047's U22 guard on the sibling test.

### Wave 4 — U14: roadmap

- [x] **Objective 4**: Close the 047 bucket in the Global Roadmap with a measured account.
    - `[x]` U14 — `docs/roadmaps/core/pipeline/021-030-program-queue.md` (`c6b61d1`): "Six findings" corrected to five with `KI-047-2`'s absorption explained; `KI-047-3`'s stale premise (2 broken anchors, uncorrected) rewritten — both were fixed inside 047 by U25/U26, the real gap was checker coverage; bucket marked applied.
    - `[x]` U14 follow-up (`584a7b2`, Gate 1 round 1 remediation): `KI-047-3`'s row corrected again to state only the anchor-resolution half landed, and a new *"Still open for a later program — routed out of Sprint 048"* section opened with `KI-048-1` (the 59-file `check_invocation_coverage` policy question).

### Incident — concurrent-agent git-index race during Wave 1, fully recovered

Wave 1 dispatched three `implementer_agent` instances concurrently for U10, U11
and U13 (each targeting a disjoint file — `jurisdictional_lock`/`no_interference`
both satisfied, no `task_scope.md` row double-claimed). Their `git add`/`git
commit` calls raced on the **shared `.git/index`** of the one checkout:

1. U10's first `git commit` was swept into U11's commit by the race (wrong
   commit `70d3a35`, two unrelated files in one commit). U10's agent detected
   this via `git log`/`git reflog`, took a backup branch, `git reset --soft` to
   the parent, and recommitted `tests/test_mode.py` and
   `scripts/map_workflows.py` separately — restoring `map_workflows.py`'s
   content from the known-good blob after a second concurrent write had
   reverted it mid-surgery.
2. U11's agent, independently trying to fix its own contaminated commit, ran
   `git reset --hard 14d6d95` (the commit before the wave started). This
   recovered its own situation but **silently discarded four other units'
   uncommitted, never-staged working-tree edits** — U1 (`agents.md`), U7
   (`agents/rule_validator.md`), U12 (`workflows/repository_hardening_workflow.md`),
   U14 (the roadmap) — which left no git object and were therefore
   unrecoverable by `git fsck`.
3. Detected by the top-level session running an independent `git log`/`git
   status`/content check rather than trusting the isolated agent reports. All
   four units were re-applied directly (U1, U7, U12 from the exact text already
   held in context; U14 redispatched alone, with no other `Bash`-holding agent
   running concurrently) and recommitted (`9be872d`, `f818ff0`, `73ef5df`,
   `c6b61d1`).

Final state verified clean: `make verify` exit `0`, `git status --porcelain`
empty, all 13 unit shas re-confirmed against `git log --oneline cb0b6bb..HEAD`
(25 commits total on this branch).

**The isolation rules held and the collision still happened** — the finding:
both Isolation rules partition *files*, and neither partitions the git index, a
serialised resource no unit claims and `task_scope.md` cannot express. Recorded
below as `KI-048-2`, deliberately not patched in this sprint. From this point
forward in the sprint, no more than one `Bash`-holding subagent was dispatched
at a time; non-`Bash` roles (`rule_validator`, `orchestrator`,
`governance_learner`) continued to run concurrently since they never touch git.

**Final tally**: 748 tests pass (747 baseline + 1 new, U8's paired test).
`make verify` exit `0`.

---

## 🧠 Rule Amendments & Heuristic Harvest

| Friction Point | Resolution / Workaround | KI ID |
| :--- | :--- | :--- |
| Extending **both** halves of `verify_references.py` check (d) to `skills/*/scripts/*.py` and `tests/*.py` surfaced **59** files with no `invoked_by:` declaration and no typed exception — 5.9× Abort criterion 2's threshold of 10. Most are ordinary pytest suites and skill helper modules never individually required to declare an invoker | Abort criterion 2 executed as written: the unit was scoped down mid-execution to the anchor-resolution half alone (0 findings) under a human decision, and the remainder routed out rather than absorbed. The open question is policy, not mechanics — must every `tests/*.py` declare `invoked_by:`, or does `config/invocation_exceptions.json` carry a blanket typed exception? | `KI-048-1` (`021-030-program-queue.md`, *Still open for a later program — routed out of Sprint 048*) |
| Two subagents with **disjoint structural subjects** — fully compliant with `jurisdictional_lock` and `no_interference` as restated by this sprint's own U1 — collided on the shared `.git/index` during Wave 1. Both Isolation rules partition files; neither partitions the index | Recovered in-session (see *Incident* above). Not patched here: widening `jurisdictional_lock` in the same sprint that restates it would re-import the ambiguity U1 just removed. Candidate remedies to cost separately: serialise commit execution to one agent at a time (adopted for the remainder of this sprint); or a declared index lease held for the duration of a unit's commit | `KI-048-2` |
| Three documents give three different owners for the graph rebuild: `workflows/pipeline_workflow.md:24` puts it in Phase 8, `workflows/close_workflow.md:30` puts it in close Phase 5 after `atomic_commit` (with the measured reason: rebuilding in Phase 1 left `graph.json` mtime behind later commits, so `session_probe.py` reported a false *behind*), and `Makefile:29,33` comments still label both targets "close_workflow Phase 1" | `close_workflow.md` Phase 5 is the authority — most specific, only one carrying its own measurement. The other two are stale by exactly the `RA-14` class this sprint exists to remove | `KI-048-3` (candidate) |
| A session's `agents.md` context (via the host `CLAUDE.md` import) is a snapshot taken at session start. A sprint that amends `agents.md` mid-session cannot assume its own later-dispatched subagents see the amendment unless explicitly told to re-`Read` the file from disk — `anti_amnesia` covers session start and post-compaction, not "the rule changed mid-session". Every Phase-6/7 dispatch in this sprint that depended on U1's landed text was explicitly instructed to trust the on-disk file over its own injected context, which is why none were misled — but the instrument was manual, not structural | Candidate: when a unit's structural subject is `agents.md` or a `rules/*.md` file, every subsequent subagent dispatch in that sprint should be told to `Read` the amended section directly, as a standing instruction rather than a per-dispatch reminder | `KI-048-4` (candidate) |

### Deviations from the approved plan

- **U8 landed narrower than approved.** The plan's `D5` scoped U8 to a shared helper correcting **both** halves of check (d). Extending `check_invocation_coverage` alongside `check_invoked_by_anchors` produced 59 findings, over Abort criterion 2's threshold of 10. Per that criterion, a **human mid-execution scoping decision** confined U8 to the anchor-resolution half; no shared helper was built. The 59-item remainder is `KI-048-1`. Abort criteria 1 and 3 were not reached.
- **The Implementation Plan was edited during execution and at both Gate-1 remediation rounds** (`5742d86`, `f432b97`, on top of the Phase-5-approved `1bde7d9`) — the U8 Work row, the `## Verification` grep-expectation row, and `D5`'s design narrative were each corrected to state the landed (narrower) scope, in place, with the finding ID that motivated the correction. These are additive record corrections that never altered an approved scope item's intent; the approval stamp (`Plan commit at approval: 1bde7d9`) still points at the text the human actually approved.
- **U9 not executed.** A contingency slot the plan authorized conditionally; its condition (defects surfaced by U8's first run) evaluated to 0. Recorded as `n/a — not triggered`, not as an incomplete unit.
- **`docs/decisions/ADR-0001-no-parallel-fan-out.md:37` deliberately unpatched.** Its "(one file per subagent)" gloss is stale under U1; `D2` records the decision not to patch it — an ADR records a decision as reasoned at the time and its argument (disjointness of subjects is as trivial as disjointness of files) is unaffected. A recorded exclusion, not an `RA-14` miss.
- **The roadmap's `## Status` "Next / in flight" line was deliberately not updated for Sprint 048.** Checked the precedent rather than assuming: Sprint 047's own entry first appears only at `cb0b6bb` ("mark Sprint 047 deployed as v4.30.0"), not at its close (`72ed706`) — the field is a deploy-time record, not a close-time one. Sprint 048 is not yet deployed.

---

## 🚦 Quality Gate

| Gate | Round | Verdict | Class | Notes |
| :--- | :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | REJECTED | charter | Functional work independently verified clean (`make verify` exit 0, 748 passed, U10 byte-identical, commit-type honesty, the six restated statements internally consistent, RA-14 propagation grep closed). Three blocking findings, all record-integrity, none functional: **F-048-QA1** — `task_scope.md` never transcribed `✅ <sha>` per landed unit, contradicting `pipeline_workflow.md:22`'s own Done-criterion. **F-048-QA2** — U8's landed rescope (anchor-half only) was not reflected in the plan's Work row, `task_scope.md`, or `skill_assignment.md`, which still described the wider, abandoned extension. **F-048-QA3** — Abort criterion 2's own escape hatch ("route the remainder to a dedicated sweep") had no landing place, since U14 had consumed the only "Still open for a later program" section that existed. Three testifying annotations carried into remediation without counting: **F-048-QA4** stale "six findings" in `task_scope.md`/plan Context; **F-048-QA5** inverted attribution in `agents.md:70`'s restated text; **F-048-QA6** the plan's Verification-table grep row named `ADR-0001-no-parallel-fan-out.md` as proof of a pattern that file does not actually match. |
| QA Agent (Gate 1) | 2 | RECORD | testifying | Fresh-context re-audit. All three round-1 blockers independently re-verified resolved — `git show <sha> --stat` run on all 13 unit shas confirming each touches exactly its named file(s); the 59-finding figure independently **reproduced** in a throwaway worktree; the new roadmap section and `KI-048-1` row confirmed present. `make verify` re-run fresh: exit 0, 748 passed. Two further one-sentence residues found and fixed in the same pass (not counted, not bounced): **F-048-QA7** — `IMPLEMENTATION_PLAN.md` `D5` still asserted the abandoned "one shared helper corrects both halves" design as current, three sections after the Work/Verification rows were already corrected (`f432b97`). **F-048-QA8** — `task_scope.md` described `agents/rule_validator.md:19`'s stale wording in the present tense, after U7 had already corrected it (`d729e00`). |
| Tester Agent (Gate 2) | 1 | RECORD | testifying | Full suite executed directly, twice (748 passed both times, exit 0), plus `make verify` end-to-end. Zero regression confirmed against a clean `cb0b6bb` baseline (747 tests). Every sprint-added/modified test proven non-vacuous by mutation, not by reading the assertion: U8's paired test reds (`0 == 2`) when the two added globs are reverted; U13's `is_nucleus` guard reds when flipped to `False`, and — stronger — the base tree in a `.git`-less sandbox actually fails this exact test while HEAD passes it, reproducing `KI-047-6` and confirming its repair; U11's `ruff check tests/test_mode.py` passes clean and reintroducing the `noqa` reproduces `RUF100`, confirming it was genuinely stale; U10's byte-identity re-confirmed with **both** the landed and the pre-refactor generator against the same tree. One testifying finding, same root cause as `F-048-QA3`/round 1: the roadmap's `KI-047-3` row (at the time) claimed both check (d) halves were extended; resolved by the same `584a7b2` remediation this Gate-1 round-1 finding produced. |

No third consecutive `REJECTED` on any logic block; `workflows/remediation_workflow.md` was not invoked. `check_gate_log.py` and `check_role_artifact.py` both exit `0` against this table.

---

## ⚓ Documentation Entry Point Seal

**Strategic Lock**: LOCKED
**Next Phase**: Both gates closed (`RECORD`/`testifying`, no bounce) → Phase 8 Sprint Closeout → `workflows/close_workflow.md`

*Certified under conventional commit standard: docs(sprint): message #048*
