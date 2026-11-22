# 🏛️ Blueprint: GITHUB_BROKER
**File**: `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` (RA-06 Option B naming)
**Status**: `DRAFT`
**Sprint of origin**: #060
**Last Audit Sprint**: #060
**Last Audit Date**: 2026-11-22
**Last Audit Commit SHA**: 479d8c3

---

arc42-lite (`rules/documentation_standard.md §5`) — Reference only. This document states current facts, verifiably; it never argues for them. Any decision behind this module's shape lives in a linked ADR, not here.

Implementation status: designed, not yet implemented (Sprint 060 A-03/A-04). Every row below describes the module as designed; none is a measured result. Measurement instrument: `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` M1-M5 (created in A-10, extended in A-15; it does not exist when this Blueprint is written).

## 1. Introduction & Goals
The GitHub broker is a stdio MCP server (`scripts/github_broker.py`, JSON-RPC by lines, Python standard library only) that executes a closed list of GitHub operations (`push_branch`, `open_pr`, `merge_pr`, `push_tag`, `create_release`, `pr_status`) on behalf of an agent running under the sandbox. It authenticates as a GitHub App: it signs an App JWT with `openssl`, exchanges it for a one-hour installation token, and keeps that token in process memory only. A second script (`scripts/install_broker.py`) lets the human install the broker into `~/.config/agents-broker/` from a signed tag or a named `main` commit.

| Goal | Done-criterion (ADR-0025 §1) |
| :--- | :--- |
| A session under the sandbox pushes `ai-sprint/060`, opens and merges the PR, pushes the signed tag `v4.43.0` and publishes the Release | No `gh` or `git push` run by the human; recorded as `BROKER_MEASUREMENT.md` M5 (A-15) |

## 2. Context & Scope
| Aspect | Value |
| :--- | :--- |
| **Upstream dependencies** | GitHub REST API (App installation on the nucleus repository only; permissions Contents RW, Pull requests RW, Metadata R; no Administration); `openssl` (App JWT signing); `git` (branch and tag push, SSH tag signing); Claude Code MCP stdio launch (`claude mcp add --scope user`); `config/allowed_signers` (signer principal `agents-broker`); `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` M1-M5 |
| **Downstream consumers** | `workflows/deployment_workflow.md` (push, PR, merge, tag, Release; A-11); `agents/devops_agent.md` (GitHub operations through the MCP tools; A-12); `scripts/install.py` and `scripts/sync_agents_pin.py` (tag-signature check against `config/allowed_signers`; A-07, A-08); `scripts/graph_mcp.py` (installed by the same installer; M-04, M-18) |

Out of scope: the human's own setup steps (`docs/guides/GITHUB_BROKER_SETUP_GUIDE.md`, A-09); the closure of `F-055-N1` (ADR-0025 §1, Open finding).

## 3. Building Block View
| Aspect | Value |
| :--- | :--- |
| **Owns** | `scripts/github_broker.py`; `scripts/install_broker.py`; `tests/test_github_broker.py`; `tests/test_install_broker.py`; install location `~/.config/agents-broker/` (human-installed copy of the broker); keys under `~/.config/agents-broker/keys/` (App private key, `tag_signing` SSH key); `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` (instrument) |
| **Must not touch** | `claude/mcp.json` and the project `.mcp.json` (agent-writable; `grep -c agents-broker claude/mcp.json` → `0`); `main` as a push target; `.env` (`RA-09`); any `sandbox.excludedCommands` entry (`RA-19`); any socket or daemon |

Components:

| Component | Path | Role (as designed) | Plan row |
| :--- | :--- | :--- | :--- |
| Broker server | `scripts/github_broker.py` | stdio MCP server; reads JSON-RPC messages line by line; exposes the six operations; applies the D4 refusals; mints and holds the installation token in memory | A-03 |
| Installer | `scripts/install_broker.py` | Run by the human; verifies the tag signature, then copies the broker file from `git show <tag>:` into `~/.config/agents-broker/` | A-04 |
| Key store | `~/.config/agents-broker/keys/` | App private key and SSH tag-signing key; in `sandbox.filesystem.denyRead`; `permissions.deny` `Read`/`Edit`/`Write` on `~/.config/agents-broker/**` and `~/.claude.json` | A-05 (deny lists), A-09 (human key generation) |
| Signer list | `config/allowed_signers` | One line `agents-broker namespaces="git" <public key>`; the public-key value is pasted by the human | A-06 |
| Tag verification | `scripts/sync_agents_pin.py`, `scripts/install.py` | `git verify-tag` against `config/allowed_signers`; invalid or missing signature → exit `2` | A-07, A-08 |
| Tests | `tests/test_github_broker.py`, `tests/test_install_broker.py` | One rejection case per operation; case "modified working tree is not installed" | A-03, A-04 |
| Instrument | `BROKER_MEASUREMENT.md` | M1-M5 (see §6) | A-10, A-15 |

Contracts (formal interfaces this module exposes). No `docs/contracts/GITHUB_BROKER_CONTRACT.md` exists and no plan row creates one; the interface is the operation list of ADR-0025 D4, restated in the table below.

| Interface | Type | Defined in |
| :--- | :--- | :--- |
| `push_branch` | MCP tool (function) | `docs/decisions/ADR-0025-github-app-broker.md` D4 |
| `open_pr` | MCP tool (function) | same, D4 |
| `merge_pr` | MCP tool (function) | same, D4 |
| `push_tag` | MCP tool (function) | same, D4 |
| `create_release` | MCP tool (function) | same, D4 |
| `pr_status` | MCP tool (function) | same, D4 |
| Any other operation | Refused with an error | same, D4 |
| `scripts/install_broker.py --tag vX.Y.Z` | CLI (human-run) | same, D5 |

Operation refusals (D4):

| Operation | Allowed when | Refused when |
| :--- | :--- | :--- |
| `push_branch` | Branch matches `ai-sprint/*`, `hotfix/*` or `deploy-notes/*` | Target is `main`; any `--force`; any other branch pattern |
| `open_pr` | Listed in D4 with no further condition stated | Not stated in D4 beyond the closed operation list |
| `merge_pr` | Head matches `ai-sprint/*` or `hotfix/*`; base is `main`; the 3 required checks are in `success` | Any other head or base; any required check not in `success` |
| `push_tag` | Tag is `vX.Y.Z`; it points at a commit of `main`; the broker signs it over SSH | Any other tag name; a commit not on `main` |
| `create_release` | Listed in D4 with no further condition stated | Not stated in D4 beyond the closed operation list |
| `pr_status` | Listed in D4 with no further condition stated | Not stated in D4 beyond the closed operation list |

Data model (summary only):
- Installation token: GitHub App installation token valid 1 hour; minted by the broker; held in process memory only; never written to a file, the environment, MCP output or `ps`.
- App JWT: signed by the broker with `openssl` using the App private key from `keys/`; used only to obtain the installation token.
- Tag-signing key: dedicated ed25519 SSH key at `~/.config/agents-broker/keys/tag_signing`, generated by the human; signer principal `agents-broker`.
- Install source: a signed tag `vX.Y.Z` (read with `git show <tag>:`) or, for the first bootstrap only, a `main` commit the human names.

## 4. Runtime View
Flow 1 — Operation call:

1. Claude Code launches `scripts/github_broker.py` over stdio from the user-scope registration (no socket exists).
2. The agent calls an MCP tool; the broker reads the JSON-RPC message from one line.
3. The broker checks the operation against the closed list; any other operation returns an error.
4. The broker applies the D4 refusal for that operation (branch pattern, head/base, required checks, tag name); a refusal returns an error and performs no GitHub call.
5. The broker signs an App JWT with `openssl`, obtains the installation token and keeps it in memory.
6. The broker performs the GitHub operation (for `push_tag`, it first signs the tag over SSH with the `tag_signing` key).
7. The broker returns the result to the agent; the token is not part of the response.

Flow 2 — Human installation from a signed tag:

1. The human runs `python3 scripts/install_broker.py --tag vX.Y.Z` (host form `python3 .agents/scripts/install_broker.py`; `agents.md §0 Command paths`).
2. The installer verifies the tag signature against `config/allowed_signers`.
3. The installer copies `scripts/github_broker.py` from `git show <tag>:`, never from the working tree, into `~/.config/agents-broker/`.
4. The human registers the server with `claude mcp add --scope user`.

Flow 3 — First bootstrap: as Flow 2, with the source being a `main` commit the human names, because `v4.43.0` does not exist yet. The exact command-line form of this path is defined in A-04; it is not stated in ADR-0025.

## 5. Crosscutting Concepts
| Concept | Rule (as designed) |
| :--- | :--- |
| Error handling | Operations outside the closed list and every D4 refusal return an error; there is no fallback to `gh` run by the human (Plan Abort criterion 1) |
| Auth boundary | Claude Code spawns the broker over stdio; the broker has no listening socket, so no caller authentication is designed (ADR-0025 D1) |
| Secret handling | The installation token stays in broker process memory; keys stay under `~/.config/agents-broker/keys/`; the agent never reads or generates them (`RA-09`, RV-15) |
| Install provenance | Installation reads from a signed tag or a human-named `main` commit via `git show`, so no agent-writable content is executed (`RA-19` (3)) |
| Registration scope | User scope only; project `.mcp.json` and `claude/mcp.json` never carry the server (`F-055-N1`) |
| Dependencies | Python standard library, `openssl`, `git`; no third-party package |
| Claim limit | Boundary claims cover only the set M1-M5 enumerates (`RA-19`) |

## 6. Non-negotiable Constraints
| Constraint | Verification |
| :--- | :--- |
| The installation token never leaves the broker process | `BROKER_MEASUREMENT.md` M3: environment of sandbox processes, files under `~/.config/agents-broker/`, MCP output to the transcript and `ps` → 0 findings; claim limited to that set |
| The broker is not registered in agent-writable files | `grep -c agents-broker claude/mcp.json` → `0` |
| Keys are unreadable and uneditable from the sandbox | `BROKER_MEASUREMENT.md` M1 (exit codes only, no content printed) and M2 (installed broker not editable): `cat`, `Read`, `Edit` from the sandbox → denied |
| Only the six D4 operations run, with the D4 refusals | `pytest tests/test_github_broker.py` → exit `0`, one rejection case per operation; `BROKER_MEASUREMENT.md` M4 (refusals observed live) |
| `main` is never a push target and `--force` is never used | `pytest tests/test_github_broker.py` → exit `0` (`push_branch` rejection case) |
| Installation never uses the working tree | `pytest tests/test_install_broker.py` → exit `0`, including "modified working tree is not installed" |
| A tag without a valid signature is rejected by the host tooling | `pytest tests/test_sync_agents_pin.py tests/test_install.py` → exit `0` with a "tag without signature" case |
| `config/allowed_signers` holds the signer line | `grep -c "^agents-broker namespaces=\"git\"" config/allowed_signers` → `1` |
| The App holds no Administration permission | Human setup step (A-09); permissions Contents RW, Pull requests RW, Metadata R |
| Push, PR, merge, signed tag and Release are executed by the agent through the broker | `BROKER_MEASUREMENT.md` M5 with the GitHub ID of each operation (A-15) |
| If any of M1-M5 fails, execution stops and the sprint returns to Phase 1 | Plan Abort criterion 1 |

## 7. Decisions
This module's ADR log — link, don't restate:
- `docs/decisions/ADR-0025-github-app-broker.md`: GitHub App broker as an MCP stdio server (D1), user-scope registration (D2), key store (D3), operation list (D4), signed install from `git show <tag>:` (D5), tag-signature verification and the dedicated signing key (D6).
- `docs/decisions/ADR-0019-sandbox-regime.md`: sandbox regime; its D2 (`gh`) and D6 (GitHub credential) are superseded by ADR-0025; every other part is unchanged.

## 8. Glossary
| Term | Meaning in this module |
| :--- | :--- |
| Broker | `scripts/github_broker.py` running as a stdio MCP server; the only holder of the installation token |
| GitHub App | The App installed on the nucleus repository only; source of the installation token |
| App JWT | Short-lived token signed with the App private key by `openssl`; exchanged for the installation token |
| Installation token | GitHub token valid 1 hour; kept in broker process memory only |
| Key store | `~/.config/agents-broker/keys/` |
| User scope | `claude mcp add --scope user` registration, outside every agent-writable tree |
| Bootstrap | First install from a `main` commit the human names, used while `v4.43.0` does not exist |
| `allowed_signers` | `config/allowed_signers`; signer list for `git verify-tag`; principal `agents-broker` |
| M1-M5 | Measurements in `BROKER_MEASUREMENT.md`: M1 keys unreadable, M2 installed broker not editable, M3 no token reachable in the enumerated set, M4 D4 refusals live, M5 the five deployment operations (push, PR, merge, signed tag, Release) |
| `F-055-N1` | Open finding: entry points outside the sandbox writable by the agent; not closed by this module |

---
*A module without a ratified Blueprint cannot enter Execution (agents.md §0). C4 Level 3 (Component diagram) required here if this module qualifies per `rules/documentation_standard.md §2.1` — see `**C4 Level Override**` for a manually-justified exception. This module declares no `**C4 Level Override**`; the component list in §3 is a table, not a diagram.*
