# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in this repository (the framework itself — its hooks, installer, or CI, not a specific host project that uses it), please report it privately rather than opening a public issue.

- **Email**: the maintainer's address is listed in `config/framework_identity.json` (`framework_author_email`).
- Include what you found, how to reproduce it, and its potential impact if you can.
- You should expect an acknowledgment within a few days. There is no bug bounty program.

## Host findings: channel C

A host project that finds a framework defect touching `RA-09`/`RA-19`, secrets, hooks or the sandbox reports it here, never as a public `host-finding` issue (`agents.md §4 feedback_upstream`, channel C).

- Use GitHub Private Vulnerability Reporting: the repository's **Security** tab → **Report a vulnerability**. The email above is the fallback.
- Paste the outbox entry (`docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` shape) with `channel: C`, genericized (`RA-15`). `upstream_outbox.py export` refuses channel C, so nothing prints a public `gh issue create` command for it.
- A public `host-finding` issue whose text matches the intake filter's security words is labelled `security-suspect` and receives a comment redirecting it here. That filter is a word list and does not decide what is sensitive; the reporter does.

## Supported Versions

Only the latest tagged release receives security fixes. There is no backport policy for older tags — pin to a release (see `README.md` → Getting Started) and upgrade when a fix lands.

## Scope

In scope: `hooks/`, `scripts/install.sh`/`install.py`, the CI workflow, and anything in the core framework that could let untrusted input execute code or exfiltrate secrets from a host project.

Out of scope: vulnerabilities in vendored third-party skills (`-3rd` suffix) — report those upstream to their original source instead. See `NOTICE.md` and `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` for what's vendored versus native.
