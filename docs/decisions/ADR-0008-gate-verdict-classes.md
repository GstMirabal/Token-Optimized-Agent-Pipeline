# 📜 ADR-0008: Gate verdict classes

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 031
**Last Audit Date**: 2026-08-25

---

## 1. Context

`F-093-G1`: the Double-Gate had no severity class, so a round cap could not
fire. Hosts and this nucleus treated every finding as a charter bounce.
`rules/qa_and_testing.md` §4 named Structural Halt and Functional Lock, then
the remediation loop; it did not name an emitible verdict set. Gate profiles
said "forcefully rejects" with no third outcome.

A round cap is the wrong instrument for a stale comment. The reporting host
already had N=2 and it did not fire.

## 2. Decision

Phase 7 emits exactly one of `APPROVED` | `REJECTED` | `RECORD` per gate,
with class `charter` / `instructing` / `testifying` (`RA-17`,
`rules/qa_and_testing.md` §4).

`RECORD` is a **completed** Phase 7 verdict. Close accepts it as "one QA
verdict and one Tester verdict". It does not increment consecutive
`REJECTED` counts and does not invoke `remediation_workflow.md`.

Rejected alternatives: alias `CARRY`; a maximum of N rounds; raising the
three-strikes threshold.

## 3. Consequences

- Instructing documents (`agents.md`, `rules/`, `workflows/`, skill
  `SKILL.md`) that state a false procedure stay `REJECTED` / `instructing`.
- Testifying defects (sprint logs, comments, Makefile observations) can
  close after round 1 without remediation.
- `scripts/check_gate_log.py` pins vocabulary from sprint 31 onward;
  021–030 are skipped, not rewritten.
- Misclassifying a secret or a red suite as `RECORD` is an abort criterion
  of Sprint 031, not a feature.
