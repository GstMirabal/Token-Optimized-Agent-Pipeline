# Upstream findings reported by a host

Framework-class findings under `agents.md §4 feedback_upstream`: each affects
every host that installs this nucleus, so `strict_rule` correctly forbids a host
from patching it and routes it here instead. Most were found while running the
pipeline inside a host project; the *Added by Sprint 023* section holds three
that were not, and each of those states its own provenance.

Genericized per `RA-15`: no host project name, no absolute paths, no host
business logic. Where a measurement is quoted it is a count, not an identity.

**Four sections, and the differences are load-bearing.**

| Section | What it holds | Reproduction status |
| :--- | :--- | :--- |
| *Reported by a host* | The original seven | Reproduced against `v4.4.0` when this file was written, and **re-measured again** when each was closed |
| *Added by Sprint 023* | Three items the nucleus found in itself | Measured against the tree at the time each was written. **Not** `v4.4.0` |
| *Added by Sprint 026* | Three items the nucleus found in itself: one at the Agent Assignment phase, one at the Phase 4 tier audit, one during Hito 1 execution, none while repairing another entry | Measured against the tree at `b5bfb6a`, the commit `docs/sprints/026-core-pipeline/task_scope.md` names as Sprint 026's base |
| *Inherited from host sprint records* | Leads from a host's sprint history | **Not** re-measured when written. Treat each as a lead, reproduce it first, and delete it if it no longer holds |

A finding carried forward on the strength of an old record is exactly the defect
several of these findings are about — which is why *Inherited from host sprint
records* carries its status in the table above rather than leaving it to be
inferred from where the section sits.

**Status at Sprint 023 (2026-08-24).**

| | |
| :--- | :--- |
| **Closed** | All **seven** items of *Reported by a host*, plus two leads from *Inherited from host sprint records* — `G-03` and `#12`. Ten ticked entries in total, the tenth being `F-023-D5`, which was opened and closed by the same sprint |
| **Opened, still open** | **`F-023-S4`** — it defeats `agents.md RA-09 SECRET_SOVEREIGNTY` and survived the repair of `F-086-S1`/`F-086-S2`. **`F-021-A2`** was *declared* by Sprint 023, not opened by it; its entry says where |
| **Ticked on what basis** | Re-measurement against the current tree, **never** on the sprint record that claimed the fix. Rule 1 of this file governs closing an item exactly as it governs opening one |

**The corrections reproduction produced are recorded where a reader needs them**,
not collected in a list. `F-086-S3` carries three: it was **narrower** than
reported in one respect, **wider** in another, and its Evidence block was
outright **disproved** — a repair built on that block deleted hand-authored
governance content. `F-093-N2` carries one: it was **wider**, and the obvious fix
would have shipped a worse defect than the one reported. The third measurement
correction became its own entry, `F-023-D5`, because what it corrected was not a
finding in this file but a security count being carried against the nucleus.

**A note on rule 3, which asks for the pull request that closed each item.**
Sprint 023 has not merged, so every item it closed has **a commit and no pull
request**. The commit is recorded and the pull request is named `pending 023`.
Writing a PR number that does not exist yet would make this file assert something
unverifiable — the failure shape most of these findings describe. `#12` is the one
item that closed earlier, in Sprint 022, and it carries its real PR.

---

## Reported by a host — verified against `v4.4.0`

### - [x] `F-086-A1` — the profile that owns deployment artifacts cannot write one

**Evidence.** `agents/devops_agent.md:4`

```
tools: Read, Glob, Grep, Bash
```

Line 3 of the same file gives this role the environment and deployment
responsibility. It has no `Write` and no `Edit`, so the one profile that owns
`Dockerfile`, entrypoint and compose files cannot author or amend any of them.

**How it surfaces.** Every host that containerises hits this on its first
attempt. The reporting host worked around it by having `principal_agent` issue
the writes while `devops_agent`'s ruleset governed them — a declared deviation
that had to be carried into `task_scope.md` so the structural gate audited it
rather than discovering it. Four sprints later the same workaround was still
being restated.

**Proposed fix.** Add `Write, Edit` to the `tools:` line — one line, and it
preserves the existing role map. The alternative, splitting a
`container_build_agent` profile that owns the deployment artifacts, is cleaner if
the role map is being revisited anyway, and larger.

**Closed** — Sprint 023 unit `C5`, commit `aa2b11d` (PR pending 023). The first option
was taken: `agents/devops_agent.md:4` now reads
`tools: Read, Glob, Grep, Bash, Write, Edit`, and `agents.md §6` was amended in
the same unit to say what that grant covers — the framework-root `scripts/` and
`hooks/` trees, **not** `skills/[name]/scripts/`, which `skill_architect` forges.
Re-measured: the line resolves today.

**The second option was not taken, and the void it would have closed is now
declared rather than resolved** — see `F-021-A2` below. This entry was the
visible case of a structural gap that is wider than one profile.

---

### - [x] `F-087-P1` — the platform probe reports an enabled control as disabled

**Evidence.** `scripts/session_probe.py:147`

```python
security = gh_json("api", f"repos/{slug}", "--jq", ".security_and_analysis") or {}
for control in ("secret_scanning", "secret_scanning_push_protection",
                "dependabot_security_updates"):
    if security.get(control, {}).get("status") != "enabled":
        findings.append(f"{control} disabled")
```

`GET /repos/{owner}/{repo}` **omits `security_and_analysis` entirely** for
repositories where the caller cannot read it — private repositories on plans
without Advanced Security among them. The `or {}` then makes `security` empty,
`.get(control, {})` returns `{}`, `.get("status")` returns `None`, and the probe
appends `"<control> disabled"`.

**This is the worst failure shape a probe has**: absent evidence rendered as a
negative finding. The reporting host confirmed from three independent sources
that `dependabot_security_updates` was *enabled* while the probe called it
disabled.

**Cost.** A host chases a control that is already on, finds nothing, and learns to
distrust the whole probe. The next real finding it reports is discounted.

**How to reproduce.** Point the probe at a private repository on a plan without
GitHub Advanced Security. Compare its output against
`gh api repos/{owner}/{repo}/automated-security-fixes`.

**Proposed fix.** Distinguish *absent* from *disabled*. When the key is missing
from the response, say so — `"<control>: cannot determine (field not returned)"`
— rather than asserting a state. And read `dependabot_security_updates` from its
own endpoint, `GET /repos/{owner}/{repo}/automated-security-fixes`, which answers
for repositories where the aggregate field does not appear.

Worth noting while in this function: `vulnerability-alerts` two lines below is
checked by return code, which is the correct shape. `F-087-P1` is the block above
it drifting from that pattern.

**Closed** — Sprint 023 unit `C2`, commits `26367cf` + `ca29010` + `509f525`
(PR pending 023). Both halves of the proposed fix landed. Re-measured:
`scripts/session_probe.py` now collects into a separate `undetermined` list and
emits `"<control> — cannot determine (<cause>)"`, and reads
`repos/{slug}/automated-security-fixes` as its own call rather than inferring the
control from the aggregate field. The **cause** is carried through rather than
only the fact of not knowing, which the original proposal did not ask for and a
host chasing the finding needs.

**Wider than reported.** The same *absent-rendered-as-negative* shape was found
in branch protection while fixing this, and is covered by the same mechanism:
`"branch protection — cannot determine (no default branch reported)"`. The entry
named one control; the defect was a pattern in the function.

---

### - [x] `F-086-S1` — the secret auditor's patterns are correct and its file list is not

**Evidence.** `skills/env-shielding-auditor/scripts/env_shielding_auditor.py:25`

```python
if file.endswith((".py", ".js", ".ts", ".json", ".env", ".env.example", ".sh", ".bash")):
```

The `SECRET_PATTERNS` above this line were verified against the credential forms
that appear in infrastructure files and **do match them**. They are simply never
reached, because no `Dockerfile`, no `.yml`/`.yaml`, no `.toml`, no `Makefile`
and no `.dockerignore` passes this filter — the file types most likely to carry a
literal credential in a containerised host.

**How to reproduce.** Write a recognised secret pattern into a `Dockerfile` and a
`docker-compose.yml` in a scanned tree, then run the auditor. Zero findings.

**Proposed fix.** Two changes in the same condition. Extend the suffix tuple with
`.yml`, `.yaml`, `.toml`, `.cfg`, `.ini`, `.conf`, `.tf`, `.example`; and match
**by name as well as by suffix**, since `Dockerfile`, `Makefile` and
`docker-compose.yml` are identified by name. A filter that only knows about
suffixes cannot see a file whose whole name is the type.

**Closed** — Sprint 023 unit `C3`, commits `aa83309`…`5bcbdf6` (PR pending 023).
Fixed in **one** unit with `F-086-S2`, as rule 2 of this file requires.
Re-measured: `env_shielding_auditor.py` now carries `SCANNED_SUFFIXES` with all
eight proposed suffixes and a separate `SCANNED_NAMES` tuple for the
whole-name types.

**A third form the entry did not anticipate.** `Dockerfile.prod` and
`api.Dockerfile` pass neither test — splitting the build file leaves an affix
that is not a format suffix — so a `BUILD_FILE_NAME` match was added. It was
found by the gates in two successive rounds, and the reason it mattered is that
the auditor and `hooks/on_commit.py` **disagreed about what a build file is
called** until then. Two halves of one gap can be fixed in one unit and still
not meet.

---

### - [x] `F-086-S2` — the commit hook's file list is correct and its pattern is not

**Evidence.** `hooks/on_commit.py:90`

```python
SECRET_ASSIGNMENT = re.compile(
    rf"""^[ \t]*
        (?P<name>[A-Za-z0-9_]*(?:{SECRET_WORDS})[A-Za-z0-9_]*)
        [ \t]*(?::[^=\n]+)?[ \t]*=[ \t]*
        (?P<q>['"])(?P<value>(?:(?!(?P=q)).)*)(?P=q)
    """, re.IGNORECASE | re.MULTILINE | re.VERBOSE)
```

The word list and the affix handling are good — a secret word may be the whole
identifier, a prefix or a suffix, and the comment above says so. The **shape** is
the problem: the pattern requires an `=` and a **quoted** value, so it recognises
`NAME = "value"` and nothing else.

Silent past it:

| Form | Where it appears |
| :--- | :--- |
| `ENV API_KEY abc123` / `ARG API_KEY=abc123` | Dockerfile |
| `api_key: abc123` | any YAML — compose, CI workflows, config |
| `https://host/path?api_key=abc123` | a URL in any file type |

Note the pairing with `F-086-S1`: this hook scans **all** file types behind the
wrong pattern, and the auditor above has the right patterns behind the wrong file
list. Between them, an infrastructure credential is caught by neither. Fixing one
without the other leaves the gap open.

**How to reproduce.** Stage a `Dockerfile` containing `ENV API_KEY "abc123"` and
commit. The hook passes.

**Proposed fix.** Three alternations in the same expression — a leading
`ENV|ARG` keyword with an optional `=`, a `key: value` form for YAML, and
`[?&]\w*(key|token|secret|password)=` for URL query strings. Same file, no new
mechanism. Unquoted values need a terminator (end of line, whitespace, or `&`),
which is the only part that needs care.

**Closed** — Sprint 023 unit `C3`, same unit and commits as `F-086-S1`
(PR pending 023). Re-measured: `hooks/on_commit.py` now carries
`DOCKERFILE_SECRET`, `YAML_SECRET` and `QUERY_STRING_SECRET` as named patterns
beside the original `SECRET_ASSIGNMENT`, plus a `PRIVATE_KEY_BLOCK` form the
entry did not propose. They are separate compiled expressions rather than
alternations inside one, which keeps each form's terminator rule readable — the
part the entry correctly flagged as the only delicate one.

**Two things this unit produced that the entry could not have known.** First,
the gates found the fix **blocking a harmless file while still passing a harmful
one** (`c691045`), so the existing false-positive exclusions had to be carried
onto all three new forms rather than left on the old one. Second, the unit was
halted at the remediation trigger and reopened as `C3.2` (`50094c1`), which
added a documented `ALLOW_MARKER` bypass; its rule —
`rules/qa_and_testing.md §5 Waiving a secret-scan finding` — landed separately in
`4a3c64a`, after a gate found the marker was claiming a waiver it never applied.
The reasoning: a secret gate with no compliant way to commit a deliberate
example gets tuned down instead of obeyed, and a gate that has been tuned is not
a gate.

**Still open, and not covered by this entry — see `F-023-S4` below.** A literal
`.env` holding live credentials still passes this hook **after** the fix above.
The reason is not that the new forms require quotes — three of them do not. It is
that they are **selected by file type**, and **no form selected for a `.env`
covers an unquoted `NAME=value` at all**: the two that accept unquoted values,
`YAML_SECRET` and `DOCKERFILE_SECRET`, accept them only in their own shapes
(`key: value`, `ENV`/`ARG`), and are never selected for a `.env` regardless.
Selecting them for it would close nothing. `F-023-S4` carries the measurement;
this note exists so a reader of *this* entry does not conclude the gap closed
here.

---

### - [x] `F-086-S3` — `mass-standardizer` orphaned a vendored skill, and has been unusable since

**Evidence.**

```
skills/django-expert-3rd/SKILL.md          20 lines   <- generated stub
skills/django-expert-3rd/skills/SKILL.md  247 lines   <- the vendor's real skill
```

The root `SKILL.md` is a scaffold stub. It says *"(Automatic scaffolding)"* in its
own body, mentions neither the nested vendor file nor `references/`, and is the
one skill loading discovers. The vendor's content is present on disk and
unreachable.

**Consequence, measured across host sprints.** `mass-standardizer` is the
sanctioned auditor of the Three-File Standard (`agents.md §3 enforcement`). The
reporting host has recorded it as **rejected and not run** in every skill
assignment since the sprint that found this — it cannot be trusted against any
skill with nested vendor content until the behaviour changes. The standard's own
enforcement tool has been out of service for six sprints.

**Scope note.** `rules/skills_and_integrations.md §3` forbids editing vendored
skill documentation. The stub is **framework-generated, not vendored**, so
repairing it is in scope; the nested vendor `SKILL.md` must not be touched.

**How to reproduce.** Run `mass-standardizer` against any `-3rd` skill that ships
its own `skills/SKILL.md` and `references/`.

**Proposed fix.** Detect a nested `SKILL.md` before writing a root one, and
either defer to it entirely or emit a root stub whose body links the nested file
and the `references/` directory. Then re-check every `-3rd` skill: this likely
affects each one that ships nested content, not only the one that was noticed.

**Closed** — Sprint 023 unit **`C4.2`**, commit `955eb5d` (PR pending 023),
preceded by unit `C4`, commit `5056796`, which repaired the auditor. It took two
units and a **human decision** because `C4` established the finding could not be
closed by any unit acting alone — see Correction 3 below. The vendored
`skills/django-expert-3rd/skills/SKILL.md` was **not** touched, as the scope note
requires; the root is now a relative symlink to it.

> **Correction 1 — the entry was narrower than it stated.**
>
> The proposed re-check of *"every `-3rd` skill"* was unnecessary. Re-measured at
> this closing: there are **7** `-3rd` skills and **exactly one** ships a nested
> `SKILL.md`. The entry generalised from a single instance to a suspected class,
> and the class has one member.
>
> **Correction 2 — and wider, in the part that mattered.** The diagnosis
> *"generates a bad stub"* was wrong. `mass_standardizer.py:81` climbed **five**
> `.parent` levels where four are correct, so `manifest_skills.json` resolved
> **outside the repository** in nucleus and host alike. The auditor did not
> produce a bad stub — **it could not run at all**. The reporting host recorded
> it as "rejected and not run" for six sprints and attributed that to the stub;
> the cause was a path. Fixed in `C4` (`5056796`), where `base_dir` now derives
> from `agents_root()` rather than counting parents.

> **Correction 3 — the Evidence block above is disproved, and this is the one
> that cost the sprint a destructive regression.**
>
> `skills/django-expert-3rd/SKILL.md` was **not** a scaffold stub. It contained
> the template's `(Automatic scaffolding)` sentence, which is what made it look
> like one — and it also carried **three hand-authored governance directives**,
> one of them the mandate `agents.md RA-02 LAZY_SIGNAL_PARADIGM` states.
>
> `C4` acted on this entry's diagnosis and **deleted that file**. The structural
> gate found the loss with `git log -S`; nothing in the diff, the unit's
> docstring or its tests recorded it, and the test written to forbid exactly that
> deletion passed only because its fixture avoided the case. The file was
> restored byte-identical, and the substring licence was replaced by
> **byte-equality against the freshly rendered template** — the only test that
> proves nobody has edited a generated file.
>
> That left the finding genuinely unclosable inside `C4`: deleting the authored
> file is `agents.md §2 destructive_flags`, and copying vendor content into the
> framework's tree is `rules/skills_and_integrations.md §3`. **Both gates
> ratified that reading independently.** `C4` escalated to a human, who decided
> the three directives should be relocated to a new `rules/django_backend_standard.md`
> and the root repointed — which is `C4.2`, and which is why the closure above
> names two units.
>
> **The lesson for this file, not for that skill.** *"It says it is generated"* is
> not evidence that it is generated. This entry's Evidence block asserted a file's
> provenance from its own body text, a repair was built on that assertion, and the
> repair destroyed authored governance content. `A finding whose repair touches a
> generator that writes documentation is not low-risk`, whatever severity the
> finding itself carries — this one was filed as a skill-scaffolding nuisance.

---

### - [x] `F-093-N1` — the nucleus cannot satisfy its own entry-point rule

**Evidence.** `agents.md:10`

```
| **Entry Point** | Every session MUST start by reading `docs/0_SYSTEM_OVERVIEW.md`. |
```

`workflows/start_workflow.md` Phase 0 `read_ruleset` implements it: *"read
`agents.md` and `docs/0_SYSTEM_OVERVIEW.md` to adopt current governance."*

This repository has no `docs/0_SYSTEM_OVERVIEW.md`. The only match in the tree is
`docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md`, which is the template
hosts are given.

**Consequence.** In nucleus mode the mandatory entry point resolves to nothing.
Combined with the absence of `docs/active_state.json` here — correct and
deliberate, since `agents.md §5` states the nucleus traces its own work through
branches, pull requests and `CHANGELOG.md` — **`agents.md` is the only file a
nucleus session is guaranteed to read.** That is why this findings file is
announced from `agents.md §0` rather than left to be discovered.

**How to reproduce.** `find . -iname "*SYSTEM_OVERVIEW*"` at the repository root.

**Proposed fix.** Either write the nucleus's own `docs/0_SYSTEM_OVERVIEW.md`, or
declare the exception in `§0` the way `§5` already declares that the nucleus has
no `docs/sprints/` hierarchy. The second is one sentence and consistent with how
the other nucleus-mode exception is handled; the first gives nucleus sessions the
same entry point every host gets.

**Closed** — Sprint 023 unit `C6`, commit `fcd80ed` (PR pending 023). The second
option was taken, with one addition the entry did not ask for: declaring the
exception is not enough on its own, because a session that learns the mandatory
entry point does not exist still has nothing to read. `agents.md §0` and
`start_workflow.md` `read_ruleset` therefore **name the substitute** —
`agents.md` plus the generated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`. The
evidence for adding it: **sessions #2 through #5 of Sprint 023 each hit the gap
and each re-derived the same substitute independently.** An exception that says
only "this does not apply here" costs every session the same rediscovery.

> **A caveat on that count, for whoever verifies this entry.** `fcd80ed` wrote
> *"five consecutive sessions"* into `agents.md` and *"sessions #2 through #5"* —
> four — into `workflows/start_workflow.md`, in the same commit. The two
> statements have not been reconciled in the nucleus. The enumerated form is used
> above because it names which sessions and can be checked; the aggregate cannot.

**A second defect surfaced from the same premise.** This entry observes that
`agents.md` is the only file a nucleus session is guaranteed to read. Working
that observation found the nucleus `.claude/` bridge had been installed once and
never refreshed: `commands/` held 13 files and `.claude/commands/agents/` held 11
stale symlinks, so `/agents:reconcile`, `/agents:harden` and `/agents:revdoc`
**were not invocable in the nucleus** — including the one `start_workflow.md`
`drift_check` mandates on exit 2 — beside a dangling link to a deleted
`skeleton.md`. It had been that way for a month. The cause was a belief, held
across four documents, that `nucleus_neutrality` prohibited the bridge step;
it prohibits *structural scaffolding*, and a bridge install is not that. Fixed
in the same unit, and re-measured at session #7: **13 of 13, no dangling entry.**

### - [x] `F-093-N2` — a mandatory close step crashes in every host

**Evidence.** `scripts/check_readme_counts.py:47`

```python
lambda: len([p for p in Path("skills").iterdir() if p.is_dir()]),
```

`Path("skills")` is relative to the working directory. In the nucleus that
resolves; in a host the skills live at `.agents/skills/` and the path does not
exist, so the script raises `FileNotFoundError` and exits **1**.

`close_workflow.md` Phase 2 `readme_counts` names this script as a step of every
session close and says it "**Exits `2` on drift**". In a host it exits 1 without
having counted anything — a different code for a different reason, which is why
nobody reading the workflow would recognise the failure as environmental.

**How to reproduce.** Run it from the root of any host that pins this submodule.

**Consequence.** The step has never passed in a host close. Either it was skipped,
or its failure was read as drift it never measured. Both are the shape this
document keeps describing: a control whose verdict depends on where it was run.

**Proposed fix.** Resolve the counted paths against the script's own location
rather than the working directory — the same nucleus/host asymmetry
`close_workflow.md` already handles explicitly for `docs/sprints/`, `memory/` and
the Entry Point anchors. If the counts are meaningful only in the nucleus, the
workflow should say so and the script should exit 0 with that statement in a host,
rather than crashing.

**Found by** running the close protocol, not by reading it.

**Closed** — Sprint 023 unit `C1`, commit `b2d7c2e`, on top of `C0.3` (`359d03c`)
which created `scripts/_root.py` (PR pending 023). The first option was taken:
paths resolve against the script's own location, via a single `agents_root()`
definition rather than a rewrite at each call site.

> **Correction — the entry understated its own scope, and the obvious repair
> would have made things worse.**
>
> **Wider.** It names one counter. In fact **all five** counters use relative
> paths, **and so does `README = Path("README.md")`** — the file the counts are
> compared against. The reason only `skills` was visible is that `glob()` over
> an absent directory returns empty rather than raising, so the one `iterdir()`
> call crashed first and **the exception masked the other four**.
>
> **And the natural fix is a trap.** Wrapping `iterdir()` in `try/except` —
> which is what "stop the crash" suggests — converts the failure into
> `no declared count found` ×5 and exit `2`. That is **false drift in every
> host**, and it is worse than the crash, because a crash is recognisably
> environmental while a `2` reads as a measured verdict. This is the same shape
> as `F-087-P1`, one layer down: absent evidence rendered as a finding.
>
> Recorded because the entry's own framing — *"a mandatory close step crashes"* —
> invites exactly the repair that would have shipped the worse defect.

---
## Added by Sprint 023 — measured against the tree, not against `v4.4.0`

Three items that did **not** come from a host: the nucleus found them in itself
while repairing the section above. They are recorded in this file rather than in
a sprint log because they are framework-class under
`agents.md §4 feedback_upstream` — every host inherits them, and a sprint log is
not where a host looks.

**Their provenance differs, and the difference is not cosmetic.** `F-023-D5` was
opened and closed by this sprint. `F-023-S4` was opened by it and is open.
`F-021-A2` was **declared** in the sprint's own premise — written before any unit
ran — and Sprint 023 unit `C5` restated it rather than discovering it; it is listed here
because this is where an open framework-class item belongs, not because this
sprint found it.

### - [x] `F-023-D5` — the 26 dependency alerts are documentation being scanned as a lockfile

**Provenance: the third of the three measurement corrections**, and the only one
that did not correct an entry in this file. It corrects a count that was being
carried as nucleus security debt.

**What was believed.** 26 Dependabot alerts, 19 of them high, standing against
this repository and treated as exposure the nucleus carried.

**What reproduction found.** All 26 come **entirely** from
`requirements-freeze.txt`, and **no install path reads that file**:
`start_workflow.md` installs `requirements-core.txt` (1 package), and the
skillopt stack installs `requirements-skillopt.txt` (3 packages, on demand).
`skills/skillopt/SKILL.md` referred to the freeze only as something *"visible in
`requirements-freeze.txt`"* — it named the file without ever declaring it an
install input, which is the ambiguity this finding turns on. The file was a
transitive-closure snapshot — documentation — sitting in a filename the scanner
reads as a lockfile.

**Why it could not be fixed by configuration.** Dependabot **alerts cannot be
excluded by path**; `.github/dependabot.yml` governs *updates*, not *alerts*.
So the fix is the name: the file became
`docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md`, a git rename with the content in a
code block, and `skills/skillopt/SKILL.md` updated to point at it.

**This does not claim there is no exposure** — it changes whose debt it is. A
host that installs the skillopt stack resolves its own dependencies and owns the
result.

**Closed** — Sprint 023 unit `C7`, commit `7966964` (PR pending 023), a git rename
that cleared both gates on the first round.

---

### - [ ] `F-021-A2` — the role map has eight profiles that can write and no implementer

**Evidence.** `agents/devops_agent.md:35`, where it is **declared and explicitly
not resolved**.

Of the 13 profiles in `agents/`, **8** hold `Write`/`Edit` on their `tools:`
line. Not one of them is an implementer: they are documentation, governance,
skill, topology and environment roles. `F-086-A1` above closed by granting the
environment role `Write` over the framework-root `scripts/` and `hooks/` trees —
that gives those two trees *an* owner. It does not create the role, and it does
not make a `mechanical`/`haiku` tier the right author for a governance gate.

**Consequence, measured over one sprint.** Every unit of Sprint 023 was authored
by the lead session, because there is no profile to dispatch authoring to. The
work that dispatched gates then caught is work the author could not reach: in
`C4` they found the unit had **deleted hand-authored governance content**, and
that the test written to forbid exactly that deletion passed only because its
fixture avoided the case. Neither was found by re-reading — the deletion was
found with `git log -S` against a file the author had already read, and a false
count in the unit's own docstring was found by re-measuring.

**Why Sprint 023 did not fix it.** Splitting an implementer profile is a role-map
redesign, not a line change, and it should not ride on a finding about a
different role's tool list.

**How to reproduce.** Read the `tools:` frontmatter line of each profile, and
match `Write`/`Edit` **as whole list items**:

```bash
for f in agents/*.md; do
  grep -m1 '^tools:' "$f" | grep -qE '(^|[ ,])(Write|Edit)([ ,]|$)' && basename "$f"
done
```

Returns 8. Two narrower forms both fail, in the same way and by one:

| Form | Returns | Why it is wrong |
| :--- | :--- | :--- |
| `grep -l 'Write' agents/*.md` | **10** | Matches `TodoWrite` in `agents/principal_agent.md`, and matches the word in body prose (`agents/tester_agent.md`) |
| `grep -m1 '^tools:' \| grep -qE 'Write\|Edit'` | **9** | Scoped to the frontmatter, which removes the prose match — but `Write` is still a substring of `TodoWrite`, so `principal_agent` survives |

`agents/principal_agent.md` reads `tools: Read, Glob, Grep, TodoWrite`, and that
role explicitly does not write. **This entry published the second form and
asserted 8**, which is the failure this file exists to record: a recipe carrying
the exact defect its own prose warns against. The word-boundary form above is
what the count of 8 rests on, and it was reached by checking profile by profile
rather than by trusting either command.

### - [ ] `F-023-S4` — a literal `.env` still passes the commit hook, after the secret gate was repaired

**It defeats `agents.md RA-09 SECRET_SOVEREIGNTY`**, and it **survived** the fix
recorded under `F-086-S1`/`F-086-S2` above.

**Evidence — re-measured on the repaired tree at Sprint 023 session #7:**

```python
>>> find_hardcoded_secret('API_KEY=<28-char value>\n', Path('.env'))
None                                    # unquoted — the form a .env file uses
>>> find_hardcoded_secret('API_KEY="<28-char value>"\n', Path('.env'))
'API_KEY'                               # quoted — caught
>>> Path('.env').suffix
''                                      # not '.env'
```

**Two independent mechanisms, and a file need only beat one of them:**

| # | Mechanism | Why it misses |
| :--- | :--- | :--- |
| 1 | The forbidden-extension branch | `Path(".env").suffix` is `''`, not `".env"`, so the branch never fires on the one filename it exists to catch. `.env.production` is worse: its suffix is `".production"` |
| 2 | **Form selection**, not quoting | `secret_forms_for(Path('.env'))` returns `SECRET_ASSIGNMENT`, `QUERY_STRING_SECRET` and `PRIVATE_KEY_BLOCK`. Of those, only `SECRET_ASSIGNMENT` addresses the `NAME=value` shape at all — and it is the **one** form of the five that requires a quoted value. The two forms that *do* accept unquoted values, `YAML_SECRET` and `DOCKERFILE_SECRET`, accept them **each in its own shape** (`key: value` and `ENV`/`ARG`) and not in `NAME=value` — and both are gated on file type and never selected for a `.env`. **Selecting those two forms for `.env` would therefore close nothing**; see the Proposed fix |

> **Read mechanism 2 carefully before repairing it.** The obvious diagnosis —
> *"the gate's patterns require quotes"* — is **false**, and this entry stated it
> that way until the Tester gate measured it. Three of the four named forms match
> unquoted values today:
>
> ```
> SECRET_ASSIGNMENT      unquoted -> no match
> DOCKERFILE_SECRET      unquoted -> MATCH
> YAML_SECRET            unquoted -> MATCH
> QUERY_STRING_SECRET    unquoted -> MATCH
> ```
>
> Repairing on the false diagnosis means adding quote-optionality to four
> patterns where three already have it, and still shipping the bug — because the
> bug is in **which forms are selected for the file**, not in what the forms
> accept.

**Wider than `.env`.** The `NAME=value` unquoted shape is missed in **every**
file type, because no selected form covers it:

```
.env         API_KEY=<28-char value>  -> None
settings.py  API_KEY=<28-char value>  -> None
app.yml      API_KEY=<28-char value>  -> None    # YAML_SECRET needs `key: value`
Dockerfile   API_KEY=<28-char value>  -> None    # DOCKERFILE_SECRET needs ENV|ARG
```

**How to reproduce.** Stage a `.env` containing `API_KEY=<a credible value>` and
`DB_PASSWORD=<a credible value>` and commit. `audit_secret_shielding()` returns
`True` and the commit is allowed. `prod.env` blocking while `.env`,
`.env.production` and `.env.local` pass is the sharpest demonstration of
mechanism 1.

**Two traps when reproducing, in opposite directions.** Use a value that is not a
documented placeholder — the gate correctly rejects AWS's own `…EXAMPLEKEY`
quoted *and* unquoted, and testing with it yields a false negative that looks
like this finding. And do not test with a PEM block or a URL query secret: both
**are** caught in a `.env` (`PRIVATE_KEY_BLOCK` and `QUERY_STRING_SECRET` are
selected for it), so testing with either yields the inverse trap — a blocked
commit, read as the finding failing to reproduce.

**Proposed fix.** Two changes, and the second is the one the false diagnosis
hides. Match `.env` and its variants **by name**, the way `C3` already taught the
auditor to match `Dockerfile` — a suffix test structurally cannot see a filename
that begins with its own dot. And add a `NAME=value` form with an
end-of-line terminator to the set selected for **every** file type, since that
shape is currently covered nowhere.

**Provenance.** Found by a dispatched `tester_agent` while gating `C3`, end to
end rather than by reading the pattern, and correctly refused as a rider on that
unit: `C3`'s declared scope was the file list and three named alternations, and
this is neither. It then survived **three** sessions as *routed, unowned* —
which is the same shape as the loss this whole file was written to repair.

---

## Added by Sprint 026 — measured against the tree, not against a host report

Three items, found by the framework's own Agent Assignment phase, Phase 4
tier-audit pass, and Hito 1 census execution respectively — none of the three
while a host was running the pipeline and none while repairing another entry.
Recorded here, not folded into the Sprint 023 section above, because their
provenance is a different sprint and this file's own convention (see
`F-021-A2`'s provenance note) treats provenance as load-bearing rather than
cosmetic. Framework-class under `agents.md §4 feedback_upstream`: every host
that dispatches `qa_agent` or `tester_agent` inherits `F-026-A1`; every host
that dispatches a `mechanical`-tier role at a difficulty its default does not
fit inherits `F-026-A2`; every host whose checkout runs `hooks/on_init.py`
inherits `F-026-A3`.

### - [ ] `F-026-A1` — two gate profiles are assigned writes their own `tools:` grant refuses, and one already claims the capability in its own description

**Evidence.** `agents/tester_agent.md:3-4`:

```
description: Test Verifier. Use this agent as the second Double-Gate review pass (after QA Agent) to write and execute unit/integration tests against an in-memory DB, and to bounce code back for remediation on functional failures.
tools: Read, Glob, Grep, Bash
```

Its own `description` line asserts a write — "write ... unit/integration
tests" — as half the role. Its `tools:` line holds neither `Write` nor
`Edit`, so the profile cannot create the artefact its own frontmatter says it
produces.

`agents/qa_agent.md:4` carries the identical grant — `tools: Read, Glob, Grep,
Bash` — and its own `description` does not itself claim a write. The same
contradiction reaches it one layer down, at the point a plan assigns it work:
`docs/sprints/026-core-pipeline/agent_assignment.md:190-204` ("Disagreements
found," item 2) records that Sprint 026's own design (`Design §D9`) assigned
`G1.q`, `G1.t` and `A3` — verdict writes into
`docs/sprints/026-core-pipeline/SPRINT_LOG.md` — to `qa_agent` and
`tester_agent`, neither of which can perform the write under its `tools:`
line. The same note names the authority the assignment contradicts:
`config/artifact_registry.json:33-39` declares `SPRINT_LOG.md`'s `role` as
**Orchestrator** (`agents/orchestrator.md`, which does hold `Write`/`Edit`),
not either gate. `Design §D9` names the registry as its own cited basis for
the sprint directory and then diverges from what the registry says.

**Distinct from `F-021-A2`, cross-referenced and not folded in.** `F-021-A2`
(above, open) states that 8 of 13 profiles hold `Write`/`Edit` and none is an
implementer — a gap in the role map. This is the inverse defect: a profile
that describes, or is assigned, a capability its own frontmatter refuses.
`F-021-A2` closes by adding a role; this closes by making description or
assignment agree with the grant, in whichever direction is correct. The two
fixes do not overlap and neither entry substitutes for the other.

**Do not resolve this by granting `Write` to the gates.** `qa_agent` and
`tester_agent` both declare `tier: gate` (`agents/qa_agent.md:6`,
`agents/tester_agent.md:6`), and their read-only grant is sound design — a
gate that can edit what it judges is not a gate. The defect is in the
description (`tester_agent.md`) or in the assumption that the gate authors the
artefact it verifies (both profiles, via `SPRINT_LOG.md`), not in the grant.
Two candidate resolutions, not chosen between here:

1. Correct each profile's `description` / `Profile Rules` to state what it
   actually does — verify and reject, never write — and route every write it
   currently implies (test files, verdict lines) through a profile that holds
   `Write`/`Edit`.
2. Formalize routing through an authoring profile as the design: the gate
   produces the verdict, a writing profile transcribes it.
   `config/artifact_registry.json` already names `SPRINT_LOG.md`'s `role` as
   Orchestrator, which is evidence the second reading was already the
   intended design somewhere in the corpus — the profile prose in
   `agents/qa_agent.md`, `agents/tester_agent.md`, and the plan that assigned
   `G1.q`/`G1.t`/`A3` never caught up to it.

**How it was found, which says something about which controls work.** It
surfaced at Phase 4.1 of Sprint 026
(`docs/sprints/026-core-pipeline/agent_assignment.md`), when the Agent
Orchestrator assigned every unit to a named role and reconciled each against
the profile's actual `tools:` frontmatter. It did not surface in the three
prior sprints that dispatched the same two roles:
`docs/sprints/023-core-pipeline/agent_assignment.md`,
`docs/sprints/024-core-pipeline/agent_assignment.md` and
`docs/sprints/025-core-pipeline/agent_assignment.md` name neither a
disagreement nor a `Write`/`Edit` check (`grep -in
'disagreement\|write/edit' docs/sprints/02{3,4,5}-core-pipeline/agent_assignment.md`
returns nothing). An assignment phase that checks the grant is what caught
it; reading the profile was not enough, in three prior readings, because the
profile's own prose is the thing that is wrong.

**Concrete consequence, measured on this sprint, not hypothetical.**
`docs/sprints/026-core-pipeline/task_scope.md:19-38` records the affected
units under the assigned map: `P8.1`, `P9.2`, `P4.1` and `A2` target
`tests/`; `G1.q`, `G1.t` and `A3` target verdict writes into `SPRINT_LOG.md` —
seven line items in total. Under the profile map as written, every one of
them is assigned to a role that cannot perform the write.
`docs/sprints/026-core-pipeline/task_scope.md` records the workaround the
human chose **for this sprint only**, as a declared deviation: `tests/`
writes reassigned to `devops_agent` (already holding `Write`/`Edit` on
`scripts/`/`hooks/` per `F-086-A1`, treated as a sibling tree for this sprint
only, with `agents.md §6` explicitly **not** amended), and gate verdicts
routed as `<gate role> (verdict) → orchestrator (transcribes)`. Record this
as the sprint-local workaround it is, not as the framework fix — the
framework fix is the open question two paragraphs above.

**How to reproduce.**

```bash
for f in agents/tester_agent.md agents/qa_agent.md; do
  echo "== $f =="
  grep -m1 '^description:' "$f"
  grep -m1 '^tools:' "$f"
done
grep -n '"filename": "SPRINT_LOG.md"' -A6 config/artifact_registry.json
```

The first loop shows `tester_agent.md`'s `description` naming a write its
`tools:` line refuses, and shows `qa_agent.md` carrying the same read-only
grant. The second command shows `SPRINT_LOG.md`'s registered `role` is
`Orchestrator`, not either gate.

---

### - [ ] `F-026-A2` — `tier_escalation` shipped in `v4.7.0`, lay dormant for three sprints, and fired in Sprint 026 only because a human noticed a missing column

**Evidence.** `agents/token_economy_agent.md:21`:

```
| **Domain** | `tier_escalation` | When a task's difficulty diverges from its role's default — the `mechanical`-tier profile asked to author a deployment artifact — the role **proposes** the escalation in `task_scope.md`, the record notes it, and the human sees it. This is the sanctioned exception, and it is a declaration rather than a dispatch. |
```

This row shipped in **Sprint 022** (closed as upstream lead `#12`, above), released
as **`v4.7.0`** — `CHANGELOG.md:36`, the same `### Changed` entry that gives
`token_economy_agent` its three charter rows (`tier_ownership`,
`tier_escalation`, `no_selector_agent`). `task_scope.md` is the artifact the
row itself names as where the declaration lives.

**Reproduced against three sprints, and dormant in all three.**

```bash
grep -inE 'tier|model' docs/sprints/024-core-pipeline/task_scope.md
grep -inE 'tier|model' docs/sprints/025-core-pipeline/task_scope.md
```

Both return nothing — `024` and `025` do not mention tiers at all. `023` does
discuss tiers, but as a finding about attribution, not an exercised
escalation: `docs/sprints/023-core-pipeline/task_scope.md:97` records, **Unrouted**,
that *"the declared tier and the model that actually ran are not the same
fact"* — a real defect, correctly left unresolved by that sprint because it is
not the `tier_escalation` row and folding it in would have misfiled it.

> **Correction — this entry's own first pass measured a moving target, and
> the conclusion it drew was false.** The draft version of this entry, written
> before this correction, reported that Sprint 026 *also* left the mechanism
> dormant — reproduced by grepping
> `docs/sprints/026-core-pipeline/task_scope.md` for `escalat|sonnet|haiku`
> and finding nothing. That grep was accurate at the moment it ran and wrong
> about the sprint, because the file was **being written by the
> `rule_validator` concurrently with this file being read** — a collision
> `agents.md §2 no_interference` exists to prevent, missed here because the
> dispatch checked for concurrent *writes* to this register, not concurrent
> *reads* of a file still being written elsewhere. Re-run after both writes
> completed:
>
> ```bash
> grep -icE 'escalat' docs/sprints/026-core-pipeline/task_scope.md
> ```
>
> Returns **18**, not 0. `docs/sprints/026-core-pipeline/task_scope.md:75`
> carries the section `## Declared escalations — token_economy_agent audit,
> transcribed per its tier_escalation charter row`, and lines 92-96 carry the
> five-row table — `P8`, `P4`, `P9`, `P4.2`, `P4.0`, each `mechanical/haiku →
> author/sonnet` (`P8` additionally `effort medium`), each with a stated
> justification. Lines 98-101 record the inline `Assignee` annotation applied
> to those five rows in the sprint's own Work table, and each of the five now
> reads there as `devops_agent — escalated (mechanical/haiku → author/sonnet…;
> see Declared escalations)` — confirmed directly at
> `docs/sprints/026-core-pipeline/task_scope.md:153,225,261,263,305`. **Sprint
> 026 did exercise `tier_escalation`, and it is the first sprint to do so.**
> The lesson is the register's own rule 1 applied to opening an entry, not
> only to closing one: a report is not a measurement, and neither is a
> measurement taken while its target is still being written.

**The dormancy is three sprints, not four — and Sprint 026 breaking it does
not close the gap.** `023`, `024` and `025` each carried the same structural
condition the row exists to catch — `devops_agent`, `mechanical` tier,
assigned units both `023`'s own finding (line 97, above) and `026`'s later
audit treat as harder than the tier's default — and none produced a
declaration. `026` is the first exception, and it is a sharper finding than
total dormancy, not a milder one: **a dormant mechanism might be broken; this
one is demonstrably functional and still went unused for three sprints.**
Measured, per `docs/sprints/026-core-pipeline/task_scope.md:103-108`:
`devops_agent` carries **high** risk on 22 of the sprint's 67 rows, and only
the five named above were escalated — the other 17 were audited and kept
`mechanical` on stated grounds, not skipped.

**The trigger was a human noticing an absent column, not a control.** Per
`docs/sprints/026-core-pipeline/task_scope.md:75-86`: a human noticed
`task_scope.md` carried no model or tier column and asked; `token_economy_agent`
(owner of the tier map, `tier_ownership`) then audited all 67 units and
proposed the five escalations; `token_economy_agent` holds no `Write`/`Edit`
of its own, so `rule_validator` transcribed the audit into `task_scope.md` —
the same issues-decides/transcribes pattern `task_scope.md`'s gate-verdict
deviation already used. No gate, check or protocol step surfaced the gap in
any of the three prior sprints, and none is what surfaced it here either.

**Why this belongs beside `RA-16` rather than inside it.**
`agents.md RA-16 INVOCATION_COVERAGE` exists for exactly this failure shape —
*"a mechanism nothing calls is a regression, not a pending feature"* — and it
is enforced: `scripts/verify_references.py check (d)` (`:177-204`) walks
`workflows/*.md` and `scripts/*.py`, rejecting any file missing `invoked_by:`
with no exception. That walk is scoped to two directories; `agents/*.md` is
folded into the same check's text corpus only as a source of references to
verify (`:186-190`), never as a set of mechanisms that must themselves declare
an invoker. `tier_escalation` is a table row inside
`agents/token_economy_agent.md`, not a workflow, script, skill or hook — there
is no `invoked_by:` field for a charter row, and no glob in `check (d)` that
would find one if there were. **`RA-16` covers mechanisms that can declare an
invoker; it says nothing about obligations that can only be remembered** — by
a human or an agent, at Phase 4.3, rereading a profile nobody is prompted to
reread. This is that class's first confirmed member with a proof that it can
work when invoked, not only a proof that it can lie dormant; whoever picks
this up should ask how many others there are.

**`F-021-A2` is why the escalation was needed, not why it went unused.**
`agents.md §6` names `devops_agent` **"Sole holder of `Write`/`Edit` for the
framework-root `scripts/` and `hooks/` trees"**, and `F-021-A2` (above, open)
states the wider gap: 8 of 13 profiles hold `Write`/`Edit` and none is an
implementer. Because no `author`-tier profile holds `Write`/`Edit` on
`scripts/`/`hooks/`, every code unit those trees produce — regardless of
difficulty — is authored by the one `mechanical`-tier profile that can write
them at all; `tier_escalation` is the sanctioned way to compensate for that
*without* redesigning the role map, by escalating the **model** `devops_agent`
runs on for one task while its jurisdiction stays put — confirmed exactly at
`docs/sprints/026-core-pipeline/task_scope.md:77-79`, "Assignee and
jurisdiction are unchanged for every row below… each entry here is a model
escalation for one task, not a reassignment." So `F-021-A2` is not a blocker
that left `tier_escalation` with nowhere to route — Sprint 026 shows the
route works. `F-021-A2` is the reason the same structural condition (a
`mechanical`-tier profile absorbing every `scripts/`/`hooks/` unit,
high-risk ones included) recurred in all four sprints, and the reason the
compensating mechanism had three chances to fire before it did.

**Distinct from, and meeting, both open findings above.** `F-021-A2` is the
missing implementer role — the reason `devops_agent` carries every
`scripts/`/`hooks/` unit regardless of difficulty. `F-026-A1` is two gate
profiles assigned or described writes their own grant refuses. This is a
charter obligation that worked exactly once, unprompted by anything but a
human's question. Three different defects, meeting on the same rows: Sprint
026's five escalated units are `devops_agent` work only because of
`F-021-A2`, escalated only because a human asked rather than because
anything checks for it (`F-026-A2`), on a profile that the same sprint also
routed gate-adjacent writes to because the actual gate profiles cannot hold
them (`F-026-A1`).

**Two candidate directions, named and not chosen between** — choosing is a
governance decision behind `agents.md §2 triple_lock`:

1. Make the declaration a testable artifact — for example a `Tier`/`Model`
   column `task_scope.md`'s own shape check can require whenever `Risk`
   diverges from the assignee's declared default, so the absence is a
   deterministic finding rather than something a human has to notice and ask
   about.
2. Fold the tier-difficulty check into a phase's stated deliverable —
   `rule_validator`'s own Phase 4.3 audit is already the pass that produced
   `F-026-A1` by reconciling assignment against grant, and is the same pass
   that transcribed Sprint 026's five escalations; reconciling assignment
   against tier in the same pass would make the check's own declared scope,
   not a human's memory, the thing that fails loudly when the reconciliation
   is skipped.

**How to reproduce.**

```bash
grep -n "tier_escalation" agents/token_economy_agent.md
grep -inE 'tier|model' docs/sprints/024-core-pipeline/task_scope.md docs/sprints/025-core-pipeline/task_scope.md
grep -n "Unrouted" docs/sprints/023-core-pipeline/task_scope.md
grep -icE 'escalat' docs/sprints/026-core-pipeline/task_scope.md
sed -n '75,101p' docs/sprints/026-core-pipeline/task_scope.md
sed -n '177,209p' scripts/verify_references.py
```

The first returns one row, the charter declaration. The second returns
nothing for either sprint. The third returns the attribution finding at
`023-core-pipeline/task_scope.md:97`, not an escalation. The fourth returns
`18`. The fifth shows the `## Declared escalations` section and its five-row
table. The sixth shows `check_invocation_coverage` scoped to `workflows/` and
`scripts/`, never `agents/`.

---

### - [ ] `F-026-A3` — `hooks/on_init.py` hardcodes host-relative paths, and the resolver that exists for exactly this class of problem goes unused

**Evidence.** `hooks/on_init.py:13-23`:

```python
CONFIG_PATH = Path(".env")
ENV_TEMPLATE = Path(".env.template")
BRIDGE_LOCK = Path(".agents/.claude_bridge.lock")
INSTALL_SCRIPT = Path(".agents/scripts/install.py")

BRIDGE_ANCHORS = [
    Path(".claude/commands/agents/start.md"),
    Path(".claude/agents/principal_agent.md"),
]
```

Every path constant is a literal, host-relative string. The file's import
block — `os`, `subprocess`, `json`, `datetime`, `pathlib`, `sys`,
`hooks.telemetry` — names neither `scripts/_root` nor `scripts/_mode`.
`scripts/_root.py` (`agents_root()`) and `scripts/_mode.py` (`is_nucleus()`)
are the framework's sanctioned mode/root resolvers for exactly this class of
problem: `agents_root()` was built as Sprint 023 unit `C0.3`, and its own
docstring names `check_readme_counts.py` resolving `Path("skills")` against
the working directory and crashing in every host as the defect it exists to
close (`F-093-N2`, above).

**Documented, not undetected — and that is the finding, not the hardcoding by
itself.** `workflows/start_workflow.md` Phase 1.5 `bridge_check` already
states the asymmetry in its own cell: *"in a host, `hooks/on_init.py`
performs this same check ... automatically at session start ... In the
nucleus no hook runs at all"*, and in the same sentence, *"`hooks/on_init.py`
also resolves `.agents/`-prefixed paths that do not exist here."* So a reader
of that workflow cell is told the limitation. Nothing states which of two
readings is the intended end state, and this register names both rather than
choosing:

1. The hook is host-only by design and the hardcoding is correct — in which
   case `hooks/on_init.py` should say so in its own docstring, the way
   `scripts/_root.py:21` states host-scoped scripts "MUST NOT adopt
   `agents_root()`", rather than leaving a reader to infer scope from a
   workflow cell three files away.
2. The hook should resolve through `scripts/_root.py`/`scripts/_mode.py` like
   every other framework-scoped or mixed script listed in `scripts/_root.py`'s
   own `invoked_by:` block — in which case the nucleus gains the session-start
   bridge automation whose absence is what let the nucleus bridge go stale for
   a month (`start_workflow.md`, same cell; `F-093-N1`'s second defect,
   above).

**How it was found, and the mechanism matters more than the file.** During
Sprint 026 unit `P3.2.1`, a census rename inside `INSTALL_SCRIPT`
(`hooks/on_init.py:16`; row at
`docs/sprints/026-core-pipeline/task_scope.md:304`; committed `88a1e65`), the
dispatched `devops_agent` read the file's mixed path styles — some
`.agents/`-prefixed, some not — as an inconsistency, "fixed" it by dropping
the `.agents/` prefix from `INSTALL_SCRIPT`, and verified with
`Path(...).exists()` from the nucleus root, where this hook never executes.
**The check printed `True`, and the file was broken in the only context it
runs in** — a host, at session start, per `start_workflow.md`'s own cell
above. The change was caught in review and reverted; the corrected rename is
the one committed at `88a1e65`.

Record the mechanism, not only the file: **a verification run in the wrong
context produces a false green, and a file whose deployment context is
stated only in a distant workflow cell — never in its own docstring — invites
exactly that error.** This is the same failure signature as `F-026-A2`,
cross-referenced above: a control (there, a charter row nobody was prompted
to reread; here, an `.exists()` check run from the wrong root) that answers
confidently about something it did not actually inspect. It is also adjacent
to, and not the same defect as, the class Sprint 026 unit `A4.2` is scheduled
to repair: `docs/sprints/026-core-pipeline/task_scope.md:346,458` name
`hooks/on_init.py` as an `RA-16` hooks-blindness repair target (the missing
`invoked_by:` declaration), deferred to Hito 2 (`⏳→H2`). `A4.2`'s declared
scope is the missing invoker declaration; this entry's scope is the
host-relative paths inside the file that declaration would then cover.

**Noted, not inflated.** `hooks/on_init.py:18` still comments that
`install.py` links the bridge artifacts — a script that no longer
exists under that name (`INSTALL_SCRIPT` two lines above names
`scripts/install.py`). This is inside Sprint 026's own declared deferral set
(`docs/sprints/026-core-pipeline/task_scope.md` §`Declared deferral`, the
`P3.2` prose subset), scheduled for Hito 2, not an omission this entry adds
weight to.

**How to reproduce.**

```bash
grep -n "^import\|^from" hooks/on_init.py
grep -n "CONFIG_PATH\|ENV_TEMPLATE\|BRIDGE_LOCK\|INSTALL_SCRIPT\|BRIDGE_ANCHORS" hooks/on_init.py
grep -n "def agents_root\|def is_nucleus" scripts/_root.py scripts/_mode.py
grep -n "performs this same check.*automatically at session start\|resolves \`.agents/\`-prefixed paths" workflows/start_workflow.md
sed -n '304p' docs/sprints/026-core-pipeline/task_scope.md
```

The first returns no `_root`/`_mode` import. The second returns five literal,
host-relative constants. The third shows both resolvers defined and exported.
The fourth shows `start_workflow.md`'s own documented asymmetry. The fifth
shows unit `P3.2.1`'s row and its committed hash, `88a1e65`.

---

## Inherited from host sprint records — **re-measure before acting**

These were recorded by a host across sprints and were **not** reproduced while
writing this file. Each is a lead with a stated origin. Reproduce it against the
current tree first; if it no longer holds, delete the entry and say so.

### - [x] `G-03` — the artifact is specified at a path its own enforcement does not check

`workflows/pipeline_workflow.md` Phase 4.3 and `agents/rule_validator.md` locate
`task_scope.md` "at the host root, git-ignored". The host-side enforcement script
resolves it **inside the sprint folder**, and every host sprint has committed it
there. A rule validator following the framework text literally writes the file
where CI cannot see it, and reproduces a missing-artifact failure while believing
it complied.

Proposed: both documents should read
`docs/sprints/[Sprint_ID]-[Stack]-[Layer]/task_scope.md`, tracked.

**Reproduced, then closed** — Sprint 023 unit `C0`, commit `2821953`
(PR pending 023). The lead held: both documents said *"at the host root"* and
*"git-ignored"*, and both halves were false. Re-measured: `pipeline_workflow.md`
Phase 4.3 and `agents/rule_validator.md` now locate `task_scope.md` inside the
sprint directory named in `agents.md §5 mandatory_topology`, versioned, and
`scripts/docs_freshness_check.py` and `close_workflow.md` Phase 2.6 read it
there.

**The entry found a second drift in the same two documents, closed by a
different unit.** They also declared a **four-column** table for this artifact
(`Subtask | Target File | Assignee | Status`), naming neither `Operation` nor
`Risk` — a shape that matched no file on disk across sprints 021–025, where all
five `task_scope.md` files carry six columns. Corrected to
`# | File | Operation | Risk | Assignee | Status` in Sprint 023 unit **`C0.2`**,
commit `92f42da` — **not** in `C0`/`2821953`, which left the four-column form
intact in both documents. A document specifying an artifact at the wrong path was
also specifying it in the wrong shape, in the profile of the very agent that
writes it.

### - [ ] `REVDOC-G1` — the graph drops files silently

The knowledge graph omits files it cannot process without recording that it did.
A consumer cannot distinguish "not in the graph" from "not in the repository".
Proposed: emit a skipped-file manifest alongside the graph.

### - [ ] `ADR-0006` — `local_testing` mandates in-memory SQLite

`agents.md §3 local_testing` requires `sqlite:///:memory:`. A host with money
columns whose behaviour differs by database engine cannot honour it without the
suite passing while proving nothing about production. That host declared the
deviation in an ADR and runs its tests on the real engine.

Proposed: state the rule as *isolate the test database*, with the engine chosen
by fidelity requirements — or name in-memory SQLite as the default with a
declared-deviation path, which is what hosts end up building anyway.

### - [ ] `ADR-0007` — pipeline phase enforcement and the delegation conflict

Recorded by a host against phase enforcement and the delegation rules. Note that
`start_workflow.md` Phase 2 `delegation_conflict` already covers part of this
ground and was written from the same incident; check what remains before
drafting.

### - [x] `C5` — a tracked symlink into the submodule enters host gate scope

> **Identifier collision, stated because both objects appear in this file.** This
> entry's `C5` is a **host's finding ID**. Sprint 023 also had a unit of the same
> name — the one that closed `F-086-A1` — and it is a different object entirely.
> The convention, which holds throughout: **the sprint's unit is always written
> in full**, as ``Sprint 023 unit `C5` ``, and a bare `C5` therefore always means
> this entry. Other sprint units are cited in whichever form reads naturally,
> since none of them collides with anything here. The host's ID is kept unchanged
> because rule 3 says keep the entry, and renaming a finding breaks the host's own
> trace back to it.

A host's root `AGENTS.md` is a tracked symlink into this submodule. Any host gate
that walks tracked files therefore reads nucleus content, while `strict_rule`
forbids the host from changing it. Today this is latent. It becomes an unfixable
red in that host the moment the nucleus ships a file that violates one of the
host's own document rules.

Proposed: state whether symlinked nucleus content is in or out of host gate scope,
so hosts exclude it deliberately rather than discovering the conflict.

**Closed** — Sprint 026 unit `P7`, commit `435db07`. `agents.md §3` now carries
`symlink_gate_exclusion`: host-root `AGENTS.md` is out of host documentary-gate
scope; the host excludes the symlink path in its own gate configuration.
`F-021-A2` and `F-023-S4` are intentionally left open.

### - [x] `#12` — agent profiles declare `tools:` and no model tier

Every profile in `agents/` states which tools a role may use and says nothing
about which model it should run on. Each host either re-derives a tiering per
sprint or does without one and pays top-tier prices for deterministic work.

A `model:` field in the profile frontmatter would make the decision inheritable
and reviewable, exactly as `tools:` already is. Offered as a starting proposal,
not a rule:

| Tier | Roles | Basis |
| :--- | :--- | :--- |
| Top | `qa_agent`, `tester_agent`, `principal_agent` | Adversarial and planning. Produce findings nothing else produces |
| Mid | `orchestrator`, `rule_validator`, `skill_architect`, `doc_orchestrator`, `agent_orchestrator` | Structured authoring against a stated rule; errors are caught by the gates downstream |
| Low | `devops_agent`, `git_sync_agent`, `topology_mapper` | Deterministic, verifiable results. A wrong answer fails on the next command |

**Keep the gates at the top tier**, which is the part a token budget attacks
first. Across four consecutive host sprints every central defect was found by a
gate and by nothing else, and several had already survived the author's own
verification. Each was a control reporting clean because of *how it was run*
rather than what it checked — the failure a cheaper reviewer is least likely to
catch, because catching it means disbelieving a green result.

**Reproduced, then closed** — **Sprint 022, PR #45** (*Model Tiering*), which is
the one item in this file that closed before Sprint 023 and therefore carries a
real pull request. Re-measured: **13 of 13** profiles in `agents/` now declare
`model:`, and a `tier:` field beside it names the reasoning the tier encodes
rather than leaving the choice to be inferred from the model name.

**The proposal's central instruction was followed**: the gates stayed at the top
tier. Sprint 023 is the evidence for why — every rejection that mattered came
from `qa_agent` or `tester_agent`, `C4` was rejected three times over a
destructive regression its author could not see, and `C10` took six rounds and
four rejections. A cheaper gate is the one economy this file argues against.

### - [ ] `#13` — `max_lines_per_func` is a magnitude with no definition

`agents.md §1` declares `max_lines_per_func = 50 lines` and never states what
counts as a line, while the same table mandates Google-style docstrings.

A host measured the difference on its own tree: under a physical-line reading it
had roughly three times as many violations as under a code-line reading, and the
functions between the two readings crossed the limit **only on the strength of the
documentation this ruleset requires**. The largest offender under the physical
reading was a test whose docstring explained why the size gate exists.

`agents.md §1 unambiguous_action` prohibits "magnitudes without a unit". This one
has a unit and no definition, which is the same defect one level in.
`rules/code_craft.md §3` defers to `agents.md §1` for size and does not resolve
it. Two further points nothing states: whether a decorator counts toward the
function, and whether nesting is measured in blocks or in indentation columns.

That host declared **code lines — physical extent less the docstring block** in an
ADR, on the grounds that a gate satisfied by shortening a mandated docstring is
worse than no gate. **Every host inherits the ambiguity**, and the nucleus should
state which reading it means rather than leave each host to pick and then deviate.

Note for whoever implements a check: `ruff` can express neither rule. `PLR0915`
counts *statements* against a rule written in *lines*, and `PLR1702` is
preview-only with a default of 5 levels against a declared 3. Adopting either
mechanises a different rule while reporting compliance with this one.

---

## How to work this file

1. **Reproduce before repairing.** Every item above states how. The
   *Inherited from host sprint records* section especially: a finding carried on
   the strength of an old record is the defect half of these findings describe.
   This rule governs **closing** an item too — tick a box on a re-measurement,
   never on a record that claims the fix landed.
2. **One concern per pull request.** `F-086-S1` and `F-086-S2` are the exception —
   they are two halves of one gap and fixing either alone leaves it open.
3. **Tick the box and keep the entry** when a finding is fixed, with the pull
   request that closed it, until the next release seals it into `CHANGELOG.md`.
4. **Delete an entry that no longer reproduces**, and say so in the commit. An
   open item that was silently dropped is indistinguishable from one nobody read.
