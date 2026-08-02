# Rule Context: Loop Governance

Bounds unattended execution. Loaded before wrapping any phase in `/loop` or `/schedule`, or authoring a routine that runs without a human watching.

`pipeline_workflow.md` governed this in one line — `/loop` may wrap Phases 6-8, never the Approval Gate — and that was the whole of it. Nothing capped iterations, nothing noticed a loop making no progress, and nothing could stop one burning turns without advancing.

## 1. Admission — build a loop only if all four hold

| Condition | Why it is binding |
| :--- | :--- |
| The task repeats, weekly or more | Setup cost must pay back |
| The output is **auto-verifiable** | Without it the agent grades its own work |
| Failure has real cost | Otherwise iteration is theatre |
| A state store exists | Already satisfied here: `docs/active_state.json` + mirror |

Fail any of the first three and a single well-written prompt is cheaper and faster. That conclusion is **declared**, not assumed.

## 2. The stop set — three binding, one advisory

Declared **before** the first iteration, via `scripts/loop_guard.py start`:

| Stop | Status | Notes |
| :--- | :--- | :--- |
| Machine-checkable success condition | **Binding** | The guard refuses to arm a loop without one |
| Iteration cap | **Binding** | Observable and enforced |
| No-progress detector | **Binding** | Two consecutive iterations with no new commit on the sprint branch **and** no change in the `task_scope.md` `Status` column |
| Token budget | **Advisory** | No agent reads its own spend reliably. Making it binding would force a field nobody can fill truthfully — the same defect as a gate that cannot fail. Declare it if a human sets it; the guard does not arbitrate it |

`scripts/loop_guard.py check` runs as the **first action of every iteration** and **fails closed**: a `loop` block that is missing, incomplete or stale exits `2`. An agent that forgets to increment the counter gets a stop, not a free pass.

## 3. What is already solved — do not rebuild it

- **The verify gate is the Double-Gate** (`qa_and_testing.md §4`): QA structural, then Tester functional, both external to the agent being checked. Do not build a second verifier; self-grading is what the loop literature warns about and this framework already avoids.
- **The state store is `docs/active_state.json`** plus its mirror. `state_homologation` forbids a parallel one.

## 4. Boundaries that already exist

- **Never wrap the Approval Gate** (`pipeline_workflow.md` Phase 5): human authorization stays a single attended invocation.
- **The Heuristic Pulse Gate** (`close_workflow.md` Phase 2.5) has its own `/loop` exception — under `/loop` it logs and proceeds instead of blocking.
- **`RA-13 SEQUENTIAL_GATES`**: a verification and the irreversible action it guards are separate invocations. A loop that chains them re-creates the failure that put a red CI on `main`.
