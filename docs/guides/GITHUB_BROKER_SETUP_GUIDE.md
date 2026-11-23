# How-to: Set up the GitHub App broker on a human machine
**File**: `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` (RA-06 Option B naming)
**Module**: GITHUB_BROKER

---

## 1. Goal
The human creates the GitHub App, places two keys, writes `config.json`, installs the broker with `scripts/install_broker.py` and registers it at user scope, so that unit A-10 can measure it. Why the broker has this shape: `docs/decisions/ADR-0025-github-app-broker.md`; module facts: `docs/architecture/GITHUB_BROKER_BLUEPRINT.md`.

Every step below is run by the human in a terminal outside the sandbox. The agent runs none of them (ADR-0025 section 3, last row). Record exit codes and fingerprints only; never paste key material, a token or a `config.json` value into a chat, a commit or a log (`RA-09`).

## 2. Prerequisites

| Item | Done-criterion |
| :--- | :--- |
| A GitHub account that owns the nucleus repository | The human can open the repository's Settings page |
| `python3`, `openssl`, `git`, `ssh-keygen` on `PATH` (the broker uses the Python standard library, `openssl` and `git`: `scripts/github_broker.py` lines 31-43, 242, 426) | `command -v python3 openssl git ssh-keygen >/dev/null; echo $?` prints `0` |
| `claude` CLI on `PATH` | `command -v claude >/dev/null; echo $?` prints `0` |
| Current directory is the nucleus checkout root | `test -f scripts/github_broker.py; echo $?` prints `0` |
| The agent has not created `~/.config/agents-broker/` | `test ! -e ~/.config/agents-broker; echo $?` prints `0` on a first setup |

## 3. Steps

### 3.1 Create the GitHub App and install it on the nucleus only (ADR-0025 D4)

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Create a GitHub App under the owner account (GitHub Settings, Developer settings, GitHub Apps, New GitHub App) | The App named by the human | The App's settings page opens |
| 2 | Set Repository permissions: **Contents** = Read and write; **Pull requests** = Read and write; **Metadata** = Read-only | App permissions | The permissions list shows exactly these three entries |
| 3 | Leave **Administration** (and every other permission) at "No access" | App permissions | `Administration` is absent from the permissions list |
| 4 | Install the App on the nucleus repository only (installation target "Only select repositories", one repository) | Nucleus repository | The installation page lists one repository, the nucleus |
| 5 | Copy the **App ID** from the App's settings page and the **installation ID** from the installation page URL | `app_id`, `installation_id` for step 3.4 | Both are numbers held by the human, not pasted into chat |

### 3.2 Place the App private key (path read by the broker: `keys/app_private_key.pem`, `scripts/github_broker.py` line 241)

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Run `mkdir -p -m 700 ~/.config/agents-broker/keys` | Broker home and key directory | `stat -f '%Lp' ~/.config/agents-broker/keys` prints `700` (Linux: `stat -c '%a'`) |
| 2 | On the App's settings page, press "Generate a private key"; the browser downloads one `.pem` file | App private key | A `.pem` file exists in the downloads directory |
| 3 | Run `mv <downloaded-file>.pem ~/.config/agents-broker/keys/app_private_key.pem` | `keys/app_private_key.pem` | `test -f ~/.config/agents-broker/keys/app_private_key.pem; echo $?` prints `0`; `test ! -e <downloaded-file>.pem; echo $?` prints `0` |
| 4 | Run `chmod 600 ~/.config/agents-broker/keys/app_private_key.pem` | Key file mode | `stat -f '%Lp' ~/.config/agents-broker/keys/app_private_key.pem` prints `600` |
| 5 | Run `openssl rsa -in ~/.config/agents-broker/keys/app_private_key.pem -noout >/dev/null 2>&1; echo $?` | Key parses as an RSA key | Prints `0` (no key content is printed) |

### 3.3 Generate the tag-signing key (ADR-0025 D6-detail; the human generates it, never the agent, RV-15)

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Run `ssh-keygen -t ed25519 -N "" -C agents-broker -f ~/.config/agents-broker/keys/tag_signing`. The passphrase is empty because the broker passes none to `git tag -s` (`scripts/github_broker.py` lines 426-433) | `keys/tag_signing` and `keys/tag_signing.pub` | `test -f ~/.config/agents-broker/keys/tag_signing && test -f ~/.config/agents-broker/keys/tag_signing.pub; echo $?` prints `0` |
| 2 | Run `chmod 600 ~/.config/agents-broker/keys/tag_signing` | Private key mode | `stat -f '%Lp' ~/.config/agents-broker/keys/tag_signing` prints `600` |
| 3 | Print the public key fingerprint: `ssh-keygen -lf ~/.config/agents-broker/keys/tag_signing.pub` | Fingerprint A | One line `256 SHA256:... agents-broker (ED25519)`; the human notes the `SHA256:` value |
| 4 | Print the fingerprint of the key in the signer list: `cut -d' ' -f3- config/allowed_signers \| ssh-keygen -lf -` | Fingerprint B (line `agents-broker namespaces="git" <public key>`, landed by unit A-06) | One line; the `SHA256:` value equals fingerprint A |

**If fingerprint B differs from fingerprint A**: the line in `config/allowed_signers` holds another key. The human gives the agent only the **public** key value (the second and third fields of `keys/tag_signing.pub`); the agent replaces the key value in the line and keeps the prefix `agents-broker namespaces="git"`. Then step 4 is repeated until the fingerprints match. The private key `keys/tag_signing` is never pasted, printed or sent.

Check of the signer line: `grep -c "^agents-broker namespaces=\"git\"" config/allowed_signers` prints `1`.

### 3.4 Write `config.json`

The human creates `~/.config/agents-broker/config.json` as a JSON object with these fields. `scripts/github_broker.py` reads them as listed; the values are the human's.

| Field | Meaning | Read at |
| :--- | :--- | :--- |
| `app_id` | App ID from step 3.1.5; required, non-empty (used as the JWT `iss`) | lines 144-146, 239 |
| `installation_id` | Installation ID from step 3.1.5; required, non-empty | lines 144-146, 260 |
| `repository` | The nucleus repository as `owner/name`; required; must match `[\w.-]+/[\w.-]+` | lines 144-148, 222 |
| `required_checks` | JSON list with the names of the 3 required check runs that `merge_pr` requires in `success` (ADR-0025 D4); not validated at startup, but `merge_pr` is refused when it is not configured | lines 373-378 |

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Create `~/.config/agents-broker/config.json` with the four fields | `config.json` | `test -f ~/.config/agents-broker/config.json; echo $?` prints `0` |
| 2 | Run `chmod 600 ~/.config/agents-broker/config.json` | File mode | `stat -f '%Lp' ~/.config/agents-broker/config.json` prints `600` |
| 3 | Run `python3 -I -c 'import json,sys; c=json.load(open(sys.argv[1])); ok=all(c.get(k) for k in ("app_id","installation_id","repository")) and isinstance(c.get("required_checks"),list) and len(c["required_checks"])==3; sys.exit(0 if ok else 2)' ~/.config/agents-broker/config.json; echo $?` | Field presence and shape, no value printed | Prints `0` |

### 3.5 Install the broker with `scripts/install_broker.py`

**Contract this guide defines for unit A-04** (basis: ADR-0025 D5; `tests/test_install_broker.py` is A-04's check):

| Item | Contract |
| :--- | :--- |
| Run from | The nucleus checkout root: `python3 scripts/install_broker.py ...` (host form `python3 .agents/scripts/install_broker.py`; `agents.md` section 0, Command paths) |
| Flags | Exactly one of `--tag vX.Y.Z` or `--commit <40-hex SHA of a commit of main>`; neither or both is an error |
| `--tag vX.Y.Z` | Verifies the tag signature against `config/allowed_signers`, then copies `scripts/github_broker.py` from `git show <tag>:`, never from the working tree |
| `--commit <sha>` | First bootstrap only (no signed tag exists yet): the human names a commit of `main`; copies `scripts/github_broker.py` from `git show <sha>:`, never from the working tree |
| Destination | `~/.config/agents-broker/` (file `github_broker.py`) |
| Exit `0` | The file was copied |
| Exit `2` | The tag has no valid signature or is invalid; or the commit is not a commit of `main` |
| After unit M-18 | The same invocation also installs `scripts/graph_mcp.py` with the same verification (plan row M-18) |

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | First bootstrap: run `python3 scripts/install_broker.py --commit <40-hex SHA of a main commit>`. Later installs: run `python3 scripts/install_broker.py --tag vX.Y.Z` | `~/.config/agents-broker/github_broker.py` | Exit `0`; `test -f ~/.config/agents-broker/github_broker.py; echo $?` prints `0` |
| 2 | Negative control: run `python3 scripts/install_broker.py --tag v0.0.0; echo $?` (a tag that does not exist and carries no valid signature) | Installer refusal | Prints `2` |

### 3.6 Register the broker at user scope (ADR-0025 D2)

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Run `claude mcp add --scope user --env AGENTS_BROKER_HOME="$HOME/.config/agents-broker" agents-broker -- python3 "$HOME/.config/agents-broker/github_broker.py"` | User-scope registration `agents-broker` (stdio server; `python3`; the variable `AGENTS_BROKER_HOME`, `scripts/github_broker.py` line 122) | Exit `0` |
| 2 | Run `claude mcp list` | Registered servers | The output contains a line for `agents-broker` |
| 3 | Run `grep -c agents-broker claude/mcp.json` | Project template stays free of the broker (ADR-0025 D2; never in the project `.mcp.json`) | Prints `0` |
| 4 | Run `AGENTS_BROKER_HOME="$HOME/.config/agents-broker" python3 "$HOME/.config/agents-broker/github_broker.py" </dev/null; echo $?` | Broker starts, reads `config.json`, exits when stdin closes | Prints `0` (`2` means `config.json` is missing or invalid, `scripts/github_broker.py` lines 26-28, 652-654) |

### 3.7 Register the read-only graph MCP server at user scope (units M-04 and M-18, RV-28)

`scripts/graph_mcp.py` does not exist until unit M-04; `scripts/install_broker.py` installs it only after unit M-18. Run this section after M-18 and before M-16 (RV-35). This guide states nothing about the server's behaviour beyond the plan rows M-04 and M-18.

| # | Operation | Target | Done-criterion |
| :--- | :--- | :--- | :--- |
| 1 | Run `test -f ~/.config/agents-broker/graph_mcp.py; echo $?` (precondition: the file installed by `install_broker.py` per M-18) | Installed server file | Prints `0`; if it prints `1`, stop: re-run step 3.5 after M-18 has landed |
| 2 | Run `claude mcp add --scope user graphify -- python3 "$HOME/.config/agents-broker/graph_mcp.py"` | User-scope registration `graphify` (the name of the project-scope entry that unit M-05 removes from `claude/mcp.json`) | Exit `0` |
| 3 | Run `claude mcp list` | Registered servers | The output contains a line for `graphify` |

Arguments and environment of this server are fixed by unit M-04. The commit of M-18 re-reads this section and amends step 2 if M-04 needs another form (RV-36).

## 4. Verify it worked

```bash
test "$(stat -f '%Lp' ~/.config/agents-broker/keys/app_private_key.pem)" = 600; echo $?
test "$(stat -f '%Lp' ~/.config/agents-broker/keys/tag_signing)" = 600; echo $?
grep -c "^agents-broker namespaces=\"git\"" config/allowed_signers
grep -c agents-broker claude/mcp.json
claude mcp list
```

Expected output: `0`, `0`, `1`, `0`, then a server list that contains `agents-broker`.

## 5. What the agent never does

Source: ADR-0025 section 3 (last row), D3, D5, D6-detail.

| The agent never | Reason (source) |
| :--- | :--- |
| Creates or installs the GitHub App | Human step (ADR-0025 section 3, last row) |
| Generates, reads or prints the App private key or `keys/tag_signing` | D3; D6-detail (RV-15); `RA-09` |
| Reads `~/.config/agents-broker/**` or `~/.claude.json` | `permissions.deny` of D3 |
| Runs `scripts/install_broker.py` | Human step; D5 |
| Installs the broker from the working tree | D5 (install reads `git show <tag>:` or a named `main` commit) |
| Registers the broker in `claude/mcp.json` or the project `.mcp.json` | D2 |
| Writes anything into `config/allowed_signers` except the public-key value the human pastes | D6-detail |
| Receives the installation token | D1 (the token stays in the broker process) |

## 6. Measurement handoff

After sections 3.1 to 3.6 are done, unit A-10 records `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` M1-M4. Boundary claims are limited to the set that file enumerates (`RA-19`). This guide makes no boundary claim.

## 7. If something goes wrong

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Step 3.6.4 prints `2` | `config.json` missing, not valid JSON, or lacks `app_id`, `installation_id` or `repository` (`scripts/github_broker.py` lines 139-148) | Repeat section 3.4 and its step 3 |
| `install_broker.py` exits `2` with `--tag` | The tag has no valid signature against `config/allowed_signers` | Compare fingerprints (section 3.3 steps 3-4); do not bypass with `--commit` for a tag |
| `install_broker.py` exits `2` with `--commit` | The commit is not a commit of `main` | Name a 40-hex SHA that is on `main` |
| `merge_pr` is refused with "`required_checks` is not configured" | The field is absent or empty (`scripts/github_broker.py` lines 373-375) | Add the field (section 3.4) and restart Claude Code |
| `claude mcp list` has no `agents-broker` line | The registration ran at another scope or failed | Re-run section 3.6 step 1 with `--scope user` |

---
*See also: `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` (Reference), `docs/decisions/ADR-0025-github-app-broker.md` (Explanation).*
