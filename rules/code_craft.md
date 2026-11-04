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

`jurisdictional_lock` bounds **which file** a subagent claims as its subject; nothing bounded how much of that file it rewrites.

- Do not touch what you were not asked to touch. Do not reformat. Match the surrounding style even when you prefer another.
- **Every changed line must be justifiable by the task.** A line changed because "while I was in there" is reverted — including a formatter pass that buries three meaningful lines inside three hundred mechanical ones.

## 3. Debugging

`rules/qa_and_testing.md §2` (Three-Strikes) is the kill switch that fires **after** three failed guesses. This section is what keeps you from getting there.

- **Reproduce before changing.** A fix for a failure you have not observed is a guess with a commit message.
- **Read the whole error and the whole stack trace**, not the last line.
- **Change one thing at a time.** Two simultaneous changes and a passing test tell you nothing about which one worked.
- **Never paper over an unexpected `None`** with a guard. Find out why it is `None`; a guard moves the bug somewhere quieter and later.

## 4. Dependency admission

`agents.md §8` governs **how** a dependency is installed (`pnpm 11+`, `ignoreScripts`, `minimumReleaseAge`, set in `pnpm-workspace.yaml`). Nothing governed **whether it should enter at all**.

Every dependency is permanent code you do not control. Before adding one: check the standard library, then the dependencies already present. If it still earns its place, state why in the Implementation Plan and in the commit — see §7.

## 5. Named failure modes

Recognising a pattern requires it to have a name. When you catch yourself in one, **stop** — do not push through.

| Name | Shape |
| :--- | :--- |
| **Kitchen Sink** | Restructuring half the codebase while completing a small task |
| **Wrong Abstraction** | Copy-pasting twice before understanding it, then extracting the accidental similarity |
| **Optimistic Path** | The happy path handled, the 500 ignored |
| **Runaway Refactor** | One fix cascading across files, each change requiring the next |
| **Borrowed Anchor** | Measuring containment against a value the guarded input supplied. Guarding one field while its sibling in the same expression stays free is the same defect one step earlier |

### The Borrowed Anchor, in full (Sprint 042)

A check that asks *is this path inside that directory* proves nothing when the
declaration being checked chose the directory. `scripts/check_template_gates.py`
validated every render target against `sprint_dir`, and `sprint_dir` was
`scratch / case["id"] / case["scratch_sprint_dir"]` — the last component
validated, the middle one not. The predicate was then satisfied by construction:
the run exited `0`, printed `[OK]`, and wrote outside its temporary directory.

**Validate the field and you close the instance; verify the anchor and you close
the class** — a fourth component joined onto that expression is contained without
anyone remembering to guard it. State the obligation in the docstring of whatever
measures against the anchor, at the place a future contributor would reorder.

Two guards were already in place and neither helped, which is why this is named
rather than left to care: the interpreter was pinned and the script path
contained. A guarded argument vector says nothing about a second channel to the
filesystem.

## 6. Regression test first (enforced)

For a bug fix: write the failing test, **watch it fail**, then fix. This is `RA-13 SEQUENTIAL_GATES` applied to tests — the verification and the action it guards are observed separately. `qa_and_testing.md §1` demands 100% coverage, which is quantity; this is the ordering that proves the fix addressed the cause and not a symptom.

Enforced in two places, because staging a test proves only that a test exists (`F-114-N1`, Sprint 054):

| Where | Mechanism | What it checks |
| :--- | :--- | :--- |
| Commit time | `hooks/on_commit.py audit_regression_test` | A fix commit (subject matching `^fix(\([^)]*\))?!?:\|^fix\(`, so `fix:` and `fix!:` too; the same pattern as the replay below) that stages source either stages a test file **and** carries a trailer `Repro: <test id> — fails at <parent sha>` naming a staged test, or carries `Repro: manual — <SPRINT_LOG section>` when no test can show the defect (no staged test required on that route). Source and test paths are `scripts/_repro_grammar.py` `is_source_path`/`is_test_path`, the definitions the replay below also uses: source is every path that is not a test and whose suffix is not `.md`, `.rst`, `.txt`, `.yml`, `.yaml` or `.toml`, so `.json`, shell and `Makefile` count. The trailer is a claim. |
| QA Gate 1, first check | `scripts/check_fix_reproduces.py --range <base>..HEAD` | Observes the claim: each `Repro:` test exits exactly `1` on the parent tree (an import or collection error is not a reproduction) and `0` at the commit. The runner is chosen by the suffix of the id's file, per the runner table below (`KI-054-1`); a suffix with no runner is `UNREPLAYED` unless the commit says `Repro: manual`. |

**Runner table (`R-6`, `KI-054-1`; vitest runner in commit `abbf856`).** `scripts/check_fix_reproduces.py` replays each `Repro:` id in a temporary worktree of the parent commit and of the fix commit:

| Id file suffix | Runner and command | Verdict on the parent tree |
| :--- | :--- | :--- |
| `.py` | pytest, as in the QA Gate 1 row above | Exit exactly `1` is a reproduction; an import or collection error is not |
| `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs` | `pnpm exec vitest run <file> -t <name> --reporter=junit --outputFile=<tmp>.xml`, run in the same temporary worktree as the pytest path, with the `node_modules` of the main checkout symlinked into it | A `<failure>` in the junit report is a reproduction. An `<error>`, a missing report, or no executed testcase is `WRONG_FAILURE`: a setup error, not a reproduction |
| Any other suffix | None | `UNREPLAYED`, reason `no runner for <file>` |

- A JS/TS id is `UNREPLAYED` when `pnpm` is absent from the `PATH` or the main checkout has no `node_modules`; the printed reason names the missing piece.
- The nucleus adds no JS dependency. A host that uses JS/TS ids supplies its own `node_modules` and `vitest`.

**R-8: a test that reads source code as text is not a reproduction.** A test that asserts on the text of a source file passes or fails on wording, not on behavior, so it cannot show that the defect is gone. Instrument: `scripts/check_fix_reproduces.py` prints `SOURCE_TEXT <sha> <test id>: <pattern>` (commit `6bded6d`). It is a warning only: the verdict and the exit code do not change.

| Item | Value |
| :--- | :--- |
| Trigger | The inspected text contains one of five literal substrings: `readFileSync(`, `?raw`, `.read_text(`, `.read_bytes(`, `open(`. No path condition |
| Inspected text, Python ids | The source of the named test function, located with `ast` (`Class::test` included). If the function cannot be located, the whole file, with the note `(whole file: function not located)` |
| Inspected text, JS/TS ids | The whole test file, because the standard library has no JS parser |

The check is a denylist of exactly those five substrings and makes no coverage claim (`agents.md §1 fail_closed_claims`): a test that reads source by another route is not flagged. A false positive is expected and cheap, because the warning does not block: `open(` also matches `reopen(`, and reading a JSON data template is not reading source.

## 7. Dependency justification (enforced)

Enforced by `hooks/on_commit.py audit_dependency_justification`: a commit adding a dependency to `requirements*.txt`, `package.json` or `pyproject.toml` must carry a `Dependency: <name> — <reason>` line in its message.

## 8. Instrumented rules of agents.md §1 (detail)

`agents.md §1` keeps the rule; this section keeps the measurement, the instruments, the history and the precedents moved here in Sprint 059 (D10).

### linter_command (Python)

- Command: `ruff check .` (Reject if exit code > 0).
- Verified by: `make verify`, which runs the pinned `$(PY) -m ruff check .` since `ce80b0d` (Sprint 053 unit C56).
- `ruff` is pinned to `0.16.3` in `requirements-quality.txt` (`87cb3ce`) and in `ruff.toml` (`9242d3c`: `required-version = "==0.16.3"`, an explicit `select` of 413 codes, and an `extend-exclude` listing the ten vendored `skills/skill-creator/` paths of `config/quality_audit_exclusions.json`; the parity between both lists is pinned by `tests/test_ruff_config.py`, `e7a9848`).
- The Sprint 053 Wave C baseline of 176 findings was brought to 0 before the gate was wired.
- `skills/python-quality-auditor` is a separate, model-invoked tool call (`config/invocation_exceptions.json:53`) that shells to `ruff`/`mypy`/`bandit`/`radon` and prints a pass/fail line per tool; it computes no numeric score and never exits non-zero, so "Warn if score < 95" named an instrument this script does not implement (`F-049-7`, Sprint 049).
- `mypy`/`bandit`/`radon` remain uninstrumented by any gate (`ruff` is now gated by `make verify`, above) — no general style-score instrument exists.
- Separately, `scripts/quality_audit.py` (`make quality-audit`) deterministically measures function length (executable lines) and nesting depth for Python via stdlib `ast`, `sys.exit(2)` on violation — see `max_lines_per_func`/`max_indentation` below. It does not run `ruff` and computes no general style score; that broader claim stays uninstrumented.

### linter_command (JS/TS)

- Command: `pnpm run lint` (Reject if exit code > 0).
- Verified by: QA-gate judgment, NOT `make verify` — `verify` runs no `pnpm run lint` step.
- `skills/js-standardizer` is a separate, model-invoked tool call (`config/invocation_exceptions.json:58`) that checks for the presence of lint-tool config files and a single repo-wide boolean — whether *any* `.js`/`.ts` file anywhere contains the substring `@param` or `@returns`, not per-function JSDoc coverage; it computes no numeric score and never exits non-zero (`F-049-7`, Sprint 049). `pnpm run lint` itself remains unreplaced and is a host concern.
- **Deterministic complexity instrument for JS/TS** (Sprint 053, `0ec6616`, with comment-only rows excluded from executable lines since `fbbc286`, unit B3; closes `KI-050-6`): `scripts/quality_audit.py` measures `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs` and `.cjs` files (source: `JS_SUFFIXES` in `scripts/quality_audit.py`) with `tree-sitter` grammars, pinned in `requirements-quality.txt` (tree-sitter 0.26.0, tree-sitter-javascript 0.25.0, tree-sitter-typescript 0.23.2).
- Function units are `function_declaration`, `generator_function_declaration`, `function_expression`, `arrow_function` and `method_definition`; size is executable lines (an expression-bodied arrow counts 1) under the two Sprint 056 rules (`D6`, `KI-053-2`; `2e4487c`, `9f02419`): a function nested inside an expression is a boundary for its enclosing unit (only the row where it starts counts there; its body is measured as its own unit, symmetric with Python's nested `def`), and blank rows and comment-only rows are excluded also inside a multi-row statement (tree-sitter `comment` nodes and rows holding no token; Python uses stdlib `tokenize`), while a blank row inside a multi-line string or template literal still counts; depth is block-nesting depth counted over the ancestors `function_*`, `arrow_function`, `method_definition`, `class_*`, `if_statement`, `for_*`, `while_statement`, `do_statement`, `try_statement` and `switch_statement` from the `program` root.
- It fails closed on error: with JS/TS files in scope and `tree_sitter` not importable it exits 2 naming `pip install -r requirements-quality.txt`, and a parse error yields an `UNPARSED` unit counted non-compliant. The Python path stays stdlib-only.
- History: Sprint 050 built and then withdrew a stdlib-only brace scanner (Abort criterion 1, `IMPLEMENTATION_PLAN.md`) after four consecutive gate rejections found silent-compliance defects that scanner cannot fix in general (JS/TS's lexical grammar is context-sensitive — regex-literal-vs-division, keyword-vs-identifier — and needs a real lexer).
- **Prohibition**: a heuristic scanner MUST NOT be credited with a coverage claim over such a grammar without a real lexer (general form: `§1 fail_closed_claims`); the Sprint 053 instrument satisfies it because tree-sitter is a real parser.
- `tests/test_quality_audit.py` (`4585778`, `04e96c8`) covers the five failure families both Sprint 050 gates found (arrow over-detection, unenclosed module-level callbacks, nested-arrow depth loss, control-keyword method names, regex-literal masking desync).

### max_indentation

- Limit: 3 levels, measured as **block-nesting depth counted over `ast` ancestors** (`FunctionDef`, `AsyncFunctionDef`, `ClassDef`, `If`, `For`, `While`, `With`, `Try`, `Match`) from the module root, not over character columns — a module-level `def` body is level 1, and the limit is exceeded at level 4.
- Measured deterministically by `scripts/quality_audit.py`, invoked via `make quality-audit`: Python via stdlib `ast` over exactly the ancestor set above, and JS/TS via tree-sitter (Sprint 053, `0ec6616`; the JS/TS ancestor set is in the `linter_command` JS/TS row); `sys.exit(2)` on violation, `0` clean; `--report` prints the full register.
- **`make verify` runs `make quality-audit`** (Sprint 052 `U66`): the Sprint 050 baseline of 87 non-compliant units out of 1487 (`D5` Branch B withheld the wiring pending remediation) was brought to 0 by the Wave 6 refactors (Sprint 052, units `U23`–`U64`), clearing the condition that had withheld the gate.
- Ten provenance-verified vendored files under `skills/skill-creator/{scripts,eval-viewer}/`, each with upstream commit evidence, are exempted in `config/quality_audit_exclusions.json` (`e0922dd`); `scripts/quality_audit.py` (`6bc75b9`) skips them, lists them in `--report`, and exits 2 on a stale entry (a listed path that no longer exists, a malformed file, or an entry missing `path`/`reason`/`provenance`) — an absent exclusions file means no exclusions.
- Delivered Sprint 050 (`F-049-7`, Sprint 049 correction; `docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md` `D2`).

### max_lines_per_func

- Limit: 50 lines, measured in **executable lines** — statements in the function body, excluding blank lines, comment-only lines, and the docstring — not raw span, and counted over `FunctionDef.body`, so a decorator list sits outside that body and its lines never count (`#13`, `D8`; pinned by `tests/test_quality_audit.py`, `6bc75b9`).
- **Two measurement rules added in Sprint 056 (`D6`, closes `KI-053-2`; `2e4487c`, `9f02419`)**: (a) in JS/TS a function nested inside an expression is a boundary for its enclosing unit — only the row where it starts counts for the enclosing unit, never its body, which is measured as its own unit (symmetric with Python's nested `def`); (b) blank rows and comment-only rows are excluded also inside a multi-row statement — Python reads them with stdlib `tokenize` (a row holding only `COMMENT`/`NL` tokens), JS/TS with tree-sitter `comment` nodes and rows holding no token — while a blank row inside a multi-line string or template literal still counts.
- Measured deterministically by `scripts/quality_audit.py`, invoked via `make quality-audit`: Python via stdlib `ast` counting exactly the executable-line definition above, and JS/TS via tree-sitter (Sprint 053, `0ec6616`; the JS/TS function units and size rule are in the `linter_command` JS/TS row); `sys.exit(2)` on violation, `0` clean; `--report` prints the full register.
- The gate wiring and vendored exclusions are as stated under max_indentation above.
- Delivered Sprint 050 (`F-049-7`, Sprint 049 correction; `docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md` `D1`).

### exception_handling

- No `pass` in except. Explicit logging required.
- At a fault boundary where one item's failure must not stop the others (per host, per file, per entry), the handler catches every `Exception`, reports which item failed, and continues; catching only the expected types is PROHIBITED, and the test proving it injects exception types it does not enumerate, including a fresh subclass defined in the test.
- A read of a path supplied by a host or by data checks it is a regular file and caps the bytes read before opening, because a FIFO or a device hangs without raising.
- Precedent: Sprint 058 QA Gate 1 rounds 3-4 (`d702700`, `09dab75`).

### fail_closed_claims

- Two distinct properties; never use one word for both.
- (1) **Fail-closed on error**: the check exits non-zero, or counts the unit non-compliant, when its input is malformed or unparseable or a dependency is unavailable. Bare "fail-closed"/"fails closed" means this property and nothing more (`quality_audit.py`, `loop_guard.py`, `rules/loop_governance.md` use it this way).
- (2) **Coverage claim**: "fail-closed coverage", "complete", or covering "any"/"every" X. Permitted only if the check rejects everything except an explicitly reviewed set: for a structured object, exact equality of the whole object (or of every key) against a reviewed copy, with duplicate keys rejected; for free text such as shell, byte equality of the text against a reviewed copy. A denylist, pattern scan, or allowlist over a subset of keys or fields MUST state the exact subset it checks and MUST NOT carry a coverage claim.
- When a gate finds a second finding that falsifies the same coverage claim of the same guard (that is "same family") after a remediation, the next remediation MUST replace the enumeration with the reviewed-copy equality check or narrow the claim; it MUST NOT add the new vector to the enumeration.
- Precedent: Hotfix H-007 (`docs/hotfixes/H-007-mcp.md`) — `tests/test_mcp_template.py` was REJECTED in QA Gate 1 rounds 1-4 (regex, shlex parser, word denylist, `command`/`args` allowlist), each claiming coverage while a new vector (`pnpm -C dlx`, `docker run`, `env` `DYLD_INSERT_LIBRARIES`, `type`/`url`) passed.
