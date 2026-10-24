---
description: "Emergency Rollback and Remediation Protocol (Keyword: remediation)"
version: 2.0.0
invoked_by: human:/agents:remediation, rules/qa_and_testing.md#4-the-double-gate-review-protocol, workflows/pipeline_workflow.md
---

# 🛡️ Workflow: Remediation (Rollback & Recovery)

A critical emergency protocol designed to intercept infinite hallucination loops or Double-Gate stalemates. Its sole purpose is to nuke corrupted state, extract negative-heuristics natively, and return the system to safety.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Trigger** | `auto_invocation`| Triggered automatically if QA or Tester emit `REJECTED` on the exact same logic block **>3 consecutive times**. `RECORD` does not increment that count (`rules/qa_and_testing.md` §4). |
| **1. Deadlock Term**| `reversibility` | **Before any destruction**: snapshot the corrupted state with `git stash push -u -m "remediation-[date]"` (captures untracked files too). Forensics may need what the nuke erases; without the snapshot, `state_nuke` is PROHIBITED — same Reversibility Gate doctrine as Legacy Absorption. |
| **1. Deadlock Term**| `state_nuke` | Immediate execution halt. Workspace is forcibly sanitized (`git restore . && git clean -fd`) to Pre-Sprint pristine status. (Git-ignored files — `memory/`, `venv_skillopt/`, graph output — survive: no `-x` flag, by design.) |
| **2. Extraction** | `error_mining` | Find the failure origin (e.g. circular import, syntax mismatch) in two records that survive Phase 1. (1) The `REJECTED` rows of the looping logic block in `SPRINT_LOG.md` at the `current_sprint.path` of `docs/active_state.json` (`docs/sprints/[Sprint_ID]-[Stack]-[Layer]/SPRINT_LOG.md`): read their Notes and Severity cells. (2) The Phase 1 snapshot: locate the `remediation-[date]` entry with `git stash list`, then inspect it with `git stash show -p <entry>`. Done when the origin is written as one sentence naming the file and the cause. |
| **2. Extraction** | `family_check` | When the `REJECTED` rows read in `error_mining` show the second occurrence of the same S0, S1 or S2 family (`rules/qa_and_testing.md` §4, convergence rule 3), the mandatory fix is a deterministic check: a test or script that fails on every instance of the family it states it covers. The remediation replaces the existing enumeration with reviewed-copy equality, or narrows the claim; it does not add the new vector to the enumeration (`agents.md` §1 `fail_closed_claims`). Done when the check exists and fails on each recorded instance of the family. |
| **2. Extraction** | `negative_ki` | Inject logic tag into `agents.md` via `Governance Learner` banning the failed pattern. No memory logs are kept. |
| **3. Rollback** | `roadmap_tag` | Run `python3 scripts/session_state.py block --reason TERMINAL_REMEDIATION_LOOP`, which writes `current_sprint.status = BLOCKED` and `current_sprint.blocked_reason` to `docs/active_state.json`. Done when the command exits `0`; exit `2` writes nothing (the sprint is sealed or the anchor has no `current_sprint`); report that exit to the human instead of editing the anchor. |
| **3. Rollback** | `session_lock` | Tell the human user the sprint is deadlocked, then exit and enforce **SESSION LOCKED**. The block is lifted only by `python3 scripts/session_state.py unblock`, run after the human decides how to resume; never by hand-editing the anchor (`agents.md` §5 `state_homologation`). |

---
*Optimized for Pipeline Failsafe Constraints & Tabular Density (v2.0.0).*
