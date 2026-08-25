# Rule Context: QA and Testing

This rule bounds deployment scopes, establishing testing thresholds and failsafe safety nets.

> **Citation convention** (framework-wide, stated once here because this is where the first violation was found): an artifact may be cited by **bare filename** when it lives in a single well-known directory — `workflows/`, `rules/`, `agents/`, `commands/`, or the repository root. It **must** carry its full path otherwise. Bare citation is the house style at scale (`agents.md` ×22, `active_state.json` ×16, `memory_index.json` ×13), so pinning a path onto one file while a hundred others stay bare is inconsistency, not rigour. The rule is about resolvability: `close_workflow.md` resolves; `train_runner.py`, buried in `skills/skillopt/scripts/`, does not.

## 1. The Coverage Mandate
- **100% Quality Acceptance Lock**: The implementation of any logical module or integration is deemed completely invalid and terminal if not shipped alongside a robust automated test suite guaranteeing **100% Code Coverage**.
- **DevOps Gatekeeper**: Pushing modules into the production root structure is strictly denied until the local testing CI scripts output a `PASSED` signature verifying the total coverage threshold and deterministic stability in sterile environments.

## 2. The Local Kill Switch
- **Three-Strikes Restitution**: The framework actively tracks agent-provoked syntax and logical failures. If the `lint`, formatting, or baseline compiling protocols collapse and throw errors for **3 sequential logic attempts**, an automated `git restore .` is authorized.
- The session execution will halt to enforce a complete code reset, averting infinite hallucination loops or technical debt stacking.

## 3. Code Rollback Safety
- **Tracking Deviations**: Any structural detour forced by environmental variables must be explicitly marked as `:tech-debt:` inside active implementation plans, immediately rendering the block a high-priority vulnerability for retroactive analysis.

## 4. The Double-Gate Review Protocol

Phase 7 emits exactly one of `APPROVED` | `REJECTED` | `RECORD` per gate
(QA, then Tester). The class is declared on the `SPRINT_LOG.md` row (`RA-17`).
C6's operational table lives here, not in a sprint log.

| Class | When | Verdict | After the verdict |
| :--- | :--- | :--- | :--- |
| *(none)* | No findings | `APPROVED` | Proceed |
| `charter` | Plan/ADR unmet, functional suite red, secret, or missing `task_scope.md` | `REJECTED` | Bounce. Counts toward consecutive rejections of the same block |
| `instructing` | A file that tells an agent what to do states a false procedure (`agents.md`, `rules/`, `workflows/`, skill `SKILL.md`) | `REJECTED` | Bounce. Counts toward consecutive rejections of the same block |
| `testifying` | Sprint logs, comments, Makefile observations, claims about a mechanism that already works | `RECORD` | instruct; annotate. Does **not** increment the consecutive-rejection count. Does **not** invoke `remediation_workflow.md` |

- **Structural Halt**: No execution block may proceed to functional testing without the explicit, documented sign-off from the `QA Agent`, guaranteeing absolute governance, linguistic, and syntactic compliance. A `RECORD` on Gate-1 is a documented sign-off, not a missing gate.
- **Functional Lock**: The `Tester Agent` operates downstream of QA. If functional integration tests or isolated `:memory:` tests fail (`charter`), it must forcefully trigger the global **Remediation Loop** — the protocol in `workflows/remediation_workflow.md`, named here rather than alluded to, because a transition nothing names is a transition no verifier can check (`RA-16`) — routing the exact failure trace back to the initiating node. Under no circumstances may functional gaps be presented to the Human User for resolution. A `RECORD` on Gate-2 is not a functional gap.

## 5. Waiving a secret-scan finding

`hooks/on_commit.py` blocks a commit when it finds a credential assigned to a
secret-named identifier. Value shape cannot always separate a credential from a
**pointer** at one — the same string is either, depending on what reads it —
so the gate is deliberately imperfect and ships an escape rather than a fourth
round of heuristic tuning.

| Rule | Value |
| :--- | :--- |
| **Marker** | `# secret-scan: allow <reason>`, appended to the offending line |
| **Scope** | That line only. There is no file-level or blanket waiver |
| **Reason** | **Mandatory.** A marker with no reason suppresses nothing |
| **Visibility** | Every waiver that actually suppressed a finding is printed at commit time, naming the identifier and the reason |
| **Not waivable** | A forbidden file (`.env` and `.env.*` except `.env.example`, plus `.pem`, `.key`, `secrets.json`, `credentials.json`). The marker narrows a heuristic; it does not unlock the hard boundary |

A silent bypass is how `RA-09 SECRET_SOVEREIGNTY` gets defeated by the control
built to enforce it. A declared one is an audit trail. Precedent: the gate was
rejected four consecutive times in Sprint 023 for blocking legitimate pointers,
and the deciding argument each round was not the false positive but that **a
host had no way to comply except to disable the hook**.
