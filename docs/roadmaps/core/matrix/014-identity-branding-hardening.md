---
description: "Config-Driven Identity System & Personal Brand Leak Closure (Phase 14)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 14 - Config-Driven Identity & Brand Leak Closure

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100% (22/22 executable tasks; T9 dropped by human Golden Gate decision)
- **Current UID Seal:** _No graphify baseline exists for this checkout (`graphify-out/` never built here) — confirmed by QA Gate 1 as an informational scope note, not a blocker; initializing one is a separate DevOps decision outside this Sprint._
- **Quality Gates:** Gate 1 (QA, structural) — PASA on re-certification after 2 fixes (`.agents/README.md` broken banner ref, `readme-standardizer` identity-propagation reopened). Gate 2 (Tester, functional) — PASA, 56 pytest + installer sandbox test green, zero regressions.
- **Source of Truth:** `~/.claude/plans/groovy-snuggling-patterson.md` (Golden Gate passed via Plan Mode, human-approved — 9 numbered steps + Archivos Afectados + Verificación).
- **Sprint ID:** `014` — next sequential number after Phase 13 (`013-refined-telemetry-and-redundancy.md`, currently `IN_PROGRESS` on an unrelated telemetry/redundancy track). This work does **not** inherit CryptoBot host numbering (`083`+); the host's `docs/sprints/[ID]-[Stack]-[Layer]/` topology is explicitly not auto-scaffolded onto the nucleus (`agents.md §5 nucleus_neutrality`), and no `.agents/docs/sprints/` directory exists or has ever existed. `.agents`'s own history ledger for substantial work packages is this `docs/roadmaps/core/matrix/NNN-slug.md` sequence (Phases 000-013, git-verified — confirmed no `014-*` file pre-existed) plus `CHANGELOG.md` `[Unreleased]` + eventual SemVer tag. This file **is** the Sprint folder equivalent for this track, in the shape the nucleus already uses for itself — not a foreign host convention grafted on (`agents.md §3 strict_rule`).
- **Precedent checked:** the queued `documentation_standard.md` track (Track A) landed via branch `feat/documentation-standard` + `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md`, with **no** roadmap Phase file and **no** Sprint ID — it predates this Phase-numbering formalization for identity work. Not reused as the pattern here because the user's task brief explicitly invokes literal `ai-sprint/[ID]` (J-12) for this track.

## Objective
Close the personal-brand leak in the 10 distributed skill READMEs, replace ad hoc README branding with a two-tier (FRAMEWORK/HOST) config-driven render system, and retire the stale banner assets — without regenerating `.agents/README.md` from scratch (would destroy real content not present in the template).

## Branch & Execution Note (read before Phase 6)
This session (`orch_01`, Phase 3 — Tactical Blueprint) has **no shell/Bash tool available** — only `Read`/`Write`/`Edit`/`Glob`/`Grep`. The `ai-sprint/014` branch could **not** be created or checked out by this agent. Verified via `.git/modules/.agents/HEAD` and `refs/heads/`: `.agents` is currently on `main`, clean, no `ai-sprint/*` ref exists yet. The next agent with shell access (DevOps Sentinel / Principal Agent at Phase 4-5 handoff) must run, from the CryptoBot host root:
```
git -C .agents checkout -b ai-sprint/014
```
before any file in the tables below is touched, per J-12. This file itself was written directly to the working tree (still on `main` at time of writing) since `Write` has no branch awareness — the first commit onto `ai-sprint/014` should include this roadmap file (currently untracked) as its opening commit.

## Finding: plan says "11 README.md", verified count is 10 physical files
`agents.md §1 exception_handling` / due diligence check before drafting Phase C below. Grepped `.agents/skills/` for the plan's own Verification-section signature (`gst.mirabal@gmail.com|linkedin.com/in/gstmirabal|x.com/gst_mirabal`, Paso 5 + Verificación §3) — **10 files match**, exactly the 10 named in the plan's "Archivos Afectados" list (9 skill `README.md` + `readme-standardizer/assets/template.md`). A broader grep (bare `GstMirabal`/`Gustavo Mirabal`) surfaces an 11th file, `skills/readme-standardizer/SKILL.md`, but it only contains a hardcoded `GstMirabal` example URL and a generic instruction to preserve "the Contact section" — no actual email/LinkedIn/X leak. It does **not** fail the plan's own Verification gate (Paso 5, 3rd bullet), so it is **not** added as a mandatory task here (would be undiscussed scope drift past the approved Golden Gate). Flagged for the Principal Agent / human to decide whether the plan's "11" prose should be corrected to "10" (J-14 PATCH_PROPAGATION-style drift between narrative and file table) and whether `SKILL.md`'s example URL is worth a discretionary follow-up.

**Resolution (Tactical Liquidation):** the frozen, already-approved plan file (`~/.claude/plans/groovy-snuggling-patterson.md`) is left as-is — a post-hoc prose edit to an already-Golden-Gated artifact isn't worth the historical-record risk for a one-word count discrepancy that was fully surfaced and explained here. `SKILL.md` ended up edited anyway, but for a different and more serious reason found later at QA Gate 1 (see Certification Checklist below): it wasn't just an illustrative example URL, it actively instructed propagating the framework author's real contact info into third-party projects. That's fixed now, independent of this 11-vs-10 count question.

---

## Work Breakdown Structure

### Phase A — Config & Rendering Engine (Plan Steps 1-3)
| Task | File (1 per task, `jurisdictional_lock`) | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T1 | `.agents/config/framework_identity.json` | new | — |
| T2 | `.agents/docs/standards/templates/IDENTITY_TEMPLATE.json` | new | — |
| T3 | `.agents/scripts/render_readme.py` | new | T1, T2 (consumes both schemas + the Paso 1 nucleus field-mapping table) |

### Phase B — Template Rework & Command-Table Extraction (Plan Step 4)
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T4 | `.agents/docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | new | — (content sourced read-only from current `README_TEMPLATE.md`) |
| T5 | `.agents/docs/standards/templates/README_TEMPLATE.md` | edit | T3 (tag contract: `{{PROJECT_HOOK}}`, `{{GOVERNED_BY_AGENTS}}`, version badge, `{{INSTITUTIONAL_IDENTITY}}` alias must match the renderer), T4 (guide must exist before the template links out to it) |

### Phase C — Skill README Leak Closure (Plan Step 5) — 10 atomic tasks, parallelizable
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T6 | `.agents/skills/token-saver-auditor/README.md` | edit | — |
| T7 | `.agents/skills/omni-context-minimizer/README.md` | edit | — |
| T8 | `.agents/skills/python-quality-auditor/README.md` | edit | — |
| T9 | `.agents/skills/skill-creator-3rd/README.md` | edit | — |
| ~~T9~~ | ~~`.agents/skills/skill-creator-3rd/README.md`~~ | **DROPPED** — `rules/skills_and_integrations.md §3` Skill Documentation Veto blocks editing `-3rd`-suffixed skill READMEs; Golden Gate 2026-07-25 resolved via `task_scope.md` Finding #4, path (a): leave this file untouched this Sprint. Follow-up (mislabel investigation) explicitly out of scope. | — |
| T10 | `.agents/skills/readme-standardizer/README.md` | edit | — |
| T11 | `.agents/skills/readme-standardizer/assets/template.md` | edit | — |
| T12 | `.agents/skills/mcp-registry/README.md` | edit | — |
| T13 | `.agents/skills/js-standardizer/README.md` | edit | — |
| T14 | `.agents/skills/env-shielding-auditor/README.md` | edit | — |
| T15 | `.agents/skills/slash-commander/README.md` (strip identity/badges/Contact block) | edit | — |

None of T6-T15 depend on Phase A/B (plan is explicit: "no requiere que estos archivos usen `render_readme.py`"). Fix is purely subtractive: delete the badges/ToC/Contact boilerplate block, keep the skill's real documentation content above it.

### Phase D — `.agents/README.md` In-Place Patch (Plan Step 6)
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T16 | `.agents/README.md` | edit (incremental patch, **not** regenerated from template — would destroy `About`/`Built With`/`Getting Started`/`Contributing`/`License` sections the template doesn't have) | T1 (config values for banner path + short-form credit line), T4 (command table already moved out before the summary-with-link is inserted) |

Note: T16 may run using `institutional_banner.png` or the new SVG (T20), whichever exists at execution time — plan explicitly allows either (see Phase G).

### Phase E — Installer Integration (Plan Step 7)
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T17 | `.agents/scripts/install_claude.py` | edit (existence-guard scaffold of `identity.config.json`, `link_one()` pattern — not `merge_json.py`; auto-fill `repo_slug` via `git -C <host> remote get-url origin`) | T2 (file being scaffolded must exist) |

### Phase F — Stale Asset Purge, Batch 1 (Plan Step 8)
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T18 | `.agents/docs/assets/logo/Imagen.png` | delete | — (zero references repo-wide, pre-confirmed by plan's own grep) |
| T19 | `.agents/docs/assets/logo/institutional_banner111.png` | delete | — (same) |

T18/T19 have no dependency on anything else in this WBS and may execute first if a subagent slot is free.

### Phase G — New Banner & Legacy Banner Retirement (Plan Step 9, last)
| Task | File | Action | Depends On |
| :--- | :--- | :--- | :--- |
| T20 | `.agents/docs/assets/logo/<new-banner>.svg` | new (design via `frontend-design` Artifact iteration with the human; SVG saved directly, no PNG export) | — |
| T21 | `.agents/config/framework_identity.json` (`framework_banner_path` field only) | edit | T1 (file must already exist), T20 (SVG path must be known) |
| T22 | `.agents/skills/slash-commander/README.md` (repoint `<img src>` from `institutional_banner.png` to the new SVG, line 4) | edit | T15 (must be the second, later touch on this same physical file — do not run concurrently with T15), T20 |
| T23 | `.agents/docs/assets/logo/institutional_banner.png` | delete | T22, **plus** a repo-wide grep gate for `institutional_banner.png` returning zero remaining references (plan's own Verificación §5) — this is a verification gate, not a task, and must be OBSERVED before T23 is issued (`agents.md §7 J-13 SEQUENTIAL_GATES` — do not chain grep+delete in one script) |

T21 and T22 are each the **second** atomic task touching a file already written earlier (T1, T15 respectively) — permitted under `jurisdictional_lock`, which caps concurrent/instantiated scope per task at 1 file, not lifetime touches per file. They must not run concurrently with their earlier sibling task on the same file.

---

## Dependency Summary (topological order, not a literal execution script — J-13 applies at every arrow)
```
T1 ─┬─> T3 ─> T5
T2 ─┘        ^
T4 ──────────┘
T1 ────────────> T16 (also needs T4)
T2 ────────────> T17
T6..T15  (no upstream deps; T15 must precede T22)
T1 ────────────> T21 (also needs T20)
T20 ───┬────────> T21
       └────────> T22 (also needs T15)
T22 ──[grep gate]──> T23
T18, T19  (no deps, any time)
```

## Certification Checklist (Tactical Liquidation gate)
- [x] All 23 atomic tasks assigned to subagents by `agent_orchestrator` (Phase 4). T9 dropped at Golden Gate (human decision, `skills_and_integrations.md §3` Veto conflict) — 22 executed.
- [x] `rule_validator` produced `task_scope.md` confirming no two in-flight tasks targeted the same physical file concurrently (T1/T21 and T15/T22 pairs specifically) — session-scoped artifact, gitignored by design, not committed.
- [x] `qa_agent` + `tester_agent` ran the plan's own Verificación block (5 grep gates + 2 script runs) before Golden Gate closed. Gate 1 initially bounced on two real defects (broken banner ref in `.agents/README.md`; `readme-standardizer` propagating personal identity as a functional payload, not just static docs) — both fixed and re-certified PASA. Gate 2 (functional) PASA on first pass: exhaustive `render_readme.py` scenario coverage + isolated `install_claude.py` scaffold test + full existing suite (56 pytest + installer sandbox), zero regressions. One cosmetic `ruff` D209 finding (new docstring) fixed post-Gate-2.
- [x] `CHANGELOG.md` `[Unreleased]` got a Phase 14 entry; this file's `status` flipped to `COMPLETED (100%)` at close.

## Known follow-ups (out of scope for this Sprint, not blocking)
- **CryptoBot's own README/identity.config.json**: next cycle, once this lands upstream and the host's `.agents` pin is bumped (requires separate human-authorized `lightweight_sync`).
- **`skills/skill-creator-3rd/README.md` (T9)**: still leaks the framework author's contact info. Blocked on `skills_and_integrations.md §3`'s Skill Documentation Veto — needs either a mislabel correction (drop the `-3rd` suffix, since the content is native institutional boilerplate, not real vendor docs) or an explicit human exception, as its own scoped task.
- **`install_claude.py` integration point** for `identity.config.json` scaffolding: wired for the normal (non-nucleus) install path only, as scoped. Whether `--profile` installs need the same treatment was not evaluated — out of scope, no profile currently ships identity-sensitive content.
- **`render_readme.py` against `.agents/README.md` itself**: not used for this Sprint's `.agents/README.md` patch (T16 was a manual incremental edit, by design — the template doesn't yet have full content parity with the real README's `Getting Started`/`Contributing`/`License` sections). Revisit once/if the template reaches that parity.

---
*Authorized under Universal-Agents Rules (v3.3.2; `documentation_standard.md` merged and pending release as the next tag, per `CHANGELOG.md [Unreleased]`). Phase 14 closed 2026-07-26, branch `ai-sprint/014`, pending PR against `GstMirabal/.agents`.*
