# 📜 ADR-0004: No model-selector agent

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 029
**Last Audit Date**: 2026-08-25

---

## 1. Context

A human asked for an agent specialised in choosing which AI model each agent
should use. `agents/token_economy_agent.md` already owns Filter 5 (script vs
agent judgment) and the tier table. Usage reports attributed **100% of spend**
to subagent-heavy sessions
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, Sprint 028 appendix —
recommendation on the model selector).

Sprint 022 already maps role → tier → model in `config/model_tiers.json`. The
missing piece is the **exception** (declared escalation in `task_scope.md`), not
a new dispatcher.

## 2. Decision

**Do not create a model-selector agent.** Model choice is:

1. **Static** for the role's default tier (`config/model_tiers.json` + profile
   `tier:` / `model:` aliases).
2. **Declared** when difficulty diverges — `token_economy_agent` proposes,
   `rule_validator` transcribes into `task_scope.md`, the human sees it
   (`F-026-A2`).

Launching a subagent per task to pick a model is PROHIBITED: it spends the unit
of cost the program exists to reduce.

## 3. Consequences

**Easier**: one mapping file and one escalation path; no extra always-on agent in
the eight-role pipeline.

**Harder**: humans must read `Declared escalations` in `task_scope.md`; a missed
escalation runs the wrong tier until a gate or human notices.

**Left to Sprint 030**: automatic `tier_escalation` assistance (`F-026-A2`), still
without a selector agent.

## 4. Deciders

Program authors; human rejected the selector-agent request during the 021–030
queue design. Recorded as ADR in Sprint 029.

## 5. Considered Options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Create a selector agent** | Centralises choice | Costs a subagent per decision; duplicates `token_economy_agent` |
| **Only static table, no escalations** | Zero judgment | Mechanical roles stuck when asked to author (e.g. Dockerfile units) |
| **Static table + declared escalation (this ADR)** | Free default path; visible exceptions | Requires Phase 4.3 discipline |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0004-no-model-selector-agent.md`.*
