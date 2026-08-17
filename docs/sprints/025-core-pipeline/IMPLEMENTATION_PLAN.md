---
description: "Implementation Plan — Sprint 025 jurisdiction: host work never dirties the submodule"
status: "PENDING_APPROVAL"
version: 1.0.0
---

# Implementation Plan: Sprint 025 - Jurisdiction

**Branch:** `ai-sprint/025`, from `ai-sprint/024` — not from `main`.

The same reason Phase 020 branched from 019: the guard this sprint builds is
**blind without Sprint 024's `.gitignore` change**. `git status --porcelain` does
not list ignored files, and until `024` the paths a host would contaminate were
all ignored. Building the check on `main` would produce a check that passes on a
dirty tree — the exact defect both sprints exist to remove.

## Context

`agents.md §3 strict_rule` forbids a host from altering the submodule, and
`§4 feedback_upstream` routes framework-class findings to the nucleus repository
through a branch and a pull request. Between them the doctrine is complete.

**The enforcement is one sentence.** `close_workflow.md` Phase 5
`submodule_purity` says *"Verify `git -C .agents status --porcelain` is clean"*
and there is no script. `scripts/scan_workflow_determinism.py` already flags it
— that warning has been in every `make verify` run and nobody acted on it. So
the only protection against a host session dirtying `.agents` depends on an
agent remembering to type a command, and until Sprint `024` that command was
blind anyway.

Recorded as `F-024-D8`.

**The upside this unlocks is the human's stated goal**: improving the framework
*from* a host project. That is legitimate and `feedback_upstream` already
describes it — what has been missing is anything that distinguishes it from
contamination. A rule that cannot tell the sanctioned act from the forbidden one
protects neither.

## Design

### The discriminator already exists

[`scripts/session_probe.py:59-65`](../../../scripts/session_probe.py) —
`is_nucleus()` returns whether `.git` is a real directory or a submodule pointer.
`scripts/install_claude.py:284` uses the same test. It is extracted, not
reinvented.

| Mode | `.agents/.git` | Jurisdiction | This check |
| :--- | :--- | :--- | :--- |
| Nucleus | directory | the framework is the work | no-op — there is no submodule to protect |
| Submodule | file (pointer) | the host is the work | **enforced** |

### The rule, stated so a machine can check it

> A session's jurisdiction is where its anchor is. **A host session must leave
> `git -C .agents status --porcelain` empty.** Framework improvements from a
> host go through `feedback_upstream`: a branch and pull request against the
> nucleus repository, worked in a separate clone — a distinct act from the
> host's sprint, never a write into the submodule's tree.

### Why "empty" is the right threshold, not a judgement call

Everything legitimately transient inside `.agents` is already gitignored:
`venv_skillopt/`, `graphify-out/`, `memory/`, `.claude/`, the lock files, the
anchor and its mirror. If anything reaches `--porcelain`, it is real content —
so the check needs no allowlist and no severity scale.

### The answer the gate must carry

`config/abandoned_branches.json` establishes the doctrine: *a gate with no answer
gets disabled rather than satisfied*. This one answers in its message rather than
with a waiver file, because there is no legitimate dirty state to waive:

- Contributing upstream → clone the nucleus separately; the submodule stays clean
- Experimenting → `git -C .agents stash`
- Deliberate pin change → that is a gitlink change in the host, not a dirty tree

## Work

| # | Action | File |
| :--- | :--- | :--- |
| J1 | `is_nucleus()` extracted to a shared helper; `session_probe.py` and `install_claude.py` consume it instead of each testing `.git` themselves | `scripts/_mode.py` (new) + 2 consumers |
| J2 | **The check**: host mode + non-empty `--porcelain` → exit `2`, classifying *what* dirtied it (untracked content vs modified tracked file) because the two are different failures with different remedies | `scripts/submodule_purity.py` (new) |
| J3 | `close_workflow.md` Phase 5 invokes the script instead of describing a command; the determinism scanner's standing warning disappears as the proof | `workflows/close_workflow.md` |
| J4 | **The host `pre-commit` hook calls it**, so contamination is refused at commit time and not only at close. The bridge already installs into `HOST_DIR/.git/hooks/` (`install_claude.py:244`) | `hooks/on_commit.py` |
| J5 | The rule written into `agents.md §3` beside `strict_rule` and `federation`, which state the doctrine but name no enforcement | `agents.md §3` |
| J6 | `invoked_by:` declared on the new scripts (`RA-16`) | both new files |

## Tests

| Check | Must fail against the current tree |
| :--- | :--- |
| Synthetic host: `.agents/.git` as a **file**, an untracked file under `.agents/docs/` → exit `2`, naming the path | **Yes** — no script exists |
| Same host, clean submodule → exit `0` | **Yes** |
| Same host, a **modified tracked** file in `.agents` → exit `2`, classified differently from untracked | **Yes** |
| **Nucleus mode → exit `0` always**, even with a dirty tree. Regression guard: this repository's own sprints must not be refused by a check meant for hosts | **Yes**, and it is the mirror of Sprint 024's `D7` — a guard that fires on the wrong side of a boundary |
| An ignored-only dirty state (a fresh `venv_skillopt/`) → exit `0` | **Yes** |
| `scan_workflow_determinism.py` no longer warns about `submodule_purity` | **Yes** — it warns today |
| `make verify` green, `verify_references.py` check (d) resolves both new invokers | No |

## Out of scope

| Exclusion | Reason |
| :--- | :--- |
| Preventing the write itself | Would need a tool-specific `PreToolUse` hook. Sprint `027`'s rule binds: what must hold under both tools lives in git hooks or scripts, never in `settings.json`. Detection at commit and at close is the portable guarantee |
| Splitting `docs/active_state.json` by lifetime (`F-024-D9`) | Adjacent but separate: this sprint is about jurisdiction between repositories, that one is about two lifetimes inside one file |
| Automating the upstream contribution flow | `feedback_upstream` describes it and it works. What was missing is the boundary, not the path |

## Abort criterion

If the nucleus-mode regression test ever fails — the check refusing this
repository's own work — revert via `workflows/remediation_workflow.md`. A
jurisdiction guard that fires inside its own jurisdiction is Sprint 024's `D7`
defect rebuilt, and it would block every nucleus sprint.
