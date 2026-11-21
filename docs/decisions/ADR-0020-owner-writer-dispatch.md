# 📜 ADR-0020: The owner writes a bounded ledger seal without dispatching the writer
**Status**: `Accepted`
**Date**: 2026-11-21
**Triggers**: 2 (`rules/documentation_standard.md §3.1`) — changes a contract (`config/artifact_registry.json`'s schema) consumed by other containers (`scripts/check_role_artifact.py`, `scripts/docs_freshness_check.py`, `scripts/map_workflows.py`, `tests/test_artifact_registry.py`). Trigger #2 does not auto-escalate individually (`§3.2`), so this ADR is Nygard-format.
**Amends**: `ADR-0017` (`docs/decisions/ADR-0017-typed-artifact-writer.md`). `ADR-0017` stays `Accepted` and is not edited; this ADR adds one exception to its §2 and leaves every other clause in force.

---

## 1. Context

| Fact | Where to verify |
| :--- | :--- |
| Finding `C-7` — "The owner/writer split costs a dispatch per trivial step (`ADR-0017`)" — was triaged "accept for debate (needs a new ADR)", Sprint 059 | `grep -n "C-7" docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` (line 2137) |
| Sprint 059 plan rows: `P10` (the problem), `D7` (resolve with an ADR that amends `ADR-0017`; implement in the registry only if the ADR is approved; approved 2026-11-21 as `D79`), `D78` (bounds and enforcement), `F-01` (this file), `F-02` (the registry change), `F-03` (the check), `F-04` (the `ADR-0017` pointer) | `grep -nE "^\| (P10\|D7\|D78\|F-01\|F-02\|F-03\|F-04) " docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` |
| `ADR-0017` §2 splits each artifact into `role` (owner: accountable for content) and `writer` (what materializes the file); every `writer` must resolve to a profile holding `Write`/`Edit`, a script that exists, or a Makefile target that exists | `docs/decisions/ADR-0017-typed-artifact-writer.md` §2; `tests/test_artifact_registry.py::test_every_writer_resolves` |
| Three artifacts have `role: Principal Agent` and a different `writer`: `IMPLEMENTATION_PLAN.md` (`orchestrator`), `PHASE_REGISTER.md` (`doc_orchestrator`), `CHANGELOG.md` (`doc_orchestrator`) | `grep -n -B3 -A2 '"role": "Principal Agent"' config/artifact_registry.json` |
| The `principal_agent` profile declares no `Write` and no `Edit` | `grep -n "^tools:" agents/principal_agent.md` prints `tools: Read, Glob, Grep, TodoWrite` |
| `ADR-0017` §1.1 rejected granting `principal_agent` `Write`/`Edit` because a tool grant is all-or-nothing for the profile, not scoped to named paths, while a registry field can be asserted per artifact by a test | `docs/decisions/ADR-0017-typed-artifact-writer.md` §1.1, last paragraph |
| `ADR-0017` has no size condition: a two-line ledger seal of an owner-owned file costs the same dispatch (an agent launch, its context load and its return message) as a full document | `docs/decisions/ADR-0017-typed-artifact-writer.md` §2 states no exception |
| `scripts/check_role_artifact.py` reads `scope`, `required`, `role` and `filename` from each registry entry and does not read `writer` | `grep -n 'entry.get(' scripts/check_role_artifact.py` |
| `tests/test_artifact_registry.py` pins a minimum field set (`DECLARED_FIELDS`) and does not reject a key outside it (`note` is already such a key) | `grep -n "DECLARED_FIELDS" tests/test_artifact_registry.py` |
| Measured size of past changes (human decision `D78`, 2026-11-21). A ledger seal is a commit that renames `[Unreleased]` to a version in `CHANGELOG.md`. Across the 51 seal commits, lines added/deleted are: 2/0 in 16 since 4.24.0; 4/2 or 5/1 in 4 since 4.24.0 (`367e055`, 4.39.0, is 5/1; `d258b43`, `33d4c20` and `206f102` are 4/2); 3/1 in 10 from 4.10.0 to 4.17.0; 7/0 in the 2 hotfix seals 4.9.1 and 4.9.2; 11/0 to 13/13 in 3 before 4.4.0. A seal can replace lines, so `CHANGELOG.md` is not append-only. Closeout entries add 25 to 106 lines. `PHASE_REGISTER.md` is created whole in 35 of 36 commits (28 to 131 lines) | `git log --numstat --format='@%h %ad %s' --date=short -- CHANGELOG.md`, read over every commit whose subject contains `seal` (columns 1 and 2 per commit; the instrument for every seal figure in this ADR); `git log --numstat --format=%h%x20%s -- docs/sprints/*/PHASE_REGISTER.md` |

## 2. Decision

**Rule.** For an artifact that satisfies all three conditions below, the owner (`role`) MAY write the change itself, without dispatching the `writer`. The `writer` field keeps its `ADR-0017` meaning and value. Any change that fails a condition goes through the `writer` exactly as `ADR-0017` requires.

| # | Condition | Measured by |
| :--- | :--- | :--- |
| 1 | **Eligible artifact.** The registry entry declares `owner_writes`, and its `role` is `Principal Agent`. The eligible change is a **ledger seal**: a commit that renames `[Unreleased]` to a version in `CHANGELOG.md`. The property is: a change whose content the owner already authors, that is small and mechanical, and that no gate reads as content. Evidence, not definition (`rules/documentation_standard.md §6`): `CHANGELOG.md`, for ledger seals only. `PHASE_REGISTER.md` is not eligible: the measurement in §1 shows it is created whole in 35 of 36 commits (28 to 131 lines), so no commit fits the bound. Closeout entries of `CHANGELOG.md` are not eligible: they add 25 to 106 lines. `IMPLEMENTATION_PLAN.md` is not eligible: it is the first `triple_lock` lock and has no size bound | `grep -n "owner_writes" config/artifact_registry.json` lists only entries whose `"role"` is `"Principal Agent"` and whose `"filename"` is `CHANGELOG.md` |
| 2 | **Trivial change.** One commit changes the file by at most `max_added_lines` added lines and at most `max_deleted_lines` deleted lines | `git diff --numstat <commit>^ <commit> -- <path>`: column 1 (added) `<=` `max_added_lines`, column 2 (deleted) `<=` `max_deleted_lines` |
| 3 | **Bound declared in the registry.** The entry carries both numbers; absent either number the exception does not apply | `grep -n -A3 "owner_writes" config/artifact_registry.json` shows `max_added_lines` and `max_deleted_lines` |

**Bounds** (human decision `D78`; `F-02` writes them): `max_added_lines: 5`, `max_deleted_lines: 2`. Basis: the measurement in §1, taken with `git log --numstat --format='@%h %ad %s' --date=short -- CHANGELOG.md` over every commit whose subject contains `seal`. With these bounds every seal since 4.10.0 is covered (2/0, 4/2, 5/1 and 3/1). Not covered: the two 7/0 hotfix seals of 4.9.1 and 4.9.2 (7 added lines exceed 5), which stay dispatched, and the three seals before 4.4.0 (11/0 to 13/13). Closeout entries (25 to 106 added) exceed the bound by a wide margin. The exception is not append-only: a seal may delete up to 2 lines, because a seal can replace lines.

**Scope stated plainly.** The exception covers ledger seals of `CHANGELOG.md` only (a commit that renames `[Unreleased]` to a version). The 7/0 hotfix seals of 4.9.x and the three pre-4.4.0 outliers exceed the bounds and stay dispatched. Closeout `CHANGELOG.md` entries (25 to 106 added lines) exceed `max_added_lines`, and `PHASE_REGISTER.md` carries no `owner_writes` key, so both stay dispatched to the `writer` (`doc_orchestrator`).

**Registry shape F-02 encodes** (an optional key on an artifact entry; `ADR-0017`'s required fields are unchanged):

| Key | Type | Meaning |
| :--- | :--- | :--- |
| `owner_writes` | object | Present only on an entry meeting condition 1; absent means every change dispatches the `writer` |
| `owner_writes.max_added_lines` | integer `>= 1` | Upper bound for condition 2, added lines per commit |
| `owner_writes.max_deleted_lines` | integer `>= 0` | Upper bound for condition 2, deleted lines per commit |

**Not changed.** `writer`; the three `writer` forms; `test_every_writer_resolves`; the `principal_agent` profile's `tools:` line (granting it `Write` stays rejected for the reason `ADR-0017` §1.1 gives).

## 3. Consequences

**Easier**

- A ledger seal of `CHANGELOG.md` within 5 added and 2 deleted lines, written by the owner, no longer needs a dispatch, and the bound is a number in the registry that `scripts/check_role_artifact.py` (unit `F-03`) checks with `git diff --numstat`.
- The exception is per artifact and per commit, so it can be removed for one artifact by deleting one key.

**Harder / accepted risk**

| Consequence | Mapped to |
| :--- | :--- |
| The registry carries a second path to a file's bytes (owner as well as `writer`); a reader of `writer` alone no longer sees every legitimate author of an eligible artifact | `config/artifact_registry.json` `_fields` entry for `owner_writes`, added by unit `F-02` |
| Encoding the condition in the registry is unit `F-02`; `F-02` is pending (this ADR is accepted) and ends with `python3 scripts/check_role_artifact.py` exit 0 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` row `F-02` |
| Conditions 2 and 3 are not checked by any script today: `scripts/check_role_artifact.py` does not read `owner_writes`. Unit `F-03` makes it exit non-zero for an owner commit on an `owner_writes` artifact above `max_added_lines` or `max_deleted_lines` by `git diff --numstat`, with a paired test in `tests/test_check_role_artifact.py`. `F-03` does not exist yet; it is pending and runs after `F-02` | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` row `F-03` |
| `ADR-0017` carries no pointer to this ADR, because this ADR amends it and does not supersede it; a reader of `ADR-0017` alone would not learn of the exception. Unit `F-04` adds an `Amended by ADR-0020` line to the `ADR-0017` status (`rules/documentation_standard.md §6`, "annotated in place, never deleted"); `F-04` is pending | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` row `F-04` |
| The human approved this ADR on 2026-11-21 (plan decision `D79`), so `F-02`, `F-03` and `F-04` proceed; closing `C-7` in `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` is not done by this unit | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` rows `F-02`, `F-03`, `F-04` |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0020-owner-writer-dispatch.md`. Amends `ADR-0017` (`docs/decisions/ADR-0017-typed-artifact-writer.md`); source finding `C-7` (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:2137`).*
