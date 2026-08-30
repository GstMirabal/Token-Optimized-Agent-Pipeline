# Task Scope — Sprint 042 (template-gate-parity)

Source: `docs/sprints/042-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`) and
`agent_assignment.md` (Phase 4.1, the staffing authority).
Phase 4.3 of `workflows/pipeline_workflow.md`, audited by `rule_validator`.

This file is what `agents.md §2 jurisdictional_lock` and `no_interference` are
applied by **reading**. A unit not listed here has no claim on any file.

---

## Work

Shape: `# | File | Operation | Risk | Assignee | Model | Effort | Status`

`Model` / `Effort` are **required from Sprint 28 onward for every harness**, not
only under Cursor — `scripts/check_task_scope.py:38,119` (`MODEL_FROM_SPRINT = 28`).
Both assignees declare `tier: author` (`agents/implementer_agent.md:6`,
`agents/doc_orchestrator.md:6`), which `config/model_tiers.json` maps to
`sonnet` / `medium` on this harness. Family aliases only — a dated model ID in
this column is prohibited.

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U2 | `config/template_gates.json` | create | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U3 | `scripts/check_template_gates.py` | create | **high** | `implementer_agent` | opus | high | ⏳ |
| U4 | `Makefile` | modify | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U5 | `tests/test_check_template_gates.py` | create | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U6 | `README.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U7 | `docs/decisions/ADR-0012-template-gate-parity.md` | create | low | `doc_orchestrator` | sonnet | medium | ⏳ |

**Seven units, seven distinct physical files.** No file appears twice, so
`jurisdictional_lock` (one structural subject per task) and `no_interference`
(no file claimed by two in-flight subtasks) both hold by construction. Verify
with `awk -F'|' '/^\| U/ {print $3}' task_scope.md | sort | uniq -d` → empty.

### Tier escalation proposed — U3 only

`agents.md §6` routes a divergence between a task's difficulty and its role's
default tier through this file, recorded so the human sees it — never through a
selector agent, which would spend the unit of cost tiering exists to reduce.

| Unit | Default | Proposed | Reason |
| :--- | :--- | :--- | :--- |
| U3 | `sonnet` / `medium` (`author`) | **`opus` / `high`** | It executes commands declared in a data file. The four `D5` restrictions (no shell, `argv[0]` must be `python3`, script path resolved inside the repository, single expandable token) are the whole of the containment, and an incomplete implementation of them is a path from an edited `.json` to arbitrary execution inside `make verify` and CI. It is also the unit the Abort criterion is written against |

Every other unit keeps its role default. Neither assignee is a `mechanical`
profile, so no `mechanical`-at-`high` escalation note is owed
(`scripts/check_task_scope.py:207-225`).

---

## Rule audit

Findings from auditing the roadmap against `rules/` and `agents.md`.

| Rule | Verdict | Note |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | ✅ | One physical file per unit; seven distinct paths |
| `agents.md §2 no_interference` | ✅ | No duplicate target across in-flight units |
| `agents.md §2 pre_shielding` | ✅ | `git status --porcelain` listed only this sprint's own untracked directory before the branch was cut |
| `agents.md §3 strict_rule` / `jurisdiction` | ✅ | Nucleus mode (`scripts/_mode.py`): `.git` is a real directory, so the framework **is** the work and these records belong at `docs/sprints/` here. No submodule to contaminate |
| `agents.md §5 mandatory_topology` | ✅ | Canonical path `docs/sprints/042-core-pipeline/` |
| `agents.md §5 historical_log` | ✅ | Every commit carries `#042` and Conventional Commits; enforced by `.git/hooks/commit-msg` |
| `RA-08 COMMIT_SQUASH` | ✅ | Atomic local commits, one per unit; squash happens at close |
| `RA-12 BRANCH_DISCIPLINE` | ✅ | `ai-sprint/042` created at Phase 3 from `main` at `e29ac98`, before any commit |
| `RA-16 INVOCATION_COVERAGE` | ⚠️ **binding on U3** | `scripts/check_template_gates.py` is a new mechanism. Its module docstring MUST declare `invoked_by: Makefile#verify`, and `scripts/verify_references.py` check (d) must resolve it. U4 is what makes that declaration true — **U3 and U4 are not independently mergeable**, and U4 must land in the same phase, not be deferred |
| `RA-14 PATCH_PROPAGATION` | ⚠️ **binding on U1** | The `F8` correction is a status change repeated across a corpus. U1 is not closed until `grep -rn "F-023-S4\|F8" docs/ rules/ workflows/ agents.md` has been read in full and every live claim of «open» corrected. Sprint records under `docs/sprints/*` and the tick history in `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` are **history and are not rewritten** |
| `rules/code_craft.md §7` | ✅ | No new dependency. `IMPLEMENTATION_PLAN.md` `## Dependencies` says `None` explicitly |
| `rules/code_craft.md` complexity | ⚠️ **binding on U3** | Render, execute and report are three concerns. `agents.md §1` caps a function at 50 lines and 3 indentation levels; the loop over cases nests a loop over rendered files, so the per-case body belongs in its own function before the second loop is written, not after `ruff` complains |
| `rules/qa_and_testing.md` | ⚠️ **binding on U5** | Every check in the plan's `## Tests` marked **Yes** must be shown failing before its repair lands (*reproduce before repairing*). For U5 that means the divergent-template fixture is observed rejected by `check_template_gates.py` and the same fixture is observed **unnoticed** by the pre-sprint tree, which has no such check |
| `agents.md §1` `ephemeral` markers | ✅ | No `TODO`/`FIXME` may enter any unit; `make verify` rejects them |
| `agents.md §1` `code_logic` | ✅ | All seven files are English. Spanish is confined to `IMPLEMENTATION_PLAN.md`, which `agents.md §1 user_chat` permits |
| `agents.md §1` `max_lines_per_func` precedent | ⚠️ **advisory on U3** | Sprint 041 QA rejected round 1 over exactly this budget, on a function that was already over it before the sprint. U3 creates a new file, so it carries no inherited excess and has no excuse |

---

## Risk concentration

| Unit | Why it is the risk | Containment |
| :--- | :--- | :--- |
| **U3** `scripts/check_template_gates.py` | It runs subprocesses whose argument vectors come from a JSON file that any later contributor may edit. Confusing «declared by us» with «safe» is how a data file becomes an execution vector inside CI | The `D5` restrictions are enforced in code and asserted in U5, one test per restriction. `argv[0]` is compared against the literal `python3`; the script path is resolved with `Path.resolve()` and required to be relative to the framework root |
| **U3** (second face) | A checker that special-cases its gates becomes a second copy of the gates and diverges — the sprint's own defect, one level up | The Abort criterion is mechanical: `grep -c "audit_plan\|forge_ladder\|gate_log" scripts/check_template_gates.py` must be `0`. Those names live in `config/template_gates.json` |
| **U4** `Makefile` | `verify` is the single gate CI invokes (`.github/workflows/ci.yml` calls the target rather than listing steps). A malformed line breaks every check after it, locally and in CI, for every sprint | One line added beside the sibling sprint gates; `make verify` run end to end before the commit, exit read with `$?` and never through a pipe |
| **U1** `021-030-program-queue.md` | It is the document that decides what is worked on next. A wrong status here costs a planning round — measured this session | The correction states the closing artifact (`H-002-secrets`), the date, and the command that re-measures it, so the next reader verifies instead of trusting |

---

## Out of jurisdiction

Files an executing role may **not** touch under this scope, with where the
concern goes instead.

| Path | Why excluded |
| :--- | :--- |
| `docs/standards/templates/*` | **The whole point.** This sprint measures templates; it does not edit them. A unit that repairs a template to make the new check pass would be the check certifying its own author's edit. A genuine divergence found during Phase 6 is recorded and routed, not silently patched |
| `skills/token-saver-auditor/scripts/audit_plan.py`, `scripts/check_forge_ladder.py`, `scripts/check_gate_log.py` | The gates under test. Their behaviour is the regression to protect; the instrument is a harness over them, never an edit to them |
| `scripts/check_role_artifact.py` | Its exit `2` against `SPRINT_LOG_TEMPLATE.md` is correct behaviour at the wrong phase (plan `D7`). The resolution is a typed exception in U2, not a change to the gate |
| `scripts/verify_references.py` | Plan `D1` rejected adding check (g) there. Its `check_templates_exist` is a regression to protect |
| `.github/workflows/ci.yml` | It invokes `make verify` and lists no steps of its own. U4 is therefore sufficient; editing CI would duplicate the invoker `RA-16` requires to be single |
| `docs/active_state.json` | Anchor. Written only by `scripts/session_state.py` and the close workflow (`state_homologation`) |
| `hooks/on_commit.py` | `F8` is closed. U1 corrects the record of it; the code is untouched and is a regression to protect |
| `.claude/`, `.cursor/` | Generated bridge mirrors, both gitignored. Outputs of the installer, never edited by hand |

---

## Finding raised by this audit — U3 and U4 are one merge, not two

`RA-16` requires a declared, verifiable invoker for every new mechanism, and
`scripts/verify_references.py` check (d) enforces it. U3 creates a script whose
docstring declares `invoked_by: Makefile#verify`; until U4 adds that line, the
declaration names an invoker that does not invoke it.

The ordering consequence is stated here because the Work table's numbering does
not carry it: U3 may be committed before U4, but **Phase 6 does not end with U4
outstanding**, and `make verify` is not claimed green until both have landed.
This is the same class of coupling Sprint 041 recorded for `U13`+`U14`, where a
commit gate forced a fix and its assertions into one commit — here the coupling
is a rule rather than a hook, so it is recorded rather than enforced mechanically.
