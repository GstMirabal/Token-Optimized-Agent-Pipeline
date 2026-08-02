# Rule Context: Code Craft

Judgment rules for writing code, distilled from the mistakes language models make repeatedly. `agents.md §1` already governs style, typing and size; this governs the decisions those metrics cannot see — a function can be under 50 lines, fully typed, and still be the wrong abstraction built for a requirement nobody has.

Loaded when writing or modifying source code in any language. Not loaded for documentation or governance edits.

> **Exemption from Filter 5, recorded here so it is not re-litigated at every audit.** Sections 1-5 are semantic judgment with no reasonable deterministic equivalent, which `agents/token_economy_agent.md burden_of_proof` exempts by default. Sections 6-7 **are** mechanised, in `hooks/on_commit.py`.

## 1. Simplicity

Write the minimum that solves the problem in front of you, not the minimum that would solve every future version of it.

| Prohibited | Test |
| :--- | :--- |
| Premature abstraction | If the only reason for it is "in case we need to", it is over-built. Two call sites, not one, justify extraction |
| Handling errors that cannot occur | Name the input that produces the error. If you cannot, delete the handler |
| Configuring what nobody has asked to vary | Hardcode until a second value actually exists |

## 2. Surgical diff

`jurisdictional_lock` bounds how many **files** a subagent touches; nothing bounded how much of one file it rewrites.

- Do not touch what you were not asked to touch. Do not reformat. Match the surrounding style even when you prefer another.
- **Every changed line must be justifiable by the task.** A line changed because "while I was in there" is reverted — including a formatter pass that buries three meaningful lines inside three hundred mechanical ones.

## 3. Debugging

`rules/qa_and_testing.md §2` (Three-Strikes) is the kill switch that fires **after** three failed guesses. This section is what keeps you from getting there.

- **Reproduce before changing.** A fix for a failure you have not observed is a guess with a commit message.
- **Read the whole error and the whole stack trace**, not the last line.
- **Change one thing at a time.** Two simultaneous changes and a passing test tell you nothing about which one worked.
- **Never paper over an unexpected `None`** with a guard. Find out why it is `None`; a guard moves the bug somewhere quieter and later.

## 4. Dependency admission

`agents.md §8` governs **how** a dependency is installed (`pnpm 11+`, `ignore-scripts`, `minimum-release-age`). Nothing governed **whether it should enter at all**.

Every dependency is permanent code you do not control. Before adding one: check the standard library, then the dependencies already present. If it still earns its place, state why in the Implementation Plan and in the commit — see §7.

## 5. Named failure modes

Recognising a pattern requires it to have a name. When you catch yourself in one, **stop** — do not push through.

| Name | Shape |
| :--- | :--- |
| **Kitchen Sink** | Restructuring half the codebase while completing a small task |
| **Wrong Abstraction** | Copy-pasting twice before understanding it, then extracting the accidental similarity |
| **Optimistic Path** | The happy path handled, the 500 ignored |
| **Runaway Refactor** | One fix cascading across files, each change requiring the next |

## 6. Regression test first (enforced)

For a bug fix: write the failing test, **watch it fail**, then fix. This is `RA-13 SEQUENTIAL_GATES` applied to tests — the verification and the action it guards are observed separately. `qa_and_testing.md §1` demands 100% coverage, which is quantity; this is the ordering that proves the fix addressed the cause and not a symptom.

Enforced by `hooks/on_commit.py audit_regression_test`: a commit whose message starts with `fix(` must stage at least one test file.

## 7. Dependency justification (enforced)

Enforced by `hooks/on_commit.py audit_dependency_justification`: a commit adding a dependency to `requirements*.txt`, `package.json` or `pyproject.toml` must carry a `Dependency: <name> — <reason>` line in its message.
