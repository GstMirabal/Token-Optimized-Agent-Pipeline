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

> [!IMPORTANT]
> Order matters twice. Branch protection blocks history rewriting, so it goes
> after any planned rewrite. And a required status check that never runs makes
> every pull request unmergeable — so protection is configured from check names
> **observed on a real run**, never from names typed from memory.

## Execution Flow

| Phase | Action | When |
| :--- | :--- | :--- |
| **1** | Secret scanning, push protection, private vulnerability reporting | First. No code changes, immediate risk reduction |
| **2** | Dependabot alerts and security updates | First |
| **3** | Code scanning (CodeQL) | First |
| **4** | Triage every alert produced | Before any history decision |
| **5** | Community health files | Any time |
| **6** | Repository metadata: description, topics, homepage | Any time |
| **7** | History rewrite, if any | Before phase 8 |
| **8** | Branch protection | **Last** |

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
