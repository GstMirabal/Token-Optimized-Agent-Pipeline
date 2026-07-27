---
description: "Pre-Publication Hardening — Public Repo Readiness Audit (Phase 17)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 17 - Pre-Publication Hardening

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100%
- **Sprint ID:** `017` — next sequential number after Phase 16 (`016-folder-topology-migration.md`, `COMPLETED`).

## Objective
Audit and harden this repo before flipping it from private to public: purge business-sensitive/host-identifying content, disclose mixed vendored licensing, close a stray host-identifying leak the earlier terminology sweep missed, and add structural guardrails so a real host project's content never leaks into the public nucleus again.

## Work Breakdown

### Investigation (3 parallel Explore agents)
- Full `git log --all` (185 commits, stash included) audited for secrets. One real GitHub PAT found, confined to a local-only `git stash` entry (never pushed) from an auto-generated "GitHub Desktop" stash, distinct from the token currently active in the (now-removed) `.env`.
- `profiles/crypto-django/` identified as a real, identifiable production trading-bot blueprint (Django app inventory, business thresholds, KYC/vault handling, Polymarket integration) — present since commit `bb8e30d`, in all 10 tags `v3.0.0`-`v4.1.0`.
- `skills/skillopt/data/scenarios.json` found to leak a real macOS username and real host project folder name (`Cryptobot`, a casing variant the case-insensitive Phase 015 sweep still missed) in a training-scenario example path.
- License audit: `frontend-design`/`skill-creator` are Apache-2.0 (undisclosed at the repo's MIT-only root); `django-expert-3rd` is properly MIT-attributed; 11 other vendored skills lack verifiable provenance.

### Remediation
| Task | Result |
| :--- | :--- |
| Retire `.env`/`.env.template` | Confirmed unused for this project; removed both. `mcp_servers/github_mcp/` mechanism kept (may be used later), its README's setup instructions rewritten to not depend on the removed template. |
| Replace `profiles/crypto-django/` | Deleted from the working tree; replaced with `profiles/example-project/` — a fully illustrative profile (fictional rule, agent, `-3rd` skill, MCP registry, manifest) demonstrating the mechanism without any real business content. `tests/test_installer.sh`'s profile-install assertions updated to the new fixture and re-verified passing. |
| Fix `scenarios.json` leak | Real path replaced with a generic placeholder (`/Users/developer/projects/my-app/...`). |
| `NOTICE.md` | New root file disclosing the 3 confirmed non-MIT/attributed vendored skills. |
| `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | New tracking file listing 11 vendored skills with unverified provenance — not a publish blocker, flagged for future review. |
| `.gitignore` hardening | Added `*.pem`, `*.key`, `*.crt`, `id_rsa*`. |
| New CI gate | `.github/workflows/ci.yml` step scanning tracked files for real-looking local developer home paths (`/Users/[^/]+/`, `/home/[^/]+/`), allowlisting generic placeholders — automates exactly the class of leak found in `scenarios.json`. |
| `RA-15: HOST_CONTENT_GENERICIZATION` | New amendment (`agents.md §7`) requiring host-identifying content to be genericized before any `feedback_upstream` contribution; real production profiles never committed to the public nucleus (also noted in `agents.md §3 topological_order` and `skills/README.md`). |
| Community files | `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1), `SECURITY.md`, `CONTRIBUTING.md` (repo-specific: branch discipline, skill creation, what never belongs in a PR here). |

### Deliberately deferred to a separate, isolated operation
The repo's full git history still contains `profiles/crypto-django/` and the real `scenarios.json` path in every commit before this one — removing them from the *tracked tree* here does not remove them from *history*. A `git filter-repo` pass (purge path + replace-text, re-tag `v3.0.0`-`v4.1.0`, force-push) is required for genuine removal and is executed as its own explicitly-confirmed step, separate from this normal PR flow, precisely because it rewrites every commit hash and force-pushes — the highest-risk action in this whole effort.

## Certification Checklist
- [x] `pytest tests/` green (60 tests).
- [x] `tests/test_installer.sh` green against the new `profiles/example-project/` fixture.
- [x] Manifest parity clean (`generate_manifest.py`, 34 skills, `missing: []`, `unlisted: []`).
- [x] New CI absolute-path gate tested locally against the current tree — passes.
- [x] Repo-wide grep confirms no living document references `profiles/crypto-django` or `--profile crypto-django`; only historical Phase 014-016 prose and this file's own narrative mention it.

## Known follow-ups (tracked, not blocking)
- `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` — 11 vendored skills need their real license/origin confirmed.
- `origin: ECC` on 4 Django `-3rd` skills — undefined anywhere in the repo; only the repo owner can say what it refers to.
- The local PAT-bearing `git stash` should be reviewed/revoked on GitHub's side by the owner; cleaning the local stash object doesn't confirm the token's live status.
- The `git filter-repo` history rewrite itself (see "Deliberately deferred" above) — executed as a separate step after this Phase merges.

---
*Closed 2026-07-27, branch `ai-sprint/017`, pending PR against `GstMirabal/.agents`.*
