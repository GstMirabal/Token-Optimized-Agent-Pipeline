# 🧠 Knowledge Item: Roadmap Maturity Protocol (Safety Lock)

## 🚦 Context: Architecture vs Execution
During the initialization of `PHASE 3 (Datafeed Implementation)`, the Agent attempted to jump directly to execution (creating Sprint 004 and implementation plans) before the technical discovery and tactical scope were finalized. This led to a mismatch between the inherited project roadmap and the agent's proposed plan.

## ⚠️ The Blockage: Premature Sprinting
Creating sprints before the Roadmap's Milestones (M0, M1...) are fully defined and audited leads to architectural debt and loss of governance integrity.

## ✅ The Solution: Roadmap Maturity Protocol (Rule 4)
Any roadmap that is in `DISCOVERY_IN_PROGRESS` or has an active `safety_lock: LOCKED` **prohibits** the creation of:
1.  Entries in `task.md` for new sprints.
2.  Implementation plans in `task/sprints/`.
3.  Tactical execution logs.

**Standard**:
- The Agent must focus 100% on **Discovery Debate** until the roadmap is marked as `READY_FOR_EXECUTION` and the `safety_lock` is explicitly `UNLOCKED` by the user/architect.

---
`Global Protocol: .agents/governance/global_user_rules.md`
