# 📜 ADR-0009: Implementer role

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 033
**Last Audit Date**: 2026-08-25

---

## 1. Context

`F-021-A2`: eight of thirteen profiles held `Write`/`Edit` and none was an
implementer. Sprint 023 unit `C5` closed `F-086-A1` by giving
`devops_agent` write tools over framework-root `scripts/` and `hooks/`.
That owner is an environment role on `mechanical`/`haiku`. Every later
sprint excluded the role-map redesign as out of scope.

`tester_agent` and `qa_agent` remain gate-tier without `Write`
(`F-026-A1`): they verify; they do not author tests.

## 2. Decision

Add an **auxiliary** profile `implementer-agent`
(`agents/implementer_agent.md`): `tier: author`, family alias `sonnet`,
tools including `Write`/`Edit`/`Bash`. It owns framework-root `scripts/`,
`hooks/`, and `tests/`. It is **not** a ninth core pipeline role.

Transfer `Write`/`Edit` for those trees from `devops_agent` to
`implementer_agent`. `devops_agent` keeps `Bash` for venv, `.env` export,
Docker health, purge, and close git routines. `skills/[name]/scripts/`
stays with `skill_architect`.

`token_economy_agent` requests changes to its owned scripts through
`implementer_agent`.

Rejected: promoting `devops_agent` to `author`; a ninth core role; dual
`Write` owners on the same tree.

## 3. Consequences

- `agent_orchestrator` assigns `scripts/`/`hooks/`/`tests/` units to
  `implementer_agent`, not `devops_agent`.
- The `F-021-A2` write-holder count may stay eight (devops exits, implementer
  enters); closure is identity of an implementer in that set, not the count.
- Nucleus and hosts that pin this tag gain a dispatchable author for code
  and tests without widening gate write grants.

---

## 4. Amendment 2026-11-22 (Sprint 060, unit O-12, finding RV-20)

The original decision (Section 2) limited `Write`/`Edit` to framework-root
`scripts/`, `hooks/` and `tests/`. Sprint 060 assigns about 20 Work rows to
`implementer_agent` whose target files lie outside those trees, and no other
profile holds `Write`/`Edit` on those paths.

`write_scope` in `agents/implementer_agent.md` now also covers, each only
when a plan Work row assigns the file to `implementer_agent`:

| Path | Note |
| :--- | :--- |
| `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/*_MEASUREMENT.md`, `*_REPORT.md` | Current sprint directory only. |
| `docs/audits/`, `config/`, `claude/`, `.github/` | Whole trees. |
| `Makefile`, `requirements-core.txt` | Single files. |

Still PROHIBITED: `agents.md`, `rules/`, `workflows/`, `agents/`,
`skills/[name]/scripts/` (stays with `skill_architect`), and secrets
(`RA-09`). The `tools:` line, the one-subject rule and Sections 1-3 are
unchanged.
