"""Tests for scripts/github_broker.py (Sprint 060 unit A-03).

No network, no real key: HTTP and subprocess calls are replaced by recorders, and the
only key used is a throwaway RSA key generated into `tmp_path` by `openssl`.
"""

from __future__ import annotations

import base64
import importlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
broker_mod = importlib.import_module("github_broker")

TOKEN = "ghs_throwaway_installation_token"
SHA = "a" * 40
REQUIRED = ["lint", "test", "audit"]


class Recorder:
    """Records HTTP and command calls and replays scripted HTTP replies."""

    def __init__(self) -> None:
        self.http: list[tuple[str, str, dict[str, Any] | None]] = []
        self.commands: list[list[str]] = []
        self.envs: list[dict[str, str] | None] = []
        self.routes: dict[tuple[str, str], tuple[int, Any]] = {}

    def http_json(self, method: str, url: str, token: str, payload: Any = None) -> tuple[int, Any]:
        self.http.append((method, url, payload))
        if url.endswith("/access_tokens"):
            return 201, {"token": TOKEN}
        reply = self.routes.get((method, url.split("/repos/owner/repo")[-1]))
        if reply is not None:
            return reply
        return 404, {"message": "not scripted"}

    def run_command(self, args: list[str], env: Any = None, stdin: Any = None) -> Any:
        self.commands.append(args)
        self.envs.append(env)
        return subprocess.CompletedProcess(args, 0, b"ok", b"")


@pytest.fixture
def rec(monkeypatch: pytest.MonkeyPatch) -> Recorder:
    recorder = Recorder()
    monkeypatch.setattr(broker_mod, "http_json", recorder.http_json)
    monkeypatch.setattr(broker_mod, "run_command", recorder.run_command)
    return recorder


@pytest.fixture
def broker(tmp_path: Path, rec: Recorder) -> Any:
    config = {
        "app_id": "123",
        "installation_id": "456",
        "repository": "owner/repo",
        "required_checks": REQUIRED,
    }
    (tmp_path / "keys").mkdir()
    instance = broker_mod.Broker(tmp_path, config)
    # Skip the JWT signing: the token path is covered by test_app_jwt_is_signed.
    instance.app_jwt = lambda: "jwt"  # type: ignore[method-assign]
    return instance


def pull(head: str = "ai-sprint/060", base: str = "main") -> tuple[int, Any]:
    return 200, {"head": {"ref": head, "sha": SHA}, "base": {"ref": base}, "state": "open"}


def checks(conclusion: str = "success", names: list[str] | None = None) -> tuple[int, Any]:
    runs = [{"name": n, "conclusion": conclusion} for n in (names or REQUIRED)]
    return 200, {"check_runs": runs}


# -- push_branch ---------------------------------------------------------------


@pytest.mark.parametrize("branch", ["ai-sprint/060", "hotfix/H-001", "deploy-notes/059"])
def test_push_branch_allowed_without_force(broker: Any, rec: Recorder, branch: str) -> None:
    assert broker.call("push_branch", {"branch": branch}) == {"pushed": branch}
    args = rec.commands[-1]
    assert f"refs/heads/{branch}:refs/heads/{branch}" in args
    assert not any(a.startswith(("--force", "+")) for a in args)


@pytest.mark.parametrize("branch", ["main", "feat/x", "ai-sprint/../main", "+ai-sprint/x", "ai-sprint"])
def test_push_branch_rejects_other_names(broker: Any, rec: Recorder, branch: str) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("push_branch", {"branch": branch})
    assert rec.commands == []


def test_push_branch_rejects_force(broker: Any, rec: Recorder) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("push_branch", {"branch": "ai-sprint/060", "force": True})
    assert rec.commands == []


def test_push_token_is_not_in_argv(broker: Any, rec: Recorder) -> None:
    broker.call("push_branch", {"branch": "ai-sprint/060"})
    assert all(TOKEN not in " ".join(c) for c in rec.commands)
    assert TOKEN in base64.b64decode(
        rec.envs[-1]["GIT_CONFIG_VALUE_0"].split("basic ")[1]
    ).decode()


# -- open_pr / create_release / pr_status --------------------------------------


def test_open_pr_posts_and_returns_number(broker: Any, rec: Recorder) -> None:
    rec.routes[("POST", "/pulls")] = (201, {"number": 7, "html_url": "u"})
    out = broker.call("open_pr", {"head": "ai-sprint/060", "base": "main", "title": "t"})
    assert out == {"number": 7, "url": "u"}


def test_open_pr_rejects_missing_title(broker: Any) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("open_pr", {"head": "h", "base": "main"})


def test_create_release_posts_tag(broker: Any, rec: Recorder) -> None:
    rec.routes[("POST", "/releases")] = (201, {"id": 9, "html_url": "r"})
    assert broker.call("create_release", {"tag": "v4.43.0"}) == {"id": 9, "url": "r"}
    assert rec.http[-1][2]["tag_name"] == "v4.43.0"


def test_create_release_rejects_unknown_argument(broker: Any, rec: Recorder) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("create_release", {"tag": "v4.43.0", "target_commitish": "x"})
    assert rec.http == []


def test_pr_status_reports_checks(broker: Any, rec: Recorder) -> None:
    rec.routes[("GET", "/pulls/3")] = pull()
    rec.routes[("GET", f"/commits/{SHA}/check-runs?per_page=100")] = checks("failure")
    out = broker.call("pr_status", {"number": 3})
    assert out["checks"] == dict.fromkeys(REQUIRED, "failure")
    assert out["base"] == "main"


def test_pr_status_rejects_missing_number(broker: Any) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("pr_status", {})


# -- merge_pr ------------------------------------------------------------------


def script_merge(rec: Recorder, p: tuple[int, Any], c: tuple[int, Any]) -> None:
    rec.routes[("GET", "/pulls/5")] = p
    rec.routes[("GET", f"/commits/{SHA}/check-runs?per_page=100")] = c
    rec.routes[("PUT", "/pulls/5/merge")] = (200, {"merged": True, "sha": "m"})


@pytest.mark.parametrize("head", ["ai-sprint/060", "hotfix/H-001"])
def test_merge_pr_allowed(broker: Any, rec: Recorder, head: str) -> None:
    script_merge(rec, pull(head), checks())
    assert broker.call("merge_pr", {"number": 5}) == {"merged": True, "sha": "m"}
    assert rec.http[-1][0] == "PUT"


@pytest.mark.parametrize(
    ("p", "c"),
    [
        (pull("feat/x"), checks()),
        (pull("deploy-notes/059"), checks()),
        (pull("ai-sprint/060", "develop"), checks()),
        (pull(), checks("failure")),
        (pull(), checks(names=["lint", "test"])),
    ],
)
def test_merge_pr_rejections_do_not_merge(
    broker: Any, rec: Recorder, p: tuple[int, Any], c: tuple[int, Any]
) -> None:
    script_merge(rec, p, c)
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("merge_pr", {"number": 5})
    assert all(call[0] != "PUT" for call in rec.http)


def test_merge_pr_refuses_without_configured_checks(broker: Any, rec: Recorder) -> None:
    broker.config["required_checks"] = []
    script_merge(rec, pull(), checks())
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("merge_pr", {"number": 5})


def test_merge_pr_rejects_unknown_merge_method(broker: Any, rec: Recorder) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("merge_pr", {"number": 5, "merge_method": "octopus"})
    assert rec.http == []


# -- push_tag ------------------------------------------------------------------


@pytest.mark.parametrize("status", ["identical", "behind"])
def test_push_tag_signs_then_pushes(broker: Any, rec: Recorder, status: str) -> None:
    rec.routes[("GET", f"/compare/main...{SHA}")] = (200, {"status": status})
    assert broker.call("push_tag", {"tag": "v4.43.0", "commit": SHA})["pushed"] == "v4.43.0"
    sign, push = rec.commands
    assert "gpg.format=ssh" in sign and "-s" in sign and "user.email=agents-broker" in sign
    assert "refs/tags/v4.43.0:refs/tags/v4.43.0" in push
    assert not any(a.startswith(("--force", "+")) for a in push)


@pytest.mark.parametrize("tag", ["4.43.0", "v4.43", "v4.43.0-rc1", "latest"])
def test_push_tag_rejects_bad_name(broker: Any, rec: Recorder, tag: str) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("push_tag", {"tag": tag, "commit": SHA})
    assert rec.commands == []


@pytest.mark.parametrize("status", ["ahead", "diverged"])
def test_push_tag_rejects_commit_not_on_main(broker: Any, rec: Recorder, status: str) -> None:
    rec.routes[("GET", f"/compare/main...{SHA}")] = (200, {"status": status})
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("push_tag", {"tag": "v4.43.0", "commit": SHA})
    assert rec.commands == []


def test_push_tag_rejects_short_commit(broker: Any, rec: Recorder) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("push_tag", {"tag": "v4.43.0", "commit": "main"})
    assert rec.http == []


# -- closed list, token handling, errors ---------------------------------------


@pytest.mark.parametrize("name", ["delete_branch", "gh", "push_branch ", "", "close_pr"])
def test_unknown_operation_refused(broker: Any, rec: Recorder, name: str) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call(name, {})
    assert rec.http == [] and rec.commands == []


def test_tool_set_is_exactly_the_d4_list() -> None:
    assert set(broker_mod.TOOLS) == {
        "push_branch", "open_pr", "merge_pr", "push_tag", "create_release", "pr_status",
    }  # fmt: skip


def test_token_is_cached_in_memory(broker: Any, rec: Recorder) -> None:
    rec.routes[("POST", "/releases")] = (201, {"id": 1, "html_url": "r"})
    broker.call("create_release", {"tag": "v1.0.0"})
    broker.call("create_release", {"tag": "v1.0.1"})
    mints = [c for c in rec.http if c[1].endswith("/access_tokens")]
    assert len(mints) == 1


def test_token_request_failure_is_refusal(broker: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(broker_mod, "http_json", lambda *a, **k: (401, {"message": "bad"}))
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.installation_token()


def test_github_error_status_is_refusal(broker: Any, rec: Recorder) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker.call("pr_status", {"number": 99})


@pytest.mark.skipif(shutil.which("openssl") is None, reason="openssl not installed")
def test_app_jwt_is_signed(tmp_path: Path) -> None:
    keys = tmp_path / "keys"
    keys.mkdir()
    made = subprocess.run(
        ["openssl", "genrsa", "-out", str(keys / "app_private_key.pem"), "2048"],
        capture_output=True,
        check=False,
    )
    assert made.returncode == 0
    instance = broker_mod.Broker(
        tmp_path, {"app_id": "123", "installation_id": "1", "repository": "o/r"}
    )
    header, claims, signature = instance.app_jwt().split(".")
    pad = "=" * (-len(claims) % 4)
    decoded = json.loads(base64.urlsafe_b64decode(claims + pad))
    assert decoded["iss"] == "123" and decoded["exp"] > decoded["iat"]
    assert header and signature


def test_app_jwt_signing_failure_is_refusal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        broker_mod, "run_command", lambda *a, **k: subprocess.CompletedProcess(a, 1, b"", b"err")
    )
    instance = broker_mod.Broker(
        tmp_path, {"app_id": "1", "installation_id": "1", "repository": "o/r"}
    )
    with pytest.raises(broker_mod.BrokerRefusal):
        instance.app_jwt()


# -- configuration -------------------------------------------------------------


def test_load_config_missing_file(tmp_path: Path) -> None:
    with pytest.raises(broker_mod.BrokerRefusal):
        broker_mod.load_config(tmp_path)


@pytest.mark.parametrize(
    "content",
    ["[]", "{}", '{"app_id":"1","installation_id":"2","repository":"bad"}', "not json"],
)
def test_load_config_invalid(tmp_path: Path, content: str) -> None:
    (tmp_path / "config.json").write_text(content, encoding="utf-8")
    with pytest.raises(broker_mod.BrokerRefusal):
        broker_mod.load_config(tmp_path)


def test_main_exits_2_on_missing_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGENTS_BROKER_HOME", str(tmp_path))
    assert broker_mod.main() == 2


# -- MCP protocol --------------------------------------------------------------


def run_session(broker: Any, messages: list[Any]) -> list[dict[str, Any]]:
    lines = "".join((m if isinstance(m, str) else json.dumps(m)) + "\n" for m in messages)
    out = io.StringIO()
    broker_mod.serve(broker, io.StringIO(lines), out)
    return [json.loads(line) for line in out.getvalue().splitlines()]


def test_protocol_initialize_list_and_call(broker: Any, rec: Recorder) -> None:
    rec.routes[("GET", "/pulls/3")] = pull()
    rec.routes[("GET", f"/commits/{SHA}/check-runs?per_page=100")] = checks()
    replies = run_session(
        broker,
        [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "x"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "pr_status", "arguments": {"number": 3}}},
        ],
    )  # fmt: skip
    assert [r["id"] for r in replies] == [1, 2, 3]
    assert len(replies[1]["result"]["tools"]) == 6
    assert replies[2]["result"]["isError"] is False
    assert TOKEN not in json.dumps(replies)


def test_protocol_refusal_is_tool_error_and_unknown_tool_is_rpc_error(
    broker: Any, rec: Recorder
) -> None:
    replies = run_session(
        broker,
        [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
             "params": {"name": "push_branch", "arguments": {"branch": "main"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "delete_repo", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 3, "method": "nope"},
        ],
    )  # fmt: skip
    assert replies[0]["result"]["isError"] is True
    assert replies[1]["error"]["code"] == -32602
    assert replies[2]["error"]["code"] == -32601
    assert rec.commands == []


def test_protocol_survives_garbage_and_faults(broker: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError(TOKEN)

    monkeypatch.setattr(broker_mod, "http_json", boom)
    replies = run_session(
        broker,
        [
            "{not json",
            "[1]",
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "pr_status", "arguments": {"number": 1}}},
            {"jsonrpc": "2.0", "id": 5, "method": "ping"},
        ],
    )  # fmt: skip
    assert replies[0]["error"]["code"] == -32700
    assert replies[1]["error"]["code"] == -32600
    assert replies[2]["result"]["isError"] is True
    assert TOKEN not in json.dumps(replies)
    assert replies[3]["result"] == {}
