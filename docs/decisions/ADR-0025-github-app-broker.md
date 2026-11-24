# 📜 ADR-0025: GitHub App broker (MCP stdio broker, user-scope registration, key store, operation list, signed install, tag-signature verification)
**Status**: `Accepted`
**Date**: 2026-11-22
**Sprint**: 060
**Owner**: `principal_agent`
**Writer**: `doc_orchestrator`
**Supersedes**: `ADR-0019` (`docs/decisions/ADR-0019-sandbox-regime.md`) decisions D2 (`gh`) and D6 (GitHub credential) only. ADR-0019 stays `Accepted` and is not edited beyond the line `Superseded by ADR-0025` in its D2 and D6 rows; every part of it not named here is unchanged.
**Triggers**: 2, 3 (`rules/documentation_standard.md §3.1`): the deny lists in `claude/settings.hooks.json` and the tag-signature check in `install.py` are part of the contract that hosts install from the nucleus (trigger 2), and the broker holds a credential behind a security boundary (trigger 3). Trigger 3 alone requires the full MADR format of sections 4 and 5.

---

## 1. Context

Abbreviations: plan = `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` (Context, Design D1-D6, Work A-01 to A-15, Abort criterion 1); BM = `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` (the instrument of this ADR; it does not exist when this ADR is written, so no result of it is claimed here).

| Item | Statement | Source |
| :--- | :--- | :--- |
| Current state | `gh`, `git push`, merge, tag and Release are run by the human under the sandbox. `ADR-0019` D2: "`gh` stays with the human. No `sandbox.enableWeakerNetworkIsolation: true`, no `excludedCommands` entry. Revisit only after a broker exists and is measured" | `ADR-0019` D2 |
| Current credential | `ADR-0019` D6: the credential of agent-facing work is the fine-grained token of A10, held and renewed by the human; target for a later unit: a GitHub App on the nucleus only, installation tokens valid one hour, minted by a broker outside the agent's reach. Acceptance criteria: (1) the key store is unreadable from the sandbox (F-05); (2) the broker socket authenticates its caller (F-17) | `ADR-0019` D6 |
| Observed fact | `gh` does not run under the sandbox: `failed to read configuration: open ~/.config/gh/config.yml: operation not permitted` | plan Context; reproduce with `gh issue list --label host-finding --state open` |
| Human decision | 2026-11-21: the first unit of Sprint 060 is the GitHub App broker (plan of 059, decision 55) | plan Context |
| Open finding | `F-055-N1` (entry points outside the sandbox writable by the agent) is not closed by this ADR; D2 below installs the broker outside every agent-writable tree so as not to add an entry point to that finding | plan Context |
| Done when | A session under the sandbox pushes `ai-sprint/060`, opens and merges the PR, pushes the signed tag `v4.43.0` and publishes the Release without the human running `gh` or `git push` | plan Context |

## 2. Decision

Human decisions of 2026-11-21 (plan D1 to D6). Boundary claims are limited to the set that `BROKER_MEASUREMENT.md` M1-M5 enumerates (`RA-19`); M1-M5 are the instrument, not a result.

### 2.1 Decisions

| ID | Decision | Rejected alternative and why | Check |
| :--- | :--- | :--- | :--- |
| D1 | The broker is an MCP stdio server that **executes** a closed list of GitHub operations; the installation token (1 h) never leaves the broker process. Claude Code launches it over stdio, so there is no socket to authenticate (`ADR-0019` D6 criterion 2, F-17) | A launchd daemon with a socket that hands out tokens: the token would enter the sandbox for 1 h and the socket authentication would have to be designed and measured | BM M3: no sandbox process obtains a token (`env`, `ps`, broker files) → 0 findings |
| D2 | The broker is installed in `~/.config/agents-broker/` and registered at user scope (`claude mcp add --scope user`), **never** in the project `.mcp.json` nor in `claude/mcp.json`, which are writable by the agent (`F-055-N1`) | Registering it in `claude/mcp.json`: `install.py` would inject it into every host and its code would sit under `./`, writable | `grep -c agents-broker claude/mcp.json` → `0` |
| D3 | Keys (the App private key, the SSH tag-signing key) live in `~/.config/agents-broker/keys/`, in `sandbox.filesystem.denyRead`, with `permissions.deny` `Read`/`Edit`/`Write` on `~/.config/agents-broker/**` and `~/.claude.json` (`ADR-0019` D6 criterion 1, F-05) | macOS keychain: the sandbox `python3` is the same binary as the broker's, so a per-binary ACL does not separate them, and `KI-059-21` measured the keychain service as reachable | BM M1, M2: `cat`, `Read`, `Edit` from the sandbox → denied |
| D4 | Allowed operations: `push_branch` (only `ai-sprint/*`, `hotfix/*`, `deploy-notes/*`; never `main`, never `--force`), `open_pr`, `merge_pr` (head `ai-sprint/*` or `hotfix/*`, base `main`, the 3 required checks in `success`), `push_tag` (`vX.Y.Z` on a commit of `main`, SSH-signed by the broker), `create_release`, `pr_status`. Any other operation → error. App permissions: Contents RW, Pull requests RW, Metadata R; no Administration | Merge with human approval: contradicts the criterion of 2026-11-21 | `pytest tests/test_github_broker.py` → exit `0` with one rejection case per operation |
| D5 | The broker code lives in the nucleus (`scripts/github_broker.py`, versioned and tested) and **the human** installs it with `scripts/install_broker.py --tag vX.Y.Z`, which copies the file from `git show <tag>:` (not from the working tree) after verifying the tag signature; the first bootstrap (`v4.43.0` does not exist yet) copies from a `main` commit the human names. Installation therefore does not execute agent-writable content (`RA-19` (3)) | Installing from the working tree: the agent could alter the broker before the human installs it | `pytest tests/test_install_broker.py` → exit `0`, including the case "modified working tree is not installed" |
| D6 | Tag-signature verification with `git verify-tag` against `config/allowed_signers` in `scripts/sync_agents_pin.py` and `scripts/install.py`; a tag without a valid signature → exit `2` (`KI-059-26`) | Trusting the `version-tags` ruleset: it protects creation on GitHub but not what the host checks out | `pytest tests/test_sync_agents_pin.py tests/test_install.py` → exit `0` with a "tag without signature" case |
| D6-detail | The tag-signing key is a dedicated ed25519 SSH key generated by the human at `~/.config/agents-broker/keys/tag_signing`, never by the agent (RV-15). `config/allowed_signers` holds one line `agents-broker namespaces="git" <public key>`, so the signer principal is `agents-broker`, which the broker sets as the tag's signer identity. The agent writes only the public-key value the human pastes | A key generated by the agent: the agent would have held the private key, against D3 and RV-15 | `pytest tests/test_sync_agents_pin.py tests/test_install.py` (D6 check) with `config/allowed_signers` as above; BM M5 records the signed tag pushed by the broker |

### 2.2 Superseded items

| Item | Superseded text of ADR-0019 | Replaced by |
| :--- | :--- | :--- |
| D2 `gh` | "`gh` stays with the human ... Revisit only after a broker exists and is measured" | D1-D5 of this ADR: GitHub operations run through the broker's MCP tools; the sandbox is not widened (no `enableWeakerNetworkIsolation`, no `excludedCommands` entry) |
| D6 GitHub credential | The A10 fine-grained token held by the human, and the target and acceptance criteria of the later unit | D1, D3: the App installation token stays in the broker process, keys in `~/.config/agents-broker/keys/` |

## 3. Consequences

| Consequence | Unit | Evidence or done-criterion |
| :--- | :--- | :--- |
| `ADR-0019` rows D2 and D6 carry the line `Superseded by ADR-0025` (RV-10) | A-01 | `grep -c "Superseded by ADR-0025" docs/decisions/ADR-0019-sandbox-regime.md` → `2` |
| The broker module has a Blueprint before code (`agents.md §0`) | A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` exists |
| The broker MCP stdio server with the operations of D4 exists | A-03 | `pytest tests/test_github_broker.py` → exit `0` |
| The human installs the broker from a signed tag or a named `main` commit | A-04 | `pytest tests/test_install_broker.py` → exit `0` |
| `denyRead` and `permissions.deny` of D3 are in `claude/settings.hooks.json` | A-05 | BM M1, M2 |
| `config/allowed_signers` holds the line of D6-detail | A-06 | `grep -c "^agents-broker namespaces=\"git\"" config/allowed_signers` → `1` |
| `sync_agents_pin.py` rejects a tag without valid signature (exit `2`) | A-07 | `pytest tests/test_sync_agents_pin.py` → exit `0` |
| `install.py` rejects a tag without valid signature (exit `2`) | A-08 | `pytest tests/test_install.py` → exit `0` |
| The human has setup steps for the App, its permissions, key generation, `install_broker.py` and `claude mcp add --scope user` | A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` exists |
| M1 to M4 are recorded as the instrument for the claims of D1-D4, limited to the enumerated set (`RA-19`) | A-10 | `BROKER_MEASUREMENT.md` M1-M4 |
| The deployment workflow runs push, PR, merge, tag and Release through the broker | A-11 | `workflows/deployment_workflow.md` text; regenerated `WORKFLOWS_STEP_MAP_GUIDE.md` in the same commit |
| `devops_agent` runs GitHub operations through the broker's MCP tools and keeps only `Bash`, with no write authority (`ADR-0009`, RV-11) | A-12 | `agents/devops_agent.md` text |
| The `gh`/credential row of `rules/project_topology.md` names the broker (`KI-059-21`, `-22`, `-24`) | A-13 | `grep -n "ADR-0025" rules/project_topology.md` |
| `ADR-0019` D7 (measured state of the hardening workflow) and the App installation are stated in the hardening workflow | A-14 | `workflows/repository_hardening_workflow.md` text; regenerated `WORKFLOWS_STEP_MAP_GUIDE.md` in the same commit |
| M5: the agent executes push, PR, merge, signed tag and Release in the deployment of 060, each with its GitHub ID; gates read M1-M4 (RV-7) | A-15 | `BROKER_MEASUREMENT.md` M5 |
| If any of M1-M5 fails, execution stops and the sprint returns to Phase 1; there is no reversion to `gh` with the human | Plan Abort criterion 1 | `BROKER_MEASUREMENT.md` M1-M5 in green |
| The human installs the App on the nucleus only, generates both keys and runs `install_broker.py`; the agent does none of these | A-09 (steps), A-04 | Setup guide |

## 4. Deciders

| Role | Who | Part |
| :--- | :--- | :--- |
| Human | The repository owner | D1 to D6 (decisions of 2026-11-21); the choice of the dedicated tag-signing key generated by the human (RV-15) |
| `principal_agent` | Owner | Plan D1 to D6 |
| `doc_orchestrator` | Writer | This document |

## 5. Considered Options

| Item | Option | Pros | Cons |
| :--- | :--- | :--- | :--- |
| Delivery | **MCP stdio server that executes operations (chosen)** | Token never leaves the broker process; no socket to authenticate | A closed operation list limits what the agent can do |
| Delivery | launchd daemon with a token-handing socket | Generic | Token enters the sandbox for 1 h; socket authentication to design and measure |
| Registration | **User scope (chosen)** | Outside agent-writable trees | The human registers it per machine |
| Registration | `claude/mcp.json` | Installed by `install.py` in every host | Code under `./`, writable by the agent |
| Key store | **`~/.config/agents-broker/keys/` with `denyRead` and `permissions.deny` (chosen)** | Measured by M1, M2 | Boundary claim limited to the set M1-M5 enumerates (`RA-19`) |
| Key store | macOS keychain | Native store | Same `python3` binary as the sandbox; keychain service reachable (`KI-059-21`) |
| Merge | **Broker merges when head, base and the 3 required checks match (chosen)** | Meets the criterion of 2026-11-21 | No human review at merge (`KI-059-24`) |
| Merge | Human approval | Human review | Contradicts the criterion of 2026-11-21 |
| Install | **Human installs from `git show <tag>:` after signature check (chosen)** | Does not execute agent-writable content | First bootstrap needs a `main` commit the human names |
| Install | From the working tree | Simple | The agent could alter the broker first |
| Tag trust | **`git verify-tag` against `config/allowed_signers` (chosen)** | Checks what the host checks out | Needs the signer line and the key from the human |
| Tag trust | `version-tags` ruleset only | No code | Protects creation on GitHub, not host checkout |
| Signing key | **Dedicated ed25519 key generated by the human (chosen)** | The agent never holds the private key | A human step |
| Signing key | Key generated by the agent | No human step | Violates D3 and RV-15 |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`).*
