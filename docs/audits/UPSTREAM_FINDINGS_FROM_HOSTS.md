# Upstream findings reported by a host

Open items, not a blocker for publishing. Each was found while running the
pipeline inside a host project and is **framework-class** under
`agents.md §4 feedback_upstream`: it affects every host that installs this
nucleus, so `strict_rule` correctly forbade the host from patching it and routed
it here instead.

Genericized per `RA-15`: no host project name, no absolute paths, no host
business logic. Where a measurement is quoted it is a count, not an identity.

**Two sections, and the difference is load-bearing.** The first was reproduced
against `v4.4.0` while this file was written — file and line resolve today. The
second comes from host sprint records and has **not** been re-measured here; treat
each as a lead, reproduce it first, and delete it if it no longer holds. A finding
carried forward on the strength of an old record is exactly the defect several of
these findings are about.

---

## Verified against `v4.4.0`

### - [ ] `F-086-A1` — the profile that owns deployment artifacts cannot write one

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

---

### - [ ] `F-087-P1` — the platform probe reports an enabled control as disabled

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

---

### - [ ] `F-086-S1` — the secret auditor's patterns are correct and its file list is not

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

---

### - [ ] `F-086-S2` — the commit hook's file list is correct and its pattern is not

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

---

### - [ ] `F-086-S3` — `mass-standardizer` orphaned a vendored skill, and has been unusable since

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

---

### - [ ] `F-093-N1` — the nucleus cannot satisfy its own entry-point rule

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

### - [ ] `F-093-N2` — a mandatory close step crashes in every host

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

---

## Inherited from host sprint records — **re-measure before acting**

These were recorded by a host across sprints and were **not** reproduced while
writing this file. Each is a lead with a stated origin. Reproduce it against the
current tree first; if it no longer holds, delete the entry and say so.

### - [ ] `G-03` — the artifact is specified at a path its own enforcement does not check

`workflows/pipeline_workflow.md` Phase 4.3 and `agents/rule_validator.md` locate
`task_scope.md` "at the host root, git-ignored". The host-side enforcement script
resolves it **inside the sprint folder**, and every host sprint has committed it
there. A rule validator following the framework text literally writes the file
where CI cannot see it, and reproduces a missing-artifact failure while believing
it complied.

Proposed: both documents should read
`docs/sprints/[Sprint_ID]-[Stack]-[Layer]/task_scope.md`, tracked.

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

### - [ ] `C5` — a tracked symlink into the submodule enters host gate scope

A host's root `AGENTS.md` is a tracked symlink into this submodule. Any host gate
that walks tracked files therefore reads nucleus content, while `strict_rule`
forbids the host from changing it. Today this is latent. It becomes an unfixable
red in that host the moment the nucleus ships a file that violates one of the
host's own document rules.

Proposed: state whether symlinked nucleus content is in or out of host gate scope,
so hosts exclude it deliberately rather than discovering the conflict.

### - [ ] `#12` — agent profiles declare `tools:` and no model tier

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

1. **Reproduce before repairing.** Every item above states how. The second
   section especially: a finding carried on the strength of an old record is the
   defect half of these findings describe.
2. **One concern per pull request.** `F-086-S1` and `F-086-S2` are the exception —
   they are two halves of one gap and fixing either alone leaves it open.
3. **Tick the box and keep the entry** when a finding is fixed, with the pull
   request that closed it, until the next release seals it into `CHANGELOG.md`.
4. **Delete an entry that no longer reproduces**, and say so in the commit. An
   open item that was silently dropped is indistinguishable from one nobody read.
