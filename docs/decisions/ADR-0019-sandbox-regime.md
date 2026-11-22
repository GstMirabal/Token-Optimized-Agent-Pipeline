# 📜 ADR-0019: Sandbox regime
**Status**: `Accepted`
**Date**: 2026-11-14
**Sprint**: 059
**Owner**: `principal_agent`
**Writer**: `doc_orchestrator`
**Triggers**: 2, 3 (`rules/documentation_standard.md §3.1`): the regime changes the settings contract that hosts install from the nucleus (trigger 2), and it sets credential, network, filesystem and permission controls, which are a security boundary (trigger 3). Trigger 3 alone requires the full MADR format of sections 4 and 5.

---

## 1. Context

### 1.1 Sources

Every figure below is checkable in one of these documents of `docs/sprints/059-core-pipeline/`. Measurement ids (`A1-1`, `B2`, `F-05`, `M9`) are the ids used in those documents.

| Short name | Document | Unit | Content |
| :--- | :--- | :--- | :--- |
| HM | `HARNESS_MEASUREMENT.md` | S-01 to S-12 | M1-M18, findings F-01 to F-23, sections A1-A10 and B1-B11 |
| SE | `SANDBOX_ENUMERATION.md` | C-01 (`e4f435d`), C-01b | Enumeration of out-of-sandbox entry points; section 2.6 (`gh` under the sandbox), section 6.9 (case `G`) |
| HAS | `HARNESS_ATTACK_SCOPE.md` | S-16 (`b803704`) | One row per control of A1-A10 and B1-B11: what it must withstand and which result counts as its failure |
| KI | `SPRINT_LOG.md` | - | `KI-059-19` to `KI-059-26` |

### 1.2 Conditions of measurement

| Item | Value | Source |
| :--- | :--- | :--- |
| Harness of the parent session | VS Code extension, CLI `2.1.322` | HM section 1 |
| Child sessions of M1-M18 | `claude -p`, CLI `2.1.119`, launched outside the parent sandbox | HM section 1 |
| Child sessions of A1-B2 | CLI `2.1.322` and, for A1 only, `2.1.119` | HM A1, A5, A6, B1, B2 |
| Enumeration of SE | CLI `2.1.319` for the parent sandbox, `2.1.119` for the drivers | SE section 1.1 |
| Measurement dates | 2026-11-09 (SE), 2026-11-12 (M1-M18), 2026-11-14 (review, A1-B11) | SE section 1.1, HM section 1 |
| Principle for proof | A control is shown by configuration reading or by rule semantics with a control case; an agent never runs an escape attempt (plan D51 point 3, D52) | `IMPLEMENTATION_PLAN.md` D51, D52 |

### 1.3 Facts the decisions rest on

| Area | Fact | Evidence |
| :--- | :--- | :--- |
| Egress | In the parent interactive auto-mode session with no `network` key, hosts outside any list answered a request from the sandbox (HTTP 200 for `webhook.site`, `pastebin.com`, `httpbin.org`) | M6 (refuted reading), F-01, `KI-059-19` |
| Egress | With `network.allowedDomains` set to the two GitHub hosts, other hosts are denied and `api.github.com` answers (`200`), on `2.1.322` and `2.1.119`, at project level and through `--settings` | A1-1, A1-2, A1-4, A1-5 |
| Egress | With the `network` key absent, a `claude -p` child denied every host; the open egress of the parent session therefore follows the session mode (inferred, mechanism not measured) | A1-3, A1-6 |
| Loopback | The sandbox proxy tunnelled to loopback in the parent session (`200 Connection Established`); direct loopback connects returned `EPERM`; with the list set, the tunnel is denied in the measured configurations | M7, F-02, `KI-059-20`, A1-1, A1-2, A1-4, A1-5 |
| Credentials | The `gho_` token (scopes `gist`, `read:org`, `repo`, `user`, `workflow`, no expiry), the keychain service entry for the GitHub host and the git credential helper were reachable from the Bash sandbox; no value was recorded | M5, F-05, F-06, B11-5, `KI-059-21` |
| Credentials | `sandbox.filesystem.denyRead` on an absolute path blocks Bash reads of it; a directory entry covers the files under it; the keychain service is not covered by a file rule | A6-1, A6-2, B2 Reading |
| `gh` | Under the sandbox with no `excludedCommands` entry (count `0`), CLI `2.1.319`, `gh` 2.96.0: three network-bound commands exit `1` with `tls: failed to verify certificate: x509: OSStatus -26276` | SE section 2.6 |
| `gh` | `gh` works only with `sandbox.enableWeakerNetworkIsolation: true` (case `G`); the Mach service `com.apple.trustd.agent` was not probed; M2 holds for `2.1.119` and was not measured on `2.1.322`; A6-b treats the key as a sandbox-widening key | SE section 6.9, M2, HAS row A6-b |
| Tool reach | In auto mode, `WebFetch` ran with no approval prompt; the tools of B1-2 and two connected connectors are in the agent's tool list; a `permissions.deny` entry removes a tool or a whole connector | B1-1, B1-2, B1-3, B1-4, B1-5, B1-6, B1-7, `KI-059-25` |
| Write reach | Hook code (`hooks/`, `scripts/`), `agents/*.md`, `Makefile`, `venv_skillopt/` are writable from the nucleus Bash sandbox; `.git/hooks`, `.vscode/` and, for Bash, `.claude/settings*.json` are denied | A7-3, A3-3, B3, B5-1, A9-3, `KI-059-23` |
| Settings write | No rule stops the Edit tool from writing `.claude/settings*.json`; a rule `Edit(/.claude/settings*.json)` blocks it in a fixture and leaves other edits working; `Edit(~/**)` denied a project file because the project is under `HOME` | A9-1, A9-2, A9-4, A9-5, A5-1, F-10 |
| `.env` reads | `Read(/**/.env*)` denies root, nested and example `.env` files and removes them from Grep results; an out-of-project `.env` was readable by Bash and by the Read tool | A5-2, A5-3, A5-4, A5-5, A5-6, B4-9, B4-10 |
| Hooks | A hook-wrapper prototype failed open (exit `71`, `65`); its profile left gaps (`.git` rename, Mach services, DNS); no wrapper exists | F-03, F-07, F-08, F-09, M11, M12, A4 |
| Hooks | A `PreToolUse` allow hook approved a Bash call with `dangerouslyDisableSandbox` and a Write to `HOME` on `2.1.119`; not re-run on `2.1.322` | M13, M14, M15, HAS row A2-e |
| Database tests | The Docker API is refused from the Bash sandbox; a throwaway container with network mode `none`, no published port and a role without `rolsuper` and without `pg_execute_server_program` was configured; a Unix socket on a bind mount fails on Docker Desktop; a bridge to the development database reached it | A8-1, A8-2, A8-3, M8, M9, M10 |
| GitHub | The fine-grained token of A10 (Contents and Pull requests write, no Administration, no Workflows) expires `2026-12-14` and read `403` on the protection of `main`; `main` has a pull request required with `required_approving_review_count: 0`; `enforce_admins` was `false` at A10-4 and enabled at B11-6; tag ruleset `version-tags` lets the Admin role bypass always | A10-1, A10-2, A10-4, B11-4, B11-6, `KI-059-24`, `KI-059-26` |
| Supply chain | No signature check of the version tag a host checks out; `0` `--hash` lines in each requirements file | B4-1, B4-2, B5-3 |

### 1.4 Two discrepancies inside HAS

HAS records two pairs of results that disagree. Both are a time sequence, not a conflict. Unit S-10 (`2b4cbaa`) measured B4-3 (no ruleset) and unit S-06 (`c72528c`) measured A10-4 (`enforce_admins: false`) before the human changes recorded in `KI-059-26` (tag ruleset `version-tags`) and `KI-059-24` (`enforce_admins` enabled); unit S-12 (`00ba632`) measured B11-4 and B11-6 after them. All five units ran on 2026-11-14. The order rests on the unit order and on the wording of the two KIs; no timestamp records it.

| Pair | Earlier result | Later result |
| :--- | :--- | :--- |
| B4-3 against B11-4 | B4-3: `rulesets` is `[]` | B11-4: ruleset `version-tags` with the Admin role bypass `always` |
| A10-4 against B11-6 | A10-4: `enforce_admins: false` | B11-6: `enforce_admins` enabled |

### 1.5 Limits of the evidence

| Limit | Detail | Source |
| :--- | :--- | :--- |
| Versions | No design claim of M1-M18 is measured on `2.1.322` child sessions; M13, M14 and M15 keep their `2.1.119` measurement and were not re-run on `2.1.322` (human decision 2026-11-14) | HM section 1, A2 |
| User and managed settings | `allowedDomains` and `allowUnixSockets` at user and managed level are unmeasured | A1 Reading, A2-2 |
| Not reproduced or not executed | M1, M13-M18, F-04, F-09 to F-12, F-14 to F-18 are unmeasured or inferred | HM section 4, Unmeasured |
| Attack validation | No control has been attacked; every `closed` status is by configuration or rule semantics | D52, HAS section 1 |

## 2. Decision

### 2.1 Boundary claim (`RA-19`)

This ADR makes no claim that the sandbox regime is a security boundary. Its boundary claim is **PROVISIONAL** until the attack validation scoped by HAS (unit S-16) is run by a person outside the agent session and the result is recorded. Per plan D52, a control that configuration reading or rule semantics does not show receives the strictest control in the table below. HAS authorises no agent to run any row (HAS section 1).

State of each property is the property itself; the lists in this ADR are evidence of the property, never its definition (`rules/documentation_standard.md`, section "An enumeration in a decision record becomes the implementation's ceiling"). A path, tool or host missing from a list below is not thereby permitted.

### 2.2 Decisions

| # | Subject | Decision | Basis | Decided by |
| :--- | :--- | :--- | :--- | :--- |
| D1 | `RA-09` amendment | Amend `RA-09` to list the measured controls as exposure reduction: the `denyRead` list of D8 (B2), `Read(/**/.env*)` (A5-2 to A5-5), and the denies of `.env*` files outside the project (B4-9, B4-10). Keep the rule that the human runs secret commands. Record B2-c (keychain service) and B2-d (git credential helper) as open (`KI-059-21`). The text states no boundary claim. The change to `agents.md` is unit D-02; the detail in `rules/project_topology.md` is unit D-03 | A5-2 to A5-5, B2, B4-9, B4-10, F-05, F-06, HAS rows B2-c, B2-d | Human, 2026-11-14 |
| D2 | `gh` | `gh` stays with the human. No `sandbox.enableWeakerNetworkIsolation: true`, no `excludedCommands` entry. Revisit only after a broker exists and is measured. Determined by measurement under the human requirement of 2026-11-08 (`devops_agent` runs `gh` instead of the human), which the measurement does not allow to be met without widening the sandbox. Superseded by ADR-0025 | SE section 2.6 (CLI `2.1.319`, `gh` 2.96.0, `excludedCommands` `0`: `x509: OSStatus -26276`, exit `1`); SE section 6.9 case `G` (works only with `enableWeakerNetworkIsolation: true`); SE section 6.9 "Not measured" (trustd Mach service); M2 (not measured on `2.1.322`); HAS row A6-b | Measurement; human requirement of 2026-11-08 |
| D3 | D-12 (`RA-09` / `RA-19` rules) | RECORD. The rules are unchanged by D-12. Tied to D4 | Plan D6, D4 below | Human, 2026-11-14 |
| D4 | Local database route (`KI-057-1`) | RECORD. No route is approved. No end-to-end route is measured: M7, A1-b / `KI-059-20`, M9 / A2-1 and A2-d (unlink and re-bind unmeasured), M8 and M10 (the bridge reached the development database), F-11, F-13, A8-1 to A8-3 (configuration only), F-18 unmeasured. Consequence: unit D-04 is RECORD | M7, M8, M9, M10, A1-1, A2-1, A8-1, A8-2, A8-3, F-02, F-11, F-13, F-18 | Human, 2026-11-14 |
| D5 | Hooks in the nucleus (plan D6, D12, D13) | None now. Reasons: nucleus hook code is writable from the sandbox (A7-3, B3, `KI-059-23`); A4 is not measurable because no wrapper exists; the prototype failed open (F-03), its profile had gaps (M12, F-07), and its stdout drop removes framework output (F-19) and hard-codes a path (F-20); Mach services are unproven closed (F-09). Unit E-01b is RECORD. Manual `suspend` before `/clear` stays documented (plan D13). A future `sandbox-exec` wrapper requires a new implementation unit whose acceptance criteria are A4-1 and A4-2 of HM, run by an agent, plus measured write protection of the hook code (HAS rows A4-c, A7-a closed) | A4-1, A4-2, A7-3, B3, F-03, F-07, F-09, F-19, F-20, M12, `KI-059-23` | Human, 2026-11-14 |
| D6 | GitHub credential | The credential of agent-facing work is the fine-grained token of A10: expiry `2026-12-14` (A10-1), measured scopes A10-2 and A10-3. The human holds it and renews it every 30 days; it is never in an agent's reach. **Target** for a later implementation unit: a GitHub App on the nucleus only, installation tokens valid one hour, minted by a broker outside the agent's reach. Acceptance criteria of that unit: (1) the key store is unreadable from the sandbox (F-05); (2) the broker socket authenticates its caller (F-17). Superseded by ADR-0025 | A10-1, A10-2, A10-3, B10, F-05, F-17 | Human, 2026-11-14 |
| D7 | `workflows/repository_hardening_workflow.md` | Rewrite its text to the measured state: `enforce_admins: true` (B11-6, `KI-059-24`); a reviews object with `0` required approvals (A10-4); linear history and conversation resolution not required (A10-4). Merge without human review (`KI-059-24`) is then controlled by no agent holding a token with Pull requests write (D6). The edit is a later unit, not this ADR | A10-4, B11-6, `KI-059-24` | Human, 2026-11-14 |
| D8 | Network and read lists, nucleus and host template | `sandbox.network.allowedDomains: ["api.github.com","github.com"]` set explicitly; key absence depends on session mode (A1-6, F-01), so the key is never left absent. Any other domain only after it is measured. `sandbox.filesystem.denyRead`: the five existing B2 paths, the four B2-e paths and out-of-project `.env*`. Denying `~/.config/gh` stops `gh` inside the sandbox, consistent with D2 | A1-1, A1-2, A1-4, A1-5, A1-6, F-01, B2, B2-e, B4-9, B4-10 | Human, 2026-11-14 |
| D9 | Further items | Each is a later implementation unit; see section 2.3 | See section 2.3 | Human, 2026-11-14 |
| D10 | Evidence note | The discrepancies of HAS are a time sequence (section 1.4) | S-10, S-06, S-12 | Recorded, no decision |

### 2.3 Detail of D8 and D9

D8 `denyRead` entries, written as the paths of B2:

| Group | Path | Status in B2 |
| :--- | :--- | :--- |
| Existing, five | `~/.docker/config.json`, `~/.config/gh`, `~/.zsh_history`, `~/.claude/projects`, `~/Library/Keychains/login.keychain-db` | Blocked with the rule on `2.1.322` (B2 After) |
| Absent at measurement, four (strictest per D52) | `~/.ssh`, `~/.aws`, `~/.npmrc`, `~/.bash_history` | Absent and not listed; listed so that they stay unreadable if they appear (HAS row B2-e) |
| Outside the project | `.env*` files outside the project root | Readable by Bash and by Read today (B4-9, B4-10); the `Read` deny covers inside the project only (HAS row A5-b) |

D9 items:

| Item | Decision | Evidence | Limit recorded |
| :--- | :--- | :--- | :--- |
| A3 | Deny sandbox writes to `agents/*.md` | A3-3 (writable), A3-2 (14 symlinks, 0 regular files), A3-4 (0 `hooks:`) | Not applied yet |
| A9 | `Edit(/.claude/settings*.json)` deny in the nucleus and the host template | A9-1, A9-2 (no rule), A9-4 (denied), A9-5 (control allowed) | A9-c (a settings write widening a later session, F-18) is unmeasured |
| B1 / `KI-059-25` | Deny the out-of-sandbox tools of B1-2 and the connectors (B1-4, B1-5, B1-6) | B1-2, B1-4, B1-5, B1-6, B1-7 | The absence of the Claude Docs tools in B1-5 is unexplained (HM B1 Reading) |
| B5 | Hash pinning of Python dependencies and write-deny on `venv_skillopt/` | B5-1, B5-3 | Side effects of both are unmeasured |
| B7 | `allowUnsandboxedCommands: false` and no auto mode for agents | B7-4, F-21 | M14: on `2.1.119` the Write tool stays outside the sandbox with that key false |
| B10 | No agent access to the `gho_` token | B10, B11-5 | The keychain path closure is unmeasured; `KI-059-21` stays open |
| B11 / `KI-059-26` | Remove the bypass of tag ruleset `version-tags`; verify tags in `scripts/sync_agents_pin.py` | B11-4, B4-2 | Whether a token acting for the owner inherits the bypass is unmeasured (`KI-059-26`) |
| A2 | M13, M14 and M15 keep their `2.1.119` measurement | A2 | Not re-run on `2.1.322` (human decision 2026-11-14) |
| A5 | **Open.** The replacement for `Edit(~/**)`, which blocks project edits (A5-1), is not decided. It was not put to the human | A5-1, F-10 | HOME protection must name paths (A5 Reading) |

## 3. Consequences

### 3.1 Units

Unit ids for new units are assigned by `principal_agent` when the plan adds them.

| Affected unit | What it does | Done-criterion |
| :--- | :--- | :--- |
| D-02 | Edits `agents.md`: the `RA-09` row lists the D1 controls as exposure reduction, keeps "the human runs secret commands" and names B2-c and B2-d as open | `grep -n "B2-c" agents.md` finds the row; the row holds no boundary claim |
| D-03 | Edits `rules/project_topology.md` section 5 with the D1 detail: `denyRead` list, `.env*` denies, open items | `grep -n "KI-059-21" rules/project_topology.md` finds the section |
| D-04 | RECORD (D4). Adds no local database route and no rule change | The sprint log names D4 as the reason |
| E-01b | RECORD (D5). Installs no hook in the nucleus | `.claude/settings.json` holds no `hooks` entry (A7-1 re-read) |
| New unit: D6 target | Builds the GitHub App broker | A key store unreadable from the sandbox (F-05) and a broker socket that authenticates its caller (F-17), each shown by a measurement of its own |
| New unit: D7 | Rewrites the `enforce_admins`, reviews, linear-history and conversation-resolution text of `workflows/repository_hardening_workflow.md` to A10-4 and B11-6 | `grep -n "enforce_admins" workflows/repository_hardening_workflow.md` shows `true` |
| New unit: D8 | Sets `sandbox.network.allowedDomains` and `sandbox.filesystem.denyRead` in `.claude/settings.json` and the host template `claude/settings.hooks.json` | A1-1 and B2 re-run by `make sandbox-probe` report closed |
| New units: D9 A3, A9, B1, B5, B7, B10, B11 | One unit each, as in section 2.3 | Each unit names the HM check it re-runs |
| New unit: wrapper (D5, future) | Builds a `sandbox-exec` hook wrapper only if a human opens it | A4-1 and A4-2 run by an agent, and measured write protection of the hook code (HAS rows A4-c, A7-a closed) |
| Per CLI version | `make sandbox-probe` (units S-13 to S-15) is re-run on every CLI version (B9) | The probe exits non-zero when a case expected closed is open or not measurable (HAS row B9-a); B9 itself is "Not yet measured" in HM |
| Attack validation | A person outside the agent session runs the rows of HAS after the implementation units and records the result | Result recorded; the boundary claim of section 2.1 then stops being provisional |

### 3.2 What becomes easier

| Gain | Basis |
| :--- | :--- |
| The egress and loopback controls have an explicit setting measured in child sessions on two CLI versions | A1-1, A1-2, A1-4, A1-5 |
| Credential files of the Bash sandbox are unreadable once the D8 list is set | B2 After |
| The regime states which items are open, by id, so a later session starts from the open list | Sections 1.5, 2.3 |

### 3.3 What becomes harder or stays open

| Cost or open item | Basis |
| :--- | :--- |
| The human runs every `gh` command; `devops_agent` does not, until a broker exists and is measured | D2 |
| The human renews the A10 token every 30 days; a missed renewal ends agent-facing GitHub access on `2026-12-14` | D6, A10-1 |
| Denying `~/.config/gh` stops `gh` in the sandbox | D8, B2 Reading |
| The keychain service (B2-c) and git credential helper (B2-d) stay open; `denyRead` of files does not cover them | `KI-059-21`, F-05, F-06 |
| No local database route, no hook in the nucleus: tests with a container and the `suspend` before `/clear` stay manual | D4, D5, D13 of the plan |
| The boundary claim stays provisional until the validation of HAS is run and recorded | Section 2.1 |
| The A5 replacement rule for `Edit(~/**)` is undecided; `Edit(~/**)` stays unusable as protection | A5-1 |
| `allowUnixSockets`, `allowedDomains` at user and managed level, M13-M15 on `2.1.322`, and the Mach service of trustd are unmeasured | Section 1.5, SE section 6.9 |

## 4. Deciders

| Role | Who | Part |
| :--- | :--- | :--- |
| Human | The repository owner | D1, D3, D4, D5, D6, D7, D8, D9 (decisions of 2026-11-14 in chat); the requirement of 2026-11-08 behind D2 |
| `principal_agent` | Owner of the ADR | Brief and scope of the decisions |
| `doc_orchestrator` | Writer | Text of this ADR from the brief and the measurements |
| Measurement | `devops_agent` units S-02 to S-12, C-01, C-01b | D2 (determined by measurement) |

## 5. Considered Options

| Subject | Option | Pros | Cons |
| :--- | :--- | :--- | :--- |
| `gh` | **`gh` stays with the human (chosen)** | No widening key; no new credential path; matches the measured TLS failure | The human runs every `gh` command |
| `gh` | Native `gh` with `enableWeakerNetworkIsolation: true` | Works in the sandbox (case `G`) | Adds a Mach lookup of `com.apple.trustd.agent`, unmeasured, called a "potential data exfiltration vector" in the binary text (M2); A6-b lists the key as widening; not measured on `2.1.322` |
| `gh` | In-sandbox REST client | Authenticated REST returned `200` (M4) | The agent holds the token (M5); egress was open in the parent session (F-01) |
| `gh` | Broker outside the sandbox | Keeps the token out of the sandbox | No broker exists; key store and caller authentication unproven (F-05, F-17); unlisted routes reach `main` (F-16) |
| GitHub credential | **Fine-grained token held by the human (chosen)** | Single repository, no Administration, no Workflows, expires (A10-1, A10-2, A10-3) | Manual renewal every 30 days |
| GitHub credential | GitHub App with one-hour installation tokens | Short-lived credentials | Needs a broker and key store that do not exist; recorded as the target |
| GitHub credential | The `gho_` token | Already in place | Broadest scopes, no expiry, readable from the sandbox today (M5, B10, `KI-059-21`) |
| Hooks in the nucleus | **None now (chosen)** | No hook runs agent-writable code outside the sandbox | Manual `suspend` before `/clear` |
| Hooks in the nucleus | Hooks wrapped in `sandbox-exec` | Writes and TCP held in the prototype (M11) | Failed open (F-03), profile gaps (M12, F-07, F-08, F-09), drops framework output (F-19), absolute path (F-20) |
| Hooks in the nucleus | Unwrapped hooks | Framework output intact | Hook code writable from the sandbox (A7-3); an allow hook approved calls on `2.1.119` (M13) |
| Local database | **RECORD, no route (chosen)** | No unmeasured path is approved | Container tests need a permission prompt (A8 Reading) |
| Local database | Bridge to the development database | Works as plumbing (M10) | Reached the development database; no error handling (M10, F-11, F-12) |
| Local database | Throwaway container with network mode `none` | Configuration shows no network and a non-superuser role (A8-2, A8-3) | The Docker API is refused from the sandbox (A8-1); Unix socket on a bind mount fails on Docker Desktop (M8); reach not exercised |
| `RA-09` | **List the controls as exposure reduction, no boundary claim (chosen)** | States what is measured and what is open | The keychain and helper stay open |
| `RA-09` | Claim a boundary | Simpler text | Prohibited by `RA-19` without a measured enumeration and the attack validation |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0019-sandbox-regime.md`.*
