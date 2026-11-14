"""Tests for scripts/sandbox_probe.py (Sprint 059 unit S-14).

The environment is fully simulated: no real socket, network, home file or proxy
is touched. Every parametrized list is derived from `CASES`, so a new case
cannot go untested.
"""

from __future__ import annotations

import base64
import errno
import importlib
import logging
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
probe = importlib.import_module("sandbox_probe")

SECRET = "s3cr3t-marker"
PROXY_HOST = "proxy.invalid"
PROXY_URL = f"http://user:{SECRET}@{PROXY_HOST}:3128"
LEAKS = (SECRET, "user:", PROXY_HOST)
EXPECTED_CASE_IDS = [case.case_id for case in probe.CASES]


class FakeSock:
    """Socket and file stand-in that records what is sent and never does I/O."""

    def __init__(
        self,
        sent: list[bytes],
        status: int = 200,
        connect_error: Exception | None = None,
        bind_error: Exception | None = None,
    ) -> None:
        """Store the scripted behavior.

        Args:
            sent: Shared list that receives every `sendall` payload.
            status: HTTP status returned on the first `recv`.
            connect_error: Raised by `connect` when set.
            bind_error: Raised by `bind` when set.
        """
        self.sent = sent
        self.status = status
        self.connect_error = connect_error
        self.bind_error = bind_error
        self.replied = False

    def settimeout(self, value: float) -> None:
        """Accept and ignore the timeout."""

    def connect(self, path: str) -> None:
        """Raise the scripted error or succeed."""
        if self.connect_error is not None:
            raise self.connect_error

    def bind(self, path: str) -> None:
        """Raise the scripted error or succeed."""
        if self.bind_error is not None:
            raise self.bind_error

    def listen(self, backlog: int) -> None:
        """Accept and ignore the backlog."""

    def sendall(self, data: bytes) -> None:
        """Record the payload."""
        self.sent.append(data)

    def recv(self, size: int) -> bytes:
        """Return the status line once, then end of stream."""
        if self.replied:
            return b""
        self.replied = True
        return f"HTTP/1.1 {self.status} X\r\n\r\n".encode()

    def close(self) -> None:
        """Accept and ignore the close."""


def eperm() -> PermissionError:
    """Return a fresh `PermissionError` carrying EPERM."""
    return PermissionError(errno.EPERM, "Operation not permitted")


def build_env(
    home: Path,
    sent: list[bytes],
    *,
    closed: bool,
    tcp_open: bool = False,
    bind_error: Exception | None = None,
    environ: dict[str, str] | None = None,
) -> object:
    """Build a fully faked `Env`.

    Args:
        home: Fake home directory (never read).
        sent: Shared list recording bytes sent to fake sockets.
        closed: True makes every probe hit EPERM (proxy returns 403); False
            makes every probe succeed (proxy returns 200).
        tcp_open: When closed, still let direct TCP connects succeed.
        bind_error: Overrides the error raised by a Unix `bind`.
        environ: Overrides the fake environment mapping.

    Returns:
        A `sandbox_probe.Env` whose callables are all fakes.
    """

    def tcp_connect(addr: tuple[str, int], timeout: float = 0.0) -> FakeSock:
        if addr[0] == PROXY_HOST:
            return FakeSock(sent, status=403 if closed else 200)
        if closed and not tcp_open:
            raise eperm()
        return FakeSock(sent)

    def sock_factory(*args: object) -> FakeSock:
        return FakeSock(
            sent,
            connect_error=eperm() if closed else None,
            bind_error=bind_error or (eperm() if closed else None),
        )

    def opener(path: object, mode: str = "r") -> FakeSock:
        if closed:
            raise eperm()
        return FakeSock(sent)

    def lister(path: str) -> list[str]:
        if closed:
            raise eperm()
        return []

    values = environ if environ is not None else {
        "HTTPS_PROXY": PROXY_URL,
        "SSH_AUTH_SOCK": "/fake/agent.sock",
    }
    return probe.Env(
        environ=values,
        home=home,
        tcp_connect=tcp_connect,
        sock_factory=sock_factory,
        opener=opener,
        lister=lister,
    )


@pytest.fixture(autouse=True)
def fake_tempdir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Route `probe_unix_bind`'s temp dir into pytest's tmp_path."""

    def mkdtemp(prefix: str = "") -> str:
        target = tmp_path / "bind"
        target.mkdir(exist_ok=True)
        return str(target)

    monkeypatch.setattr(probe.tempfile, "mkdtemp", mkdtemp)


@pytest.fixture()
def sent() -> list[bytes]:
    """Return the shared record of bytes sent to fake sockets."""
    return []


@pytest.fixture()
def make_env(tmp_path: Path, sent: list[bytes]) -> Callable[..., object]:
    """Return a builder of fake environments bound to this test's home."""

    def builder(**kwargs: object) -> object:
        return build_env(tmp_path / "home", sent, **kwargs)  # type: ignore[arg-type]

    return builder


def case_by_id(case_id: str) -> object:
    """Return the case with the given id."""
    return next(case for case in probe.CASES if case.case_id == case_id)


# 1. One test per case ------------------------------------------------------


def test_case_table_is_not_empty() -> None:
    """The parametrized lists below are only meaningful on a non-empty table."""
    assert EXPECTED_CASE_IDS
    assert len(set(EXPECTED_CASE_IDS)) == len(EXPECTED_CASE_IDS)


@pytest.mark.parametrize("case", probe.CASES, ids=EXPECTED_CASE_IDS)
def test_case_observed_closed_on_eperm_or_403(case: object, make_env: Callable[..., object]) -> None:
    """EPERM (or a proxy 403) is observed `closed` for every case."""
    result = probe.run_case(make_env(closed=True), case)
    assert result.observed == "closed", (case.case_id, result)


@pytest.mark.parametrize("case", probe.CASES, ids=EXPECTED_CASE_IDS)
def test_case_observed_open_on_success(case: object, make_env: Callable[..., object]) -> None:
    """A successful call (or a proxy 200) is observed `open` for every case."""
    result = probe.run_case(make_env(closed=False), case)
    assert result.observed == "open", (case.case_id, result)


# 2. Exit codes -------------------------------------------------------------


def test_exit_1_when_closed_case_is_open(make_env: Callable[..., object]) -> None:
    """M7-1 connecting is a FAIL and exits 1."""
    lines, rows = probe.run_all(make_env(closed=True, tcp_open=True))
    assert any(line.startswith("M7-1 ") and "verdict=FAIL" in line for line in lines)
    assert probe.exit_code(rows) == 1


def test_exit_1_takes_precedence_over_not_measurable(make_env: Callable[..., object]) -> None:
    """A FAIL and a NOT-MEASURABLE closed case in one run still exit 1."""
    env = make_env(closed=True, tcp_open=True, bind_error=RuntimeError("boom"))
    lines, rows = probe.run_all(env)
    verdicts = {line.split(" ", 1)[0]: line for line in lines}
    assert "verdict=FAIL" in verdicts["M7-1"]
    assert "verdict=NOT-MEASURABLE" in verdicts["M9-1"]
    assert probe.exit_code(rows) == 1


def test_exit_2_when_not_under_sandbox(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without SANDBOX_RUNTIME, main prints the line, exits 2 and probes nothing."""
    monkeypatch.delenv("SANDBOX_RUNTIME", raising=False)
    calls: list[str] = []

    def forbidden(*args: object, **kwargs: object) -> None:
        calls.append("called")
        raise AssertionError("a probe ran outside the sandbox")

    monkeypatch.setattr(probe, "run_all", forbidden)
    monkeypatch.setattr(probe, "run_case", forbidden)
    monkeypatch.setattr(probe, "run_probe", forbidden)
    monkeypatch.setattr(probe, "Env", forbidden)
    assert probe.main([]) == 2
    out = capsys.readouterr().out
    assert "not running under the sandbox" in out
    assert "no probe run" in out
    assert calls == []


def test_exit_2_when_closed_case_not_measurable(make_env: Callable[..., object]) -> None:
    """A closed case whose probe raises an unexpected exception exits 2."""
    env = make_env(closed=True, bind_error=RuntimeError("boom"))
    case = case_by_id("M9-1")
    result = probe.run_case(env, case)
    assert result.observed == "not-measurable"
    _, rows = probe.run_all(env)
    assert probe.exit_code(rows) == 2


def test_exit_0_when_everything_closed(make_env: Callable[..., object]) -> None:
    """A fully closed run exits 0."""
    _, rows = probe.run_all(make_env(closed=True))
    assert probe.exit_code(rows) == 0


@pytest.mark.parametrize(
    ("rows", "code"),
    [
        ([("closed", "ok")], 0),
        ([("closed", "ok-absent"), ("known_open", "RECORD")], 0),
        ([("known_open", "NOT-MEASURABLE")], 0),
        ([("closed", "NOT-MEASURABLE")], 2),
        ([("closed", "FAIL"), ("closed", "NOT-MEASURABLE")], 1),
    ],
)
def test_exit_code_table(rows: list[tuple[str, str]], code: int) -> None:
    """`exit_code` counts only rows expected `closed`."""
    assert probe.exit_code(rows) == code


# 3. Classification units ---------------------------------------------------


@pytest.mark.parametrize(
    ("exc", "observed"),
    [
        (PermissionError(errno.EPERM, "x"), "closed"),
        (PermissionError(errno.EACCES, "x"), "closed"),
        (FileNotFoundError(errno.ENOENT, "x"), "absent"),
        (ConnectionRefusedError(errno.ECONNREFUSED, "x"), "open"),
        (TimeoutError(), "open"),
        (OSError(errno.EIO, "x"), "open"),
    ],
)
def test_classify_oserror(exc: OSError, observed: str) -> None:
    """Only EPERM and EACCES are `closed`; ENOENT is `absent`; the rest `open`."""
    assert probe.classify_oserror(exc).observed == observed


@pytest.mark.parametrize(
    ("status", "observed"),
    [
        (200, "open"),
        (502, "open"),
        (403, "closed"),
        (404, "closed"),
        (407, "not-measurable"),
        (301, "not-measurable"),
        (None, "not-measurable"),
    ],
)
def test_classify_status(status: int | None, observed: str) -> None:
    """Proxy statuses map fail-closed to an observation."""
    assert probe.classify_status(status).observed == observed


@pytest.mark.parametrize(
    ("expected", "observed", "ki", "verdict"),
    [
        ("closed", "closed", "", "ok"),
        ("closed", "absent", "", "ok-absent"),
        ("closed", "open", "", "FAIL"),
        ("closed", "not-measurable", "", "NOT-MEASURABLE"),
        ("control", "open", "", "ok"),
        ("control", "closed", "", "NOT-MEASURABLE"),
        ("control", "absent", "", "NOT-MEASURABLE"),
        ("control", "not-measurable", "", "NOT-MEASURABLE"),
        ("known_open", "open", "KI-1", "RECORD KI-1"),
        ("known_open", "absent", "KI-1", "RECORD KI-1"),
        ("known_open", "open", "", "RECORD"),
        ("known_open", "closed", "KI-1", "CLOSED KI-1 may be resolved"),
        ("known_open", "closed", "", "CLOSED may be resolved"),
        ("known_open", "not-measurable", "KI-1", "NOT-MEASURABLE"),
    ],
)
def test_classify(expected: str, observed: str, ki: str, verdict: str) -> None:
    """`classify` returns the documented verdict for every handled pair."""
    assert probe.classify(expected, observed, ki) == verdict


def test_apply_control_turns_a1_not_measurable() -> None:
    """A1 non-control cases become not-measurable when the control is not open."""
    raw = probe.Result("open", "200")
    for case_id in ("A1-1", "A1-2"):
        result = probe.apply_control(case_by_id(case_id), raw, control_open=False)
        assert result.observed == "not-measurable"
        assert probe.apply_control(case_by_id(case_id), raw, control_open=True) is raw


def test_apply_control_leaves_control_and_other_sources() -> None:
    """The control itself and non-A1 cases are never overridden."""
    raw = probe.Result("closed", "EPERM")
    assert probe.apply_control(case_by_id("A1-C"), raw, control_open=False) is raw
    assert probe.apply_control(case_by_id("M7-1"), raw, control_open=False) is raw
    assert probe.apply_control(case_by_id("B2-1"), raw, control_open=False) is raw


def test_run_all_marks_a1_not_measurable_when_control_fails(
    tmp_path: Path, sent: list[bytes]
) -> None:
    """A proxy answering 407 to the control makes A1-1 and A1-2 not-measurable."""
    env = build_env(tmp_path, sent, closed=False)
    env.tcp_connect = lambda addr, timeout=0.0: (
        FakeSock(sent, status=407) if addr[0] == PROXY_HOST else FakeSock(sent)
    )
    lines, _ = probe.run_all(env)
    by_id = {line.split(" ", 1)[0]: line for line in lines}
    for case_id in ("A1-C", "A1-1", "A1-2"):
        assert "observed=not-measurable" in by_id[case_id]


# 5. parse_proxy ------------------------------------------------------------


def test_parse_proxy_unset_is_none() -> None:
    """No proxy variable yields None."""
    assert probe.parse_proxy({}) is None


def test_parse_proxy_missing_port_is_none() -> None:
    """A proxy URL without a port yields None."""
    assert probe.parse_proxy({"HTTPS_PROXY": "http://proxy.invalid"}) is None


def test_parse_proxy_reads_lowercase_and_credentials() -> None:
    """The lowercase variable is honored; userinfo becomes a Basic credential."""
    host, port, auth = probe.parse_proxy({"https_proxy": PROXY_URL})
    assert (host, port) == (PROXY_HOST, 3128)
    token = base64.b64encode(f"user:{SECRET}".encode()).decode()
    assert auth == f"Basic {token}"


def test_parse_proxy_without_userinfo_has_empty_auth() -> None:
    """A proxy URL without userinfo carries no credential."""
    assert probe.parse_proxy({"HTTPS_PROXY": "http://p.invalid:8080"}) == ("p.invalid", 8080, "")


def test_probe_proxy_unset_is_not_measurable(make_env: Callable[..., object]) -> None:
    """With no proxy variable the proxy probe is not-measurable."""
    env = make_env(closed=False, environ={})
    assert probe.run_case(env, case_by_id("A1-C")).observed == "not-measurable"


# 4. Secret hygiene ---------------------------------------------------------


def assert_no_leak(text: str) -> None:
    """Fail when any secret-bearing fragment appears in `text`."""
    for fragment in LEAKS:
        assert fragment not in text, fragment


def test_connect_request_carries_basic_proxy_authorization(
    make_env: Callable[..., object], sent: list[bytes]
) -> None:
    """The CONNECT sent to the fake proxy carries the Basic credential."""
    probe.run_case(make_env(closed=False), case_by_id("A1-C"))
    request = b"".join(sent).decode()
    token = base64.b64encode(f"user:{SECRET}".encode()).decode()
    assert request.startswith("CONNECT api.github.com:443 HTTP/1.1\r\n")
    assert f"Proxy-Authorization: Basic {token}" in request


def test_report_never_prints_proxy_secret(
    make_env: Callable[..., object], caplog: pytest.LogCaptureFixture
) -> None:
    """run_all, format_line and summarize output carries no proxy fragment."""
    env = make_env(closed=True, bind_error=RuntimeError(f"{SECRET} {PROXY_HOST} user:"))
    with caplog.at_level(logging.DEBUG):
        lines, rows = probe.run_all(env)
        report = "\n".join(lines) + probe.summarize(rows, probe.exit_code(rows))
        report += probe.format_line(probe.CASES[0], probe.Result("open", "x"), "FAIL")
    assert_no_leak(report)
    assert_no_leak(caplog.text)
    assert "M9-1 raised RuntimeError" in caplog.text


def test_main_never_prints_proxy_secret(
    monkeypatch: pytest.MonkeyPatch,
    make_env: Callable[..., object],
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    sent: list[bytes],
) -> None:
    """main with faked probes prints no proxy fragment to stdout, stderr or logs."""
    monkeypatch.setenv("SANDBOX_RUNTIME", "1")
    monkeypatch.setenv("HTTPS_PROXY", PROXY_URL)
    env = make_env(closed=True, bind_error=RuntimeError(f"{SECRET} {PROXY_HOST}"))
    monkeypatch.setattr(probe, "Env", lambda environ, home: env)
    with caplog.at_level(logging.DEBUG):
        code = probe.main([])
    captured = capsys.readouterr()
    assert code == 2
    assert "summary:" in captured.out
    assert_no_leak(captured.out)
    assert_no_leak(captured.err)
    assert_no_leak(caplog.text)
    assert any(b"Proxy-Authorization: Basic" in chunk for chunk in sent)
