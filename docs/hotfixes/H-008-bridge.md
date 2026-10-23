# 🚑 Hotfix: H-008-bridge
**File**: `docs/hotfixes/H-008-bridge.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `CRITICAL`
**Detected**: 2026-10-23 · **Resolved**: 2026-10-23

---

## 1. Symptom

Sprint 056 closed `SANDBOX_ENUMERATION.md` `E10` by adding `-I` to the `graphify` MCP server of
the template (`246cd20`). Without `-I`, `python -m graphify.serve` puts the host root first on
`sys.path`, so a `graphify/serve.py` that the sandboxed agent writes in the host root runs outside
the sandbox when Claude Code starts the server. The fix reached fresh installs only. Measured on
2026-10-23, five local hosts bridged before `246cd20` (all at `v4.38.0` or earlier) still carry
`"args": ["-m", "graphify.serve", "graphify-out/graph.json"]`. Re-running the installer does not
repair them. It produces `["-m", "graphify.serve", "graphify-out/graph.json", "-I"]`, where `-I`
is an argument to the module and does not isolate the interpreter. QA Gate round 5 of Hotfix
`H-007` measured that shape running a shadow `graphify/serve.py` (`F-H007-R5-1`).

The same merge keeps MCP servers the template has retired. One host holds both `git-sync-agent`
and an older name for the same launcher, `github-sentinel`. Each ran an unpinned registry package
with a GitHub token in its environment until `H-007` deleted the launcher.

## 2. Root Cause

`scripts/merge_json.py` merges every template value into the host file additively.
`_merge_list_append` appends the list items the host lacks, which treats `args`, an ordered argv,
as a set. `_merge_value` keeps the host's value for a conflicting scalar such as `command`. For
an MCP server the template owns, the merge therefore writes an entry the template does not
contain. Nothing removes a server the template stopped shipping: `RETIRED_VALUES` holds list
strings, not mapping keys.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `scripts/merge_json.py` | In `mcpServers`, every server the template defines replaces the host entry of that name as a whole. A host entry that differed is reported. A retired server is removed when its launch equals a launch the framework shipped. A host-changed retired entry is kept and reported |
| `tests/test_merge_json.py` | Pin that after a merge, every template-defined server equals the template entry, for each historical host shape. Pin that retired servers are removed only when their launch matches |

Branch/commit: `hotfix/H008` → `f98f4d2`; `E10` correction in `SANDBOX_ENUMERATION.md` `86bab2a` (hotfixes may merge outside the sprint cycle, but never unreviewed). **Branch prefix is mandatory (`agents.md` RA-03)** — `fix/`, `feat/`, and `chore/` branch names are protocol loss even when the Conventional Commits message type is `fix`.

**Perimeter (`agents.md §1 fail_closed_claims`).** Covered: the `mcpServers` entries the template
defines, and the retired servers listed in `scripts/merge_json.py`, in any `.mcp.json` the merge
writes (`scripts/install.py` `merge_into` and `scripts/merge_json.py` `main`). Not covered:
- MCP servers the host defines itself. These are host jurisdiction.
- A host that does not re-run the installer after the pin bump. The repair happens at the next merge.
- Hook entries duplicated by the merge. `install.merge_into` does not call
  `prune_deprecated_hooks`. These are not a security vector because they run the same code, and
  they are routed to Sprint 057.
- Retired permission/sandbox list values (`KI-056-3`).
- The code a server runs.

## 4. Verification

- The new tests fail on the parent commit and pass at the fix (`Repro:` trailer on `f98f4d2`;
  `python3 scripts/check_fix_reproduces.py --range main..HEAD` exits `0`).
- Copies of the `.mcp.json` of the five local hosts, merged with `scripts/merge_json.py`: every
  template-defined server equals the template entry, and `github-sentinel` is removed.
- `make verify` exits `0`.

## 5. Rule Amendment Check
- [ ] Is this failure class systemic? Yes. A fix to a template value reached fresh installs only, and no check compared the merged host result with the template. The rule question is routed to Sprint 057: should every template change that closes a vector carry a merge test over the historical host shapes?
- [ ] Does the root cause reveal a design decision worth recording? Yes. The template owns the servers it names. N/A here; recorded in this file
- [x] Master Ledger entry added under `[Unreleased]`.
