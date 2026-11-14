"""Deterministic sandbox probes: check that what is closed stays closed.

Re-runs measurements M7 (loopback TCP), M9 (Unix sockets), A1 (proxy CONNECT)
and B2 (sensitive-path openability) of
`docs/sprints/059-core-pipeline/HARNESS_MEASUREMENT.md` from inside the Claude
Code Bash sandbox, so a new CLI version (B9) can be compared against the
recorded state. It only observes: no attack, no escape attempt, no data sent to
a third party, no file content read, no byte sent over a socket.

Classification is fail-closed (`agents.md §1 fail_closed_claims`): a socket or
file case is observed `closed` only on EPERM or EACCES; success, ECONNREFUSED,
a timeout or any other errno is `open` (the sandbox did not stop the call). A
missing path is `absent`. A proxy case is `open` on 200 or 5xx, `closed` on a
4xx other than 407, and `not-measurable` on 407, an unset proxy variable or a
failure to reach the proxy. When the control A1-C is not `open`, every A1 case
is `not-measurable`. No environment value (proxy URL, userinfo, socket path) is
ever printed or logged.

invoked_by: Makefile target sandbox-probe (Sprint 059 unit S-15).

Usage:
    python3 -I scripts/sandbox_probe.py

Exit codes:
    0 - no case expected closed was open, and none was not measurable
    1 - at least one case expected closed was observed open (takes precedence)
    2 - not running under the sandbox (`SANDBOX_RUNTIME` unset), or a case
        expected closed was not measurable
"""

import argparse
import base64
import errno
import logging
import os
import socket
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit

LOGGER = logging.getLogger("sandbox_probe")

TIMEOUT_SECONDS = 3.0
CLOSED_ERRNOS = frozenset({errno.EPERM, errno.EACCES})

OPEN = "open"
CLOSED = "closed"
ABSENT = "absent"
NOT_MEASURABLE = "not-measurable"


@dataclass(frozen=True)
class Case:
    """One probe case.

    Attributes:
        case_id: Short identifier printed on the output line.
        source: Source measurement in HARNESS_MEASUREMENT.md.
        target: Printable target description (never an environment value).
        expected: `closed`, `known_open` or `control`.
        ki: Known-issue id for `known_open` cases, else empty.
        kind: Key into `PROBES`.
        arg: Probe argument (host, path, port, ...), kind-specific.
    """

    case_id: str
    source: str
    target: str
    expected: str
    ki: str
    kind: str
    arg: tuple[str, ...] = ()


@dataclass(frozen=True)
class Result:
    """Observation of one case: state plus an errno name or HTTP status."""

    observed: str
    detail: str = ""


@dataclass
class Env:
    """Injectable environment so tests can simulate every observation."""

    environ: Mapping[str, str]
    home: Path
    tcp_connect: Callable[..., socket.socket] = socket.create_connection
    sock_factory: Callable[..., socket.socket] = socket.socket
    opener: Callable[..., object] = open
    lister: Callable[[str], list[str]] = os.listdir
    extras: dict[str, str] = field(default_factory=dict)


CASES: tuple[Case, ...] = (
    Case("M7-1", "M7", "tcp 127.0.0.1:5432", "closed", "", "tcp", ("127.0.0.1", "5432")),
    Case("M7-2", "M7", "tcp [::1]:5432", "closed", "", "tcp", ("::1", "5432")),
    Case("M7-3", "M7", "tcp 127.0.0.1:6379", "closed", "", "tcp", ("127.0.0.1", "6379")),
    Case("M9-1", "M9", "unix bind+listen in tempdir", "closed", "", "unix_bind"),
    Case("M9-2", "M9", "unix ~/.docker/run/docker.sock", "closed", "", "unix_home", (".docker/run/docker.sock",)),
    Case("M9-3", "M9", "unix /var/run/docker.sock", "closed", "", "unix_abs", ("/var/run/docker.sock",)),
    Case("M9-4", "M9", "unix SSH_AUTH_SOCK", "closed", "", "unix_env", ("SSH_AUTH_SOCK",)),
    Case("A1-C", "A1 control", "connect api.github.com:443", "control", "", "proxy", ("api.github.com", "443")),
    Case("A1-1", "A1", "connect 127.0.0.1:5000", "known_open", "KI-059-20", "proxy", ("127.0.0.1", "5000")),
    Case("A1-2", "A1", "connect example.org:443", "known_open", "KI-059-19", "proxy", ("example.org", "443")),
    Case("B2-1", "B2", "file ~/.docker/config.json", "known_open", "KI-059-21", "file", (".docker/config.json",)),
    Case("B2-2", "B2", "file ~/.config/gh/hosts.yml", "known_open", "KI-059-21", "file", (".config/gh/hosts.yml",)),
    Case("B2-3", "B2", "file ~/.zsh_history", "known_open", "KI-059-21", "file", (".zsh_history",)),
    Case("B2-4", "B2", "file ~/Library/Keychains/login.keychain-db", "known_open", "KI-059-21", "file",
         ("Library/Keychains/login.keychain-db",)),
    Case("B2-5", "B2", "dir ~/.claude/projects", "known_open", "KI-059-21", "listdir", (".claude/projects",)),
)


def errno_name(code: int | None) -> str:
    """Return the symbolic errno name, or `ERR<n>` / `NOERRNO` when unknown.

    Args:
        code: The errno value of an `OSError`, possibly `None`.

    Returns:
        The name such as `EPERM`.
    """
    if code is None:
        return "NOERRNO"
    return errno.errorcode.get(code, f"ERR{code}")


def classify_oserror(exc: OSError) -> Result:
    """Classify an `OSError` from a socket or file call, fail-closed.

    Args:
        exc: The raised error.

    Returns:
        `closed` only for EPERM/EACCES, `absent` for ENOENT, else `open`.
    """
    code = exc.errno
    if isinstance(exc, TimeoutError):
        return Result(OPEN, "timeout")
    if code in CLOSED_ERRNOS:
        return Result(CLOSED, errno_name(code))
    if code == errno.ENOENT:
        return Result(ABSENT, errno_name(code))
    return Result(OPEN, errno_name(code))


def probe_tcp(env: Env, host: str, port: str) -> Result:
    """Connect directly (no proxy) to a loopback TCP port and close at once.

    Args:
        env: Injectable environment.
        host: Target host literal.
        port: Target port as text.

    Returns:
        The classified observation.
    """
    try:
        conn = env.tcp_connect((host, int(port)), timeout=TIMEOUT_SECONDS)
    except OSError as exc:
        return classify_oserror(exc)
    conn.close()
    return Result(OPEN, "connected")


def probe_unix_connect(env: Env, path: str) -> Result:
    """Connect to a Unix socket path, send nothing and close at once.

    Args:
        env: Injectable environment.
        path: Socket path (not printed).

    Returns:
        The classified observation.
    """
    sock = env.sock_factory(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.settimeout(TIMEOUT_SECONDS)
        sock.connect(path)
    except OSError as exc:
        return classify_oserror(exc)
    finally:
        sock.close()
    return Result(OPEN, "connected")


def probe_unix_bind(env: Env) -> Result:
    """Bind and listen on a fresh Unix socket inside a private temp dir.

    Args:
        env: Injectable environment.

    Returns:
        The classified observation; the temp dir is always removed.
    """
    tmp = tempfile.mkdtemp(prefix="sbprobe")
    sock = env.sock_factory(socket.AF_UNIX, socket.SOCK_STREAM)
    path = os.path.join(tmp, "p.sock")
    try:
        sock.bind(path)
        sock.listen(1)
    except OSError as exc:
        return classify_oserror(exc)
    finally:
        sock.close()
        if os.path.exists(path):
            os.unlink(path)
        os.rmdir(tmp)
    return Result(OPEN, "bound")


def probe_file(env: Env, path: Path) -> Result:
    """Open a file in binary mode and close it without reading a byte.

    Args:
        env: Injectable environment.
        path: File to open.

    Returns:
        The classified observation.
    """
    try:
        handle = env.opener(path, "rb")
    except OSError as exc:
        return classify_oserror(exc)
    handle.close()  # type: ignore[attr-defined]
    return Result(OPEN, "opened")


def probe_listdir(env: Env, path: Path) -> Result:
    """List a directory and discard the entries.

    Args:
        env: Injectable environment.
        path: Directory to list.

    Returns:
        The classified observation.
    """
    try:
        env.lister(str(path))
    except OSError as exc:
        return classify_oserror(exc)
    return Result(OPEN, "listed")


def parse_proxy(environ: Mapping[str, str]) -> tuple[str, int, str] | None:
    """Parse the HTTPS proxy variable into (host, port, auth header value).

    Args:
        environ: Environment mapping.

    Returns:
        `None` when unset or unparseable, else host, port and a possibly empty
        `Basic ...` credential string. Nothing is printed.
    """
    raw = environ.get("HTTPS_PROXY") or environ.get("https_proxy")
    if not raw:
        return None
    parts = urlsplit(raw)
    if not parts.hostname or not parts.port:
        return None
    auth = ""
    if parts.username is not None:
        userinfo = f"{unquote(parts.username)}:{unquote(parts.password or '')}"
        auth = "Basic " + base64.b64encode(userinfo.encode()).decode()
    return parts.hostname, parts.port, auth


def read_status(sock: socket.socket) -> int | None:
    """Read only the HTTP status line from a socket.

    Args:
        sock: Connected socket that has sent a request.

    Returns:
        The numeric status code, or `None` when the line is malformed.
    """
    data = b""
    while b"\r\n" not in data and len(data) < 512:
        chunk = sock.recv(256)
        if not chunk:
            break
        data += chunk
    fields = data.split(b"\r\n", 1)[0].split()
    if len(fields) >= 2 and fields[1].isdigit():
        return int(fields[1])
    return None


def classify_status(status: int | None) -> Result:
    """Map a proxy CONNECT status to an observation.

    Args:
        status: HTTP status code or `None`.

    Returns:
        `open` for 200 and 5xx, `closed` for 4xx other than 407, else
        `not-measurable`.
    """
    if status is None or status == 407:
        return Result(NOT_MEASURABLE, str(status))
    if status == 200 or 500 <= status < 600:
        return Result(OPEN, str(status))
    if 400 <= status < 500:
        return Result(CLOSED, str(status))
    return Result(NOT_MEASURABLE, str(status))


def probe_proxy(env: Env, host: str, port: str) -> Result:
    """Issue one HTTP CONNECT through the proxy and read the status line.

    Args:
        env: Injectable environment.
        host: Target host of the CONNECT.
        port: Target port of the CONNECT, as text.

    Returns:
        The classified observation; `not-measurable` when the proxy variable is
        unset or the proxy cannot be reached.
    """
    proxy = parse_proxy(env.environ)
    if proxy is None:
        return Result(NOT_MEASURABLE, "no-proxy")
    try:
        sock = env.tcp_connect((proxy[0], proxy[1]), timeout=TIMEOUT_SECONDS)
    except OSError:
        return Result(NOT_MEASURABLE, "proxy-unreachable")
    target = f"{host}:{port}"
    lines = [f"CONNECT {target} HTTP/1.1", f"Host: {target}"]
    if proxy[2]:
        lines.append(f"Proxy-Authorization: {proxy[2]}")
    try:
        sock.settimeout(TIMEOUT_SECONDS)
        sock.sendall(("\r\n".join(lines) + "\r\n\r\n").encode())
        return classify_status(read_status(sock))
    except OSError:
        return Result(NOT_MEASURABLE, "proxy-io-error")
    finally:
        sock.close()


def probe_unix_path(env: Env, case: Case) -> Result:
    """Probe a Unix-socket path resolved from the case kind.

    Args:
        env: Injectable environment.
        case: A `unix_home`, `unix_abs` or `unix_env` case.

    Returns:
        The observation; `absent` when `SSH_AUTH_SOCK` is unset.
    """
    if case.kind == "unix_home":
        return probe_unix_connect(env, str(env.home / case.arg[0]))
    if case.kind == "unix_abs":
        return probe_unix_connect(env, case.arg[0])
    value = env.environ.get(case.arg[0])
    if not value:
        return Result(ABSENT, "unset")
    return probe_unix_connect(env, value)


def run_probe(env: Env, case: Case) -> Result:
    """Dispatch a case to its probe function.

    Args:
        env: Injectable environment.
        case: The case to run.

    Returns:
        The observation.
    """
    if case.kind == "tcp":
        return probe_tcp(env, case.arg[0], case.arg[1])
    if case.kind == "unix_bind":
        return probe_unix_bind(env)
    if case.kind.startswith("unix_"):
        return probe_unix_path(env, case)
    if case.kind == "proxy":
        return probe_proxy(env, case.arg[0], case.arg[1])
    if case.kind == "file":
        return probe_file(env, env.home / case.arg[0])
    return probe_listdir(env, env.home / case.arg[0])


def run_case(env: Env, case: Case) -> Result:
    """Run one case behind a fault boundary.

    Args:
        env: Injectable environment.
        case: The case to run.

    Returns:
        The observation, or `not-measurable` on any unexpected exception (only
        the case id and exception type are logged).
    """
    try:
        return run_probe(env, case)
    except Exception as exc:  # noqa: BLE001 - one case must not stop the rest
        LOGGER.error("case %s raised %s", case.case_id, type(exc).__name__)
        return Result(NOT_MEASURABLE, "exception")


def classify(expected: str, observed: str, ki: str = "") -> str:
    """Pure verdict from the expectation and the observation.

    Args:
        expected: `closed`, `known_open` or `control`.
        observed: `closed`, `open`, `absent` or `not-measurable`.
        ki: Known-issue id for `known_open` cases.

    Returns:
        The verdict text.
    """
    if observed == NOT_MEASURABLE:
        return "NOT-MEASURABLE"
    if expected == "control":
        return "ok" if observed == OPEN else "NOT-MEASURABLE"
    if expected == "closed":
        return {CLOSED: "ok", ABSENT: "ok-absent"}.get(observed, "FAIL")
    tag = f" {ki}" if ki else ""
    if observed == CLOSED:
        return f"CLOSED{tag} may be resolved"
    return f"RECORD{tag}"


def exit_code(rows: list[tuple[str, str]]) -> int:
    """Compute the exit code from (expected, verdict) pairs.

    Args:
        rows: One pair per case.

    Returns:
        1 if a closed case is `FAIL`, else 2 if a closed case is
        `NOT-MEASURABLE`, else 0.
    """
    closed = [verdict for expected, verdict in rows if expected == "closed"]
    if "FAIL" in closed:
        return 1
    if "NOT-MEASURABLE" in closed:
        return 2
    return 0


def format_line(case: Case, result: Result, verdict: str) -> str:
    """Format one output line.

    Args:
        case: The case.
        result: Its observation.
        verdict: Its verdict.

    Returns:
        The line without trailing newline.
    """
    detail = f" [{result.detail}]" if result.detail else ""
    return (f"{case.case_id} {case.target} expected={case.expected} "
            f"observed={result.observed}{detail} verdict={verdict}")


def apply_control(case: Case, result: Result, control_open: bool) -> Result:
    """Override an A1 observation when the control did not reach its host.

    Args:
        case: The case just run.
        result: Its raw observation.
        control_open: Whether the A1 control was observed `open`.

    Returns:
        `not-measurable` for an A1 non-control case without an open control,
        else `result` unchanged.
    """
    if case.source == "A1" and case.expected != "control" and not control_open:
        return Result(NOT_MEASURABLE, "control-not-open")
    return result


def run_all(env: Env) -> tuple[list[str], list[tuple[str, str]]]:
    """Run every case in table order, applying the A1 control rule.

    Args:
        env: Injectable environment.

    Returns:
        The output lines and the (expected, verdict) pairs.
    """
    lines: list[str] = []
    rows: list[tuple[str, str]] = []
    control_open = True
    for case in CASES:
        result = apply_control(case, run_case(env, case), control_open)
        if case.expected == "control":
            control_open = result.observed == OPEN
        verdict = classify(case.expected, result.observed, case.ki)
        lines.append(format_line(case, result, verdict))
        rows.append((case.expected, verdict))
    return lines, rows


def summarize(rows: list[tuple[str, str]], code: int) -> str:
    """Build the summary line: count per verdict and the exit code.

    Args:
        rows: One (expected, verdict) pair per case.
        code: The exit code.

    Returns:
        The summary line.
    """
    counts: dict[str, int] = {}
    for _, verdict in rows:
        key = verdict.split(" ", 1)[0]
        counts[key] = counts.get(key, 0) + 1
    body = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    return f"summary: {body} exit={code}"


def main(argv: list[str] | None = None) -> int:
    """Run the probes and print the report.

    Args:
        argv: Optional argument list (only `--help` is accepted).

    Returns:
        The process exit code.
    """
    argparse.ArgumentParser(description="Sandbox closed-stays-closed probes.").parse_args(argv)
    logging.basicConfig(level=logging.ERROR, format="%(message)s", stream=sys.stderr)
    if "SANDBOX_RUNTIME" not in os.environ:
        print("sandbox_probe: not running under the sandbox (SANDBOX_RUNTIME unset); no probe run")
        return 2
    env = Env(environ=dict(os.environ), home=Path.home())
    print(f"sandbox_probe: cli={os.environ.get('AI_AGENT') or 'unknown'}")
    lines, rows = run_all(env)
    code = exit_code(rows)
    print("\n".join(lines))
    print(summarize(rows, code))
    return code


if __name__ == "__main__":
    sys.exit(main())
