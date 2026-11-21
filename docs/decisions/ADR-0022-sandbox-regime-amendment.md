# 📜 ADR-0022: Sandbox regime amendment (A5, B7, D6)
**Status**: `Accepted`
**Date**: 2026-11-15
**Sprint**: 059
**Owner**: `principal_agent`
**Writer**: `doc_orchestrator`
**Amends**: `ADR-0019` (`docs/decisions/ADR-0019-sandbox-regime.md`) on three items only: section 2.3 row A5, section 2.3 row B7, and decision D6. ADR-0019 stays `Accepted` and is not edited; every part of it not named here is unchanged.
**Triggers**: 2, 3 (`rules/documentation_standard.md §3.1`): the A5 and B7 rules are part of the settings contract that hosts install from the nucleus (trigger 2), and all three items set filesystem, permission and credential controls, which are a security boundary (trigger 3). Trigger 3 alone requires the full MADR format of sections 4 and 5.

---

## 1. Context

| Item | Fact | Source |
| :--- | :--- | :--- |
| A5 | ADR-0019 section 2.3 row A5 was open: the replacement for `Edit(~/**)`, which blocks project edits because the project is under `HOME` (A5-1), was not decided | ADR-0019 section 2.3, A5-1, F-10 |
| A5 | Unit P-02 measured candidate sets C1 to C4 and the human chose C1 | `HARNESS_MEASUREMENT.md` (HM) section A5, sub-heading "A5 candidate rules naming HOME paths (unit P-02)", commit `e51109f`; `SPRINT_LOG.md` 2026-11-15 |
| B7 | ADR-0019 section 2.3 row B7 requires "no auto mode for agents" without naming the key; unit P-01 found it | HM sub-heading "B7 key that disables auto mode (unit P-01)", commit `35ba2db` |
| D6 | ADR-0019 D6 recorded the GitHub App broker as a target with no sprint; plan D54 had set it aside and plan D55 reversed that | `IMPLEMENTATION_PLAN.md` D54, D55; `SPRINT_LOG.md` 2026-11-15 |
| Immutability | An `Accepted` ADR is not edited in place; the in-place edit drafted by P-03 was discarded without a commit | `rules/documentation_standard.md §3`, plan D56 |

## 2. Decision

Human decisions of 2026-11-15, recorded in `SPRINT_LOG.md`.

### 2.1 Amended items

| Item | Amends | Decision | Evidence | Limits |
| :--- | :--- | :--- | :--- | :--- |
| A5 | ADR-0019 section 2.3 row A5 (open) | The replacement for `Edit(~/**)` is set C1 of HM section A5: `Edit(~/.ssh/**)`, `Edit(~/.aws/**)`, `Edit(~/.gnupg/**)`, `Edit(~/.config/gh/**)`, `Edit(~/.docker/**)`, `Edit(~/Library/LaunchAgents/**)`, `Edit(~/Library/Keychains/**)`. Sets C2 (`Edit(~/.zshrc)` and the other seven home files of HM) and C3 (`Edit(~/.claude/settings.json)`) are not adopted, so no A5 rule denies their paths. C4 (`Edit(~/.claude/**)`) stays rejected because it denies `~/.claude/projects/` (HM) | A5-1, F-10; A5-11 to A5-14, A5-17, A5-18 with control A5-20: the directory pattern denies Edit and Write inside the directory, in new subdirectories, and at the exact directory path when it is absent, and project edits under HOME stay allowed | Measured on CLI `2.1.119` only, not `2.1.322`. Rule-based denials do not appear in `permission_denials` (A5-9, A5-12, A5-13, A5-16, A5-17, A5-18), so a check that reads only that field misses them. No path under the project root may be named by any rule (A5-1) |
| B7 | ADR-0019 section 2.3 row B7 (key not named) | The key that disables auto mode is `permissions.disableAutoMode` with the string `"disable"`. The rest of the B7 row (`allowUnsandboxedCommands: false`) is unchanged | Source: 2.1.322 code reads `e.permissions?.disableAutoMode==="disable"\|\|e.disableAutoMode==="disable"`; a top-level `disableAutoMode` is also read; only the string `"disable"` is checked. B7-5 (2.1.322, project `.claude/settings.json` with the key): requested auto mode starts as `default`, silently. B7-6 (control `{}`): stays `auto` | Exit codes were not captured. User and managed levels were not run. An interactive VS Code session was not run. 2.1.119 was only read, not run. Precedence between levels and override by `--settings` or the flag were not tested. The `defaultMode: "auto"` path was read, not run |
| D6 | ADR-0019 D6 (broker as a target with no sprint) | The GitHub App broker target is kept and decided for Sprint 060 (plan D55 of Sprint 059). In that design the agent creates the version tag through the broker and the same helper signs the tag with a key the agent does not read. Units R-09 to R-11 move to Sprint 060 | The A10 token facts of ADR-0019 (expiry `2026-12-14`, scopes A10-2 and A10-3) are unchanged; ADR-0019 acceptance criteria stay: key store unreadable from the sandbox (F-05), broker socket authenticates its caller (F-17) | Not measured: no broker or key store exists yet |

## 3. Consequences

| Consequence | Evidence or owner |
| :--- | :--- |
| Unit R-01 adds the B7 key and the seven C1 rules to `claude/settings.hooks.json`; the ADR-0019 text it cited for them is replaced by section 2.1 | `task_scope.md` row R-01 |
| The boundary claim of ADR-0019 section 2.1 is not amended here; unit V-02 records the result of V-01 in a separate ADR-0023 | Plan D57, `task_scope.md` row V-02 |
| `Edit(~/**)` stays unusable as protection (A5-1); `HOME` paths outside C1 (shell rc files, `~/.gitconfig`, `~/.npmrc`, `~/.netrc`, `~/.claude/settings.json`) have no A5 deny, which is a negative consequence of not adopting C2 and C3 | HM A5 candidate table |
| The A5 rules are measured on `2.1.119` only and the harness of the parent session runs `2.1.322`; a denial may be missed if a check reads only `permission_denials` | HM A5 Reading |
| B7 is measured at project level on `2.1.322` only; a user or managed level is not shown to behave the same | HM B7 Limits |
| The human renews the A10 token every 30 days until the Sprint 060 broker exists; unit T-01 keeps access if the broker is absent on `2026-12-14` | ADR-0019 D6, plan D55 |
| Units R-09 to R-11 depend on the helper key and are not done in Sprint 059 | Plan D55 |

## 4. Deciders

| Role | Who | Part |
| :--- | :--- | :--- |
| Human | The repository owner | A5 set C1 (unit P-02), B7 key (unit P-01), D6 target for Sprint 060 (plan D55); the choice to amend through this ADR (plan D56); all on 2026-11-15 |
| `principal_agent` | Owner | Plan D55, D56; unit P-03 |
| `doc_orchestrator` | Writer | This document |

## 5. Considered Options

| Item | Option | Pros | Cons |
| :--- | :--- | :--- | :--- |
| Form | **New ADR amending ADR-0019 (chosen)** | Respects the immutability rule; ADR-0019 history stays intact | Readers follow two documents |
| Form | Edit ADR-0019 in place | One document | Forbidden for an `Accepted` ADR (`rules/documentation_standard.md §3`); discarded by plan D56 |
| Form | Supersede ADR-0019 | Single current record | Restates the unchanged decisions of ADR-0019; only three items change |
| A5 | **C1 directory rules (chosen)** | Isolated with positive controls; blocks no framework work found by configuration reading | Leaves shell rc files and `~/.claude/settings.json` without an A5 rule |
| A5 | C1 with C2 and C3 | Covers more `HOME` paths | Not chosen by the human |
| A5 | C4 `Edit(~/.claude/**)` | Covers the harness directory | Denies `~/.claude/projects/` (agent memory) |
| D6 | **GitHub App broker for Sprint 060 (chosen)** | Short-lived installation tokens; helper signs the version tag with a key the agent does not read | Broker and key store do not exist yet |
| D6 | Keep the A10 token only (plan D54 reading) | No new component | Reversed by the human on 2026-11-15 (plan D55) |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`).*
