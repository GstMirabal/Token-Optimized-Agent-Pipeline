---
description: "Repository Hardening Protocol (Keyword: harden)"
version: 1.0.0
invoked_by: human:/agents:harden
---

# 🔒 Workflow: Repository Hardening

Turn on the platform controls a public repository should have, in an order that
does not lock you out of your own work. Runs **first** in any multi-repository
programme — it reduces risk without touching code — except for the last phase,
which runs **last** for a reason given below.

**Mode**: This protocol applies in nucleus mode too. It governs the `.agents`
repository itself, not only host projects. Precedent (`RA-16`): `/agents:harden`
shipped in PR #29 and was never run against this repository, so five platform
controls sat disabled for weeks. Run it here exactly as it is run against any
host.

> [!IMPORTANT]
> Order matters twice. Branch protection blocks history rewriting, so it goes
> after any planned rewrite. And a required status check that never runs makes
> every pull request unmergeable — so protection is configured from check names
> **observed on a real run**, never from names typed from memory.

## Execution Flow

One row per phase. **Operation** is the imperative action to take. **Verify** is
the read-back that proves it, lifted from the phase prose below. Phases 2, 3, 6
and 7 have no `gh` verify call in their prose, so the standard read-back for that
setting is given instead. `$R` is `owner/repo` as set at the top of Phase 1.

| Phase | Step id | Operation | Verify |
| :--- | :--- | :--- | :--- |
| **1** | `secret_scanning` | Enable secret scanning, secret-scanning push protection and private vulnerability reporting, then confirm each setting reads back as `enabled` | `gh api "repos/$R" --jq '.security_and_analysis'` |
| **2** | `dependabot` | Enable Dependabot alerts and Dependabot security updates, then confirm the alert stream is live | `gh api "repos/$R" --jq '.security_and_analysis.dependabot_security_updates'` |
| **3** | `code_scanning` | Enable CodeQL code scanning and confirm the analysis state is reported as configured | `gh api "repos/$R/code-scanning/default-setup" --jq '.state'` |
| **4** | `alert_triage` | Triage every open alert into false positive, expired credential or live credential; verify fixes against a clean install, never the manifest file | `python3 -m venv /tmp/verify && /tmp/verify/bin/pip install -q -r requirements.txt; /tmp/verify/bin/pip list --format=freeze \| grep -iE '^(django\|cryptography\|pillow)='` |
| **5** | `community_health` | Create repository-specific `SECURITY.md`, `CONTRIBUTING.md` and issue templates only where the account-level `.github` defaults would be wrong | `gh api graphql -f query='{ repository(owner:"OWNER", name:"REPO") { issueTemplates { name filename } } }'` |
| **6** | `repo_metadata` | Update the repository description, topics and homepage URL | `gh api "repos/$R" --jq '{description, homepage, topics}'` |
| **7** | `history_rewrite` | Rewrite or squash history only after confirming explicit per-operation human authorization, stating what will be lost before each irreversible action | `git log --oneline origin/main..HEAD` |
| **8** | `branch_protection` | Update branch protection on `main` from the status-check names observed on a real check-run listing, requiring exactly those checks with `enforce_admins:false` and `required_pull_request_reviews:null` | `gh api "repos/$R/commits/main/check-runs" --jq '.check_runs[] \| select(.conclusion=="success") \| .name'` |

## Phase 1 — What is free, and what is not

```bash
R=owner/repo
gh api -X PATCH "repos/$R" -f 'security_and_analysis[secret_scanning][status]=enabled'
gh api -X PATCH "repos/$R" -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'
gh api -X PUT "repos/$R/private-vulnerability-reporting"
```

**Check `private-vulnerability-reporting` specifically.** A `SECURITY.md` —
including the one GitHub applies from an account-level `.github` repository —
typically instructs readers to use the Security tab's *Report a vulnerability*.
That button does not exist until this is enabled, so the policy documents a
channel that is switched off, and a researcher either cannot report or reports
publicly.

Not free on every plan: `secret_scanning_non_provider_patterns` and
`secret_scanning_validity_checks` belong to GitHub Secret Protection. On a free
account **the API accepts the PATCH, returns 200, and leaves the value
`disabled`** — no error. Verify by reading the value back:

```bash
gh api "repos/$R" --jq '.security_and_analysis'
```

Provider-format tokens (AWS, Stripe, GitHub) are still scanned. Generic secrets
— a Fernet key, a hex pepper, a signing key — are not. Where that gap matters,
a local pre-commit hook is the compensating control, and it is free.

## Phase 4 — Triage before deciding anything about history

Classify each alert: **false positive**, **expired credential**, **live
credential**. This replaces a manual scan; the tooling is already there and was
merely switched off.

Two things worth knowing:

- **A live credential is rotated, not erased.** Rewriting history does not
  remove it — GitHub retains unreachable commits addressable by SHA. Rotation
  is the fix; rewriting is cosmetic.
- **Dependabot alerts lag.** After raising a version floor, alerts against the
  old manifest stay open until the next scan. Verify against a **clean
  install**, not against the manifest file:

```bash
python3 -m venv /tmp/verify && /tmp/verify/bin/pip install -q -r requirements.txt
/tmp/verify/bin/pip list --format=freeze | grep -iE '^(django|cryptography|pillow)='
```

A floor of `>=12.3.0` in a file proves what the file says. What resolves proves
what you ship.

## Phase 5 — One place, not nine

An account-level repository named `.github` supplies `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `SECURITY.md`, `ISSUE_TEMPLATE/` and
`PULL_REQUEST_TEMPLATE.md` to every repository that lacks its own.

Write a repository-specific file only where a generic one would be wrong. For a
project holding credentials, `SECURITY.md` should state the boundary between
what the project owns and what its host owns, the limitations that are known
and deliberate, and what to do if a key is exposed — none of which an
account-wide file can say.

**Verification note**: `repos/$R/community/profile` reports `issue_template` as
`null` when templates live in an `ISSUE_TEMPLATE/` **directory**, which is the
current form. That field is a false alarm. Check the real thing:

```bash
gh api graphql -f query='{ repository(owner:"OWNER", name:"REPO")
  { issueTemplates { name filename } } }'
```

## Phase 8 — Branch protection, from observed check names

Collect the names from a run that actually happened:

```bash
gh api "repos/$R/commits/main/check-runs" \
  --jq '.check_runs[] | select(.conclusion=="success") | .name'
```

Then require exactly those:

```bash
gh api -X PUT "repos/$R/branches/main/protection" --input - <<'JSON'
{
  "required_status_checks": {"strict": true, "checks": [{"context": "ci / Lint and tests"}]},
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_linear_history": true,
  "required_conversation_resolution": true
}
JSON
```

Two deliberate choices for a solo maintainer:

- **`enforce_admins: false`.** A required check that breaks — a renamed job, a
  third-party outage — otherwise locks the owner out of their own repository
  with no way back in.
- **`required_pull_request_reviews: null`.** Requiring an approval with no
  second maintainer makes every pull request unmergeable.

What is being bought here is the part that matters: no force-push, no branch
deletion, linear history, and checks that must pass.

## Phase 7 — On rewriting history

Weigh it against what the history now contains. A history of noisy early
commits is worth compacting; one whose recent commits explain *why* each
decision was taken is not — squashing destroys exactly the part worth reading.

Both operations are irreversible from an agent's side. **Ask before each one,
every time**, and state plainly what will be lost.

---
*Complements `deployment_workflow.md`, which owns tags and releases. This
workflow owns platform configuration only.*
