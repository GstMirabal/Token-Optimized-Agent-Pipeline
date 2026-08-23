# Rule Context: Django Backend Standard

Governs Django-specific architecture the language-level rules cannot express: app decoupling, signal registration, and the shape of an endpoint's response. Loaded when writing or modifying Django code — models, views, serializers, `signals.py`, app layout, or DRF endpoints. Not loaded for other stacks; `rules/code_craft.md` remains the language-level rule for Python regardless.

> **Why a stack-specific rule lives in core `rules/`, recorded here so it is not
> re-litigated.** These three directives were recovered from prose inside
> `skills/django-expert-3rd/SKILL.md` in Sprint 023 unit `C4` — a unit that had
> **deleted that file** believing it to be generated scaffolding, until the QA
> gate found the loss with `git log -S`.
>
> **The objection this placement must answer is `agents.md §4
> feedback_upstream`**, an always-loaded MUST: *"**project-family-class**
> findings route to `profiles/[name]/` (rules/skills/docs)"*. Django guidance is
> project-family-class, and the real Django profile is not in this repository —
> `RA-15` keeps production profiles out of the public nucleus. `profiles/example-project/README.md`
> repeats the prohibition in weaker form, citing `agents.md §3 topological_order`,
> which governs *skills* topology and does not reach `rules/`.
>
> **The precedent that answers it is `rules/frontend_modular_standard.md`** — a
> stack-specific rule context already living in core `rules/`, governing React
> and TSX down to `View.tsx` suffixes. This file is the same class of artifact
> for the other half of the stack, and is named to match. `RA-02` is a second,
> weaker precedent: Django-specific governance in `agents.md §7`, but an
> amendment rather than a rule context.
>
> **The human resolved it in favour of core `rules/`.** One measurement and one
> judgment supported that, kept apart here because only the first can be checked.
> The **judgment**: the content is stack-wide rather than tied to one project's
> business rules, so a profile would under-serve it. The **measurement**, stated
> at the scope it was actually taken — the vendored 247-line Django skill does
> not already cover this content, because **no guidance on signal *registration*
> exists anywhere in its tree.** Paths below are relative to
> `skills/django-expert-3rd/skills/`, which is where the vendored content starts.
> `signals.py`, `receiver`, `post_save` and `pre_save` appear in zero files;
> `signal` appears three times, all incidental — two ORM caveats that
> `bulk_create()` and `update()` do not send them (`references/models-and-orm.md:249`,
> `:281`) and one auth-logging import (`references/security-checklist.md:344`).
> Every `decoupl*` match across the tree is the `python-decouple` library, all
> four in `references/production-deployment.md`.
>
> A future contributor who concludes the profile route was right should move the
> file rather than duplicate it.
>
> `skills/django-expert-3rd/SKILL.md` now points at the vendored skill it used to
> shadow, which is what closes `F-086-S3`. Recovered and promoted to a rule
> context in Sprint 023, unit `C4.2`.

## 1. App Decoupling

- **Decoupled app structures are mandatory**, to prevent cross-app contamination. An app that cannot be removed without editing another app's modules is not decoupled.
- Cross-app access goes through each app's declared public surface, never by reaching into another app's internal modules. This is the same boundary `rules/frontend_modular_standard.md §2` enforces for frontend modules, applied to Django apps.

## 2. Signal Registration

- **`RA-02: LAZY_SIGNAL_PARADIGM` governs every signal definition** (`agents.md §7`): local imports inside the receiver, and lazy sender strings.
- Stated as a reference and **not restated**, so that the amendment and this rule cannot drift apart (`RA-14`). `agents.md §7` is the single definition; this section exists so that a session loading the Django rule is told the amendment applies without having to already know it does.
- The citation this directive carried was `Clause J-02`, the numbering abolished by the `J-XX` → `RA-XX` sweep in Phase 015. That sweep declared itself repo-wide and named the one host-family file it caught (`docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md:52`); it missed this one, which then carried the abolished citation through Phases 016-022 and was found in 023. `rules/LEGACY_RULE_CONCORDANCE.md` maps the old numbers.

## 3. I/O Contracts

- **Every endpoint returns a standardized JSON payload carrying traceability metadata.** A response a caller cannot correlate back to the request that produced it is not a contract, it is output.
- The payload shape itself is a per-project decision and belongs in that project's profile or its `[MODULE]_BLUEPRINT.md`. What this rule fixes is that one exists, is uniform across endpoints, and carries correlation data — not what its fields are called.
