# 📝 Sprint Log: #024 — `close-machinery-verdicts`

**Session Tracker**: `25b16540-e1d3-4edb-98ee-c6ccba98ce12`
**Role Active**: Principal Agent (sequential — see `agent_assignment.md`)

---

## 🚦 Session Metadata

| Parameter | Value |
| :--- | :--- |
| **Active Layer** | `core` / `pipeline` |
| **Strategic Goal** | Make three close-machinery controls return the verdict they claim to return |
| **Intelligence State** | `CERTIFIED` — `make verify` green, 127 tests |
| **Start Time** | 2026-08-16T20:16:40Z |
| **Base** | `main` at `a3c6f5f`, tag `v4.4.0` |

---

## 🏁 Sprint Progression

- [x] **Objective 1**: the drift check stops reporting sealed work as drift
    - `[x]` Sealing tags derived by crossing `git tag` with ledger sections
    - `[x]` Five verdicts, exit code following the required action
    - `[x]` Orphaned baseline falls back to `merge-base` and says so
    - `[x]` 10 tests, including the anti-whitewash calibration
- [x] **Objective 2**: the close gate stops refusing the branch it is sealing
    - `[x]` `local_branches()` skips the checked-out branch
    - `[x]` 2 tests proving the exclusion is positional, not permanent
- [x] **Objective 3**: the protocol text describes a verdict, not a boolean
    - `[x]` `start_workflow.md` Phase 0.4, `close_workflow.md` Phase 5.5
    - `[x]` Generated step map regenerated in the same commit
- [x] **Objective 4**: the nucleus can version its own pipeline record
    - `[x]` `.gitignore` stops hiding contamination from `submodule_purity`
    - `[x]` This sprint directory, and `agents.md §5` amended to match
    - `[x]` Freshness gate reaches its checks for the first time here

---

## 🧠 Rule Amendments & Heuristic Harvest

| Friction Point | Resolution / Workaround | KI ID |
| :--- | :--- | :--- |
| The pipeline's opening command was blocked by a control that reported a false state on a clean tree | Verdicts instead of a boolean; exit code follows the required action. `ADR-0002` | `F-024-D1` |
| The baseline a close writes is orphaned by the deployment that follows it, and `cat-file -e` cannot see it | `merge-base` fallback, substitution stated in the output | `F-024-D2` |
| Phase 5.5 refused the seal for the branch Phase 6 says stays unmerged | Exclude the checked-out branch; positional, not permanent | `F-024-D3` |
| `.gitignore` hid host contamination from `submodule_purity`, the one check built to catch it | Exclusion removed; protection restated where `strict_rule` and `submodule_purity` already enforce it | `F-024-D4` |
| The `R` verdict was designed to exit `0` and would have whitewashed the Phase 018 scenario | **A Phase 019 test refuted the design.** `R` exits `2` | `F-024-D5` |
| `make docs-freshness-check` passed an empty `SPRINT_ID`, so the phase-artifact check returned immediately in every project | `SPRINT_ID` defaults to the anchor's `current_sprint.id` | `F-024-D6` |
| The anchor declared `current_sprint_id` at the root while the gate reads `current_sprint.last_audit_sprint` — the exact bug the script's own comment describes in a host | Anchor restructured; the structural-change check runs here for the first time | `F-024-D7` |

**Harvest for `agents.md`**: every one of the seven was found by *running* a
protocol, never by reading it. Four were controls that reported success because
of how they were invoked, not because of what they checked — the same class as
`F-093-N2`, and the reason `RA-16` exists.

---

## ⚓ Documentation Entry Point Seal

**Strategic Lock**: `CLOSED`
**Next Phase**: Sprint `021` (`cost-instrumentation`) — the session-cost meter,
the session-length bound, and the `SUSPENDED` anchor state that lets a sprint
survive a session boundary.

**Not yet integrated**: `ai-sprint/024` is unpushed. Merging is
`deployment_workflow.md`'s job (`RA-12`), and it holds the Tester signature and
the observed-green CI gate (`RA-13`).

*Certified under conventional commit standard: `fix(scope): message #024`*
