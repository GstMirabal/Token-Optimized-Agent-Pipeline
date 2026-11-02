# Changelog

All notable changes to {{PROJECT_NAME}}. This file is the **Master Ledger** (agents.md §0): every Sprint Closeout appends its sprint entry under `[Unreleased]`; every deployment seals that section as `[vX.Y.Z] - date` immediately before tagging.

Format: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/).

> Jurisdiction note: framework changes live in `.agents/CHANGELOG.md`, never here. When the `.agents` pin is updated, this ledger records only the bump (e.g. `chore(deps): pin .agents to v3.1.0 #[Sprint_ID]`).
>
> Host findings: a `.agents/CHANGELOG.md` entry that publishes a finding this host sent upstream cites it as `host:<id>`, the id of its outbox entry (agents.md §4 `feedback_upstream`). After a bump, `sync_agents_pin.py` prints `Ships host findings: <ids>`; the pin-bump entry here names them (e.g. `chore(deps): pin .agents to v3.1.0, ships host:H-7 #[Sprint_ID]`), and `upstream_outbox.py deltas` lists the local rule deltas they retire.

## [Unreleased]

### Added
- Adopted Token-Optimized Agent Pipeline governance ({{AGENTS_VERSION}}) — onboarding scenario: {{SCENARIO}} (see `docs/{{ONBOARDING_REPORT}}` if applicable). #{{SPRINT_ID}}

## [{{LAST_VERSION}}] - {{DATE}}
_Seed entry: state of the project at governance adoption. For scenario C (mature project), summarize the audited inherited state here._
