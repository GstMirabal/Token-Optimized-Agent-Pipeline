# Rule Context: QA and Testing

This rule bounds deployment scopes, establishing testing thresholds and failsafe safety nets.

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
- **Functional Lock**: The `Tester Agent` operates downstream of QA. If functional integration tests or isolated `:memory:` tests fail, it must forcefully trigger the global **Remediation Loop**, routing the exact failure trace back to the initiating node. Under no circumstances may functional gaps be presented to the Human User for resolution.
