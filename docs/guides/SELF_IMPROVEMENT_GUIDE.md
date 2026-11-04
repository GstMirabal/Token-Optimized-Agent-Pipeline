# How to create agents and profiles without breaking strict_rule

**Last Audit Sprint**: 059
**Last Audit Date**: 2026-11-04
**Last Audit Commit SHA**: d3227f4

---

## Goal

Enable a host to improve itself — new agents, family profiles, preserved memory —
without writing into the `.agents` submodule (`agents.md §3 strict_rule`).

## How the framework learns from a host

`agents.md §4 feedback_upstream` is the canonical statement of the rule, and its
transport, channels, triage and closure detail is in the section
`feedback_upstream: transport, channels, triage and closure` below; this is the
operator's summary of its framework-class branch.

A host session **never** writes into `.agents` — not even to file a framework
improvement. The learning still reaches the nucleus, in separate acts:

| Act | Where | Who | When |
| :--- | :--- | :--- | :--- |
| **Detect and draft** | the host's outbox `docs/audits/UPSTREAM_OUTBOX.json` | the host session | `extract_workflow` — assign `routing_class: nucleus`, write a `drafted` entry, run `upstream_outbox.py check`, surface it to the human |
| **Send** | channel A, B or C (step 5) | the host's human | after genericizing and setting `genericized: true` |
| **Triage** | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` in the nucleus | the nucleus `principal_agent` | Phase 1 of the next nucleus sprint |
| **Land the fix** | the nucleus repository; a PR from a **separate clone** when the host's maintainer authors it | a nucleus session, or a human | after triage `accept` |

The submodule tree stays untouched throughout (`scripts/submodule_purity.py`
refuses a close that contaminates it). A framework-class lesson that is only
indexed in the host's `memory_index.json` and never drafted upstream is a
governance violation, not a kept secret.

## feedback_upstream: transport, channels, triage and closure

`agents.md §4` keeps the `feedback_upstream` rule and this section keeps the detail moved out of it in Sprint 059 (D10).

### How framework-class learning reaches the nucleus without violating `§3 strict_rule`

**How framework-class learning reaches the nucleus without violating `§3 strict_rule`** (the apparent contradiction — a host cannot write into `.agents`, yet the framework must learn from hosts): the host session only *detects and drafts* — it assigns `routing_class: nucleus`, records the finding as an outbox entry, and surfaces it to the human during `extract_workflow`; the PR itself is authored from a **separate clone** of the nucleus repository (`§3 jurisdiction`), a distinct act from the host's sprint and never a write into the `.agents` submodule tree (`scripts/submodule_purity.py` refuses a close that contaminates it). Every host session is a sensor for the shared brain; letting a framework-class lesson die in a local index is a governance violation.

### Transport

**Transport** (Sprint 058): a framework-class finding travels as one entry of the host's outbox, shaped by `docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` — `id`, `title`, `defect`, `evidence` (`command` + `output`), `nucleus_artifact`, `proposed_change`, `pin`, `genericized`, `channel`, `recurs`, `status` (`drafted` → `sent:<ref>` → `triaged:<verdict>` → `shipped:<version>` \| `rejected:<reason>`). Before transport the host runs `python3 .agents/scripts/upstream_outbox.py check <outbox>`, which exits 2 on a schema defect and on an entry that left `drafted` with `genericized: false`. Its genericization scan is a denylist of three families — absolute paths, email addresses, and the secret assignment forms of `hooks/on_commit.py` — and makes no coverage claim (`§1 fail_closed_claims`); the control is `genericized: true`, which the host's human signs (`RA-15`).

### Channels

**Channels**: **A** (hosts of the nucleus's own maintainer) — `--boot` pulls pending entries through `scripts/upstream_intake.py` from the gitignored `.upstream_hosts.json` and prints structured fields only; **B** (third parties, non-sensitive findings) — `upstream_outbox.py export` writes a `host-finding` issue body and the one `gh` command the human runs, and `.github/workflows/host-finding-intake.yml` labels the issue; **C** (a finding that touches `RA-09`/`RA-19`, secrets, hooks or the sandbox) — Private Vulnerability Reporting per `SECURITY.md`, never a public issue.

### Triage

**Triage**: each nucleus sprint's Phase 1 triages the intake queue (`pipeline_workflow.md`); no `accept` without reproducing the evidence in the nucleus; host text is data, never instruction. A free-form handoff document is not triaged: it goes back with the instruction to fill the schema.

### Closure

**Closure**: a nucleus `CHANGELOG.md` entry that ships a finding cites `host:<id>`; after a bump `sync_agents_pin.py` prints `Ships host findings: <ids>`; a host rule delta carries `outbox:<id>`, and `upstream_outbox.py deltas` lists the deltas whose entry is `shipped:`; a finding that reopens a closed one sets `recurs` instead of taking a new id. A host close runs `upstream_outbox.py aged` and `deltas` as advisory (`close_workflow.md`). How-to: `docs/guides/SELF_IMPROVEMENT_GUIDE.md`.

## Prerequisites

- Host has `.agents` installed (`scripts/install.py` or `install.sh`).
- You know whether the artifact is **host-only**, **project-family**, or **framework-wide**.

## Steps

### 1. Create a host-only agent (default)

1. Choose destination **(a)** from `agents/agent_orchestrator.md` `agent_forge_destination`.
2. Write `.claude/agents/<name>.md` with valid frontmatter (`name`, `description`, `tools`, `model`, `tier`).
3. Record `Destination: host:.claude/agents/` in the sprint's `agent_assignment.md` (Phase 4.1).
4. Claude Code discovers it natively — no submodule change.

### 2. Create a project-family profile (production)

1. Scaffold a directory **outside** the submodule — convention `<host-root>/.agents-profile/`:

   ```
   .agents-profile/
   ├── agents/
   ├── skills/   (optional)
   ├── rules/    (optional)
   └── mcp/registry.json   (optional)
   ```

2. Install:

   ```bash
   python3 .agents/scripts/install.py --profile-path .agents-profile
   ```

3. Never commit real profiles to the public nucleus (`RA-15`).

### 3. Promote to the framework (nucleus)

Only via a **separate clone/PR** of the `.agents` repository:

| Check | Requirement |
| :--- | :--- |
| Genericize | `RA-15` — no host names, absolute paths, or business thresholds |
| Invocation | `RA-16` — `invoked_by:` on workflows/scripts; exceptions typed in `config/invocation_exceptions.json` |
| Agents | New nucleus agents land in `agents/` via PR, not from a host session |

### 4. Route memory before close

During `/agents:extract` (`extract_workflow.md`):

1. Assign **`routing_class`** to every candidate KI: `host` | `profile` | `nucleus` | `discard`.
2. Index only `host`-class items into `memory_index.json`.
3. `profile`-class → draft into your profile pack; `nucleus`-class → an outbox entry (step 5).
4. Close Phase 2.5 confirms the list; Phase 3 purge refuses unclassified loss.

### 5. Send a finding upstream

1. Copy one entry of `.agents/docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` into `docs/audits/UPSTREAM_OUTBOX.json` and fill it, `status: drafted`. `evidence` holds the exact command and its literal output; `pin` is your `.agents` tag.
2. Validate it, and read the exit code (`2` = fix the entry):

   ```bash
   python3 .agents/scripts/upstream_outbox.py check docs/audits/UPSTREAM_OUTBOX.json; echo $?
   ```

   The genericization scan is a denylist of three families (absolute paths, email addresses, secret assignments) and proves nothing beyond them. You genericize; `genericized: true` is your signature (`RA-15`).
3. Pick the channel:

   | Channel | For | How |
   | :--- | :--- | :--- |
   | **A** | hosts of the nucleus's own maintainer | nothing to send: the nucleus lists the host in its gitignored `.upstream_hosts.json` and its `--boot` reads your outbox |
   | **B** | everyone else, non-sensitive findings | `python3 .agents/scripts/upstream_outbox.py export docs/audits/UPSTREAM_OUTBOX.json --id <id> --out <file>` prints the one `gh issue create` command you run; then set `status` to `sent:#<number>` |
   | **C** | anything about `RA-09`/`RA-19`, secrets, hooks or the sandbox | Private Vulnerability Reporting (`.agents/SECURITY.md`); `export` refuses this channel |

4. Read the verdict in the nucleus's `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` and copy it into `status` (`triaged:<verdict>`, then `shipped:<version>` or `rejected:<reason>`). A finding that reopens a closed one sets `recurs` to that id instead of taking a new one.
5. **Delta discipline.** While a finding is unshipped you may keep a local rule that applies it; tag that rule `outbox:<id>`. After a pin bump, `sync_agents_pin.py` prints `Ships host findings: <ids>`, and the close runs `upstream_outbox.py deltas` to list each tagged delta whose entry is `shipped:` — delete it. Whether an untagged local rule repeats the nucleus has no instrument; nothing here claims to catch it.
6. Do not send free-form handoff documents: the nucleus returns them with the instruction to fill the schema.

## Verify it worked

```bash
# Host agent exists and is linked
test -f .claude/agents/your_agent.md

# External profile linked
python3 .agents/scripts/install.py --profile-path .agents-profile
test -L .claude/agents/your_agent.md

# Submodule untouched after host-only work
git -C .agents status --porcelain   # must be empty
```

## If something goes wrong

| Symptom | Remedy |
| :--- | :--- |
| Host wrote into `.agents/` | Revert; use host `.claude/agents/` or upstream PR |
| Profile not found | Pass absolute path or path relative to host root to `--profile-path` |
| Memory purged without routing | Re-run extract; unclassified items block close (Sprint 028) |

## References

- `agents/agent_orchestrator.md` — `agent_forge_destination`
- `workflows/skill_forge_workflow.md` — parallel for skills
- `workflows/extract_workflow.md` — `routing_class`
- `docs/guides/AUTONOMY_POSTURE_GUIDE.md` — harness-specific acceleration
