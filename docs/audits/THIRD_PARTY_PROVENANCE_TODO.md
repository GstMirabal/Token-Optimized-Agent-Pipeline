# Third-Party Provenance TODO

Tracking file, not a blocker for publishing. These vendored skills lack a verifiable license/source and were confirmed to be genuinely third-party content (not self-authored) during the pre-publication audit — see evidence per item. Each needs its actual origin confirmed, then either (a) proper attribution added (a `LICENSE.txt`/README credit, matching `NOTICE.md`'s pattern), or (b) removed if the origin can't be verified or the license turns out to be incompatible with redistribution.

## Resolved

- [x] **`origin: ECC` identified** — the 4 Django skills come from [`affaan-m/ECC`](https://github.com/affaan-m/ECC) ("The agent harness performance optimization system"), **MIT licensed**. Confirmed, not inferred: ECC's own `skills/django-patterns/SKILL.md` carries a byte-identical `description` to the vendored copy and stamps `metadata: origin: ECC` on its own skills, which is exactly the field that appears here. ECC also ships `django-security`, `django-tdd` and `django-verification` under the same paths. Attribution added to `NOTICE.md`; the vendored `SKILL.md` files themselves are left untouched under the Skill Documentation Veto (`rules/skills_and_integrations.md §3`).
  - `skills/django-patterns-3rd/`, `skills/django-security-3rd/`, `skills/django-tdd-3rd/`, `skills/django-verification-3rd/`

- [x] **`skills/vite/` traced and attributed** — its `source` metadata already named the chain; both ends verified **MIT** via the GitHub API: [vitejs/vite](https://github.com/vitejs/vite) (the content) and [antfu/skills](https://github.com/antfu/skills) (the generation scripts, by Anthony Fu, matching the declared `author`).
- [x] **`skills/seo/` and `skills/accessibility/` traced and attributed** — the unresolvable-looking `author: web-quality-skills` is [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), **MIT**. Confirmed rather than assumed: that repo ships both skills under `skills/seo/` and `skills/accessibility/`, and each `description` is byte-identical to the vendored copy — the same verification method that resolved ECC.

## Confirmed third-party, license/origin unverified

- [ ] `skills/vercel-composition-patterns/` — `author: vercel`, `license: MIT` declared, no `LICENSE.txt` bundled.
- [ ] `skills/vercel-react-best-practices/` — same pattern (`author: vercel`, `license: MIT` declared, no `LICENSE.txt`).
- [ ] `skills/tailwind-css-patterns/` — no license/author/source metadata at all.
- [ ] `skills/nodejs-backend-patterns/` — no license/author/source metadata at all.
- [ ] `skills/nodejs-best-practices/` — self-declares `risk: unknown`, `source: community` — the skill's own metadata already flags this as unverified.

## Why these are confirmed third-party, not self-written

All of the above were added in the **same commit** `324e12c` ("chore(skills): register new design and backend skills #066", 2026-05-14) — a single batch-registration commit, consistent with a bulk import from an external skill registry/marketplace rather than original authorship. (The 4 Django skills, added separately, are now resolved — see above.)

## Not a blocker

None of this contains secrets or exposes anything sensitive — it's a license-compliance gap, not a security issue. Publishing before this is resolved is a judgment call the repo owner already made; this file exists so it doesn't get forgotten.
