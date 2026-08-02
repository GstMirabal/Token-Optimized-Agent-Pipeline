---
description: "Post-Publication Field Hardening — Defects and protocols surfaced by running the framework across real hosts (Phase 18)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 18 - Post-Publication Field Hardening

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100%
- **Sprint ID:** `018` — next sequential number after Phase 17 (`017-pre-publication-hardening.md`, `COMPLETED`).

## Objective
Record the work merged into `main` after the `v4.3.0` tag (pull requests `#26`-`#30`). Unlike every prior phase, this one was not planned from a roadmap: each item was surfaced by installing the published framework into three real host repositories and hitting a defect the nucleus's own test suite could not see. The phase exists to restore traceability for that work, and to make explicit that its shared origin — field use rather than internal audit — is what the items have in common.

## Work Breakdown

| PR | Commit | Scope | Files |
| :--- | :--- | :--- | :--- |
| `#26` | `dfa68ed` | 1280x640 social card source for the GitHub link preview | `docs/assets/logo/social_card.svg` |
| `#27` | `7608113` | Secret scanner: distinguish a leak from a lookup | `hooks/on_commit.py` |
| `#28` | `ea1f322` | Freshness gate: make it capable of failing, and of seeing host code | `scripts/docs_freshness_check.py`, `tests/test_docs_freshness_check.py` |
| `#29` | `369bc22` | Hardening and reverse-documentation protocols | `workflows/` (2 new), `commands/` (2 new), `agents.md`, `README.md`, `scripts/verify_references.py` |
| `#30` | `763fe54` | Native pre-commit hook installed by the bridge | `scripts/install_claude.py`, `tests/test_installer.sh` |

### The two gates that were not gating

Both defects share a shape worth naming: a verification that reported green because it could not report anything else.

- **`audit_secret_shielding` (`#27`)** matched bare uppercased substrings (`API_KEY =`, `SECRET =`, `PASSWORD =`, `PRIVATE_KEY`), which flags every legitimate *read* of a secret — `password = request.data.get("password")`. One host hit seven false positives in a single commit and could not pass the gate at all, so the guard blocked all work while catching nothing. The fix keys on the right-hand side: a secret-named identifier assigned a string **literal**, with environment interpolation (`$VAR`, `{VAR}`, the pattern `RA-09` sanctions), obvious placeholders, values under 8 characters, and test fixtures excluded. Detection widened to `MASTER_KEY`, `SIGNING_KEY`, `ACCESS_KEY`, `PEPPER`, `CREDENTIAL` — the previous list missed all five, including the primary encryption secret of the host where this was found.
- **`docs_freshness_check.py` (`#28`)** had a single unconditional `sys.exit(0)`, and `FreshnessReport.has_block` was defined and referenced nowhere: the verdict was computed on every run and consulted on none, while `documentation_standard.md §4` describes the script as gating `SESSION LOCKED`. Three further defects came out with it — the only blocking check was skipped in silence when `last_audit_sprint` was unreadable; `root: "."` made `source_file[len(root):]` strip the first character of every path, so the submodule matched as a container of the host while the host's own code was invisible; and absolute paths produced containers with empty names. Five tests added (suite 60 → 65), one of which found the fourth defect.

### The two protocols

`repository_hardening_workflow.md` (`/agents:harden`) and `reverse_documentation_workflow.md` (`/agents:revdoc`) were distilled from work that happened on all three hosts and was reconstructed from memory each time. Both sit **outside** the 8-phase sprint pipeline. `harden`'s content is its ordering — branch protection blocks history rewriting, and a required status check that never runs makes every pull request unmergeable, so protection is configured from check names observed on a real run. `revdoc` puts the graph first as the *input* to reverse engineering rather than a check applied afterwards, and its contract-writing phase is what earns its place: reading each entry point end to end surfaced both capital-risk findings in a trading relay, neither visible at blueprint level.

The same PR indexed `unambiguous_action` into `agents.md §1`, which names what vagueness consists of rather than merely prohibiting it.

### Coverage the hook never had (`#30`)

The secret scanner ran only as a Claude Code `PreToolUse` hook, so it saw only commits the agent made through its Bash tool. A commit typed in a terminal, made from an IDE, or produced by any other tool bypassed it entirely — in a repository with a human in it, that is most of the commits. None of the three audited hosts had a native `.git/hooks/pre-commit`, and since `.git/hooks/` is not versioned, the bridge installer is the only place it can come from. An existing pre-commit hook belongs to the project and is never overwritten; the installer prints the line to add instead.

## Findings recorded

| Finding | Consequence |
| :--- | :--- |
| A pattern gap and a coverage gap are one problem, not two. | `#30` alone would have widened the net over a hole: a staged `MASTER_KEY = "<literal>"` passed the native hook exactly as it passed the agent hook, because the pattern list covered neither `MASTER_KEY` nor `ENCRYPTION_PEPPER`. Shipping the mechanism without `#27` would have produced a *more* confident false green. |
| A host roadmap had recorded the wrong diagnosis. | It held that the pattern was right and the hook had never run. The hook ran; the pattern missed. Verifying end to end — staging a real secret and committing from a terminal — is what separated the two. |
| The nucleus test suite cannot see host-shaped defects. | All three of `#27`, `#28`, `#30` were green in the nucleus and broken in the field. `#28`'s path bug specifically required a *host* directory layout to manifest. |
| `RA-15` caught a contribution from this framework's own author. | `#28` initially used `/Users/someone/` in a test fixture; the repository's own absolute-path gate rejected it because `someone` is not among the allowed generic names. |

## Certification Checklist
- [x] `pytest tests/` green (65 tests collected).
- [x] All 5 pull requests merged to `main` through review; working tree clean at `763fe54`.
- [x] `/agents:harden` and `/agents:revdoc` verified to resolve to existing workflow files.
- [x] Native pre-commit hook verified end to end (secret staged, commit refused from a terminal, no object created).
- [x] Command counts re-verified against the tree during this closeout: 12 workflows, 13 commands, 13 agents, 8 rule contexts, 34 skills.

## Documentation debt closed during this closeout
This phase was merged without a ledger entry or a roadmap record; both were reconstructed on 2026-08-02 from commit bodies and diffs. Three `RA-14 PATCH_PROPAGATION` violations left by `#29` were repaired at the same time:
- `README.md` "At a Glance" still read `10 protocols … 11 slash commands` while the same PR updated the prose below it to `all 13 commands`.
- `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md §3.2` listed 11 commands and never documented `/agents:harden` or `/agents:revdoc`, although `README.md` points readers to it for "all 13 commands".
- The guide's §3.1 retrofit sequence still ended at `/agents:pipeline`, while `README.md`'s parallel sequence had gained the `harden` → `revdoc` → `pipeline` ordering.

## Known follow-ups (tracked, not blocking)
- Commits in this phase carry **host** sprint suffixes (`#001`, `#022`) rather than a nucleus sprint ID, because the work was discovered while operating inside host projects. `agents.md §5 historical_log` does not currently state which ID governs a `feedback_upstream` contribution. Candidate for a rule amendment.
- `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` — 5 open items remain (`vercel-*`, `tailwind-css-patterns`, `nodejs-*`), unchanged by this phase.
- The installed `graphify` skill reports version `0.8.28` against package `0.8.30`; `graphify install` would realign it.

---
*Reconstructed 2026-08-02 from `v4.3.0..763fe54`. Work executed 2026-07-30 → 2026-08-02 across pull requests `#26`-`#30`; not released — the ledger entry sits under `[Unreleased]`.*
