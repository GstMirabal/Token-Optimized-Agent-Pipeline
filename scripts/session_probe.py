"""Session-start readiness probes: graph freshness, documentation, platform.

These PROPOSE; they never execute. `revdoc` reads all of `docs/` and rewrites
contracts in place, and `harden` flips platform controls that can lock you out
of your own repository — both are irreversible enough that `agents.md §2
triple_lock` requires human authorization. A probe that fired on its own would
turn a one-file session into a documentation re-engineering, or a review into a
branch-protection lockout.

Every probe carries a way to stop repeating itself, because that is the
difference between a check and background noise:
  * the platform probe caches for 7 days (`last_platform_probe`) — repository
    configuration changes a couple of times a year, not once a session;
  * any probe can be acknowledged (`acknowledged_gaps` in the anchor) when the
    human has seen the gap and accepted it.

Without those, this probe would fire on every start against this very
repository, which has no `docs/decisions/` and no Blueprints. A proposal that
repeats with no way to answer it is a proposal people learn to skip.

invoked_by: start_workflow.md#readiness_probe and #platform_probe,
close_workflow.md#platform_recheck (with --force-platform).

Usage:
    python3 scripts/session_probe.py [--force-platform]

Exit codes:
    0 — nothing to propose
    1 — advisory findings printed (never 2: these do not block, RA-11)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_cost  # noqa: E402
from _mode import is_nucleus as _is_nucleus  # noqa: E402

HARD_RATIO = 15  # rules/token_economy.md §3.1

ACTIVE_STATE = Path("docs/active_state.json")
GRAPH = Path("graphify-out/graph.json")
PLATFORM_TTL_DAYS = 7
SOURCE_SUFFIXES = ("*.py", "*.js", "*.ts", "*.tsx", "*.go", "*.rs", "*.java")


def load_state() -> dict:
    if not ACTIVE_STATE.exists():
        return {}
    try:
        return json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def acknowledged(state: dict, key: str) -> str | None:
    return state.get("acknowledged_gaps", {}).get(key)


def is_nucleus() -> bool:
    """Whether this checkout is the framework repository itself.

    Delegates to `_mode.is_nucleus`, which two files answered independently
    before Sprint 025 extracted it (`rules/code_craft.md §1`: two call sites
    justify extraction).
    """
    return _is_nucleus()


# --- probes -----------------------------------------------------------

def probe_graph() -> str | None:
    """Is the knowledge graph older than the newest source commit?"""
    if not GRAPH.exists():
        return "No knowledge graph at graphify-out/. Propose: `graphify update .`"

    args = ["git", "log", "-1", "--format=%ct", "--"]
    args += [f"*{suffix[1:]}" for suffix in SOURCE_SUFFIXES]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        return None

    last_source_commit = int(result.stdout.strip())
    if GRAPH.stat().st_mtime < last_source_commit:
        behind = subprocess.run(
            ["git", "log", "--oneline", "--since", str(int(GRAPH.stat().st_mtime))],
            capture_output=True, text=True,
        ).stdout.count("\n")
        return (f"Knowledge graph is older than the latest source commit "
                f"({behind} commit(s) behind). Propose: `graphify update .`")
    return None


def probe_docs(state: dict) -> str | None:
    """Are the artifacts `rules/documentation_standard.md` mandates present?"""
    if acknowledged(state, "docs") is not None:
        return None

    missing = []
    if not Path("docs/decisions").is_dir():
        missing.append("docs/decisions/ (ADR log, documentation_standard.md §3)")
    if not any(Path("docs").rglob("*_BLUEPRINT.md")):
        missing.append("any *_BLUEPRINT.md (agents.md §0 requires one per module)")

    if not missing:
        return None

    scope = ("modules here are workflows, agents, skills and hooks"
             if is_nucleus() else "modules here are the host's applications")
    return ("Documentation artifacts absent — " + "; ".join(missing) +
            f".\n   Scope: {scope}."
            "\n   Propose: `/agents:revdoc`. If this gap is known and accepted, "
            "record it in `acknowledged_gaps.docs` in the anchor with a reason.")


def probe_anchor_sprint(state: dict) -> str | None:
    """Does the anchor name the sprint the checked-out branch is working?

    Opening a sprint updates neither field: `session_state.py claim` takes only
    a session id, so `current_sprint.id` is a hand edit with no gate. Found on
    the resume of Sprint 023 — the anchor still read `22` while `ai-sprint/023`
    and its sprint directory both existed, which is exactly what a cold session
    reads first and trusts.

    Compared against the BRANCH, not against the newest sprint directory. That
    other comparison looks equivalent and is not: measured on this repository,
    `docs/sprints/` holds `024` and `025` while `023` is legitimately in flight,
    so "a directory newer than the anchor" fires on a correct state. The branch
    is the sprint being worked, by `RA-12`.

    Args:
        state (dict): Parsed `docs/active_state.json`.

    Returns:
        str | None: The finding, or None when the two agree or nothing can be
            compared. A branch outside `ai-sprint/*` is not a mismatch — it is
            no evidence either way, and is reported as neither.
    """
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True)
    branch = result.stdout.strip()
    if result.returncode != 0 or not branch.startswith("ai-sprint/"):
        return None

    suffix = branch.split("/", 1)[1]
    if not suffix.isdigit():
        return None

    anchored = state.get("current_sprint", {}).get("id")
    if anchored is None or int(anchored) == int(suffix):
        return None

    return (f"Anchor names sprint {anchored} while the checked-out branch is `{branch}`. "
            "Opening a sprint writes neither field — no script does — so the anchor a cold "
            f"session reads first is behind the work.\n   Propose: set `current_sprint.id` "
            f"to {int(suffix)} in `docs/active_state.json` and refresh the mirror.")


# Three answers, because two cannot express doubt — the same shape `C9` gave
# branch integration. A security report is the last place where "I could not
# find out" may be rendered as "it is off".
ENABLED, DISABLED, UNDETERMINED, PAUSED = "enabled", "disabled", "undetermined", "paused"

# `gh` appends the status as `(HTTP nnn)`. Read it, never search stderr for the
# substring "404": measured with the real binary, a dead proxy on a repository
# whose NAME contains 404 emits `dial tcp … /repos/acme/tools404/… connection
# refused`, and a 503 body reading `upstream cache miss for /404/handler` comes
# back as `gh: upstream cache miss for /404/handler (HTTP 503)`. Both were
# classified as "the feature is off" by the substring test.
HTTP_STATUS_RE = re.compile(r"\(HTTP (\d{3})\)")


def gh_call(*args: str) -> tuple[int, str, str]:
    """Raw `gh` invocation.

    Args:
        *args: Arguments passed straight to `gh`.

    Returns:
        tuple[int, str, str]: return code, stdout, stderr.
    """
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def gh_json(*args: str) -> dict | list | None:
    rc, stdout, _ = gh_call(*args)
    if rc != 0:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def http_status(stderr: str) -> int | None:
    """The HTTP status `gh` reported, or None when it reported none.

    Args:
        stderr (str): `gh` standard error.

    Returns:
        int | None: The status code, or None for a transport-level failure that
            never reached an HTTP response.
    """
    match = HTTP_STATUS_RE.search(stderr)
    return int(match.group(1)) if match else None


def state_from_exit(rc: int, stderr: str, is_admin: bool | None) -> str:
    """Classify an endpoint whose reachability is itself the answer.

    **A 404 means two different things, and only the caller's permission
    separates them.** For an administrator the endpoint exists and the feature
    is off. For everyone else GitHub answers 404 on an admin-only endpoint
    whether the feature is on or off — measured live against `cli/cli` and
    `torvalds/linux`, both demonstrably hardened, which answered 404 on all
    three probed endpoints for a non-admin token. Reading that as `disabled`
    told a hardened repository it was exposed and offered to patch a repository
    the caller cannot administer.

    Args:
        rc (int): `gh` exit code.
        stderr (str): `gh` standard error, carrying the `(HTTP nnn)` status.
        is_admin (bool | None): Whether the token administers this repository.
            None when that could not be established, which is itself doubt.

    Returns:
        str: `ENABLED`, `DISABLED` or `UNDETERMINED`.
    """
    if rc == 0:
        return ENABLED
    if http_status(stderr) == 404 and is_admin is True:
        return DISABLED
    return UNDETERMINED


def undetermined_cause(rc: int, stderr: str, is_admin: bool | None) -> str:
    """Why an endpoint check could not be answered, measured rather than assumed.

    Args:
        rc (int): `gh` exit code.
        stderr (str): `gh` standard error.
        is_admin (bool | None): Whether the token administers this repository.

    Returns:
        str: A short cause. Every doubt line used to read "field not returned"
            regardless of what actually happened — the same defect one level
            down, inside the unit written to remove it.
    """
    status = http_status(stderr)
    if status == 404 and is_admin is not True:
        return "admin-only endpoint, and this token does not administer the repository"
    if status is not None:
        return f"HTTP {status}"
    return f"no HTTP response (rc={rc})"


def dependabot_updates_state(slug: str, is_admin: bool | None) -> str:
    """Whether Dependabot security updates are on, from the endpoint that says so.

    `automated-security-fixes` is the only endpoint carrying `paused`, which
    `security_and_analysis` cannot express — verified against the live API, it
    returns `{"enabled": true, "paused": false}`.

    Args:
        slug (str): `owner/name` of the repository.
        is_admin (bool | None): Whether the token administers this repository.

    Returns:
        str: `ENABLED`, `PAUSED`, `DISABLED` or `UNDETERMINED`. A body without a
            boolean `enabled` is `UNDETERMINED`, never `DISABLED`: absence is
            treated the same way here as in `analysis_state`, and it was not —
            one unit held two opposite rules for a missing field, and the branch
            that failed was the security one.
    """
    rc, stdout, stderr = gh_call("api", f"repos/{slug}/automated-security-fixes")
    if rc != 0:
        return state_from_exit(rc, stderr, is_admin)
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return UNDETERMINED
    if not isinstance(data, dict) or not isinstance(data.get("enabled"), bool):
        return UNDETERMINED
    if data["enabled"] is not True:
        return DISABLED
    return PAUSED if data.get("paused") is True else ENABLED


def branch_protection_state(slug: str, branch: str, is_admin: bool | None) -> str:
    """Whether a branch is protected, read from the field a non-admin can see.

    `branches/{branch}/protection` is admin-only and answers 404 to everyone
    else, so asking it alone cannot tell an unprotected branch from an
    unprivileged caller. `branches/{branch}` carries a public `protected`
    boolean — measured on `cli/cli` with a non-admin token, `.protected` is
    `true` while `.../protection` returns 404.

    Args:
        slug (str): `owner/name` of the repository.
        branch (str): Branch name. Slashes are not escaped, verified: GitHub
            routes `branches/ai-sprint/023` unencoded.
        is_admin (bool | None): Whether the token administers this repository.

    Returns:
        str: `ENABLED`, `DISABLED` or `UNDETERMINED`.
    """
    rc, stdout, stderr = gh_call("api", f"repos/{slug}/branches/{branch}")
    if rc != 0:
        return state_from_exit(rc, stderr, is_admin)
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return UNDETERMINED
    if not isinstance(data, dict) or not isinstance(data.get("protected"), bool):
        return UNDETERMINED
    return ENABLED if data["protected"] else DISABLED


def analysis_state(security: dict | None, control: str) -> str:
    """One `security_and_analysis` control, with absence kept distinct from off.

    Args:
        security (dict | None): The `security_and_analysis` object, or None when
            the call did not answer.
        control (str): Control key, e.g. `secret_scanning`.

    Returns:
        str: `ENABLED`, `DISABLED` or `UNDETERMINED`. Only an explicit
            `"disabled"` is reported as off. A key that is absent, a value that
            is not an object, or a `status` that is missing or unrecognised are
            all `UNDETERMINED` — the two-value collapse this function was
            written to remove had merely moved one level in. Safe because a
            genuinely-off control is stated explicitly: this repository's live
            payload returns `secret_scanning_validity_checks: disabled` in full.
    """
    if not isinstance(security, dict) or control not in security:
        return UNDETERMINED
    entry = security[control]
    if not isinstance(entry, dict):
        return UNDETERMINED
    status = entry.get("status")
    if status == "enabled":
        return ENABLED
    return DISABLED if status == "disabled" else UNDETERMINED


def collect_security_controls(slug: str, security: dict | None,
                              is_admin: bool | None, branch: str | None) -> tuple[list[str], list[str]]:
    """Interrogate every platform security control, sorting answers from doubt.

    Args:
        slug (str): `owner/name` of the repository.
        security (dict | None): The repository's `security_and_analysis` object.
        is_admin (bool | None): Whether the token administers this repository.
        branch (str | None): Default branch name, or None if none was reported.

    Returns:
        tuple[list[str], list[str]]: (findings, undetermined). A control is
            named in exactly one of them, and never in both.
    """
    findings: list[str] = []
    undetermined: list[str] = []

    def record(control: str, control_state: str, off_text: str, cause: str) -> None:
        """File one control under the heading its state actually warrants."""
        if control_state == DISABLED:
            findings.append(off_text)
        elif control_state == PAUSED:
            findings.append(f"{control} enabled but PAUSED — no updates are being applied")
        elif control_state == UNDETERMINED:
            undetermined.append(f"{control} — cannot determine ({cause})")

    for control in ("secret_scanning", "secret_scanning_push_protection"):
        record(control, analysis_state(security, control), f"{control} disabled",
               "field not returned" if security is not None
               else "the repository payload did not answer")

    rc, _, err = gh_call("api", f"repos/{slug}/automated-security-fixes")
    record("dependabot_security_updates", dependabot_updates_state(slug, is_admin),
           "dependabot_security_updates disabled", undetermined_cause(rc, err, is_admin))

    rc, _, err = gh_call("api", f"repos/{slug}/vulnerability-alerts")
    record("Dependabot alerts", state_from_exit(rc, err, is_admin),
           "Dependabot alerts off", undetermined_cause(rc, err, is_admin))

    # The default branch is asked for, not assumed to be `main`: on a repository
    # that never had one, the old check reported "main not protected" forever
    # while the branch that IS protected went uninspected.
    if not branch:
        undetermined.append("branch protection — cannot determine (no default branch reported)")
    else:
        rc, _, err = gh_call("api", f"repos/{slug}/branches/{branch}")
        record(f"{branch} protection", branch_protection_state(slug, branch, is_admin),
               f"{branch} not protected", undetermined_cause(rc, err, is_admin))

    return findings, undetermined


def collect_repo_hygiene(repo: dict) -> list[str]:
    """Repository metadata and community files, all of which are simply present or not.

    Args:
        repo (dict): The `gh repo view` payload.

    Returns:
        list[str]: Findings. No doubt bucket: these are read from a payload
            already in hand or from the working tree, so there is nothing here
            that can fail to answer.
    """
    findings = []
    if not repo.get("description"):
        findings.append("no description")
    if not repo.get("homepageUrl"):
        findings.append("no homepage")

    # Community files are checked against the TREE, never against
    # `community/profile`: that endpoint reports issue_template as null whenever
    # templates live in a directory, which is the current form — this repository
    # ships three and still scores null at 100% health.
    for name in ("CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"):
        if not Path(name).exists():
            findings.append(f"{name} missing")
    if not Path(".github/ISSUE_TEMPLATE").is_dir() and not Path(".github/ISSUE_TEMPLATE.md").exists():
        findings.append("no issue templates")
    return findings


def platform_report(findings: list[str], undetermined: list[str]) -> str | None:
    """Render the two buckets as two separately-remediable blocks.

    Args:
        findings (list[str]): Controls measured to be in the wrong state.
        undetermined (list[str]): Questions this probe could not answer.

    Returns:
        str | None: The report, or None when there is nothing to say.
    """
    if not findings and not undetermined:
        return None

    report = []
    if findings:
        report.append("Platform controls not in the state "
                      "`repository_hardening_workflow.md` mandates:\n   • "
                      + "\n   • ".join(findings) +
                      "\n   Propose: `/agents:harden` (it has an ordering that exists "
                      "so it does not lock you out).")
    if undetermined:
        # Reported apart from the accusations above, and with a different
        # remedy, because the two are different problems: a disabled control
        # needs turning on, an unanswered question needs a token that can see
        # the answer. GitHub answers 404 on admin-only endpoints to any caller
        # without administrative access, and reading that as "disabled" told
        # `cli/cli` and `torvalds/linux` — both hardened — that they were exposed.
        report.append("Platform controls this probe could NOT determine — "
                      "not a finding, an unanswered question:\n   • "
                      + "\n   • ".join(undetermined) +
                      "\n   Check `gh auth status` and whether the token administers this "
                      "repository. Re-run before treating any of these as disabled.")
    return "\n\n • ".join(report)


def probe_platform(state: dict, force: bool) -> str | None:
    """Are the controls `repository_hardening_workflow.md` mandates enabled?"""
    if acknowledged(state, "platform") is not None:
        return None
    if not shutil.which("gh"):
        return None  # No GitHub CLI: skip silently, not every host has one.

    if not force:
        last = state.get("last_platform_probe")
        if last:
            try:
                seen = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) - seen < timedelta(days=PLATFORM_TTL_DAYS):
                    return None
            except ValueError:
                pass

    repo = gh_json("repo", "view", "--json",
                   "nameWithOwner,description,homepageUrl,defaultBranchRef")
    if not isinstance(repo, dict):
        return None  # Not a GitHub remote, or unauthenticated: skip silently.
    slug = repo["nameWithOwner"]

    # One call carries both the permission that interprets every 404 below and
    # the controls themselves. `permissions.admin` is readable without admin —
    # measured: true here, false on `cli/cli` and `torvalds/linux`.
    detail = gh_json("api", f"repos/{slug}")
    detail = detail if isinstance(detail, dict) else {}
    is_admin = (detail.get("permissions") or {}).get("admin")
    security = detail.get("security_and_analysis")
    branch = (repo.get("defaultBranchRef") or {}).get("name")

    findings, undetermined = collect_security_controls(
        slug, security if isinstance(security, dict) else None, is_admin, branch)
    findings += collect_repo_hygiene(repo)
    return platform_report(findings, undetermined)


def probe_cost(state: dict) -> str | None:
    """Report what the previous session spent, and whether any cycle broke the bound.

    `rules/token_economy.md §3.1` makes the session bound binding because
    `session_cost.py` reads spend from the transcript rather than asking an agent
    to estimate it. This is where a human sees the previous session's shape
    before deciding how much to take on in this one.

    Advisory, like every probe: it proposes and never executes. A cycle over the
    hard threshold is a fact about a session that already ended — acting on it is
    a decision about the one starting.

    Args:
        state: the parsed anchor, for `acknowledged_gaps`.

    Returns:
        str | None: the finding, or None when clean or unmeasurable.
    """
    if (note := acknowledged(state, "cost")):
        return None
    try:
        result = session_cost.measure_previous(Path.cwd())
    except Exception:
        # A probe that crashes on a malformed transcript would block every start.
        return None
    if result is None or not result.get("measurable"):
        return None

    breaches = [(n, c) for n, c in enumerate(result["cycles"], 1)
                if (c["ratio"] or 0) > HARD_RATIO]
    if not breaches:
        return None
    worst = max(breaches, key=lambda pair: pair[1]["ratio"])
    return (
        f"Previous session ({result['session'][:8]}) had {len(breaches)} context "
        f"cycle(s) past the hard bound of {HARD_RATIO}x — worst was cycle "
        f"{worst[0]} at {worst[1]['ratio']}x its first turn "
        f"({worst[1]['peak']:,} tokens). Cost is the area under the sawtooth, and "
        f"compaction resets the axis without reducing it "
        f"(`rules/token_economy.md §3.1`). Reproduce: "
        f"`python3 .agents/scripts/session_cost.py --session {result['session']}`."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--force-platform", action="store_true",
                        help="Ignore the 7-day cache (session close invalidates it).")
    args = parser.parse_args()

    state = load_state()
    findings = [f for f in (probe_graph(),
                            probe_anchor_sprint(state),
                            probe_docs(state),
                            probe_platform(state, args.force_platform),
                            probe_cost(state)) if f]

    if not findings:
        print("✅ Readiness probes clean — graph current, documentation present, platform configured.")
        return 0

    print("⚠️  Readiness findings (advisory — nothing is executed automatically):")
    for finding in findings:
        print(f"\n • {finding}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
