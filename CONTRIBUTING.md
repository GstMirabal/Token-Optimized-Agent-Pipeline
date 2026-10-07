# Contributing

This repo governs its own development the same way it governs any host project — read `agents.md` first, it's the actual source of truth. This file is a practical, contributor-facing summary of the parts that matter for a PR.

## Branching and commits

- All work happens on a branch named `ai-sprint/[ID]`, never directly on `main` (`RA-12 BRANCH_DISCIPLINE`, `agents.md §7`). Pick the next sequential ID after the latest `docs/roadmaps/core/pipeline/NNN-*.md` file.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) and must end with a `#[Sprint_ID]` reference, e.g. `fix(hooks): resolve X #018`. This is mechanically enforced by `hooks/on_commit.py` when running under Claude Code.
- **The same hook scans staged content for hardcoded secrets and will refuse the commit.** Since Sprint 023 it recognises `ENV`/`ARG` lines in a `Dockerfile`, `key: value` pairs in YAML, and secrets embedded in URL query strings — not only quoted `NAME = "value"` assignments. Hotfix H-002 also refuses a staged `.env` / `.env.*` (except `.env.example`) and unquoted `NAME=value` in every file type. A contribution that legitimately contains a credential-shaped **example** can be blocked where it previously passed. When the value really is an example, waive that one finding with the documented `ALLOW_MARKER` rather than rewording it until the scanner stops noticing: the procedure and what a valid justification looks like are in `rules/qa_and_testing.md §5`. A gate that gets tuned down to pass is not a gate.
- **Since Sprint 052 the hook also refuses a sprint commit that reaches outside the sprint directory before `task_scope.md` exists.** A commit suffixed `#[ID]` on `ai-sprint/[ID]` that stages any path outside `docs/sprints/[ID]-*/` is blocked until that directory holds `task_scope.md`, either committed or staged. Plans, logs and the scope itself commit freely (upstream `ADR-0007`, Guard 5 in `hooks/on_commit.py`).
- **Since Sprint 054 a `fix(` commit that stages source must show its test failing first.** Beyond staging a test, the message carries a trailer naming that test and the parent it fails on — `Repro: tests/test_x.py::test_y — fails at <short sha>` — or, when no automated test can show the defect, `Repro: manual — <SPRINT_LOG section>`. The hook only checks the claim; QA Gate 1 observes it by running `scripts/check_fix_reproduces.py --range <base>..HEAD`, which replays each named test on the parent (it must fail with pytest exit `1`; an import or collection error does not count) and at the commit (it must pass). Write the test, watch it fail, then fix (`rules/code_craft.md §6`).
- Open a PR from your `ai-sprint/[ID]` branch into `main`. CI (`.github/workflows/ci.yml`), which runs `make verify`, must pass before merge. `make verify` gates these code-quality checks beyond the tests:
  - **Complexity, since Sprint 052:** `scripts/quality_audit.py` fails the gate on a function over 50 executable lines or nested deeper than 3 blocks (`agents.md §1 max_lines_per_func` / `max_indentation`). Run `python3 scripts/quality_audit.py --report .` locally to see the register. Vendored upstream files are exempted one by one, with provenance, in `config/quality_audit_exclusions.json`, never by directory.
  - **JS/TS measurement, since Sprint 053:** the same audit also measures `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs` and `.cjs` files through `tree-sitter` (`agents.md §1 linter_command`, JS/TS row). When JS/TS files are in scope and `tree_sitter` is not importable, the audit fails closed with exit 2 and tells you to run `pip install -r requirements-quality.txt`. Python measurement stays stdlib-only.
  - **Lint, since Sprint 053:** `make verify` runs the pinned `ruff check .` (`agents.md §1 linter_command`, Python row). `ruff` is pinned to `0.16.3` in `requirements-quality.txt` and `ruff.toml` (`required-version = "==0.16.3"`, explicit `select`, `extend-exclude` listing the ten vendored `skills/skill-creator/` paths from `config/quality_audit_exclusions.json`). Install and run it locally with `venv_skillopt/bin/pip install -r requirements-quality.txt` then `venv_skillopt/bin/ruff check .`. Suppress a finding only with `# noqa: <code>` plus an inline reason.

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
