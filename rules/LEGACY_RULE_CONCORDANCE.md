# Rule Context: Legacy Rule Concordance

Before the tabular refactor of the governance ruleset (commit `36ab935`), governance rules were numbered ("Rule 1-113"). The refactor replaced numbers with keyed rows in `agents.md`, but historical citations survive in skill docs, templates, and vendored `-3rd` material — which the **Skill Documentation Veto** (`rules/skills_and_integrations.md §3`) forbids editing. This concordance makes every surviving numbered citation resolvable. Load it whenever you encounter a `Rule NN` reference; CI (`scripts/verify_references.py`) fails on any citation not mapped here.

| Legacy number | Current authority | Subject |
| :--- | :--- | :--- |
| **Rule 0 / 0.1** | `agents.md §0` (Documentation Entry Point) | Session entry and documentation index. |
| **Rule 1** | `agents.md §1 code_logic` | Technical English in all code/artifacts. |
| **Rule 10** | `agents.md §2 anti_amnesia` | Governance context alignment/re-read discipline. |
| **Rule 27** | `agents.md §1 code_logic` | Technical English in generated skill code. |
| **Rule 33** | `agents.md §5 historical_log` | Conventional Commits + `#[Sprint_ID]` suffix. |
| **Rule 35** | `agents.md §1 linter_command` | Linter gates (ruff / pnpm run lint). |
| **Rule 37** | `agents.md §3 dependencies` + `rules/project_topology.md` | Isolated local interpreters (venv prefix discipline). |
| **Rule 40 / 40.x** | *(removed)* | Was profile-scoped to a real production profile, self-defined and never a framework-wide rule; the profile itself was removed from this public repo (not published — see `RA-15`). No citation to resolve. |
| **Rule 41 / 041 / 41.x** | `rules/frontend_modular_standard.md` | Frontend modular standard (self-defined). |
| **Rule 52** | `agents.md §5 state_anchor` | State redundancy / mirror protocol (`.agent_state/mirror.json`). |
| **Rule 60** | `agents.md §3 three_file_standard` | Three-File Skill Standard for skills. |
| **Rule 66** | `agents.md §3 secret_sovereignty` + `RA-09` | Never read `.env` into context; secret shielding. |
| **Rule 70** | `rules/skills_and_integrations.md §1` | Skill discovery escalation ladder. |
| **Rule 71** | `agents.md §3 topological_order` + `rules/skills_and_integrations.md §3` | Flat skills topology + `-3rd` external suffix. |
| **Rule 74 / 75** | `agents.md §4` (Memory Management) | KI distillation and zero-tolerance purge. |
| **Rule 78** | `skills/readme-standardizer/` (Gold Standard) | Institutional README/doc identity. |
| **Rule 79** | `agents.md §4 definitive_amnesia` | Log purge after ratification. |
| **Rule 83** | `agents.md §5 state_anchor` | `docs/active_state.json` as authoritative anchor. |
| **Rule 113** | `agents.md §3 federation` + `skills/slash-commander/` | Workflows accessible as slash commands. |

> New documents MUST cite keyed rules (`agents.md §N key` or `rules/<file>.md §N`) — numbered citations are legacy-only and frozen to this table.
