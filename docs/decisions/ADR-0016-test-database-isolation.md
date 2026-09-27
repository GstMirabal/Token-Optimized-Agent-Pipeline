# 📜 ADR-0016: `local_testing` restated as test-database isolation, with a declared-deviation path

**Status**: `Accepted`
**Date**: 2026-09-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`) — changes a contract (`agents.md §3 local_testing`) consumed by every host and by `agents.md §3` itself, which every session in this framework reads. Trigger #2 does not auto-escalate individually (`§3.2`), so this ADR is Nygard-format.

---

## 1. Context

`agents.md §3 local_testing` today reads: *"Overwrite native URLs to
instantiate in RAM (`sqlite:///:memory:`)."* It names one engine
unconditionally, for every host regardless of what the host's own schema
requires.

Upstream finding `ADR-0006`
(`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` ~line 1264): a host with money
columns whose behaviour differs by database engine cannot honour the rule
without its suite passing while proving nothing about production. That host
declared the deviation in its own ADR and runs its tests on the real engine
— a path the framework's rule does not name.

Sprint 051 examined this entry and did not re-measure it: it is a lead
describing a host's **declared deviation** from a rule, not a defect in the
rule's machinery, so it carried no failing command to run. It stays open
because the deviation, while reasonable, is undocumented in the rule that
governs every other host — the reporting host built the escape hatch without
the framework naming one, which is silent divergence by construction.

The finding itself names the rejected alternative: leaving the rule as
written and letting hosts deviate silently. That is the status quo, and it
is what produced the gap — a host with a genuine fidelity requirement had no
sanctioned way to record it, so the deviation exists only in that host's own
project, invisible to `agents.md` and to any other host that hits the same
wall.

## 2. Decision

`agents.md §3 local_testing` is restated as *isolate the test database*,
not *use this one engine*. In-memory SQLite (`sqlite:///:memory:`) remains
the **default** for every project. A host whose fidelity requirement cannot
be met by SQLite (an engine-specific column type, extension, or query
behaviour SQLite does not emulate) MUST declare the deviation in a host ADR
naming: the fidelity requirement SQLite cannot satisfy, the real engine
substituted, and the isolation mechanism used in its place (an ephemeral
database or schema created per test run and torn down after — never a
shared or persistent database). An undeclared deviation — tests running
against a real, shared, or persistent database with no such ADR — remains
out of policy exactly as it was under the prior wording.

Proposed replacement text for the `agents.md §3 local_testing` row (applied
by companion unit `U15`, not by this ADR):

| Category | Rule (Key) | Value / Constraint (Value) |
| :--- | :--- | :--- |
| **QA Framework** | `local_testing` | Isolate the test database. Default: overwrite native URLs to instantiate in RAM (`sqlite:///:memory:`). A host whose fidelity requirement cannot be met by SQLite (engine-specific column types, extensions, or query behaviour) MUST declare the deviation in a host ADR naming the required engine and the isolation mechanism it substitutes (an ephemeral database/schema per test run, torn down after) — never a shared or persistent database. An undeclared deviation is a rule violation, not a project choice (`ADR-0016`). |

Rejected: leaving the rule unchanged and letting hosts deviate silently —
the status quo this ADR closes, and the alternative the upstream finding
itself already rejected.

## 3. Consequences

**Easier**

- A host with a real fidelity requirement (money columns, engine-specific
  behaviour) has a sanctioned path instead of the silent divergence the
  reporting host already had to build.
- A future audit can `grep` a host's test configuration for the required
  ADR citation instead of inferring intent from a persistent-database test
  setup that may or may not be deliberate.

**Harder / accepted risk**

- The rule now requires judgment ("cannot be met by SQLite") rather than
  naming one fixed value, which opens room for a host to over-claim a
  fidelity requirement to justify a more convenient but less isolated test
  database. The required ADR is the check on that claim — a human-readable
  justification, not a machine gate; no script in this repository
  currently parses `local_testing` compliance, and this ADR does not add
  one.
- Every host pinning a future tag inherits a rule that now branches on a
  judgment call instead of a single literal string, which is a harder rule
  to grep for compliance than the one it replaces.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0016-test-database-isolation.md`. Closes upstream `ADR-0006`. Companion unit `U15` applies the replacement row text to `agents.md §3`.*
