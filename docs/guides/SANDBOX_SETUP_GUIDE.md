# 🧭 How-to: Set up and troubleshoot the Claude Code sandbox
**File**: `docs/guides/SANDBOX_SETUP_GUIDE.md` (RA-06 Option B naming)
**Module**: CORE / SANDBOX

---

## 1. Goal
Install the sandbox settings the framework ships, confirm they are active, and resolve each restriction a sandboxed session shows. The sandbox reduces exposure; it is not a security boundary (`RA-09`, `RA-19`). Decisions: `docs/decisions/ADR-0019-sandbox-regime.md`, `docs/decisions/ADR-0024-sandbox-egress-amendment.md`. Mechanism and measurements: `rules/project_topology.md` section 5.

## 2. Prerequisites
- Claude Code 2.1.219 or later (`sandbox.network.strictAllowlist` needs it), `python3` and `jq` on the PATH.
- A clone of the framework has **no sandbox** until `.claude/settings.json` exists: `.gitignore` ignores `.claude/`, and `claude/settings.hooks.json` is a template that Claude Code does not load.
- Command forms: **host** (`.agents/` is a git submodule) runs `python3 .agents/scripts/<name>.py` and `make -f .agents/Makefile <target>` from the host root; **nucleus** (this repository is `.agents`) runs `python3 scripts/<name>.py` and `make <target>` (`agents.md` section 0, "Command paths").
- Commands marked **human** are run by you in your own shell, never by the agent (`RA-09`).

## 3. Steps

### 3.1 Install the project-scope settings
| Mode | Command | What `scripts/install.py` does |
| :--- | :--- | :--- |
| Host | `python3 .agents/scripts/install.py --target claude` | Merges `claude/settings.hooks.json` into the host `.claude/settings.json` (existing keys kept) and, on macOS only, merges the `env` pair `PIP_USE_DEPRECATED` / `PIP_CERT`. |
| Nucleus | `python3 scripts/install.py --target claude` | Merges the `sandbox` and `permissions` keys of the template into `.claude/settings.json`, minus the host-only `denyWrite` paths `./.agents` and `./.git/modules/.agents`, plus `./agents` and `./venv_skillopt`; same macOS `env` pair; no hooks. |

### 3.2 Set the user-scope settings
`install.py` never writes `~/.claude/settings.json` (`ADR-0024`). After each run it reads that file read-only and, when `sandbox.network.strictAllowlist` is not `true` or a base domain is missing, prints a backup-and-`jq` command. **Human** runs the printed command (full text and domain list: `rules/project_topology.md` section 5). Complete settings print nothing.

### 3.3 Where to run it
Run `install.py` outside a sandboxed agent session. When a write is refused it prints `PermissionError: cannot write <path> (agent sandbox protects it). Run <command> outside the sandbox.` and the human re-runs the printed command in their own shell.

## 4. Verify it worked
```bash
jq '.sandbox | {enabled, allowUnsandboxedCommands}' .claude/settings.json
```
Expected output: `{"enabled":true,"allowUnsandboxedCommands":false}` (jq prints it indented unless `-c` is added).

Then, from a Claude Code session in the repository, run `touch ../sandbox-write-probe` through the Bash tool. Expected: it fails (`Operation not permitted`) and no file appears outside the repository. A success means the sandbox is not active in that session.

Optional re-measurement of the network cases against the live sandbox: `make sandbox-probe` (host: `make -f .agents/Makefile sandbox-probe`); exits 0 with cases A1-1 and A1-2 `closed`.

## 5. If something goes wrong
One row per restriction. Project scope keys live in `.claude/settings.json`; user scope keys in `~/.claude/settings.json`.

| Symptom | Cause | Command | Check |
| :--- | :--- | :--- | :--- |
| **`sandbox.enabled`**: Bash commands run with no restriction; the write probe of section 4 succeeds | `.claude/settings.json` is missing or has `sandbox.enabled` not `true`; a clone ships no such file | Run the install command of section 3.1 (outside a sandboxed session) | `jq '.sandbox.enabled' .claude/settings.json` prints `true` |
| **`sandbox.autoAllowBashIfSandboxed`**: a Bash command inside the sandbox prompts for approval, or runs with no prompt and you expected one | The key `true` auto-approves Bash commands that run inside the sandbox; `false` prompts for each | Edit the value in `.claude/settings.json` (human); the shipped value is `true` | `jq '.sandbox.autoAllowBashIfSandboxed' .claude/settings.json` prints the value you set |
| **`sandbox.allowUnsandboxedCommands`**: a refused command cannot be retried outside the sandbox | The key is `false`: no command may leave the sandbox, and no `sandbox.excludedCommands` entry may exist (`RA-09`) | Keep `false`. Human runs the command in their own shell instead | `jq '.sandbox.allowUnsandboxedCommands' .claude/settings.json` prints `false` |
| **`sandbox.network.allowedDomains`** (project): a host outside `api.github.com`, `github.com`, `pypi.org`, `files.pythonhosted.org` prompts for approval | The project list skips the prompt for its entries and does not deny other hosts (`ADR-0024`) | None to add a domain here: a project-scope entry does not make an unlisted host refuse or pass under `strictAllowlist` (see the user-scope rows) | `jq '.sandbox.network.allowedDomains' .claude/settings.json` lists the four domains |
| **`sandbox.filesystem.denyRead`**: `cat ./.env` or a read of `~/.ssh`, `~/.aws`, `~/.npmrc`, `~/.config/gh`, `~/.docker/config.json`, `~/.zsh_history`, `~/.bash_history`, `~/.claude/projects`, the login keychain file, or any `.env*` under `~/` fails with `Operation not permitted` | The path is in `sandbox.filesystem.denyRead`. By design: an agent session never reads these (`RA-09`) | None. Never remove an entry to make a read work; the human reads the file in their own shell | `jq '.sandbox.filesystem.denyRead' .claude/settings.json` lists the entry |
| **`sandbox.filesystem.allowRead`**: `./.env.example`, `./.env.sample` or `./.env.template` is unreadable | These three names are re-allowed inside the `./.env.*` deny. A different template name (for example `.env.local.example`) stays denied | Rename the template to one of the three names, or add its path to `allowRead` (human) | `jq '.sandbox.filesystem.allowRead' .claude/settings.json` lists the file |
| **`sandbox.filesystem.denyWrite`**: a write to `./.env`, `./.agents` (host), `./.git/modules/.agents` (host), `./agents` or `./venv_skillopt` (nucleus) fails from the agent | The path is in `sandbox.filesystem.denyWrite`. Write-denies reduce exposure and are not a boundary (`RA-19`) | Human makes the change in their own shell; a host changes the framework through a nucleus contribution (`agents.md` section 4, `feedback_upstream`) | `jq '.sandbox.filesystem.denyWrite' .claude/settings.json` lists the entry |
| **`sandbox.credentials.files`**: a command that needs the secrets in `./.env` finds none; `pytest` with no explicit paths exits `4` (`found no collectors`) because `stat()` of `.env` is refused | `./.env` is declared a credential file with `mode: deny` | Scope the walker with explicit paths, or the human runs it unsandboxed; secret commands are prepared by the agent and run by the human (`RA-09`) | `jq '.sandbox.credentials.files' .claude/settings.json` prints `[{"path":"./.env","mode":"deny"}]` |
| **`env` pair `PIP_USE_DEPRECATED` / `PIP_CERT`**: `pip install` fails with a TLS certificate error under the sandbox on macOS | macOS `trustd` is unreachable inside the sandbox; the pair makes pip use `legacy-certs` and the file `/etc/ssl/cert.pem`. `install.py` merges it on macOS only | Re-run the install command of section 3.1; do not set another `PIP_*` override | `jq '.env' .claude/settings.json` prints `{"PIP_USE_DEPRECATED":"legacy-certs","PIP_CERT":"/etc/ssl/cert.pem"}` |
| **`sandbox.network.strictAllowlist`** (user): `curl https://example.org` is approved or prompts instead of failing; or `install.py` prints `strictAllowlist is not true` | The key is absent or `false` at user scope. Only user (or managed) scope denies; the project scope never does (`ADR-0024`) | Human runs the command that `install.py` prints (backup, then `jq` merge into `~/.claude/settings.json`) | `jq '.sandbox.network.strictAllowlist' ~/.claude/settings.json` prints `true`; `curl https://example.org` from a session is refused |
| **`sandbox.network.allowedDomains`** (user, base list) and new-domain procedure: `deny network-outbound <host>:443 (host is not on the allow list)` for `registry.npmjs.org` or another host | The host is not in the user-scope list, which holds `api.github.com`, `github.com`, `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`. Procedure, four steps: (1) agent reproduces the refusal; (2) agent prints the `jq` command with the new domain, **human** runs it; (3) agent re-measures the host and an unlisted control; (4) human decides whether the domain stays. Summary only: full table and PROHIBITED list in `rules/project_topology.md` section 5 | Human runs the printed command; the agent never edits `~/.claude/settings.json` and never routes around the proxy | `jq '.sandbox.network.allowedDomains' ~/.claude/settings.json` lists the domain; the listed host answers and `curl https://example.org` is still refused |
| **`gh` under the sandbox**: `tls: failed to verify certificate: x509: OSStatus -26276`; or the output stops at `(END)` | `gh` (Go TLS) fails certificate verification inside the sandbox (`S-5`); no `gh` exclusion may exist (`RA-09`, `N1`). `(END)` is the pager | Human runs the command the agent prepared, with the pager off: `GH_PAGER=cat gh pr list` (example). An unsandboxed session with no `HTTPS_PROXY` set may run it | The command prints its result and returns to the prompt with exit `0` |
| **`.env` unreadable by the agent**: `sh: ./.env: Operation not permitted`; a command cannot see a key stored only in `.env` | By design (`RA-09`): the agent never reads `.env` or prints a value from it. `Makefile` or `source .env` in a subshell is not sanctioned | Human runs the command that needs the key in their own shell. For graphify: `make graphify-deep` (host: `make -f .agents/Makefile graphify-deep`) | The human's run completes; the agent session still cannot read `.env` |
| **`pnpm` store**: `pnpm install` fails with `No such file or directory` under `.pnpm-store/v11` (the store path moved from its usual place to the repository) | Under the sandbox `pnpm store path` relocates the store to `<repo>/.pnpm-store/v11`, where writes fail (`S-6`); the host-reported `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK` was not reproduced | Human runs `pnpm store path` outside the sandbox and adds the printed path to `sandbox.filesystem.allowWrite` in `~/.claude/settings.json`; or the human runs the install unsandboxed | `pnpm store path` prints the path you added, and `pnpm install` completes |
| **pip TLS error `OSStatus -26276`** | Same cause as the `env` pair row: `trustd` is unreachable inside the sandbox (rows A1-7, A1-8, A1-10) | Merge the `env` pair (section 3.1) | `pip install --dry-run <package>` completes without the TLS error |
| **`git worktree` refused**: `git worktree add` exits `128` with `fatal: could not create leading directories of '.git/worktrees/<name>': Operation not permitted`; `git worktree remove` exits `255` with `failed to delete '.git/worktrees/<name>': Operation not permitted` | The sandbox write scope refuses writes under `.git/worktrees` (`docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` for `add`; Sprint 059 `KI-059-17` for `remove`) | Human runs `git worktree add <path> <branch>`, or `git worktree prune` and `git branch -D <branch>`, in their own shell; for a read-only replay the agent uses a scratch clone under `$TMPDIR` (the QA gate does) | `git worktree list` shows the expected state |

---
*See also: `rules/project_topology.md` section 5 (Reference) · `docs/decisions/ADR-0019-sandbox-regime.md` · `docs/decisions/ADR-0024-sandbox-egress-amendment.md` · `docs/guides/AUTONOMY_POSTURE_GUIDE.md`.*
