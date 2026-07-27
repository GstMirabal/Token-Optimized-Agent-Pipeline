# Third-Party Provenance TODO

Tracking file, not a blocker for publishing. These vendored skills lack a verifiable license/source and were confirmed to be genuinely third-party content (not self-authored) during the pre-publication audit — see evidence per item. Each needs its actual origin confirmed, then either (a) proper attribution added (a `LICENSE.txt`/README credit, matching `NOTICE.md`'s pattern), or (b) removed if the origin can't be verified or the license turns out to be incompatible with redistribution.

## Confirmed third-party, license/origin unverified

- [ ] `skills/django-patterns-3rd/` — frontmatter says `origin: ECC`, no URL, no license. "ECC" is not defined anywhere else in the repo.
- [ ] `skills/django-security-3rd/` — same (`origin: ECC`).
- [ ] `skills/django-tdd-3rd/` — same (`origin: ECC`).
- [ ] `skills/django-verification-3rd/` — same (`origin: ECC`).
- [ ] `skills/vite/` — has real attribution metadata: `author: Anthony Fu`, `source: Generated from https://github.com/vitejs/vite, scripts at https://github.com/antfu/skills`. Easiest one to close — the source is already named, just needs the actual license (Vite itself is MIT) confirmed and a `LICENSE.txt`/notice added.
- [ ] `skills/seo/` — `author: web-quality-skills`, `license: MIT` self-declared, but no `LICENSE.txt` bundled and "web-quality-skills" isn't a resolvable URL/org as-is.
- [ ] `skills/accessibility/` — same pattern as `seo` (`author: web-quality-skills`, `license: MIT` declared, no `LICENSE.txt`).
- [ ] `skills/vercel-composition-patterns/` — `author: vercel`, `license: MIT` declared, no `LICENSE.txt` bundled.
- [ ] `skills/vercel-react-best-practices/` — same pattern (`author: vercel`, `license: MIT` declared, no `LICENSE.txt`).
- [ ] `skills/tailwind-css-patterns/` — no license/author/source metadata at all.
- [ ] `skills/nodejs-backend-patterns/` — no license/author/source metadata at all.
- [ ] `skills/nodejs-best-practices/` — self-declares `risk: unknown`, `source: community` — the skill's own metadata already flags this as unverified.

## Why these are confirmed third-party, not self-written

All of the above (except the 4 Django ones) were added in the **same commit** `324e12c` ("chore(skills): register new design and backend skills #066", 2026-05-14) — a single batch-registration commit, consistent with a bulk import from an external skill registry/marketplace rather than original authorship. The 4 Django skills were added together in commit `99e4ec1` and already carry the correct `-3rd` naming suffix; only their actual source is undocumented.

## Not a blocker

None of this contains secrets or exposes anything sensitive — it's a license-compliance gap, not a security issue. Publishing before this is resolved is a judgment call the repo owner already made; this file exists so it doesn't get forgotten.
