# 📜 ADR-0010: Cursor Task applies tier map

**Status**: `Accepted`
**Date**: 2026-08-26
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 035
**Last Audit Date**: 2026-08-26

**Related**: ADR-0003 · ADR-0004 · ADR-0007
**Supersedes (context only)**: the claim in ADR-0007 §1 that Cursor has no
subagent primitive and therefore cannot apply Model/Effort via Task.
**Does not supersede**: ADR-0007's prohibition on Anthropic API delegation.

---

## 1. Context

ADR-0007 recorded that Cursor had **no subagent primitive**, so under
`delegation_mode: sequential` the Model and Effort columns in `task_scope.md`
were ignored at runtime — the operator switched models in the UI, or the
session model ran everything.

Cursor `Task` now accepts a `model` argument (platform slugs). The static map
in `config/model_tiers.json` already binds role → tier → `(modelId, effort)`
per session tool (ADR-0003, ADR-0004). Without a resolver that returns those
pairs to `Task`, the map remains advisory under Cursor.

ADR-0007's **Anthropic API prohibition** stays in force: this decision does
not reopen remote Claude fan-out from a Cursor session.

## 2. Decision

**Runtime applies `config/model_tiers.json` under Cursor via**
`scripts/audit_cursor_models.py --resolve <tier|profile>`, which returns
`(modelId, effort)`.

| Case | Behaviour |
| :--- | :--- |
| Mechanical units and Phase 7 gates | Launch `Task` with the resolved `model` slug (or the escalated Model column from `task_scope.md` when declared) |
| `gate.cursor.model` is `null` | `--resolve gate` returns `session` — **never invent** a gate slug |
| Parent session | `delegation_mode` stays `sequential`; `Task` applies the column for that unit — it does **not** fan out eight Claude-style roles |

Filling a non-null `gate.cursor` cell by structural ceiling is a separate
decision (ADR-0011, Sprint 035 unit H1).

## 3. Consequences

**Easier**: Model/Effort in `task_scope.md` become enforceable under Cursor;
mechanical and gate units stop silently inheriting the chat picker when a map
cell exists.

**Harder**: callers must invoke `--resolve` (or the escalated column) before
every Cursor `Task` that claims a tier; a null gate cell still means session
model until ADR-0011 / H2 writes a ceiling.

**Unchanged**: no Anthropic API credentials or remote subagent spawn from
Cursor (ADR-0007 decision intact); no model-selector agent (ADR-0004); gates
do not drop tier for cost (ADR-0003).

## 4. Deciders

Human owner during Sprint 035 planning; recorded as ADR in Sprint 035
(Design D5 / unit E1).

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md`.*
