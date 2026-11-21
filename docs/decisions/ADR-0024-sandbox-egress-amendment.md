# 📜 ADR-0024: Sandbox egress amendment (egress, loopback, D8, unit D8, user and managed scope)
**Status**: `Accepted`
**Date**: 2026-11-18
**Sprint**: 059
**Owner**: `principal_agent`
**Writer**: `doc_orchestrator`
**Amends**: `ADR-0019` (`docs/decisions/ADR-0019-sandbox-regime.md`) on five items only: the section 1.3 row Egress that begins "With `network.allowedDomains` set", section 1.3 row Loopback, decision D8 (network list part), the section 3.1 row "New unit: D8", and the two statements that `allowedDomains` at user and managed level is unmeasured (section 1.5 row "User and managed settings", and the section 3.3 row listing `allowUnixSockets`, `allowedDomains` at user and managed level, M13-M15 and trustd). ADR-0019 stays `Accepted` and is not edited; every part of it not named here is unchanged.
**Triggers**: 2, 3 (`rules/documentation_standard.md §3.1`): the network keys are part of the settings contract that hosts install from the nucleus (trigger 2), and the egress control is a security boundary (trigger 3). Trigger 3 alone requires the full MADR format of sections 4 and 5.

---

## 1. Context

Abbreviations: HM = `docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` section B9; plan = `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`.

### 1.1 What ADR-0019 states

| Item | Quoted text of ADR-0019 | Line |
| :--- | :--- | :--- |
| Egress row (section 1.3) | "With `network.allowedDomains` set to the two GitHub hosts, other hosts are denied and `api.github.com` answers (`200`), on `2.1.322` and `2.1.119`, at project level and through `--settings`" (evidence A1-1, A1-2, A1-4, A1-5) | 40 |
| Loopback row (section 1.3) | "... with the list set, the tunnel is denied in the measured configurations" (evidence M7, F-02, `KI-059-20`, A1-1, A1-2, A1-4, A1-5) | 42 |
| D8 | "`sandbox.network.allowedDomains: [\"api.github.com\",\"github.com\"]` set explicitly; key absence depends on session mode (A1-6, F-01), so the key is never left absent. Any other domain only after it is measured." | 94 |
| New unit: D8 | "Sets `sandbox.network.allowedDomains` and `sandbox.filesystem.denyRead` in `.claude/settings.json` and the host template `claude/settings.hooks.json`"; done-criterion "A1-1 and B2 re-run by `make sandbox-probe` report closed" | 136 |
| Limits row "User and managed settings" (section 1.5) | "`allowedDomains` and `allowUnixSockets` at user and managed level are unmeasured" | 71 |
| Consequences row (section 3.3) | "`allowUnixSockets`, `allowedDomains` at user and managed level, M13-M15 on `2.1.322`, and the Mach service of trustd are unmeasured" | 161 |

### 1.2 What the measurements of Sprint 059 show

| Id | Commit | Fact | Source |
| :--- | :--- | :--- | :--- |
| P-11 | `d885bac` | `sandbox.network.allowedDomains` at project scope is an allowlist that skips the prompt, not a denylist. For an unlisted host (`example.org`) the sandbox proxy asks for approval: in `default` the harness showed the prompt and the human denied it, ending as `000`, curl exit `28` (CLI `2.1.119`); in `auto` the proxy answered `HTTP/1.1 200 Connection Established` with no prompt (VS Code, agent session, user-scope `permissions.defaultMode: "auto"`) | HM P-11 table and Reading; plan D65, D66 |
| P-10 | recorded with P-11 | With the project list only: `make sandbox-probe` in `default` gave A1-1 and A1-2 `not-measurable [proxy-timeout]`; in `auto` it gave A1-1 and A1-2 `expected=closed observed=open [200]`. The `200` of the `default` `curl` to `webhook.site` was an approved prompt (P-11 correction) | HM P-10 table and Correction |
| P-12 | `55e3d2d` | After R-18, with `sandbox.network.strictAllowlist: true` at user scope and the project `allowedDomains` unchanged, the proxy refused unlisted hosts without a prompt and without auto-approval: A1-C `closed [403]`, `curl https://example.org` `000` exit `56`, in terminal CLI `2.1.311` (`default` and `auto`) and VS Code `2.1.325` (Manual and inferred auto). It also refused `api.github.com`, which the project list names (`<sandbox_violations>`: `host is not on the allow list`), so the project-scope `allowedDomains` was not honored in those sessions; the A1 cases stayed `not-measurable [control-not-open]`, exit `2` | HM P-12 table and Reading |
| R-18 | `50a09bb` | The human upgraded the CLI to `2.1.311` and set `sandbox.network.strictAllowlist: true` in `~/.claude/settings.json` | plan row R-18 |
| R-21 | `bfbbbec` | The human added `sandbox.network.allowedDomains` = `api.github.com`, `github.com`, `pypi.org`, `files.pythonhosted.org` to `~/.claude/settings.json` next to `strictAllowlist` | plan row R-21 |
| P-13 | `4339f38`, `094c822` | With both keys at user scope: A1-C `api.github.com:443` `open [200]`, A1-1 `127.0.0.1:5000` `closed [403]`, A1-2 `example.org:443` `closed [403]`, `make sandbox-probe` `ok=15` exit `0`, `curl https://example.org` `000` exit `56`, `curl https://api.github.com` `200` exit `0`; no network prompt. Measured on VS Code `2.1.325` in auto (inferred) and on terminal CLI `2.1.311` in `default`; VS Code `default` and CLI `auto` were not re-run | HM P-13 table and Reading |
| R-04 | `d5eec41` | `tests/test_sandbox_probe.py` pins the `403` refusal form with the control open as `closed`, and the P-12 form as `not-measurable` | plan row R-04 |

### 1.3 Scope of the evidence

| Statement | Status |
| :--- | :--- |
| `strictAllowlist` is honored only at user, managed or `--settings` scope, has no effect in a repository `.claude/settings.json` or `.claude/settings.local.json`, and exists from v2.1.219 | Taken from the Claude Code documentation read by plan D66 (settings reference, `sandbox-network-strictallowlist`), not from a measurement. HM measured the key at user scope only |
| `strictAllowlist` or `allowedDomains` at managed scope | Not measured; no managed-settings file exists on the measured host (HM P-09) |
| Loopback under `strictAllowlist` | Measured only as the probe case A1-1 (`127.0.0.1:5000`): `closed [403]` in P-13 on two surfaces. Not measured: the M7 route (`200 Connection Established` to loopback from the parent session) outside `make sandbox-probe`, any other loopback port, and `strictAllowlist` without the user-scope `allowedDomains` as a loopback control (in P-12 the A1-1 case was `not-measurable` because the control was refused) |
| Loopback under the project list only | Not shown denied: P-10 `auto` measured A1-1 `open [200]` with the project list set |
| `--settings` scope at CLI `2.1.311` and `2.1.325` | Not measured in P-11 to P-13 (ADR-0019 A1-4 and A1-5 measured `--settings` on `2.1.322` and `2.1.119`, before `strictAllowlist` was set) |

## 2. Decision

Human decision of 2026-11-18 (plan D68, after R-04 `d5eec41`), on the evidence of section 1.

### 2.1 Decision text

Denial of egress to unlisted hosts requires `sandbox.network.strictAllowlist: true` together with `sandbox.network.allowedDomains`, both at user or managed scope. The project `.claude/settings.json` alone does not deny. `scripts/install.py` writes project settings only, so it cannot set either user-scope key; the human of each host sets them (the nucleus did it in R-18 and R-21).

### 2.2 Amended items

| Item | Amends (ADR-0019 line) | New statement | Evidence | Limits |
| :--- | :--- | :--- | :--- | :--- |
| 1. Egress row | Section 1.3 row Egress, line 40 | `allowedDomains` at project scope does not deny other hosts. It skips the approval prompt; an unlisted host is prompted in `default` and approved silently in `auto`. The other hosts are denied (`403`, no prompt, both modes) only with `strictAllowlist: true` plus `allowedDomains` at user scope. The A1-1 to A1-5 results of ADR-0019 (denied hosts with the project list) are not re-measured here and are not reproduced in the parent sessions of P-10 and P-11 | P-11 (`d885bac`), P-10, P-12 (`55e3d2d`), P-13 (`4339f38`, `094c822`) | The `200` for `api.github.com` is unchanged where `allowedDomains` is the effective list; under `strictAllowlist` the project list is not honored (P-12) |
| 2. Loopback row | Section 1.3 row Loopback, line 42 | "With the list set, the tunnel is denied" holds for the project list only where nothing approves the connection: it did not hold in `auto` (P-10 A1-1 `open [200]`). With `strictAllowlist` and `allowedDomains` at user scope, the probe case A1-1 (`127.0.0.1:5000`) is `closed [403]` on VS Code `2.1.325` auto and CLI `2.1.311` default (P-13) | P-10, P-13 | Loopback under `strictAllowlist` is measured for case A1-1 only; the M7 route and other ports are not measured (section 1.3 of this ADR) |
| 3. D8 | Decision D8, line 94 (network list part only) | `sandbox.network.allowedDomains` in the project file stays set explicitly, and it is not the egress control. The egress control is `sandbox.network.strictAllowlist: true` plus `sandbox.network.allowedDomains` at user or managed scope (R-18, R-21). The list of the human's user file is `api.github.com`, `github.com`, `pypi.org`, `files.pythonhosted.org`. "Any other domain only after it is measured" stands. The `denyRead` part of D8 is unchanged | P-11, P-12, P-13, R-18 (`50a09bb`), R-21 (`bfbbbec`) | Managed scope not measured |
| 4. Row "New unit: D8" | Section 3.1 row "New unit: D8", line 136 | The unit sets the project keys only; it does not deny egress. Its done-criterion "A1-1 and B2 re-run by `make sandbox-probe` report closed" is met only on a host whose user or managed scope also holds `strictAllowlist: true` and `allowedDomains`: P-13 `ok=15`, exit `0`, on the nucleus host | P-13, R-04 (`d5eec41`) | On a host without the user-scope keys the probe reports A1-1 and A1-2 not `closed` (P-10) |
| 5. User and managed rows | Section 1.5 row "User and managed settings", line 71, and section 3.3 row, line 161: the `allowedDomains` part only | `allowedDomains` at user scope is measured (P-13) and, together with `strictAllowlist`, is the scope that denies. At managed scope it stays unmeasured. `allowUnixSockets` at user and managed level, M13-M15 on `2.1.322`, and the Mach service of trustd stay unmeasured as ADR-0019 states | P-13, HM P-09 (no managed file) | The user-scope result is on one host, two surfaces and two CLI versions (`2.1.311`, `2.1.325`) |

## 3. Consequences

| Consequence | Unit or owner | Evidence or done-criterion |
| :--- | :--- | :--- |
| `rules/project_topology.md` section 5 states that `allowedDomains` skips the prompt, that denying unlisted hosts requires `strictAllowlist: true` plus `allowedDomains` at user or managed scope, that `install.py` cannot set it, that under `strictAllowlist` the project list is not honored, and cites ADR-0024; no sentence says `allowedDomains` alone denies | R-20 (`task_scope.md` row R-20) | `grep -n "ADR-0024" rules/project_topology.md` finds the section |
| `registry.npmjs.org` for `pnpm` is measured with a control and the Node TLS setting; it is not on any list of the user file today (`pypi.org` and `files.pythonhosted.org` are) | P-07 (`task_scope.md` row P-07) | Result recorded in HM; until then no list entry exists for it (ADR-0019 D8 "any other domain only after it is measured") |
| Hosts that do not set the two user-scope keys have no egress denial; their `make sandbox-probe` reports A1-1 and A1-2 not `closed` | Human of each host, with the command R-20 documents | P-10 |
| The project `allowedDomains` has no denying effect under `strictAllowlist`; a host that sets only `strictAllowlist` blocks `github.com`, `api.github.com` and the package hosts (`git push`, `gh`, `pip` fail) | R-21 for the nucleus host; R-20 for hosts | P-12 |
| KI-059-27 (open egress to unlisted hosts in `auto`) is closed in the measured sessions by R-18 and R-21 | R-18, R-21, P-13 | P-13 `ok=15`, exit `0` |
| The pinned refusal forms of the probe remain the test of the measurement | R-04 (`d5eec41`) | `tests/test_sandbox_probe.py` |
| Not measured: VS Code `default` and CLI `auto` after R-21 (P-12 showed all four combinations alike before R-21), managed scope, `--settings` scope, the M7 loopback route under `strictAllowlist`, other ports | No unit | Listed as limits in section 2.2; this ADR assigns no future work to them |

## 4. Deciders

| Role | Who | Part |
| :--- | :--- | :--- |
| Human | The repository owner | The egress decision of section 2.1 (plan D68, 2026-11-18); R-18 and R-21 (the user-scope settings); the choice to amend through this ADR (plan D68) |
| `principal_agent` | Owner | Plan D66, D67, D68 |
| `doc_orchestrator` | Writer | This document |

## 5. Considered Options

| Item | Option | Pros | Cons |
| :--- | :--- | :--- | :--- |
| Form | **New ADR amending ADR-0019 (chosen)** | Respects the immutability rule; ADR-0019 history stays intact; same pattern as ADR-0022 | Readers follow two documents |
| Form | Edit ADR-0019 in place | One document | Forbidden for an `Accepted` ADR (`rules/documentation_standard.md §3`); the first dispatch's edit was discarded without a commit (plan D68) |
| Form | Supersede ADR-0019 | Single current record | Restates the unchanged decisions of ADR-0019; only five items change |
| Egress control | **`strictAllowlist: true` plus `allowedDomains` at user or managed scope (chosen)** | Refuses unlisted hosts with `403` and no prompt in `default` and `auto` (P-12, P-13); `make sandbox-probe` exits `0` | A human sets it per host; `install.py` cannot; managed scope not measured |
| Egress control | Project `allowedDomains` only | Installable by `install.py` | Does not deny: prompts in `default`, approves in `auto` (P-11) |
| Egress control | `strictAllowlist` at user scope without user-scope `allowedDomains` | One key | Refuses `api.github.com` too (P-12); `git push`, `gh`, `pip` blocked |
| Egress control | `strictAllowlist` in the project file or the host template | Installable | The documentation read in plan D66 says it has no effect there; not measured in the repository file |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`).*
