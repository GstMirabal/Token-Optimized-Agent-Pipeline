# 📦 Profile: example-project

Illustrative project-family pack, kept in the public repo purely to demonstrate the `profiles/[name]/` mechanism (`agents.md §3 topological_order`) end to end — a real production profile (with a project's real business rules, real app inventory, real domain-specific agents) does **not** belong in this public core. It lives in a private companion location for that project instead, and is only referenced locally via `--profile [name]` pointing at that path.

## Contents
| Path | What it adds |
| :--- | :--- |
| `rules/domain_example_standard.md` | Example of a project-family rule (data-normalization convention for a fictional domain). |
| `agents/domain_specialist_example.md` | Example of a project-family specialist agent, scoped to a fictional jurisdiction. |
| `skills/example-api-bridge-3rd/` | Example of a vendored `-3rd` skill wrapping a fictional external API. |
| `mcp/registry.json` | Example of project-specific MCP server registrations. |
| `docs/EXAMPLE_MANIFEST.json` | Example of a project-specific manifest file a profile might carry. |

## Installation (opt-in only)
The base installer never links profiles. From the host project root:

**Illustrative pack inside the submodule** (this repo only):

```bash
.agents/scripts/install.sh --profile example-project
```

**Production / private profile outside the submodule** (RA-15 — your real project pack):

```bash
# Convention: host-root/.agents-profile/ or any path you control
.agents/scripts/install.sh --profile-path .agents-profile
# or
.agents/scripts/install.sh --profile-path /path/to/your-profile
```

The profile directory MUST contain the same layout: `agents/`, optional `skills/`,
`rules/`, optional `mcp/registry.json`.

## Governance
- Profile contents follow the same governance ruleset (`agents.md`) as the core framework.
- New project-specific learning goes into a profile like this one (or a new `profiles/[name]/`), never into the framework's core `rules/`, `agents/`, or `skills/` (`agents.md §3 topological_order`).
- **Real, production project profiles are not committed to this public repo.** See `RA-15` (`agents.md §7`) and `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` for why.
