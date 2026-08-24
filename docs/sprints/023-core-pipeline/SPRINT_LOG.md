# Sprint Log — 023 (`upstream-findings`)

**Branch**: `ai-sprint/023` from `main` at `18696c5` (`v4.7.0`)
**Status**: open. **All 14 units delivered and gated.** No unit remains; `F8` is
written up in the program queue and routed by human decision to an `RA-03`
hotfix, to be executed after Sprint `026`.

> [!IMPORTANT]
> **This file's `## Delivered` section narrates `C9`, `C0`–`C4` and stops there.**
> `C4.2`, `C5`, `C6`, `C7`, `C8` and `C10` are delivered and gate-approved but
> have **no entry below**. The authoritative per-unit record is the status table
> in `task_scope.md`, which carries every unit, its commits and its gate verdicts.
> Stated rather than patched with one catch-up entry: writing `C8`'s narrative
> alone would leave five units missing while the header claims fourteen, which is
> the drift this sprint has recorded four times under `RA-14`. **Closing the
> sprint requires writing the six missing entries** — that is closeout work, not
> a footnote, and it is named here so the closeout meets it as a known task
> rather than discovering it.

## Delivered

### `C9` — branch integration answers in three values, not two (`437493b`)

Ran first because this sprint's own close invokes `branch_sovereignty audit`.
Repairing that gate last would have meant tripping on the defect the sprint
exists to remove.

**The defect.** `merged_pr_exists` returned a bool and mapped every non-zero
exit to `False`, so *"I could not find out"* became *"no merged PR exists"*.
Measured against the live API: **2 of 12 calls returned `rc=1`, `HTTP 503`**.
Because `content_is_integrated` already returns `False` for every squash-merged
branch, one 503 was enough to flip an **integrated** branch to unintegrated.
Reproduced as two triple-runs of `audit` on an unchanged tree exiting `0,2,0`
and `0,0,2` — **accusing a different branch each time**, which is the signature
of a per-call failure rather than a property of any branch.

**Why it mattered despite failing safe.** `prune` never deleted what it could
not prove, so nothing was destroyed. The damage was the remediation the gate
induced: it steered the operator toward a permanent waiver for a healthy
branch — the *"weakening the check"* the module docstring already warned
against. The docstring promised *"reported, not assumed"*; the code assumed.

**The fix.** `YES` / `NO` / `UNKNOWN`, with retry and backoff. `UNKNOWN` still
blocks — a real outage that passed would be a false green, the same defect
inverted — but it is reported as doubt, separately from an accusation, and is
**never offered the waiver**.

**Two traps caught during implementation, both recorded in the code:**

1. **The truthiness inversion.** `classify`'s condition was
   `content_is_integrated(...) or merged_pr_exists(...)`. With a three-valued
   string answer, `NO` and `UNKNOWN` are both non-empty and therefore truthy —
   that chain would have reported **every** branch integrated. A silent
   inversion of the gate is far worse than the flakiness being removed.
2. **`rc=1` means two different things.** Probed rather than recalled:
   `no git remotes found`, `not a git repository` and
   `none of the git remotes …` mean there is no GitHub side to ask, so no pull
   request can exist — a definitive `NO`. Treating them as `UNKNOWN` would
   **refuse the seal forever in every local-only repository**, trading an
   intermittently wrong gate for a permanently closed one.
   `Could not resolve to a Repository` stays `UNKNOWN`: a misconfigured remote
   must surface rather than read as clean.

Also closes an `agents.md §1 exception_handling` violation — the error became a
datum with no log.

**Verification**: `make verify` **168 passed** (161 + 7 new); gate run 5×, exit
measured without a pipe, `0,0,0,0,0`. That does not *prove* determinism — only
that no three consecutive failures occurred. What changed structurally is that
three are now required instead of one, and every path has a direct test.

`RA-14` propagation: `close_workflow.md` steps `branch_audit` and `local_prune`
both described integration as binary; `local_prune` also offered the waiver
without distinguishing doubt from abandonment. Both patched.

### `C0` — the Implementation Plan gets a location and a gate (`2821953`)

**The defect.** The plan was the only pipeline deliverable with no home. It is
`triple_lock`'s first lock, the Phase 1 deliverable, and `rules/code_craft.md`
requires justifying every dependency in it — mentioned **seven times** across the
governance corpus, and **no document said where it is written**. Measured: 11
templates in `docs/standards/templates/` and none for a plan; a host's sprint 093
folder left six artifacts and none was the plan. The consequence was measured too
— a host lost an approved plan, and this repository held two Implementation Plans
from April 2026 untracked for four months.

**The sequencing contradiction, which no document had resolved.** The plan is
*authored* at Phase 1; the sprint directory is *instantiated* at Phase 3. The
canonical path does not exist when the plan is written. Resolved explicitly:
Phase 1 authors, Phase 3 extracts and commits, Phase 5 checks existence as a
precondition, close verifies retrospectively. Without that, the rule would have
been unexecutable while reading as complete.

**What the gate proves, written into the workflow.** It proves the plan exists and
is versioned — the loss it was built against. It does **not** prove the plan
existed before approval; that ordering rests on the Phase 5 precondition, an
attended human step. Stated rather than implied, because a gate suggesting a
guarantee it does not give is this program's subject.

**No new mechanism** (`RA-16`): `PHASE_ARTIFACTS` in `docs_freshness_check.py`
gains one entry and the dict is reordered by phase, so a sprint that skipped
several steps reads in the order they should have run.

**`RA-14` found three false paths, not two.** The full grep — the rule's actual
requirement, as opposed to patching where one happened to look — turned up
`agents/rule_validator.md:19` calling `task_scope.md` a *"git-ignored session
artifact at the host root"*, both halves false since Sprint 024, **in the profile
of the agent that produces the file**. `pipeline_workflow.md` Phase 4.3 and
`agents/token_economy_agent.md:25` were the other two.

**Verification**: the gate measured **red then green** on this tree — naming
`IMPLEMENTATION_PLAN.md` and Phase 1 while absent, silent once written — with the
exit read from `$?` directly and never through a pipe. `check_phase_artifacts`
shipped in PR `#37` with **no test at all**; it now has six, and three of them
could not have passed before this change. `make verify`: **174 passed**.

This sprint's own plan is filed with the commit, from the new template, and says
in its header that it was filed retroactively.

### `C0.2` — each phase is defined by the artifact it leaves (`92f42da`)

**The defect.** The pipeline's coordination matrix existed as four
hand-maintained copies of overlapping lists: three filenames in
`docs_freshness_check.py`, six in `map_workflows.py`, two demanded by
`close_workflow.md` Phase 2.6, and prose in `pipeline_workflow.md` that
described deliverables without naming them. Nothing reconciled the four.

**The principle, which is what makes it worth a mechanism.** A framework
requiring *"Phase 4.1 leaves `agent_assignment.md`"* runs under Claude Code,
under Cursor and from a terminal. One requiring *"invoke `agent_orchestrator`"*
runs only where that primitive exists. Sprint `026` (`tool-portability`)
consumes this registry for exactly that reason, and Sprint `027` needs it for
the `SubagentStop` hook.

**Measured red, then green, on this tree.** With the list externalised the
freshness gate immediately named `agent_assignment.md` (Phase 4.1) and
`skill_assignment.md` (Phase 4.2) as missing from this sprint — **both produced
by sprints `021`, `022`, `024` and `025`**, and both invisible to the
three-filename map that preceded the change. The unit caught a real skipped
phase on the sprint that built it, and the two records were then written rather
than the finding quietly dropped.

**Why `map_workflows.py` could not have found it.** It matched workflow prose by
literal filename against six state artifacts and zero documentary ones, so a
phase describing its deliverable in words was invisible by construction — which
is how `task_scope.md` came out registered as `pipeline_workflow`'s *consumer*
while `close_workflow` writes it. Phases 3, 4.1, 4.2 and 8 now name their
artifact; the matrix carries twelve columns and a legend derived from the same
registry.

**The doubt path, because this sprint's subject is gates that answer when they
do not know.** Externalising a list creates a new way to report a false green: a
missing registry would make the loop iterate over nothing and pass a sprint that
left no artifact at all. The freshness gate reports *"the check did not run"*;
`map_workflows.py` raises instead, because a matrix with no columns reads as
*"no workflow touches any artifact"*. Opposite directions, deliberately: one
reports findings, the other generates a document.

**Two artifacts are deliberately not required**, and the registry says so per
entry: `PHASE_REGISTER.md` and `graph_stats.json` are written *during* the
close, so demanding them would fail every sprint at the moment the check fires.
`graph_stats.json` also already has its own dedicated check, so a second warning
would double-report the same absence.

**`R6` was already satisfied, and that is recorded rather than manufactured.**
The roadmap predicted `task_scope.md` would need an `Assignee` column added.
Measured: all five sprint files already carry `# | File | Operation | Risk |
Assignee | Status`. What was actually wrong was the *declared* shape —
`pipeline_workflow.md` Phase 4.3 and, found by the `RA-14` grep,
`agents/rule_validator.md` both declared a four-column form naming neither
`Operation` nor `Risk`, matching no file on disk, in the profile of the agent
that writes them.

**The third finding routed to this unit** (`16ed3e9`). Opening a sprint updates
no field of the anchor and no script does, so `current_sprint.id` is a hand edit
with no gate — this sprint's own resume read `22` while `ai-sprint/023` and its
directory both existed. **The instrument the record proposed was rejected by
measurement**: comparing the anchor against the newest directory under
`docs/sprints/` fires on a *correct* state here, since `024` and `025` exist as
directories while `023` is legitimately in flight. The probe compares against the
checked-out `ai-sprint/[ID]` branch instead, and a test pins the rejected
comparison so the cheaper wrong instrument cannot come back.

**Verification**: `make verify` exit `0` read from `$?` directly, never through
a pipe — **190 tests** (174 + 16). `check_phase_artifacts` keeps its six `C0`
tests and gains three; the registry contract gets eight, one of which pins that
every registry filename is named literally in some workflow, so `R2` cannot
silently regress; the anchor probe gets five.

### `C0.3` — the framework root resolved once (`359d03c`, plus its fix)

**The defect, measured rather than described.** Five framework-scoped scripts
addressed `README.md`, `skills/`, `workflows/`, `rules/` and `config/` as bare
relative paths. Each was copied out of the tree and run from an empty directory,
and the three failure modes differ — only one of them fails the way it should:

| Script, before `C0.3`, from another directory | Result |
| :--- | :--- |
| `scan_workflow_determinism.py` | `[OK] no candidates found`, exit `0` — **a clean pass over nothing** |
| `verify_references.py` | Crash: `FileNotFoundError: agents.md` |
| `check_manifest_parity.py` | Exit `1`, *"run from the .agents root"* — a false failure that told the human to compensate for the defect |

`map_workflows.py` is not measurable that way: copying the file displaces the
`__file__` its registry path anchors to. Said rather than a fourth row invented.

**A rename, not a redesign.** Sprint 025 wrote this exact anchoring as
`_mode.agents_dir()` on purpose and said so in its docstring. `scripts/_root.py`
now holds `agents_root()`, `_mode.py` imports it and keeps only `is_nucleus`.
One function, one name, one definition — a second name for the same fact would
have been the defect `C0.2` had just removed one level up.

**Why the cwd is set instead of every path rewritten**, written into `_root.py`
so the next contributor inherits the reasoning: rewriting each `Path("workflows")`
would turn every message these scripts print from a relative path into an
absolute one, and `C0.3`'s stated limit is that no observable behaviour changes;
and the next bare `Path("docs")` added would silently reintroduce the defect.
`verify_references.LOADABLE` evaluated its globs at import — before any entry
point — so it became a function.

**The inverse error is the larger one, and host-scoped scripts now say so in
their own docstrings.** Anchoring `hooks/telemetry.py` to the framework would
write a host's error log inside the submodule, which `§3 strict_rule` forbids
outright. Two mixed-scope paths did move: `branch_sovereignty`'s `WAIVERS`, the
relative path deferred out of `C9`, and `docs_freshness_check`'s `DENYLIST_DIR`,
which named `.agents/scripts/denylists` — correct in a host, non-existent in the
nucleus, so the three denylists that ship were never loaded here.

**What this unit broke, and how it was caught.** Anchoring `WAIVERS` converted
`test_waived_branch_does_not_block` from a test writing into its own `tmp_path`
into one **overwriting the repository's real `config/abandoned_branches.json`**
with fixture data, destroying the three keys that document the valve. The suite
passed green throughout; it was found by reading the commit's diff. The remedy
is not only the restore and the patched test but the assertion that was missing:
`make verify` now runs `git diff --exit-code config/ hooks/ scripts/` after the
suite. **Anchoring a constant is not a local change** — every test that wrote
through it now writes into the real repository.

**Verification**: `make verify` exit `0` read from `$?` directly — **200 tests**
(190 + 10). The acceptance criterion is one parametrised test comparing exit
code, stdout *and* stderr of each anchored script run from the repository root
and from a temp directory: an anchored script cannot tell where it was called
from.

### `C1` — a mandatory close step that had never completed in a host (`b2d7c2e`)

`F-093-N2`. `close_workflow.md` Phase 2 invokes `check_readme_counts.py` from
the **host** root, where every path it read resolved against the host: `README.md`
became the host's README, `rules/` and `agents/` globbed empty, and
`skills/`.iterdir() raised. Measured from a directory holding only a host
README — `FileNotFoundError: 'skills'`, **exit 1**, not the exit `2` the script's
own docstring and that workflow both promise. Measured green from the same
directory after anchoring, and the script joins the parametrised cwd-invariance
test that `C0.3` had deliberately excluded it from.

`iterdir()` is still not wrapped in `try/except`, and the reason now lives in the
code rather than only in the roadmap: anchored, those directories always exist,
so an exception means a broken checkout. Catching it would report **0 skills**,
which reads as drift against the README and sends the reader to edit a number
that was never measured.

**Two collateral fixes, both the same lesson `C0.3` had just taught.** The readme
fixture steered the script by cwd — the mechanism this unit removes — so it
substitutes `agents_root` instead. And the tree-mutation guard added in `c8c8c35`
compared against `HEAD`, so it failed on its own author's unstaged edits: a guard
that fires on normal development is one that gets disabled rather than satisfied.
It now compares before against after the suite, and was **verified to still fire
on a real mutation** rather than assumed to.

### `C2` — the platform report answers in four values (`26367cf` + `ca29010` + `509f525`, approved)

**The first unit of this sprint gated by dispatched subagents, the first
rejected, and the only one whose author did not sign off on his own work.**
Both gates returned `REJECTED` on round 1. Session #2 ran the remaining rounds:
`tester_agent` **APPROVED** at round 2, `qa_agent` **REJECTED** at round 2 and
**APPROVED** at round 3. Three rejections across two gates before this unit
passed — more than the rest of the sprint combined.

**The defect the unit was for.** `security.get(control, {}).get("status") !=
"enabled"` turned a field the API never returned into a disabled security
control, and `security_and_analysis` is omitted wholesale for a caller without
administrative access — so a hardened repository was told three of its controls
were off.

**The defect the unit introduced, which is the more instructive one.** The
repair mapped HTTP `404` to `disabled`. GitHub answers `404` on an admin-only
endpoint to any caller lacking administrative access, whether the feature is on
or off. The Tester gate reproduced it live against `cli/cli` and
`torvalds/linux` — both demonstrably hardened — and got three false accusations
each, under the accusation heading, with a remedy offering to patch a repository
the caller cannot administer. **This sprint's own defect, rebuilt inside the
function written to remove it.** The author had measured only against this
repository, where the token is an admin, stated that blind spot aloud, and did
not act on it. The first test suite asserted the defect rather than catching it.

The discriminator was free and readable without admin: `permissions.admin`, in
the same call that already carries `security_and_analysis`. A `404` is
`disabled` only for a caller who could have seen the answer.

**Six more defects, all reproduced rather than argued.** Branch protection asked
an admin-only endpoint when the public `protected` boolean answers it; the HTTP
status was matched by searching stderr for `404`, which a dead proxy on a
repository whose *name* contains `404` defeats; a missing `enabled` read as
`disabled` while a missing analysis key read as doubt — two opposite rules for
absence in one unit, the failing one being the security branch;
`{"enabled": "false"}` reported an off control as on; a non-dict payload raised
`AttributeError` and would have taken down the entire readiness probe; and every
doubt line hardcoded *"field not returned"* over causes it never measured — the
unit's thesis violated one level down.

**What the author rejected, with a measurement.** Gate 1's `F-5` claimed the
report joiner renders a bullet at an indent used nowhere else. Rendered: it is
exactly the indent `main()` gives every top-level finding. A gate is not right
by virtue of being a gate.

**`G-1` — the sprint's own defect, a third time, and the most instructive of the
three.** The QA gate rejected `26367cf` because `collect_security_controls`
fetched an endpoint to derive the doubt line while the state function fetched
the **same** endpoint again internally. Both arguments to `record()` evaluate
eagerly, so the cause came from one response and the state it annotated came
from another; a failure between the two calls made the report explain an answer
it had never received. **Invisible in every rendering** — under a healthy network
both responses agreed — and therefore found by *counting calls*, not by reading
output: **5 invocations for 3 endpoints**. The correct one-call shape already
existed twelve lines away in the same function, so one function held two
opposite patterns, which is the exact shape of `D4` one level up. Fixed in
`ca29010`: the two classifiers now take `(rc, stdout, stderr, is_admin)`, the
shape `state_from_exit` and `undetermined_cause` already used, and the caller
fetches once. Pinned by a test that counts calls rather than asserting a string.

**`D1` was verified live, which is the whole point.** Round 1's suite had
asserted the defect rather than catching it, so a unit test proving `D1` fixed
would have proven nothing. Measured against real repositories the token does not
administer:

| Repository | Round-1 code | HEAD accusations | HEAD doubt |
| :--- | :--- | :--- | :--- |
| `cli/cli` | **5 false** | **0** | 4, each naming its measured cause |
| `torvalds/linux` | **5 false** | 1 (**true positive**) | 4 |
| `rust-lang/rust`, `python/cpython` | — | **0** | 4 |

The `torvalds/linux` line was checked before being counted: `.protected` is
`false` and `rulesets` is `[]`, so the branch genuinely is unprotected. The
false-negative vector the new `protected` discriminator could have introduced —
a branch protected by rulesets only — was tested against four repositories with
2 to 15 rulesets each, all reporting `protected=true`. **Anti-inversion holds**:
on administered repositories genuinely disabled controls are still accused
(3 accusations, 0 doubt), so the tri-state did not become the permanently closed
gate the Implementation Plan names as an abort criterion.

**Approved with coverage debt, and the debt was paid the same session.** The
Tester approved the unit while naming three defects that survived a green suite
when reintroduced by mutation — `T-1` no test asserted which URL is asked;
`T-2` nothing pinned the `permissions.admin` extraction, which is the whole of
`D1`; `T-3` `D6` was pinned for one classifier and not its twin. It approved
rather than blocked because all three concern a *future* regression and no path
was found, live or synthetic, where the shipped code answers wrongly — the gate
declining to be right by virtue of being a gate, the same discipline the author
showed rejecting `F-5`. Closed in `509f525` and verified by mutation: baseline
exit `0`, all three mutants exit `1`, restored exit `0`. **`T-1` is a coverage
*regression*, not an omission** — the URL used to live inside
`branch_protection_state` where its own test could see it, and `ca29010` moved
the fetch to the caller, out of every test's reach. Fixing `G-1` cost a test.

**Verification**: `make verify` exit `0` read from `$?` — **230 tests**, from
226 at `26367cf` (+1 for `G-1`'s pin, +3 for `T-1`/`T-2`/`T-3`). The live probe
reports no platform finding on this repository.

### `C3` + `C3.2` — the secret gate reads the formats credentials live in (`aa83309`…`5bcbdf6`, `50094c1`)

**Recorded here retrospectively, in session #4.** Session #3 delivered both units
and wrote their full account into `task_scope.md` without adding a section to
this log, so between `2026-08-18` and `2026-08-22` this file's status line read
*"5 of 13 units delivered; `C2` awaiting gate round 2"* while eight units were
delivered and `C2` was approved. That is drift in the artifact whose purpose is
to prevent it, and it is stated rather than quietly corrected.

Five Tester rounds, four rejections, one approval. `C3.2` was added mid-sprint at
the `remediation_workflow.md` Phase 0 halt, after three consecutive rejections of
the same logic block: a value-side test deciding whether a matched string is a
credential or a pointer at one. The conclusion, reached by the gate and ratified
by the human: **value shape cannot separate a pointer from a credential**,
because the same string is either one depending on what reads it. `C3.2` gives
the gate the allowlist affordance every production scanner ships, with a
mandatory reason printed at commit time — a silent bypass is how `RA-09` would be
defeated by the control built to enforce it. Full account, including the two
findings closed rather than routed in round 5, is in `task_scope.md`.

### `C4` — the official auditor could not run, and harmed the tree when it did (`5056796`)

Four rounds, three rejections. The roadmap named two defects; execution found a
third, and the unit committed a fourth against itself.

**Defect 1, the root.** `base_dir` climbed five `.parent` levels where four are
correct, so `manifest_skills.json` resolved one directory *above* the framework.
`agents.md §3 enforcement` calls this script the official auditor of the
Three-File Skill Standard; it could not run from the repository root or anywhere
else. It now adopts `agents_root()`, the `C0.3` anchor the roadmap already named
it for.

**Defect 2, the false green.** That failure path printed `ERROR: Manifest not
found …` and returned exit `0`. The same class as `C9` and `C10` — a control
reporting a determination it cannot support — this time telling every caller
that a run which never happened had succeeded.

**Defect 3, found only by running the repaired script.** `scripts/` was created
for **every** skill in the manifest, so the auditor violated the standard it
enforces: `agents.md §3` prohibits padding a knowledge skill with empty
scaffolding. Measured — the first run that reached this library wrote
`scripts/__init__.py` into **11** knowledge skills and a template `README.md`
into 9, reverted with `git clean`. It stayed invisible because defect 1 hid it.
`F-086-S3` reads *"the auditor does not generate a bad stub: it cannot run"*;
repairing the second clause is what exposed the first. **The sprint's governing
rule, read forward:** *reproduce before repairing* also means run it after, or a
defect that needs the fix in place to appear cannot be seen at all.

**Defect 4, committed by this unit against itself.** A root `SKILL.md` was
treated as a generated stub because it contained the template's `(Automatic
scaffolding)` sentence, and `skills/django-expert-3rd/SKILL.md` was deleted. It
also carried three authored directives, one of them the mandate `RA-02` states.
The QA gate found it with `git log -S`; nothing in the diff, the docstring or the
tests recorded the loss, and **the test written to forbid that deletion passed
only because its fixture avoided the case**. Restored byte-identical to HEAD. The
substring licence is replaced by byte-equality with the freshly rendered
template — the only shape proving nobody edited the file after this script wrote
it. On the single production sample the substring existed to judge, it was wrong
every time.

**`F-086-S3` is not closed, and no unit can close it.** The vendored 247-line
skill stays unreachable through that root, because the root file is legitimate
content. Deleting it is `agents.md §2 destructive_flags`; copying vendor content
into the framework tree is `rules/skills_and_integrations.md §3`. Both gates
ratified that reading independently. The condition is now printed as one `[!]`
line on every run instead of being latent, and the decision is the human's.

**Verification**: `make verify` exit `0` read from `$?` — **372 tests**, from 357
at `4a3c64a`. Against the pre-fix tree 14 of the 15 new tests fail; both gates
confirmed the suite also catches the destructive version above.

### Gate rounds — `C4`

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| **QA Agent** (dispatched) | 1 | **REJECTED** — the unit deleted hand-authored governance content; the abort criterion was a substring; the safety test certified an invariant the tree disproved; the tests were not hermetic |
| **Tester Agent** (dispatched) | 1 | **REJECTED** — `monkeypatch` died on `AttributeError` so defect 2 was never reproduced; no test observed the *process* exit code; the docstring recorded a discrimination count that measurement contradicted |
| **Tester Agent** | 2 | **APPROVED** — one advisory: the strong/weak split was 9/5 where measurement gave 8 strong, 5 `AttributeError`, 1 `OSError` |
| **QA Agent** | 2 | **REJECTED** — `RA-14`: three statements describing the corrected behaviour left standing in `README.md` ×2 and `SKILL.md` ×1 |
| **QA Agent** | 3 | **REJECTED** — `RA-14` again, one word: the table was corrected to 8 while the prose three lines below still read *nine* |
| **QA Agent** | 4 | **APPROVED** |
| **Tester Agent** | 3 | **APPROVED** — verdict re-confirmed on the tree as it stood after the documentation fixes, not carried forward |

Both gates were **dispatched as subagents**, on a per-unit lift the human granted
at session start. Every blocking finding above was raised by a gate and none was
reachable by the author: the deletion was found with `git log -S` against a file
the author had read and not registered, and the false count was found by
re-measuring rather than by re-reading. `C4` is the second unit of this sprint
where author and reviewer are distinct, and the one that would have shipped a
destructive regression without it.

### Gate rounds — `C9`, `C0`, `C0.2`, `C0.3`, `C1`

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| **QA Agent** (structural — `make verify`: reference integrity, determinism scan, manifest parity, absolute-path scan, step-map regeneration, README counts) | 1 | **PASSED**, exit `0` read from `$?` |
| **Tester Agent** (functional — `pytest tests/`, installer sandbox, nucleus self-bridge) | 1 | **PASSED** — 201 tests, no regressions against the 174 inherited |
| **Tester Agent**, `C0.3` regression | 2 | **REJECTED then PASSED** — the suite was green while a test destroyed a tracked config file. The rejection came from reading a diff, which is why `make verify` now asserts the tree is unchanged after the suite |

Both gates were applied by the lead session under the respective rulesets, not
dispatched as subagents. That is the declared deviation recorded below, and it
is stated here rather than left for a reader to infer from a green verdict.

## Suspended, not closed

`rules/token_economy.md §3.1` hard threshold: cycle 7 reached **16.5×** its
first turn against a bound of 15×. The rule is binding, the sprint is open, so
the session suspends. **This is the first time that bound has fired** since
Sprint 021 built it — recorded as `forced: true` with unfinished work in
`task_scope.md`, which is the calibration signal `§3.1` asks for rather than
one to infer later.

**The session resumed after compaction** and delivered `C0`. That does not erase
the record above: the bound fired, and the calibration `§3.1` asks for needs the
event kept, not tidied away once the work continued.

**A second session resumed the sprint on 2026-08-18** and delivered `C0.2`. The
resume worked off the record rather than the conversation, which is what Sprint
021's session bound was built for: `SUSPENDED` was read as a resume and not a
collision, and `IMPLEMENTATION_PLAN.md`, `task_scope.md` and `resume_pointer`
carried the state across the boundary.

## Suspended at the token bound, a second time

`rules/token_economy.md §3.1`: cycle 1 of session `50ce34a7` reached **15.1×**
its first turn against a bound of 15×. The rule is binding and the sprint is
open, so the session suspends. The first firing in this sprint was cycle 7 at
16.5×; two firings across two sessions of one sprint is the calibration signal
`§3.1` asks to be recorded rather than inferred later.

**Re-gating `C2` was deliberately left undone.** A verification performed on
exhausted context is the low-quality check the bound exists to prevent, and an
approval produced that way is worse than the absence it replaces.

**Next Phase, in order**: (1) re-gate `C2` — dispatch `qa_agent` and
`tester_agent` against `26367cf`, round 2; (2) `C3` (`env_shielding_auditor.py`
and `hooks/on_commit.py` — the secret-scanning suffix tuple and the three regex
alternations, preserving every existing false-positive exclusion, since that
hook already blocked a host once). Eight units remain; `task_scope.md` holds
per-unit status and the findings routed out of `C0`, `C0.2`, `C0.3`, `C1` and
this session's start, including three that no unit owns.
