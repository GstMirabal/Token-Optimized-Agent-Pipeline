# 📜 ADR-0018: In-session token economy
**Status**: `Accepted`
**Date**: 2026-11-09
**Triggers**: 2 (`rules/documentation_standard.md §3.1`): the HARD threshold is a value that `session_cost.py` exposes and the Phase 6 workflow step consumes.

---

## 1. Context

The in-session meter compares the context size of the current cycle against the context size of its first turn (decision D1 of `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`). Two relative bounds were planned: soft at 5x and hard at 15x. `KI-059-9` asked whether 15x still holds once the baseline is context size (D1, D19). `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` section 5 holds the data and section 8 holds the debate; the decisions were taken by the human GstMirabal on 2026-11-09, session `593ffb72`.

| Fact (study section) | Value |
| :--- | :--- |
| Closed sessions measured (5) | 27, all from one repository |
| Largest context observed (5) | 550,187 tokens, which is 9.08x the median baseline of 60,612 |
| 15x of the median baseline (5) | 909,180, which is 1.65 times the largest observed context |
| Sessions above 5x against their own first turn (5) | 7 of 27 |
| Sessions above 15x against their own first turn (5) | 0 of 27 |
| Origin of the 958K figure in `KI-059-9` (5) | 15 x 63,883, the first turn of `7204cadc` |
| Rule C medians for `fresh` (7) | 4,613 (low risk) against 54,797 (high risk) |
| Spread inside low-risk `fresh` (7, 8.2) | 676 to 365,769 |
| Subagents (7, 8.2) | 5m cache TTL against 1h for main; 7.9% cold-cache turns against 1 of 2,726 in main |
| `agents:*` command files (8.3) | 13 files, 3,835 bytes in total |

## 2. Decision

| # | Subject | Decision | Objection recorded (study section 8) |
| :--- | :--- | :--- | :--- |
| 1 | Hard bound | The relative 15x bound is replaced by an absolute trigger of **550,000 tokens of context size**. Basis: the largest context observed in 27 closed sessions is 550,187, and only that session would have reached 550,000 | The value is chosen from 27 sessions of one repository and cannot be validated (8.1) |
| 2 | Soft bound | Stays relative at **5x the first-turn context**, advisory | None recorded |
| 3a | Method adopted | The per-unit budget with planned suspend points (D14), estimated on `fresh` tokens (`input + output + cache_creation`) instead of the four-field total (`input + output + cache_creation + cache_read`) | The spread inside each group is wide, and the four-field total depends on context size at execution time (8.2, method 1) |
| 3b | Method adopted | Cut the boot baseline | A smaller baseline raises the ratio for the same growth, so the 5x trigger fires sooner (8.2, method 4) |
| 4a | Not adopted | Subagent delegation as a cost method | 5m cache TTL and 7.9% cold-cache turns; the measured figures do not show a saving (8.2, method 3) |
| 4b | Not adopted | Opt-in installation of the `agents:*` commands; `scripts/install.py` keeps installing all of them for every host | Reinstalling reverts any deletion of a command (study section 3.1), and 3,835 bytes give no appreciable saving (8.3) |

Method 2 of study section 7 (lower the hard bound, or add an absolute-token trigger) is not a separate method; decision 1 covers it (8.2).

### 2.1 Effect on plan decisions D2 and D3

| Plan decision | Text it carries | Effect of this ADR |
| :--- | :--- | :--- |
| D2 | The in-session meter is a workflow step in Phase 6; provisional: this ADR may replace it with the method from the debate (D8); if the debate does not close, D2 is implemented as written | **Confirmed.** The debate closed. The methods it adopted (3a, 3b) are a per-unit budget and a baseline cut; neither places the meter anywhere else. D14 states that the in-session measurement stays, to check the estimate. The meter remains a Phase 6 workflow step |
| D3 | At hard (15x) the meter only warns (exit 0) while calibration is n=1 | **Trigger replaced, exit code unchanged.** The hard condition is no longer "15x the baseline" but "context size reaches 550,000 tokens" (decision 1). The exit 0 of the human decision of 2026-11-02 stays: nothing lifted it, and calibration stays at one repository |
| D3 (SOFT) | Not stated in D3; the soft bound is 5x in D14 | Unchanged: 5x the first-turn context, advisory (decision 2) |

## 3. Consequences

| Effect | Detail |
| :--- | :--- |
| Easier | The hard trigger no longer moves when the `agents.md` trim lowers the first-turn context, because it is absolute (reason recorded in study 8.1) |
| Easier | The per-unit budget on `fresh` tokens avoids the dependence of the four-field total on context size at execution time |
| Harder | Soft stays relative, so the `agents.md` trim, which lowers the first-turn context, makes the same growth reach 5x sooner (`KI-059-9`) |
| Harder | 550,000 is a single-repository figure: 27 sessions, one of which exceeds it. No other repository has been used to validate it |
| Edits that this decision makes necessary | `scripts/session_cost.py` (plan row A-02), `scripts/session_probe.py` (plan row A-55) and `rules/token_economy.md` (plan row A-03) carry the 550,000 trigger and the `fresh` estimate instead of 15x and the four-field total; the plan rows name the form as "the form that ADR-0018 fixes" |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0018-in-session-token-economy.md`.*
