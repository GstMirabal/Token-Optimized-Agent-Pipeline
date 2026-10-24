# How to review instruction text against the Claude Opus 5.5 prompting criteria
**File**: `docs/guides/PROMPT_CRITERIA_GUIDE.md` (RA-06 Option B naming)
**Module**: CORE / PIPELINE

---

## 1. Goal

Review every new or changed instruction text line by line against one checklist, so text written for older models does not enter the framework. Instruction text means `agents.md`, `rules/*.md`, `workflows/*.md`, `agents/*.md` and the `SKILL.md` files this repository owns. Vendored skills are excluded (`rules/skills_and_integrations.md` forbids editing them).

| Item | Value |
| :--- | :--- |
| Applies to | All new or changed instruction text of Sprints 057, 058 and 059 |
| Audit of the existing corpus | Sprint 060 (this guide does not audit it) |
| Target model | Claude Opus 5.5 |
| Sources | claude-api skill, `shared/prompt-audit.md`; claude-api skill, `shared/model-migration.md` → Migrating to Claude Opus 5.5 |

## 2. Prerequisites

- The diff of the text under review (`git diff` of the changed instruction files).
- `rg` (ripgrep) to run the signals in section 3. Run each signal over the changed files first, then over the corpus for PC-04.
- Read `agents.md` §1 `unambiguous_action` (section 5 of this guide explains how it interacts with trimming).

## 3. Steps

For each added or changed line, run the signal of every row, then apply the fix of each row that matches. A line that matches no row stays. A match is a finding only when the "why" holds for that line; record the row ID in the review note.

### 3.1 Checklist

| ID | Check | Greppable signal | Why | Fix |
| :--- | :--- | :--- | :--- | :--- |
| PC-01 | Emphasis that over-triggers: capitalized emphasis words, repeated MUST/NEVER/CRITICAL, "IMPORTANT" | `rg -c -e 'CRITICAL' -e 'IMPORTANT' -e '!!' -e '\bMUST\b' -e '\bNEVER\b' -e '\bALWAYS\b'` (density per file) | Opus 4.5 and later follow the prompt closely; text written to overcome old reluctance now over-applies (migration, prompt-behavior change 1) | State the rule at normal volume with its reason; keep one emphasized line only when a test showed that instruction underweighted |
| PC-02 | Hedges on real requirements | `rg -i -e 'try to' -e 'if possible' -e 'ideally'` | Current models read hedges literally as permission to under-deliver (prompt-audit 1a) | Remove the hedge and state the requirement ("Include a summary.") |
| PC-03 | Trait claims and tone scolding | `rg -i -e 'you tend to' -e 'you often' -e 'you sometimes' -e "don'?t be too"` | The prompt's register becomes the output's register; an anxious register produces a hedging output (prompt-audit 1a) | State the target behavior ("Keep responses to the length the question needs.") |
| PC-04 | Contradiction across documents: the same key term ruled on differently in two files | `rg -n -e '<key term>' agents.md rules workflows agents skills` for every term the change touches | Loaded together the model must reconcile them; loaded one at a time behavior depends on load order (prompt-audit Group 2) | Quote both locations, make the newer one canonical, point the other to it (RA-14 patch propagation); a narrower file that names the rule it overrides is an override, not a conflict |
| PC-05 | Historical narrative or precedent story in always-loaded text: incident IDs, sprint numbers, past tense, "was added because" | `rg -e 'Precedent' -e 'Sprint [0-9]{3}' -e 'was added' -e 'was found' -e 'until Sprint'` | A rule's authority is the behavior it prescribes, not the incident behind it; the archaeology costs tokens on every load (prompt-audit Group 2) | Move the story to the ADR or sprint record, keep the rule and its one-line reason, link the record |
| PC-06 | Migration-relative phrasing: "now", "no longer", "instead of" attached to a rule | `rg -w -e 'now' -e 'no longer' -e 'instead of'` | The text reads as a diff against a version the model never saw and implies phantom alternatives (prompt-audit 1d) | Write the current rule as if it were the only rule that ever existed |
| PC-07 | Instruction redundant with default model behavior: generic virtues, "be thorough", "do not be lazy", "plan before acting", "think step by step" | `rg -i -e 'be thorough' -e 'do not be lazy' -e 'step by step' -e 'plan before' -e 'do not hallucinate'` | Current models are proactive and plan unprompted; such lines add over-planning and spend thinking tokens (prompt-audit 1a, 1b, 1d) | Delete; if behavior is still too eager, lower `effort` instead of adding prose. Removal of `do not hallucinate` is low confidence: re-test it |
| PC-08 | Prose steering thinking depth, or a rule telling the model not to think | `rg -i -e 'think harder' -e 'think less' -e "don'?t overthink" -e 'do not think'` | Thinking is always on in Opus 5.5; effort is the only control and a "do not think" rule cannot be followed (migration, breaking change 1) | Delete the line and set `effort`; keep a "reply directly" line only where a latency measurement shows it helps |
| PC-09 | Required reasoning in the output: "show your thinking", a `reasoning` or `trace` field | `rg -i -e 'show your thinking' -e 'show your reasoning' -e 'scratchpad'` | Instructing reasoning reproduction can be declined as `reasoning_extraction` and is not retried (migration, Safeguards) | Ask for a short explanation of the answer or a summary of actions taken |
| PC-10 | Step-by-step choreography for judgment tasks | `rg -e 'STEP [0-9]' -e '^[0-9]+\. Always' -e '^[0-9]+\. Never'` | A hand-written script usually loses to the model's own plan (prompt-audit 1c) | State outcome, constraints and how to verify; keep numbered steps only where order is part of the contract |
| PC-11 | Prohibition cluster: three or more consecutive "do not / never / avoid" lines | `rg -n -e '^[-*] *Do not' -e '^[-*] *Never' -e '^[-*] *Avoid'` and read runs of 3+ | A prohibition without provenance can anchor the model toward the failure it names (prompt-audit 1c, 1e) | Keep each line that carries a reason or a real policy constraint; restate the rest as one positive line |
| PC-12 | Output-shaping limbs: numeric ceilings, fixed update cadences | `rg -i -e 'at most [0-9]+ words' -e 'at most [0-9]+ sentences' -e 'at most [0-9]+ bullets' -e 'every [0-9]+ tool calls' -e 'under [0-9]+ words'` | Caps starve reasoning and cadences duplicate natural narration; remove every limb together (prompt-audit 1b, 1f) | Re-express as audience and outcome without the number; keep real format requirements as format instructions |
| PC-13 | Update suppressors and anti-formatting rules | `rg -i -e "don'?t narrate" -e 'no interim' -e 'hold all findings' -e 'never use bullets' -e 'never use headers'` | Written against chatty models; Opus 5.5 under-narrates with them present (prompt-audit 1d) | Remove and re-test; if narration is wanted, say when user-facing text is wanted |
| PC-14 | Examples: a single gold output, or examples of judgment the model already owns | `rg -n -e '[Ee]xample' -e 'e\.g\.'` and read each hit | The model copies the length, tone and structure of an example; one example freezes that shape (prompt-audit 1c) | Use several varied examples labeled illustrative; delete examples of easy judgment; keep an example only where it pins a format-sensitive output |
| PC-15 | Examples help: format-sensitive output, a named pattern to avoid | none (judgment) | Opus 5.5 responds to named patterns to avoid; a vague "avoid a generic look" swaps one default for another (migration, frontend defaults) | Keep the list of named patterns and extend it from the first result |
| PC-16 | Long document: the always-loaded part carries material only some tasks need | `wc -l agents.md rules/*.md workflows/*.md`; `rg -n -e 'rules/' config/rule_triggers.json` | Size is paid on every load; bulk inflates thinking spend (prompt-audit Group 2, 1c) | Put the rule in the file whose `config/rule_triggers.json` trigger fires for that task; order a file so the rule every reader needs comes first, reference tables after |
| PC-17 | Duplicated rule across sections or files | `rg -c -e '<distinctive phrase>' agents.md rules workflows` | Duplicates drift apart and the model spends effort reconciling wording (prompt-audit 1c) | State once in the owning file and reference it; a single end-of-document recap of key constraints is allowed |
| PC-18 | Volatile specifics: hardcoded counts, versions, paths with no re-measure command | `rg -e '[0-9]+ rules' -e '[0-9]+ files' -e '[0-9]+ sprints' -e 'v[0-9]+\.[0-9]+'` | Skills rot as code ships; nothing re-checks them (prompt-audit Group 2) | Attach the command that reproduces the figure (`rules/documentation_standard.md` §6) or remove the figure |
| PC-19 | Enforceable by code but written as prose | none (judgment) | A rule no code path checks carries no signal and is less reliable than a hook or validator (prompt-audit 1d) | Enforce it in a script or hook; delete the prose if nothing enforces it and nobody misses it |
| PC-20 | Opus 5 era mitigations not re-tested: verbosity, over-verification, scope, thinking-off workarounds | `rg -i -e 'verbos' -e 'before each tool call' -e 'before a tool call' -e 'internal XML tags' -e 'internal tags'` | These patched Opus 5 behavior; Opus 5.5 may not reproduce the failure (migration, behavioral shifts) | Re-test the removal on the sprint's own checks; keep the line only if the failure reproduces |

Every signal joins alternatives with repeated `-e`, never with `\|`. PC-01 reports a count per file; the review flags every line that holds two or more of the capitalized words and records the per-file count in the review note.

### 3.2 Keep list

Do not remove or soften these, even when a signal matches.

| ID | Keep | Reason |
| :--- | :--- | :--- |
| PC-K1 | Safety prohibitions and prohibitions that carry a reason or a policy constraint (secrets, destructive operations, branch rules) | The failure reproduces and the constraint is observable (prompt-audit keep list 5) |
| PC-K2 | Measured facts, the command that reproduces them, and their reasons | Context only the author knows is never cruft (keep list 1) |
| PC-K3 | Exit codes, interface and tool contracts, parameter semantics, failure modes | Contract detail stays and often grows (keep list 4) |
| PC-K4 | Ownership: which role or file owns which artifact | Context the model cannot infer (keep list 1) |
| PC-K5 | Exact commands for fragile operations where one sequence is safe | Low-freedom text is correct for destructive or compliance steps (keep list 3) |
| PC-K6 | Trigger and routing text (skill `description`, rule-trigger rows) | May carry calibrated urgency; flag shouting in bodies only (keep list 6) |
| PC-K7 | A one-line role statement, a single end-of-document recap, format-pinning examples labeled illustrative | Working text, not padding (keep list 8-10) |
| PC-K8 | Added guidance for Opus 5.5 failure modes | Re-baselining sometimes adds text (keep list 11) |

## 4. Verify it worked

| Check | Command or evidence |
| :--- | :--- |
| Every added line was run against the signals | The review note lists each PC-ID that matched and the action taken |
| No deletion rests on length alone | Each removal names its PC-ID; no row cites "too long" |
| No contradiction introduced | PC-04 grep of each key term the change touched returns one canonical statement |
| Removed text had no out-of-band reader | `rg -e '<removed phrase>' .` returns no test, script or workflow matching that text |
| Removal is a hypothesis | Re-run the sprint's gates after each contested removal; if one regresses, re-add the minimal form, not the original |

## 5. Interaction with `unambiguous_action`

`agents.md` §1 `unambiguous_action` has priority over every row above: an instruction must stay executable without interpretation. Trimming removes noise around an instruction, never the operation, target or done-criterion inside it.

| Situation | Resolution |
| :--- | :--- |
| A trim would delete the done-criterion of a step | Keep the criterion; PC-07 and PC-17 apply only to text that adds no operation, target or check |
| Shortening a prohibition makes its subject vague | Keep the explicit prohibition (`restrictions` requires prohibitions to be defined explicitly) and attach its reason; PC-11 changes the form, not the scope |
| Positive rewrite replaces an enumerated list | Allowed only when the rewritten line names the operation and target; otherwise keep the list |
| A criterion reads "correct" or "clean" | Replace the adjective with the check that proves it, as `unambiguous_action` requires |

## 6. If something goes wrong

| Symptom | Action |
| :--- | :--- |
| A signal matches text the keep list protects | Leave the text; note the PC-K ID in the review |
| A row and an `agents.md` rule disagree | Follow `agents.md`; record the conflict for the Sprint 060 corpus audit |
| A signal fires on many lines of one file | Treat as one finding per row, not one per line, and defer corpus-wide cleanup to Sprint 060 |
