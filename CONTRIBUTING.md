# Contributing

This repo governs its own development the same way it governs any host project — read `agents.md` first, it's the actual source of truth. This file is a practical, contributor-facing summary of the parts that matter for a PR.

## Branching and commits

- All work happens on a branch named `ai-sprint/[ID]`, never directly on `main` (`RA-12 BRANCH_DISCIPLINE`, `agents.md §7`). Pick the next sequential ID after the latest `docs/roadmaps/core/pipeline/NNN-*.md` file.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) and must end with a `#[Sprint_ID]` reference, e.g. `fix(hooks): resolve X #018`. This is mechanically enforced by `hooks/on_commit.py` when running under Claude Code.
- Open a PR from your `ai-sprint/[ID]` branch into `main`. CI (`.github/workflows/ci.yml`) must pass before merge.

## Adding a new skill

Use the `skill-creator` skill to scaffold the boilerplate (`SKILL.md`, `README.md`, `scripts/__init__.py` for executable skills — the "Three-File Skill Standard", `agents.md §3`). Register it in `skills/manifest_skills.json` by running `python3 skills/mass-standardizer/scripts/generate_manifest.py` — that file is generated, never hand-edited (CI enforces this).

Vendoring an existing third-party skill? Suffix its directory name `-3rd` (e.g. `some-skill-3rd/`) and include real attribution (source URL, license) — see `NOTICE.md` for the pattern. Don't add a `-3rd`-suffixed skill without knowing its actual license; see `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` for what happens when that slips.

## What does NOT belong in a PR to this repo

- **Real project profiles.** `profiles/[name]/` is for illustrating the mechanism (see `profiles/example-project/`) — a real production profile, with a real project's business rules, real app inventory, or real domain agents, stays in that project's own private location and is referenced locally via `--profile [name]`, never committed here.
- **Anything host-identifying**, if you're contributing a fix you found while working inside a real host project: real absolute filesystem paths, real project/company names, real business logic or thresholds. Genericize before you open the PR (`RA-15 HOST_CONTENT_GENERICIZATION`, `agents.md §7`).
- Secrets of any kind, obviously — `.env` files, tokens, keys. `skills/env-shielding-auditor/` runs in CI and will catch the obvious cases, but don't rely on it as your only check.

## Framework-class contributions

If you're fixing something you found while using this framework inside a host project, and the fix would help *every* host (not just yours), that's a framework-class contribution (`agents.md §4 feedback_upstream`) — exactly what this repo wants. Just genericize it first (see above) before the PR.

## Questions

Open a discussion or issue. For anything sensitive, see `SECURITY.md`.
