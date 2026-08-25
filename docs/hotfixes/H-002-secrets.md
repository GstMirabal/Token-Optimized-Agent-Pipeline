# Hotfix: H-002-secrets
**File**: `docs/hotfixes/H-002-secrets.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `CRITICAL`
**Detected**: 2026-08-24 · **Resolved**: 2026-08-25

---

## 1. Symptom

A staged `.env` holding live `NAME=value` credentials (no quotes) passed `hooks/on_commit.py`. `audit_secret_shielding()` returned `True` and the commit was allowed. `prod.env` blocked while `.env`, `.env.local` and `.env.production` passed. Recorded as `F-023-S4` / `F8`; source material is `docs/roadmaps/core/pipeline/021-030-program-queue.md` (Carried out of `023`). Under Cursor this hook is the only secret gate.

## 2. Root Cause

Two independent mechanisms; a file need only beat one. Re-measured on the repaired tree, not carried from the report.

| # | Mechanism | Evidence |
| :--- | :--- | :--- |
| 1 | Forbidden-extension branch never fires on the filenames in use | `Path(".env").suffix` is `''`, not `".env"`. `.env.production` has suffix `".production"`. `prod.env` **is** blocked — the gate caught the name nobody uses |
| 2 | Form selection, not quoting | `secret_forms_for(Path('.env'))` returned `SECRET_ASSIGNMENT`, `QUERY_STRING_SECRET`, `PRIVATE_KEY_BLOCK`. Only `SECRET_ASSIGNMENT` addresses `NAME=value`, and it requires a quoted value. `YAML_SECRET` and `DOCKERFILE_SECRET` accept unquoted values in *their* shapes (`key: value`, `ENV`/`ARG`) and are never selected for a `.env` |

The unquoted `NAME=value` shape was missed in **every** file type (`settings.py`, `app.yml`, `Dockerfile`), not only `.env`. The obvious diagnosis — *"the patterns require quotes"* — is false: three of four named forms already accept unquoted values. Repairing on it would add quote-optionality where it already exists and still ship the bug.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `hooks/on_commit.py` | Name-match dotenv files (`.env`, `.env.*` except `.example`); add `UNQUOTED_ASSIGNMENT` (`NAME=value` with EOL terminator) to the set selected for every file type; expose `is_forbidden_secret_file()` |
| `tests/test_on_commit.py` | Pin both mechanisms. Fixtures use `LIVE`, not a documented placeholder and not a PEM or query-string secret |
| `rules/qa_and_testing.md` | Forbidden-file list names dotenv files by name |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `F-023-S4` ticked closed |

Branch/commit: `hotfix/H-002` (SHA recorded by git; do not hand-edit).

## 4. Verification

Failing tests written first and observed red (`API_KEY=<LIVE>` → `None` on `.env`, `settings.py`, `app.yml`, `Dockerfile`). After the hook change:

```
./venv_skillopt/bin/python -m pytest tests/test_on_commit.py -q --tb=line
# 152 passed
```

Reproduction that must now refuse: stage `.env` containing `API_KEY=<credible non-placeholder value>` and `DB_PASSWORD=<same>`; `is_forbidden_secret_file(Path(".env"))` is `True`; `find_hardcoded_secret` on the unquoted line returns the identifier in every file type.

## 5. Rule Amendment Check

- [x] Systemic process pattern? The *unowned routing* is already indexed (`F-023-S4` provenance). The technical miss is the same class `C3` already closed for `Dockerfile` (a suffix test cannot see a name that begins with its own dot). No new `RA-XX`. Link: `N/A`
- [x] New architectural choice? No. The gate's contract did not change: `.env` was always intended as a forbidden file. Name-matching vs suffix is the `C3` decision applied to dotenv. ADR: `N/A`
- [x] Master Ledger entry added under `[Unreleased]`.
