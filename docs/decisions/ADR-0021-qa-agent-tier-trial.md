# 📜 ADR-0021: `qa_agent` tier trial
**Status**: `Accepted`
**Date**: 2026-11-04
**Triggers**: 2 (`rules/documentation_standard.md §3.1`)

**Related**: ADR-0003 · ADR-0011
**Supersedes (clause only)**: ADR-0003 §2 clause "`qa_agent` ... stay at the `gate` tier", for `qa_agent` only and only for the duration of this trial.
**Does not supersede**: every other clause of ADR-0003. `tester_agent` and `principal_agent` stay at the `gate` tier.

---

## 1. Context

ADR-0003 keeps `qa_agent`, `tester_agent` and `principal_agent` at the `gate` tier and forbids moving them without a new ADR. Its reasoning: across four consecutive host sprints, every central defect that survived the author's own verification was found by a gate, and cheapening the reviewer is the first thing a budget attacks.

Sprint 059 plan `P2` measured `/usage`, whose first recommended saving is `qa-agent` running on `opus`. The tier map in `config/model_tiers.json` is consumed by `scripts/check_model_tiers.py` and by `agents/qa_agent.md` (`model:` and `tier:`), so moving `qa_agent` changes a contract between those files; that is trigger 2. Plan row `D9` proposes the move as a trial with a return criterion (plan `## Abort criterion`, item 4).

| Fact | How to reproduce |
| :--- | :--- |
| `qa_agent` was listed under the `gate` tier when Sprint 059 started | `git show 08c669c:agents/qa_agent.md \| grep -n '^tier:'` |
| `tester_agent` stays on `opus` | `grep -n '^model:' agents/tester_agent.md` |

## 2. Decision

During the Sprint 059 trial, `qa_agent` runs on the `author` tier (`model: sonnet`). This supersedes the ADR-0003 clause that places `qa_agent` at the `gate` tier, for `qa_agent` only.

| Item | Rule |
| :--- | :--- |
| Scope | `qa_agent` only. `tester_agent` and `principal_agent` remain under ADR-0003 unchanged, so an `opus` reviewer is present in every sprint through `tester_agent` |
| Return criterion | If a later gate finds a defect that QA Gate 1 on `sonnet` should have seen, the change is reverted: `qa_agent` returns to `opus` and the `gate` tier, and the reversion is recorded in the sprint's `SPRINT_LOG.md` (plan abort criterion 4) |
| Permissions | `qa_agent` stays read-only: no `Write` and no `Edit`, as `tests/test_agent_profile_census.py` enforces |
| Moving the tier without an ADR | PROHIBITED. This ADR exists to prevent a tier move that has no record and no return criterion |

## 3. Consequences

**Easier**: the first saving `/usage` recommends is taken, and the tier map carries the trial and its return criterion in a record instead of in chat.

**Harder**: the risk ADR-0003 named is now accepted for `qa_agent`: a structural review on `sonnet` can miss what `opus` would catch. The mitigation is `tester_agent` on `opus` plus the return criterion above, not a claim that the risk is absent. This ADR does not make the move permanent: the trial stays in force until the return criterion fires or a later ADR decides otherwise.

## 4. Considered options

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Trial `qa_agent` on `author` with a return criterion (this ADR)** | Takes the `/usage` saving; reversible by a defined event | Accepts the ADR-0003 risk for one reviewer |
| Discard the trial | Keeps `qa_agent` on `opus`; no new risk | Loses the D9 saving |

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0021-qa-agent-tier-trial.md`.*
