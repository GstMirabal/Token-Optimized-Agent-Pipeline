# 📝 Sprint Log: #021 — `cost-instrumentation`

**Session Tracker**: `25b16540-e1d3-4edb-98ee-c6ccba98ce12`
**Role Active**: Principal Agent (sequential — see `agent_assignment.md`)

---

## 🚦 Session Metadata

| Parameter | Value |
| :--- | :--- |
| **Active Layer** | `core` / `pipeline` |
| **Strategic Goal** | Build the instrument before the rule, then bound the session it measures |
| **Intelligence State** | `CERTIFIED` — `make verify` green, 151 tests |
| **Base** | `main` at `36dd96a` (`v4.5.0`) |

---

## 🏁 Sprint Progression

- [x] **Objective 0**: correct the measurement that ordered the queue
    - `[x]` Four context cycles measured; the monotonic claim refuted
    - `[x]` Four propagation sites corrected (`RA-14`), including the bound's own unit
- [x] **Objective 1**: the meter
    - `[x]` `session_cost.py`, segmenting by context cycle, discarding `<synthetic>`
    - `[x]` Reports tokens, never currency
    - `[x]` Live acceptance: reproduces 38.3x / 44.9x / 14.0x / 30.0x
- [x] **Objective 2**: the bound
    - `[x]` `token_economy.md §3.1` — soft 5x, hard 15x, per cycle
    - `[x]` `loop_governance.md` premise corrected: spend is read, not estimated
    - `[x]` `session_probe.py` reports the previous session's breaches
- [x] **Objective 3**: continuity across the cut the bound creates
    - `[x]` `SUSPENDED` state, `suspend` subcommand, `resume_pointer`, `session_count`
    - `[x]` The asymmetry declared in `close_workflow.md`, where it gets miswired
- [x] **Objective 4**: a plan cannot be lost
    - `[x]` `plansDirectory` in the bridge template, with its two roles distinguished

---

## 🧠 Rule Amendments & Heuristic Harvest

| Friction Point | Resolution | KI ID |
| :--- | :--- | :--- |
| The finding that ordered the whole queue was measured over an undeclared scope — the first 400 messages, entirely inside cycle 1 | Re-measured over 1,070. The session is a sawtooth; the conclusion survives and strengthens | `F-021-M0` |
| Compaction was assumed to control cost | **Measured: it does not.** Four resets, 423M spent anyway. Cost is the area under the sawtooth | `F-021-M1` |
| A bound against the session's first turn would stop firing after the first reset | The unit is the **cycle**. Four propagation sites corrected with it | `F-021-M2` |
| `loop_governance.md` justified its advisory budget with a premise the meter falsified | Corrected in place rather than left standing (`RA-14`) | `F-021-M3` |
| The roadmap announced modifying the collision guard for `SUSPENDED` | **Unnecessary**: `claim()` blocks only on `IN_PROGRESS`, so the resume already passed. What was missing was writing the state and leaving a trace | `F-021-M4` |
| `M5` appeared in the sprint's work table and **in no commit** | Found while closing. Split into its own commit rather than folded into the ledger (`RA-08`) | `F-021-M5` |
| `plansDirectory` was about to be written from memory | Verified against Claude Code's changelog first. Sixth instance of `J6` avoided rather than committed | `F-021-M6` |

**Harvest**: five of the seven were found by *measuring or verifying before writing*, not by review. `J6`'s mitigation — every measured claim carrying the command that reproduces it — is what made re-measuring possible at all.

---

## ⚓ Documentation Entry Point Seal

**Strategic Lock**: `CLOSED`
**Next Phase**: Sprint `022` (`model-tiering`) — now measurable, because the meter exists.

**Not yet integrated**: `ai-sprint/021` is unmerged. Integration is
`deployment_workflow.md`'s job (`RA-12`).

*Certified under conventional commit standard: `feat(scope): message #021`*
