# 📜 ADR-0014: The RA-13 CI gate emits a RECORD, not a block, when branch protection is not inspectable on the repository's plan

**Status**: `Accepted`
**Date**: 2026-09-06
**Triggers**: 6 (`rules/documentation_standard.md §3.1`) — an availability/reliability boundary: the condition under which the RA-13 gate fails closed versus fails open. Trigger #6 does not auto-escalate individually (`§3.2`), so this ADR is Nygard-format.

---

## 1. Context

`scripts/ci_gate.py` is the `RA-13` gate named by `deployment_workflow.md` Phase 1
`test_audit`. It answers one question — *does the base branch's every required
status check report and pass?* — and its verdict is observed as a separate
invocation before `gh pr merge` is issued (`RA-13 SEQUENTIAL_GATES`).

To know what is required, it reads two GitHub endpoints and unions them
(`ci_gate.py` module docstring, "The two sources are not interchangeable"):

| Endpoint | Purpose |
| :--- | :--- |
| `repos/{slug}/branches/{base}/protection/required_status_checks` | classic branch protection |
| `repos/{slug}/rules/branches/{base}` | repository rulesets |

On a **private repository on the GitHub free plan**, both endpoints return
**HTTP 403 `Upgrade to GitHub Pro`**. Before this decision, `required_checks`
mapped "both sources unreadable" to a single hard failure, and `resolve_inputs`
mapped that to exit `2`. The consequence, reported from a host session
(`F-BOOT-3`): the `RA-13` gate was **inoperable for every such host** — no token
and no retry could make it pass, and `deployment_workflow.md` Phase 1 could not
complete.

This is distinct from the states the gate already handles correctly and must
keep blocking:

- **One source 403, the other declares nothing** (`_from_one_source`) — genuinely
  ambiguous; stays exit `2`.
- **One source 403, the other transiently fails** (e.g. HTTP 503) — retryable
  doubt; stays exit `2`.
- **Both sources answer that nothing is required** — an unprotected branch;
  stays exit `2` and routes to `/agents:harden`.

The new path fires only when **both** sources refuse specifically with
`FORBIDDEN` (HTTP 403): nothing is retryable, and the required set cannot be
established on this plan by any means available to the operator.

## 2. Decision

When both protection sources return HTTP 403, `ci_gate.py`:

1. `required_checks` returns the dedicated sentinel `PROTECTION_NOT_INSPECTABLE`
   (not the composed error string).
2. `resolve_inputs` prints a `RECORD (testifying)` line (`RA-17` vocabulary) and
   returns exit `0` — the gate does not block.
3. The `RECORD` line names the manual substitute: run `gh pr checks <N>` and
   confirm every check is green, **as a separate observed step before the merge
   is issued**. `RA-13`'s guarantee — a verification observed separately from the
   irreversible action it guards — is preserved by that separate observation,
   not voided.

`RECORD` is Phase-7 gate vocabulary (`RA-17`, `rules/qa_and_testing.md §4`).
Extending it to a merge-time script is deliberate: it is the existing word for
"observed, not a pass, not a block", and inventing a fourth outcome for one
script would be worse than reusing the established one.

## 3. Consequences

**Easier**

- `deployment_workflow.md` Phase 1 completes on a free-plan private repository
  instead of dead-ending at exit `2`.
- The operator is told exactly what to run instead, rather than being told to
  "use a token that can read branch protection" — a token that does not exist
  on that plan.

**Harder / accepted risk**

- On a free-plan repository the gate no longer *proves* the required set was
  verified; it *records* that it could not and delegates to a named manual
  step. A distracted operator can skip that step. This is a real reduction in
  the automatic guarantee, bounded to repositories whose plan already prevents
  the automatic check from running at all — the gate is not weakened anywhere it
  currently works.
- `RECORD` now has two loci (`ci_gate.py` and the Phase-7 gates). A second
  script reaching for it triggers a rule-amendment proposal via
  `governance_learner` rather than a third ad-hoc extension.
- The 403-detection is specific to `FORBIDDEN` on **both** sources. If GitHub
  changes the free-plan response to HTTP 404, this path will not fire and the
  gate returns to exit `2` — caught by the `deployment_workflow` operator, not
  silently. Revisit if that response shape changes.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md`. Cross-references `ADR-0002` (drift verdict exit codes: a verdict follows the action required, not the severity observed) and `RA-13` / `RA-17`.*
