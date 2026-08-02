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
- **Structural Halt**: No execution block may proceed to functional testing without the explicit, documented sign-off from the `QA Agent`, guaranteeing absolute governance, linguistic, and syntactic compliance.
- **Functional Lock**: The `Tester Agent` operates downstream of QA. If functional integration tests or isolated `:memory:` tests fail, it must forcefully trigger the global **Remediation Loop** — the protocol in `workflows/remediation_workflow.md`, named here rather than alluded to, because a transition nothing names is a transition no verifier can check (`RA-16`) — routing the exact failure trace back to the initiating node. Under no circumstances may functional gaps be presented to the Human User for resolution.
