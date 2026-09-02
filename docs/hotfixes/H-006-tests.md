# 🚑 Hotfix: H-006-tests
**File**: `docs/hotfixes/H-006-tests.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `HIGH`
**Detected**: 2026-09-02 · **Resolved**: 2026-09-02

---

## 1. Symptom

`make verify` exits `1` on `main` at `e29ac98`, and so does CI, which invokes that
target rather than listing its own steps. The failing assertion is
`tests/test_session_protocol.py::test_fresh_ttl_does_not_rewrite_last_platform_probe`.
Nothing was committed to cause it: the suite was green on 2026-08-31 and red on
2026-09-01, because the date changed. Blast radius is every session and every host
that runs the framework self-check, and the failure is permanent — it does not
recover on a later date.

Found on 2026-09-02 during Sprint 042 Phase 7, after both Double-Gate agents had
measured `make verify` at exit `0` earlier the same sprint. Both measurements were
correct when taken; the clock moved, not the tree. The sprint did not cause it,
verified by running the single test in a detached worktree at `e29ac98`:
`1 failed`.

## 2. Root Cause

`tests/test_session_protocol.py:1657`

```python
prior = "2026-08-25T12:00:00Z"
```

fed to `scripts/session_probe.py:594-598`, which compares that stamp against the
present:

```python
if datetime.now(timezone.utc) - seen < timedelta(days=PLATFORM_TTL_DAYS):
```

with `PLATFORM_TTL_DAYS = 7` (`scripts/session_probe.py:52`). The fixture is an
absolute instant tested against a **relative** predicate, so it was inside the TTL
for exactly seven days after 2026-08-25 and outside it from 2026-09-01 onward. The
test then measured the opposite branch from the one it names and asserts.

The defect class is a test fixture that expires. It is bounded and the bound is
measured, not assumed: `datetime.now`/`utcnow` compared against stored state
occurs exactly once in the entire codebase —
`grep -rn "datetime.now\|utcnow" scripts/*.py hooks/*.py` returns
`session_probe.py:598` and one unrelated telemetry timestamp — so this is the only
test that could fail this way, and no sibling is waiting to expire. The absolute
dates in `tests/test_ci_gate.py` are compared against each other, never against
the present.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `tests/test_session_protocol.py` | `prior` derived from the present (`now - 1 day`) instead of a literal instant, and a companion case added that pins the expired side of the same boundary (`now - 8 days`), so both branches of the TTL are asserted deterministically at any future date |

Branch/commit: `hotfix/H-006` → recorded by git (do not hand-edit). **Branch prefix
is mandatory (`agents.md` RA-03)** — `fix/`, `feat/`, and `chore/` branch names are
protocol loss even when the Conventional Commits message type is `fix`.

## 4. Verification

Failing state observed first, on the unmodified tree:

```
./venv_skillopt/bin/python -m pytest \
  tests/test_session_protocol.py::test_fresh_ttl_does_not_rewrite_last_platform_probe -q
# 1 failed
```

After the fix, and the regression test the rule requires (`test_expired_ttl_reprobes`,
which fails against a tree where the TTL comparison is removed):

```
./venv_skillopt/bin/python -m pytest tests/test_session_protocol.py -q   # all pass
./venv_skillopt/bin/python -m pytest tests/ -q                           # full suite
make verify; echo $?                                                     # 0
```

Time-independence is the property under repair, so it is verified as such rather
than by one green run: both cases are re-run under `faketime`-equivalent
conditions by deriving every fixture from `datetime.now(timezone.utc)`, which makes
the assertions true on any date the suite is executed.

## 5. Rule Amendment Check

- [x] Is this failure class systemic (a process pattern, not a one-off)? **Yes, and it is already indexed.** `agents.md §1 unambiguous_action` requires magnitudes to carry units and a done-criterion; the deeper pattern here — a fixture that is an absolute instant tested against a relative predicate — is the same class `RA-14 PATCH_PROPAGATION` and the T5 «measured figures» rule address for documents: a figure that reproduces only at one moment must carry what makes it reproducible. No new `RA-XX` is drafted, because the corrective instrument already exists and the codebase has exactly one site where it applies. Recorded here rather than amended: `N/A`
- [x] Does the root cause reveal a design decision worth recording? No. `PLATFORM_TTL_DAYS = 7` is unchanged and correct; the test was wrong about how to exercise it. ADR: `N/A`
- [ ] Master Ledger entry added under `[Unreleased]`.
