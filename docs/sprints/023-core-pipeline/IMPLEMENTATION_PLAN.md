# Implementation Plan: Sprint 023 — upstream-findings

**Canonical path**: `docs/sprints/023-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/023` · **Base**: `main` at `18696c5` (`v4.7.0`)
**Status**: `EXECUTING`

> First artifact written from `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md`,
> which unit `C0` of this sprint ships. Filed retroactively, and that is recorded rather
> than hidden: this sprint began before the rule existed, so its plan was extracted from
> a draft that lived in `~/.claude/plans/` — the exact ephemeral storage the unit is about.

---

## Context

A host running sprints 085-093 accumulated thirteen framework-class findings.
`agents.md §4 feedback_upstream` obliges routing them upstream; `§3 strict_rule`
forbids that host patching the submodule in place. **Between those two rules a nucleus
finding had nowhere to live**, and for eight sprints it lived nowhere: the inventory sat
in a session scratchpad and was lost.

The seven findings recovered from that inventory **reproduce 7 of 7** against `v4.4.0`.
The governing rule of this sprint is therefore **reproduce before repairing**: a check
that passes against the current tree proves nothing about a defect claimed to be in it.

Two more units were found while *closing* Sprint 022 — by running the close machinery
rather than reading it — and they are one defect class with the rest:
**a control that treats "I could not determine" as a determination.**

---

## Design

### The unifying frame

`C9` answers red when it does not know; `C10` answers green. Neither corrupts data;
both make a gate lie. The remedy is not to let doubt pass — a real outage that passed
would be a false green, the same defect inverted — but to **stop collapsing doubt into
a verdict**, and to report it as doubt with a different remedy attached.

### `C9` — three values, because two cannot express doubt

`merged_pr_exists` returned a bool and mapped every non-zero exit to `False`, so
*"I could not find out"* became *"no merged PR exists"*. Measured against the live API:
**2 of 12 calls returned `rc=1`, `HTTP 503`**. Since `content_is_integrated` already
returns `False` for every squash-merged branch, one 503 was enough to flip an
**integrated** branch to unintegrated — reproduced as two triple-runs of `audit` on an
unchanged tree exiting `0,2,0` and `0,0,2`, **accusing a different branch each time**.

Ran first by design: this sprint's own close invokes `branch_sovereignty audit`, so
repairing that gate last would mean tripping on the defect the sprint exists to remove.

### `C0` — the plan gets a location and a gate

The Implementation Plan is `triple_lock`'s first lock, the Phase 1 deliverable, and
`rules/code_craft.md §7` requires justifying every dependency in it. It is mentioned
**seven times** across the governance corpus and **no document said where it is written**.
Measured: 11 templates in `docs/standards/templates/` and none for a plan.

**The sequencing contradiction, resolved.** The plan is *authored* at Phase 1; the sprint
directory is *instantiated* at Phase 3. The canonical path does not exist when the plan is
written. So: Phase 1 authors, Phase 3 files and commits, Phase 5 checks as a precondition,
close verifies retrospectively.

**No new mechanism.** Enforcement reuses what PR `#37` built — the `artifact → producing
phase` map in `scripts/docs_freshness_check.py` gains one entry. No new script, no new
`invoked_by` to declare (`RA-16`).

**Declared limit.** The close gate proves the plan **exists and is versioned** — the loss
it was built against. It does **not** prove the plan existed before approval; that ordering
is held by the Phase 5 precondition, an attended human step. Written down rather than left
to be discovered.

---

## Work

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C9 | `scripts/branch_sovereignty.py`, `tests/`, `close_workflow.md` | modify | **high** — a gate | lead · `devops_agent` ruleset | ✅ `437493b` |
| C0 | `agents.md`, `pipeline_workflow.md`, `close_workflow.md`, template, 3 agent profiles | modify/create | **high** — governance | lead · `rule_validator` ruleset | ✅ `2821953` |
| C0.2 | `config/artifact_registry.json` + 3 consumers | create/modify | high | lead · `rule_validator` ruleset | ✅ `92f42da` |
| C0.3 | `scripts/_root.py` + 6 consumers | create/modify | high | lead · `devops_agent` ruleset | ✅ `359d03c` + `fix` |
| C1 | `scripts/check_readme_counts.py` | modify | high | lead · `devops_agent` ruleset | ✅ `b2d7c2e` |
| C2 | `scripts/session_probe.py` | modify | high — a security report | lead · `devops_agent` ruleset | ✅ `26367cf` + `ca29010` + `509f525`, gate-approved |
| C3 | `env_shielding_auditor.py`, `hooks/on_commit.py` | modify | **high** — secrets | lead · `devops_agent` ruleset | ✅ `aa83309`…`5bcbdf6`, gate-approved |
| C3.2 | `hooks/on_commit.py` (`ALLOW_MARKER`), `rules/qa_and_testing.md` | create | **high** — a documented bypass of a secret gate | lead · `devops_agent` ruleset | ✅ `50094c1` + `R5` fixes |
| C4 | `mass_standardizer.py`, `tests/`, skill `README.md` + `SKILL.md` | modify/create | medium — **raised to high on execution** | lead · `skill_architect` ruleset | ✅ `5056796`, gate-approved |
| C4.2 | `rules/django_backend_standard.md`, skill `SKILL.md` | create/modify | medium | lead · `rule_validator` ruleset | ✅ `955eb5d`, gate-approved |
| C5 | `agents/devops_agent.md`, `agents.md` §6 role table | modify | medium — role map | lead · `agent_orchestrator` ruleset | ✅ `aa2b11d` + `R1` — both gates APPROVED |
| C6 | `agents.md` §0, `start_workflow.md` (3 rows), `audit_workflow.md` (`federation_audit`), `docs/plans/README.md` (routing discharged), `tests/test_installer.sh` (+1 assertion), `.claude/commands/agents/` (untracked, regenerable) | modify | medium | lead · `rule_validator` ruleset | ✅ `R2` — both gates APPROVED |
| C7 | `requirements-freeze.txt` | modify | low | lead · `devops_agent` ruleset | ⏳ |
| C8 | `origin/contrib/host-findings` | modify | low | lead · `doc_orchestrator` ruleset | ⏳ |
| C10 | `scripts/ci_gate.py` (new), `deployment_workflow.md:17` | create/modify | **high** — a gate | lead · `devops_agent` ruleset | ⏳ |

---

## Dependencies

**None.** Every unit uses the standard library. `C9`'s retry uses `time.sleep`; `C10`'s
gate will shell out to `gh`, which is already a declared prerequisite of
`deployment_workflow.md` rather than a new dependency.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `branch_sovereignty audit` tri-state (`C9`) | deterministic — script | `close_workflow.md` Phase 5.5 |
| `IMPLEMENTATION_PLAN.md` phase-artifact check (`C0`) | deterministic — existing `docs_freshness_check.py`, one map entry | `Makefile docs-freshness-check` target |
| Phase 5 plan precondition (`C0`) | **attended human step, deliberately** | `pipeline_workflow.md` Phase 5 |
| `scripts/ci_gate.py` (`C10`) | deterministic — script | `deployment_workflow.md` Phase 1 |
| `# secret-scan: allow <reason>` marker (`C3.2`) | deterministic — script, and **a declared human waiver by design** | `hooks/on_commit.py audit_secret_shielding` |

`C0` adds no script, so it introduces no new invoker to declare.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `C9`: a simulated 503 yields `UNKNOWN`, not `False` | **Yes** — this is the defect |
| `C9`: a branch with a merged PR + 503 reports **indeterminate**, not unintegrated | **Yes** |
| `C9`: the indeterminate message does **not** offer `abandoned_branches.json` | **Yes** |
| `C9`: no remote → definitive `NO`, not `UNKNOWN` | **Yes** — a naive tri-state would block every local-only repository forever |
| `C9`: merged PR + healthy network → integrated, exit 0 | **No** — regression to protect |
| `C0`: the freshness gate names the missing plan **and its phase** | **Yes** — measured before the fix, then after |
| `C0`: a sprint directory holding the plan produces no warning | **No** — regression to protect |
| `C0`: a sprint with no directory still yields the Phase 3 warning, not a plan warning | **No** — regression to protect |

`check_phase_artifacts` had **no test at all** before this sprint, despite being the
mechanism `C0` extends.

---

## Verification

Exit codes read with `$?` directly, **never through a pipe** — the mistake made twice in
this sprint's own session, which reported a green verdict taken from `tail` rather than
from the command being measured.

| Command | Expected |
| :--- | :--- |
| `make verify` | exit 0; the full suite green |
| `make docs-freshness-check` before `C0`'s plan file exists | warns, naming `IMPLEMENTATION_PLAN.md` and Phase 1 |
| `make docs-freshness-check` after | back to baseline (only the unrelated `code_containers` advisory) |
| `python3 scripts/branch_sovereignty.py audit` ×5 | same verdict five times |
| `python3 scripts/map_workflows.py --check` | exit 0 after regenerating the step-map guide |

---

### `C3.2`, added mid-sprint — why a unit was added rather than the heuristic tuned again

`C3` was rejected four consecutive times by the Tester gate, firing
`workflows/remediation_workflow.md` Phase 0. Three of those rejections were the
same logic block: a value-side test deciding whether a matched value is a
credential or a pointer at one. Each fix narrowed the previous one and each was
wrong in a **new** direction — exempting every URL dropped real credentials,
exempting nothing blocked real pointers, exempting absolute paths blocked
relative ones.

The conclusion, reached by the gate and ratified by the human at the halt:
**value shape cannot separate a pointer from a credential**, because the same
string is either one depending on what reads it. Every production secret
scanner ships an allowlist or baseline for that reason. `C3.2` gives this gate
the affordance it never had, and `_points_at_a_file` is then allowed to be
deliberately imperfect instead of being narrowed a fourth time.

**The reason is mandatory and every waiver is printed at commit time.** A silent
bypass is how `RA-09 SECRET_SOVEREIGNTY` would be defeated by the control built
to enforce it; a declared one is an audit trail. The abort criterion for `C3.2`
is that a marker with no reason must not suppress anything, which is pinned by
test.

### `C5`'s tier re-evaluation — the step the roadmap assigned, and its verdict

`docs/roadmaps/core/pipeline/021-030-program-queue.md:498-503` reads: *"assign `haiku`
now, and have 023 re-evaluate that specific tier when closing `C5` — **recorded in 023's
plan as a step, not an option**."* It was recorded in no row of this plan until the QA gate
found the omission at `R1`. Filed here, with the verdict rather than only the step, because
a step whose outcome is not written is the same loss over again.

**Verdict: `devops_agent` keeps `tier: mechanical` / `model: haiku`.** The basis, not the
adjective:

| Question | Answer |
| :--- | :--- |
| Does the grant make this profile an *author* of `scripts/` and `hooks/`? | **No.** It makes it the accountable **owner**. `F-021-A2` is declared and not resolved, so no implementer role exists and authoring still falls to the lead session |
| Then does the roadmap's premise hold? | **Not yet.** *"A profile moving from verifying to authoring deployment artifacts"* presupposes the profile authors. It does not, and this sprint's own units are the evidence: every one was written by the lead session |
| Is the declared tier what actually ran? | **No, and that is already recorded** (`task_scope.md`, session #3 findings): in a session that cannot dispatch subagents, every unit runs on the session model regardless of its assignee's tier. `check_model_tiers.py` proves coherence between two declarations, never what executed |

**The roadmap does not merely permit keeping `haiku` — it forbids the alternative.** Supplied
by the QA gate at `R1`, which read the paragraph to its end where this plan had stopped at its
middle. `021-030-program-queue.md:501-503` closes: *"Pre-assigning a high tier 'just in case'
would be the speculative generality `rules/code_craft.md §1` prohibits."* Moving `devops_agent`
to `author`/`sonnet` on the strength of a capability it does not yet exercise **is** that act.
The roadmap demanded a re-evaluation with a recorded outcome, not a tier change; leaving
`config/model_tiers.json` untouched obeys it, and changing it would have breached it.

**A second reason not to touch that file**: `config/model_tiers.json` is `token_economy_agent`'s
declared `tier_ownership` (`agents/token_economy_agent.md:20`) and sits outside `C5`'s declared
scope. Editing it would have re-opened the QA gate's own finding #3.

**The trigger for re-asking, written down so it is not lost with this context**: the moment
`F-021-A2` is resolved and a profile actually *authors* under the framework-root `scripts/`
or `hooks/` trees, this tier MUST be re-evaluated **before the first dispatch**, because the
roadmap's premise becomes true at that instant. `config/model_tiers.json` records
`mechanical` as *"Deterministic, verifiable results. A wrong answer fails at the next
command"* — which describes an environment operator, not the author of a governance gate,
and `agents/devops_agent.md` says so in its own text.

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| The 7 "carried-over" findings (`G-03`, `REVDOC-G1`, `ADR-0006`, `ADR-0007`, `C5`, `#12`, `#13`) | Not reproduced. This sprint's own rule forbids acting on them |
| Splitting an implementer profile that can write code (`F-021-A2`) | A redesign of the role map. `C5` **declares** the void; it does not resolve it |
| Editing `skills/django-expert-3rd/skills/SKILL.md` | Vendored; `rules/skills_and_integrations.md §3` forbids it |
| Pruning `ai-sprint/024` and `ai-sprint/025` | Deferred until `C9` is merged, so the gate authorising the deletion is trustworthy first |
| Whether the nucleus installs its own `.claude/` bridge | Measured in `task_scope.md`: no `.claude/settings.json` exists here, so `plansDirectory` never applied to the nucleus. Routed to `C6` |

---

## Abort criterion

**`C9`**: if the tri-state gate reports `UNKNOWN` on a healthy repository with a working
remote, the change traded an intermittently wrong gate for a permanently closed one and is
reverted. Verified by the regression tests running against a temp repository with no remote.

**`C0`**: if the phase-artifact entry produces a warning on a sprint directory that does
contain the plan, the gate is worse than its absence and the entry is removed.

**Sprint-wide**: `rules/token_economy.md §3.1` hard bound at 15× per context cycle. On
reaching it the session **suspends** via `scripts/session_state.py suspend` with unfinished
work recorded in `task_scope.md`, rather than closing or pushing on. This already fired once
at cycle 7 (16.5×) — the first time since Sprint 021 built the bound.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal |
| **Date** | 2026-08-17 |
| **Plan commit at approval** | filed retroactively with `C0`; approval of the sprint scope was given per-unit in session |
| **Remaining locks** | Active Sprint ✅ `ai-sprint/023` · QA + Tester verdicts ⏳ · Human OK at close ⏳ |

*Phase 5 is a single attended human authorization and is never wrapped in an unattended
`/loop` (`rules/loop_governance.md`).*
