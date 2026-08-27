"""Claim and release the session lock in docs/active_state.json.

Until Phase 019, `start_workflow.md` was the only workflow that wrote nothing:
all nine of its steps read or verified. `close_workflow.md` had `state_sync`;
`start` had no counterpart, so `session_id` in the anchor was always the *last
closed* session's, never the running one.

The consequence was not cosmetic. `start_workflow.md` Phase 1 promised to
"abort if IN_PROGRESS exists with a different session UID (crash forensics)",
but nothing anywhere ever wrote that state — `grep -rn IN_PROGRESS` over the
Python and workflow corpus returned zero writes. The collision guard could
never fire, and an abandoned session was indistinguishable from a clean one.

Claiming the lock and recording the session are the same act, so they are one
command rather than two steps that both rewrite the same file.

invoked_by: start_workflow.md#state_claim (claim), close_workflow.md#state_sync
(release), rules/token_economy.md#3.1 (suspend, at the hard threshold),
deployment_workflow.md#sprint_seal_gate (require-released),
deployment_workflow.md#baseline_refresh (refresh-baseline).

Usage:
    python3 scripts/session_state.py claim [--session-id <uid>] [--takeover]
        [--tool claude-code|cursor|terminal] [--delegation-mode native|sequential]
        # --session-id is generated (see generate_session_id()) when the
        # harness exposes none, e.g. Cursor.
        # --delegation-mode defaults: cursor→sequential, others→native.
    python3 scripts/session_state.py release   # seals the SPRINT (sprint-branch tip)
    python3 scripts/session_state.py suspend   # ends the SESSION only
    python3 scripts/session_state.py require-released [--branch <ref>]
        # deployment preflight: refuse SUSPENDED; tip must equal last_close_commit
    python3 scripts/session_state.py refresh-baseline [--sha HEX]
        # post-deploy: set last_close_commit to the integrated tip (default HEAD)

Exit codes:
    0 — lock claimed or released, or deploy preflight passed, or baseline refreshed
    2 — a different session holds the lock, or deploy refused (RA-11: only 2 blocks)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from hooks.state_mirror import mirror_active_state  # noqa: E402

ACTIVE_STATE = Path("docs/active_state.json")
IN_PROGRESS = "IN_PROGRESS"
CLOSED = "CLOSED_SUCCESSFULLY"
SUSPENDED = "SUSPENDED"  # session ended, sprint still open (token_economy.md §3.1)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_session_id() -> str:
    """Mint a UID for a caller that supplies none (`--session-id` omitted).

    Form: `<compact UTC ISO-8601>-<PID>`, e.g. `20260824T094910Z-48213`.
    The collision guard in `claim()` compares UIDs as opaque strings, never
    their provenance, so any unique string satisfies it — `uuid4()` was
    rejected in favor of this form because a timestamp with a PID is legible
    in forensics without a tool.

    Returns:
        str: the generated UID.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{os.getpid()}"


def head_sha() -> str | None:
    """Current commit, or None outside a repository."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def load_state() -> dict:
    if not ACTIVE_STATE.exists():
        return {}
    return json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    ACTIVE_STATE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    mirror_active_state()


def resume_pointer() -> dict:
    """Where a resuming session picks up.

    Degraded on purpose, and declared: the durable form derives the last
    completed phase from `config/artifact_registry.json`, which Sprint 023
    `C0.2` builds. Until then this records the branch and its last commit, which
    is real but coarser. Faking the richer form would be worse than saying so.
    """
    return {"branch": git_branch(), "at": head_sha(), "derived_from": "git (registry pending C0.2)"}


def git_branch() -> str | None:
    """The checked-out branch, or None on a detached HEAD."""
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def derive_delegation_mode(tool: str, explicit_mode: str | None) -> str:
    """Determine the delegation mode from tool and explicit argument.

    Args:
        tool: The tool claiming the lock (`claude-code`, `cursor`, or `terminal`).
        explicit_mode: Explicit `--delegation-mode` value, or None.

    Returns:
        str: `native` or `sequential`.
    """
    if explicit_mode is not None:
        return explicit_mode
    return "sequential" if tool == "cursor" else "native"


def suspend() -> int:
    """End the session without sealing the sprint.

    The counterpart `release()` did not have. `rules/token_economy.md §3.1` makes
    the session bound binding per context cycle, so a sprint can now be cut
    mid-flight — and the protocol needs an exit for that which does not lie.

    **It deliberately does not write `last_close_commit`.** That field means "the
    commit where the last close sealed"; writing it here would set a false
    baseline and `detect_drift.py` would treat everything after as conformant,
    blinding the detector Sprint 024 repaired.

    Returns:
        int: 0 — suspending is never refused; the work is preserved, not judged.
    """
    state = load_state()
    state.update({
        "status": SUSPENDED,
        "end_time": now(),
        "last_updated": now(),
        "resume_pointer": resume_pointer(),
    })
    save_state(state)
    pointer = state["resume_pointer"]
    print(f"⏸️  Session suspended — the sprint stays open. Resume on "
          f"{pointer['branch']} at {(pointer['at'] or '?')[:7]}.")
    print("   `last_close_commit` deliberately untouched: only a sprint close seals it.")
    return 0


def claim(session_id: str | None, takeover: bool, tool: str, delegation_mode: str | None = None) -> int:
    """Record this session as the holder of the lock.

    Args:
        session_id: UID of the session claiming the lock. Some harnesses
            (Cursor) expose no session UID to the caller; when this arrives
            `None`, `generate_session_id()` mints one so the claim can still
            proceed.
        takeover: Seize a lock held by another session (crash recovery).
        tool: Which harness is claiming the lock — `claude-code`, `cursor`,
            or `terminal`. Recorded as `session_tool` alongside `session_id`
            so forensics can tell which tool left a session open.
        delegation_mode: Execution mode — `native` (8 roles) or `sequential`
            (manual). When None, derived from tool: `cursor` → `sequential`,
            others → `native`.

    Returns:
        int: 0 when claimed, 2 when another live session holds the lock.
    """
    if session_id is None:
        session_id = generate_session_id()

    state = load_state()
    holder = state.get("session_id")

    if state.get("status") == IN_PROGRESS and holder and holder != session_id and not takeover:
        # Deliberately not auto-seized: a second agent running concurrently and
        # a session that died mid-flight look identical from here, and only one
        # of them is safe to overwrite. The human decides which this is.
        print(
            f"❌ Session lock held by {holder}, still IN_PROGRESS.\n"
            f"   If that session crashed, re-run with --takeover.\n"
            f"   If it is still running, do not: two sessions writing one anchor "
            f"is the collision this guard exists to prevent.",
            file=sys.stderr,
        )
        return 2

    resuming = state.get("status") == SUSPENDED
    # The collision guard above already lets SUSPENDED through: it blocks only on
    # IN_PROGRESS. What was missing is that nothing ever wrote this state, and
    # that resuming left no trace — so a sprint spanning sessions was invisible.
    resolved_mode = derive_delegation_mode(tool, delegation_mode)
    state.update({
        "session_id": session_id,
        "session_tool": tool,
        "delegation_mode": resolved_mode,
        "status": IN_PROGRESS,
        "start_time": now(),
        "last_updated": now(),
        "session_count": state.get("session_count", 0) + 1,
    })
    state.pop("end_time", None)
    save_state(state)

    if resuming:
        pointer = state.get("resume_pointer") or {}
        print(f"▶️  Resuming a suspended sprint (session #{state['session_count']}) — "
              f"{pointer.get('branch', 'unknown branch')} at "
              f"{(pointer.get('at') or '?')[:7]}.")
        print("   Read the Implementation Plan and `task_scope.md` before new work: "
              "the conversation did not survive, the record did.")
    else:
        print(f"✅ Session lock claimed by {session_id}.")
    return 0


def release() -> int:
    """Release the lock and record the commit the close sealed at.

    Clears ``resume_pointer`` so the next ``/start`` on ``main`` does not
    advisory-flag a closed sprint's branch (Sprint 040 R1). Mid-sprint
    ``claim`` still must not auto-clear resume (Sprint 039 D-P1).
    """
    state = load_state()
    state.update({
        "status": CLOSED,
        "end_time": now(),
        "last_updated": now(),
    })
    state["resume_pointer"] = {}
    sha = head_sha()
    if sha:
        # Sprint-branch tip for require-released. Squash-merge orphans this SHA
        # from main; deployment_workflow baseline_refresh rewrites it to the
        # integrated tip (Sprint 039). Without any baseline, drift is
        # undetectable — which is how five merged PRs reached main with no
        # ledger entry (Phase 018).
        state["last_close_commit"] = sha
    save_state(state)
    print(f"✅ Session lock released{f' at {sha[:7]}' if sha else ''}.")
    return 0


def refresh_baseline(sha: str | None = None) -> int:
    """Rewrite ``last_close_commit`` to the post-deploy integration tip.

    ``release`` seals the sprint-branch tip so ``require-released`` can gate
    deploy. After squash-merge onto ``main``, that SHA is no longer an ancestor
    of HEAD — ADR-0002 substitutes merge-base and warns forever. This command
    is the refresh ADR-0002 named: call it from ``deployment_workflow`` after
    the squash tip is checked out, with default SHA = ``HEAD``.

    Does **not** change ``status`` (deploy may run while a later session has
    already claimed).

    Args:
        sha: Full or abbreviated commit to record. Defaults to ``HEAD``.

    Returns:
        int: 0 on success; 2 when the SHA cannot be resolved (RA-11).
    """
    target = sha or head_sha()
    if not target:
        print("Refusing refresh-baseline: cannot resolve HEAD.")
        return 2
    resolved = rev_parse(target)
    if resolved is None:
        print(f"Refusing refresh-baseline: cannot resolve `{target}`.")
        return 2
    state = load_state()
    state["last_close_commit"] = resolved
    state["last_updated"] = now()
    save_state(state)
    print(f"✅ Baseline refreshed to {resolved[:7]} (integration tip).")
    return 0


def rev_parse(ref: str) -> str | None:
    """Resolve a git ref to a full SHA, or None if missing."""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", ref],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def require_released(branch: str | None = None) -> int:
    """Refuse `/agents:deployment` unless the tip is exactly what close sealed.

    A session that ends in ``SUSPENDED`` leaves the sprint open — deploying
    that work would publish an unsealed sprint. ``IN_PROGRESS`` on a tip that
    is not ``last_close_commit`` is the same defect. After ``release``, the
    sealed SHA equals the sprint-branch tip; deployment merges that tip.
    Passing ``--branch ai-sprint/[ID]`` allows deploying a sealed branch while
    a later session has already ``claim``ed another tip.

    Args:
        branch: Git ref whose tip must equal ``last_close_commit``. Defaults
            to ``HEAD``.

    Returns:
        int: 0 when deployable; 2 when refused (RA-11).
    """
    state = load_state()
    status = state.get("status")
    if status == SUSPENDED:
        print(
            "Refusing deploy: status is SUSPENDED — the sprint is still open. "
            "Resume with `session_state.py claim`, or finish and `/agents:close`. "
            "Never invoke `/agents:deployment` after a suspend."
        )
        return 2

    seal = state.get("last_close_commit")
    if not seal:
        print(
            "Refusing deploy: no `last_close_commit` — no sprint has been sealed "
            "with `release`. Run `/agents:close` first."
        )
        return 2

    ref = branch or "HEAD"
    tip = rev_parse(ref)
    if tip is None:
        print(f"Refusing deploy: cannot resolve ref `{ref}`.")
        return 2
    if tip != seal:
        print(
            f"Refusing deploy: `{ref}` tip {tip[:7]} is not the sealed close "
            f"{seal[:7]}. Close seals HEAD; deployment merges that tip. "
            "If a newer session already claimed another branch, pass "
            "`--branch ai-sprint/[ID]` for the sealed sprint."
        )
        return 2

    print(
        f"✅ Deploy preflight passed — `{ref}` tip matches sealed close "
        f"{seal[:7]} (status={status})."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    claim_parser = sub.add_parser("claim", help="Record this session as lock holder.")
    claim_parser.add_argument(
        "--session-id", required=False, default=None,
        help="UID of the claiming session. Omit under harnesses (Cursor) "
             "that expose none; a UID is generated.",
    )
    claim_parser.add_argument(
        "--takeover", action="store_true",
        help="Seize a lock left behind by a crashed session.",
    )
    claim_parser.add_argument(
        "--tool", choices=["claude-code", "cursor", "terminal"], default="terminal",
        help="Harness claiming the lock, recorded as session_tool.",
    )
    claim_parser.add_argument(
        "--delegation-mode", choices=["native", "sequential"], default=None,
        help="Execution mode (native: 8 roles; sequential: manual). "
             "If omitted, derived from --tool: cursor→sequential, others→native.",
    )
    sub.add_parser("release", help="Seal the SPRINT at close.")
    sub.add_parser("suspend", help="End the SESSION with the sprint still open.")
    require_parser = sub.add_parser(
        "require-released",
        help="Deployment preflight: tip must equal last_close_commit; refuse SUSPENDED.",
    )
    require_parser.add_argument(
        "--branch",
        default=None,
        help="Ref to check (default: HEAD). Use ai-sprint/[ID] when HEAD moved on.",
    )
    refresh_parser = sub.add_parser(
        "refresh-baseline",
        help="Post-deploy: set last_close_commit to the integrated tip.",
    )
    refresh_parser.add_argument(
        "--sha",
        default=None,
        help="Commit to record (default: HEAD). Use after squash on main.",
    )

    args = parser.parse_args()
    if args.command == "claim":
        return claim(args.session_id, args.takeover, args.tool, args.delegation_mode)
    if args.command == "suspend":
        return suspend()
    if args.command == "require-released":
        return require_released(args.branch)
    if args.command == "refresh-baseline":
        return refresh_baseline(args.sha)
    return release()


if __name__ == "__main__":
    sys.exit(main())
