# 📜 ADR-0007: Cursor without API delegation

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 4 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 029
**Last Audit Date**: 2026-08-25

---

## 1. Context

Sprint 026's objective was portability: the same repository opens under Cursor or
Claude Code with coherent state. Cursor has **no subagent primitive**, so the
eight-role pipeline cannot dispatch natively
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, Sprint 026 appendix).

One proposed mitigation was to call the Anthropic API from Cursor sessions to
spawn Claude-side subagents. The human decision recorded in that appendix:

> *no calls to the Anthropic API (human decision: "for that I use Claude").*

| Layer | Ports without API? |
| :--- | :--- |
| Constitution, commands, scripts, git hooks, MCP path | Yes |
| Session hooks / `permissions.deny` | Partial / declared gaps |
| Eight-role subagent dispatch | No — sequential ruleset adoption instead |

## 2. Decision

**Cursor sessions do not delegate pipeline roles through the Anthropic API.**
Portability means:

- `delegation_mode: sequential` under Cursor (`session_state.py claim --tool cursor`).
- Authoring units adopt one profile's ruleset at a time; gates still run in
  **fresh context** (mandatory), transcribed by `orchestrator`.
- Operators who want native eight-role dispatch use Claude Code for that work.

Reopening API delegation requires a new ADR that states credentials handling,
cost attribution, and how `delegation_conflict` changes — not a silent adapter.

## 3. Consequences

**Easier**: no second supply chain of API keys inside Cursor; no fake "native"
pipeline that is actually a remote fan-out.

**Harder**: Cursor cannot match Claude Code's parallel role isolation; sequential
mode must still produce `task_scope.md` and Phase 7 verdicts or the same silent
failure class returns (host precedent in Obstacle 2 of Sprint 026).

## 4. Deciders

Human owner during Sprint 026 planning; recorded as ADR in Sprint 029.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Anthropic API fan-out from Cursor** | Restores multi-role dispatch | Credentials, cost double-counting, contradicts "for that I use Claude" |
| **Single agent covers all phases** | Simple | Proven failure: skipped Phases 4 and 7, disabled isolation rules |
| **Sequential rulesets + mandatory fresh gates (this ADR)** | Portable without API | Slower authoring; human switches models per unit via UI |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0007-cursor-without-api-delegation.md`.*
