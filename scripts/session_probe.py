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


def gh_json(*args: str) -> dict | list | None:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


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

    repo = gh_json("repo", "view", "--json", "nameWithOwner,description,homepageUrl")
    if repo is None:
        return None  # Not a GitHub remote, or unauthenticated: skip silently.
    slug = repo["nameWithOwner"]

    findings = []
    security = gh_json("api", f"repos/{slug}", "--jq", ".security_and_analysis") or {}
    for control in ("secret_scanning", "secret_scanning_push_protection",
                    "dependabot_security_updates"):
        if security.get(control, {}).get("status") != "enabled":
            findings.append(f"{control} disabled")

    if subprocess.run(["gh", "api", f"repos/{slug}/vulnerability-alerts"],
                      capture_output=True).returncode != 0:
        findings.append("Dependabot alerts off")
    if gh_json("api", f"repos/{slug}/branches/main/protection") is None:
        findings.append("main not protected")
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

    if not findings:
        return None
    return ("Platform controls not in the state `repository_hardening_workflow.md` "
            "mandates:\n   • " + "\n   • ".join(findings) +
            "\n   Propose: `/agents:harden` (it has an ordering that exists so it "
            "does not lock you out).")


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
