# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in this repository (the framework itself — its hooks, installer, or CI, not a specific host project that uses it), please report it privately rather than opening a public issue.

- **Email**: the maintainer's address is listed in `config/framework_identity.json` (`framework_author_email`).
- Include what you found, how to reproduce it, and its potential impact if you can.
- You should expect an acknowledgment within a few days. There is no bug bounty program.

## Supported Versions

Only the latest tagged release receives security fixes. There is no backport policy for older tags — pin to a release (see `README.md` → Getting Started) and upgrade when a fix lands.

## Scope

In scope: `hooks/`, `scripts/install_claude.sh`/`install_claude.py`, the CI workflow, and anything in the core framework that could let untrusted input execute code or exfiltrate secrets from a host project.

Out of scope: vulnerabilities in vendored third-party skills (`-3rd` suffix) — report those upstream to their original source instead. See `NOTICE.md` and `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` for what's vendored versus native.
