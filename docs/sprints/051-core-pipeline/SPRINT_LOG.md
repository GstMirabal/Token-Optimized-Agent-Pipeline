# Sprint 051 — Host-reported defects, and a register that stopped tracking them

**Phase reached**: 7 (Quality Gate) complete. **Branch**: `ai-sprint/051` · **Base**: `main` @ `753fbe1`
**Session**: 2026-09-23/24, Claude Code (Opus 5), nucleus mode, `delegation_mode: native`.

---

## 1. Why this sprint existed

A host swept every framework-class finding it had ever recorded — 26 — and re-verified each
against `v4.32.0` rather than against either register, because both were stale: the host's
inventory measured `v4.4.0` (2026-08-16) and `UPSTREAM_FINDINGS_FROM_HOSTS.md` had not been
touched since 2026-08-26, eleven nucleus sprints earlier.

The `/start` briefing was summarising that file as **`Still open: 0`** against nine
reproducible defects. `agents.md §0` tells every nucleus session to read it before planning,
so a register reporting nothing open misdirects exactly the sessions that obey.

One finding is why the sweep happened at all: `detect_drift.py` stopped a host's boot on its
own in-flight sprint commits, and the briefing that delivers the Documentation Entry Point runs
**after** that gate. The host planned a full session without the anchor documents the ruleset
mandates, and found the contradictions between them only by reading them by hand.

## 2. Gate log

| Gate | Round | Verdict | Class | Notes |
| :--- | :--- | :--- | :--- | :--- |
| QA Gate 1 | 1 | `REJECTED` | `charter` | Six findings. `F-1` charter: `integration_ref()` consulted the local branch before `origin/`, so a stale local `main` demoted work already on its remote out of the blocking half — the `PRs #26-#30` failure reintroduced by `W-01`, the fix meant to sharpen it. `F-2` substring citation match. `F-3` two findings existed only in a status block. `F-4` `1cb4be8` carries two structural subjects. `F-5` `--current-sprint` was in `W-07`'s done-criterion and never shipped. `F-6` `check_task_scope.py` changed with no unit row |
| QA Gate 1 | 2 | `RECORD` | `testifying` | Nothing blocks. Both `charter` defects verified closed by **constructing the failure case**, not by reading the commits — and the gate faulted the shipped regression test for failing against pre-fix code with `AttributeError` rather than behaviour. Six observations: `G2-1` five units reported `⬜` after landing, `G2-2` two leads claimed a verdict they never got, `G2-3` only two of five verdicts asserted, `G2-4` one unannotated parameter, `G2-5` `ruff` exits 1 with 56 findings identical to `main`, `G2-6` pre-existing nesting depth. `G2-1`–`G2-4` remediated |
| Tester Gate 2 | 1 | `RECORD` | `testifying` | Seven findings, none blocking; 5/5 defect-then-fix pairs reproduced independently of the shipped tests; zero tests lost against baseline. Finding 1 is the one that mattered: `integration_refs()` hardcoded `origin`, so the `charter` hole reopened under the `upstream/` remote the fork workflow `§4 feedback_upstream` **mandates** — the only place HEAD was less safe than `753fbe1`. Finding 2: the citation matched anywhere in the section, so a `git revert <sha>` in a code fence cleared the commit it says was undone. Findings 1–4 remediated |

**Three `charter`-class defects were introduced by this sprint and caught by its own gates.**
All three sit in `detect_drift.py`, the file the sprint existed to repair, and all three have
the same shape: a fix that narrowed a false positive also narrowed the true positive it was
built to catch. That is the argument for fresh-context gates, made against the session that
had just skipped Phase 4.

## 3. What landed

| Phase | Units | Effect |
| :--- | :--- | :--- |
| A + A2 | `W-01`–`W-04`, `W-15`–`W-18` | The boot and the gate: merge-base split, `pytest.ini`, two TMPDIR-blind tests, ledger-maintenance exemption, citation coverage |
| B | `W-05`–`W-08` (`W-09` withdrawn) | `node_delta` `TypeError` after eleven sprints; `loop_guard` finding its `task_scope.md` |
| C | `W-10`, `W-11` | IDE branch prefixes in `RA-03`/`RA-12`; Phase 5 scoped to one `Sprint_ID` |
| D + E | `W-12`–`W-14` | The register: 14 closures named, verdicts for the rest, two findings opened |
| F | `W-19`–`W-25` + Gate 2 | `F-051-R2`, then both gates' remediation |

Suite **780 → 813**. `make verify` exit `0`, including all seven installer scenarios.
`ruff check .` exits `1` with 56 findings **byte-identical to `main`** — zero attributable
here, and `agents.md §1`'s "reject if exit code > 0" is unsatisfiable at baseline, so it
cannot be this sprint's gate (`G2-5`).

## 4. Process deviations, recorded because they are the useful part

**Phase 4 ran after Phase 6.** The session executed every phase in-session and wrote
`task_scope.md` at Closeout — the exact shape `pipeline_workflow.md:27` cites as its
precedent. The invariant held by the author's discipline rather than by the file, and Gate 1
then found six things, two of them `charter`. Nothing external checked the work while it ran.

**`1cb4be8` carries two structural subjects** (`F-4`, confirmed). A failed `git add` on a
gitignored path short-circuited an intended split. Recorded and mapped rather than rewritten:
the squash-merge erases the boundary a rewrite would buy, and a rewrite invalidates every SHA
already cited against that commit. The first version of that note argued instead that the push
hook made a split impossible — presenting a policy choice as a technical one, which Gate 1
round 2 faulted and which is corrected in `task_scope.md`.

**Two of the host's 26 verdicts were wrong on first pass**, both by reading a symptom line
without following the call path: `F-093-N2` (`main()` chdirs) and the
`_bridge_permission_denied` lead (fixed in Sprint 044). Both recorded as closed, not as found.

## 5. Open, and where it lives

`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` — **six** open, each with its own entry, and the
count is `grep -c '^### - \[ \]'`-reproducible (`RA-14`).

| Finding | State |
| :--- | :--- |
| `F-051-R1` | Three artifacts name `principal_agent` as author; its profile holds no `Write`. Reproduced live this session. Not patched: the two fixes redraw a role boundary in opposite directions and `ADR-0009` used the second reasoning for `devops_agent` |
| `F-051-R3` | `check_role_artifact.py` resolves the **host's** script against the session cwd, so a gate auditing the nucleus was asked ten times for a row in another repository's sprint log. Satisfying it breaches `§3 jurisdiction`; not satisfying it means it repeats |
| `REVDOC-G1` | Verdict changed: third-party cause, risk retained under `§2 graph_sovereignty` |
| `ADR-0006`, `ADR-0007` | Not re-measured; declared host deviations, not defect reports |
| `#13` | `owned-by-050`, not closed |

**Carried, not closed**: Gate 2 findings 5, 6 and 7 — `pytest.ini` silences a test file that
was already uncollectible but used to fail loudly; 22 of 29 new tests fail against baseline on
API shape rather than on the defect; and `1cb4be8`'s message says "two gates" where only one
now inspects, because `check_gate_log` skips for a different reason.

## 6. Next session starts here

Phase 8 Closeout: this file, the `CHANGELOG.md` `[Unreleased]` entry, then
`close_workflow.md`, the merge to `main` and tag `v4.33.0` — which is what the reporting host
pins to so its boot reaches the briefing for the first time.
