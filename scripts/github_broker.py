"""GitHub App broker: a stdio MCP server that executes a closed list of GitHub operations.

Implements ADR-0025 D4 (`docs/decisions/ADR-0025-github-app-broker.md`) as designed in
`docs/architecture/GITHUB_BROKER_BLUEPRINT.md`. The server reads one JSON-RPC message
per line on stdin and writes one per line on stdout; logs go to stderr only. It signs an
App JWT with `openssl`, exchanges it for a one-hour installation token and keeps that
token in process memory only: it is never written to a file, passed in argv, or put in a
tool result. It holds no listening socket.

Operations (anything else is an error): `push_branch`, `open_pr`, `merge_pr`,
`push_tag`, `create_release`, `pr_status`.

Configuration is read from `$AGENTS_BROKER_HOME` (default `~/.config/agents-broker`):

| File | Content |
| :--- | :--- |
| `config.json` | `app_id`, `installation_id`, `repository` (`owner/name`), `required_checks` (list of the check-run names `merge_pr` requires in `success`) |
| `keys/app_private_key.pem` | App private key (human-generated; this script only passes its path to `openssl`) |
| `keys/tag_signing` | Dedicated ed25519 SSH key used to sign tags |

invoked_by: docs/guides/GITHUB_BROKER_SETUP_GUIDE.md

Usage:
    python3 scripts/github_broker.py        (launched by Claude Code over stdio)

Exit codes:
    0 - stdin closed
    2 - the configuration file is missing or invalid at startup
"""

import base64
import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any, TextIO

LOGGER = logging.getLogger("github_broker")

API_ROOT = "https://api.github.com"
GIT_REMOTE_TEMPLATE = "https://github.com/{repository}.git"
PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "agents-broker"
SIGNER_PRINCIPAL = "agents-broker"
HTTP_TIMEOUT_SECONDS = 30
TOKEN_REFRESH_MARGIN_SECONDS = 300

PUSH_BRANCH_RE = re.compile(r"^(ai-sprint|hotfix|deploy-notes)/[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")
MERGE_HEAD_RE = re.compile(r"^(ai-sprint|hotfix)/[A-Za-z0-9._/-]+$")
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MERGE_METHODS = ("merge", "squash", "rebase")


class BrokerRefusal(Exception):
    """An operation was refused by a D4 rule or by a missing precondition."""


def _schema(properties: dict[str, dict[str, str]], required: list[str]) -> dict[str, Any]:
    """Build a closed JSON schema for one tool.

    Args:
        properties: Property name to a one-key `type` mapping.
        required: Names of required properties.

    Returns:
        dict[str, Any]: A JSON schema that rejects unknown properties.
    """
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


STR = {"type": "string"}
INT = {"type": "integer"}
BOOL = {"type": "boolean"}

TOOLS: dict[str, tuple[str, dict[str, Any]]] = {
    "push_branch": (
        "Push a branch matching ai-sprint/*, hotfix/* or deploy-notes/* (never main, never force).",
        _schema({"branch": STR}, ["branch"]),
    ),
    "open_pr": (
        "Open a pull request.",
        _schema({"head": STR, "base": STR, "title": STR, "body": STR}, ["head", "base", "title"]),
    ),
    "merge_pr": (
        "Merge a pull request whose head is ai-sprint/* or hotfix/*, base main, required checks green.",
        _schema({"number": INT, "merge_method": STR}, ["number"]),
    ),
    "push_tag": (
        "Create an SSH-signed vX.Y.Z tag on a commit of main and push it.",
        _schema({"tag": STR, "commit": STR}, ["tag", "commit"]),
    ),
    "create_release": (
        "Publish a GitHub Release for an existing tag.",
        _schema({"tag": STR, "name": STR, "body": STR, "prerelease": BOOL}, ["tag"]),
    ),
    "pr_status": (
        "Read the state and check-run conclusions of a pull request.",
        _schema({"number": INT}, ["number"]),
    ),
}


def broker_home() -> Path:
    """Return the broker install directory.

    Returns:
        Path: `$AGENTS_BROKER_HOME`, or `~/.config/agents-broker` when unset.
    """
    override = os.environ.get("AGENTS_BROKER_HOME")
    return Path(override) if override else Path.home() / ".config" / "agents-broker"


def load_config(home: Path) -> dict[str, Any]:
    """Read and validate `config.json` under the broker home.

    Args:
        home: The broker install directory.

    Returns:
        dict[str, Any]: The validated configuration.

    Raises:
        BrokerRefusal: The file is missing, unreadable or lacks a required key.
    """
    try:
        config = json.loads((home / "config.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise BrokerRefusal(f"broker configuration unreadable: {type(error).__name__}") from error
    if not isinstance(config, dict):
        raise BrokerRefusal("broker configuration must be a JSON object")
    for key in ("app_id", "installation_id", "repository"):
        if not config.get(key):
            raise BrokerRefusal(f"broker configuration lacks `{key}`")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", str(config["repository"])):
        raise BrokerRefusal("broker configuration `repository` must be owner/name")
    return config


def b64url(data: bytes) -> str:
    """Encode bytes as unpadded base64url.

    Args:
        data: Raw bytes.

    Returns:
        str: The base64url text without padding.
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def run_command(
    args: list[str], env: dict[str, str] | None = None, stdin: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    """Run a subprocess without a shell and capture its output.

    Args:
        args: The argument vector.
        env: Environment for the child, or None to inherit.
        stdin: Bytes written to the child's stdin.

    Returns:
        subprocess.CompletedProcess[bytes]: The finished process.
    """
    return subprocess.run(
        args, env=env, input=stdin, capture_output=True, check=False, timeout=120
    )


def http_json(
    method: str, url: str, token: str, payload: dict[str, Any] | None = None
) -> tuple[int, Any]:
    """Send one GitHub REST request and decode the JSON reply.

    Args:
        method: HTTP method.
        url: Absolute URL under `API_ROOT`.
        token: A bearer token (App JWT or installation token).
        payload: Optional JSON body.

    Returns:
        tuple[int, Any]: The HTTP status and the decoded body (None when empty).
    """
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", SERVER_NAME)
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as reply:
            status, raw = reply.status, reply.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    return status, (json.loads(raw) if raw else None)


class Broker:
    """The closed operation set, holding the installation token in memory only."""

    def __init__(self, home: Path, config: dict[str, Any]) -> None:
        """Bind the broker to its install directory and configuration.

        Args:
            home: The broker install directory.
            config: The validated configuration from `load_config`.
        """
        self.home = home
        self.config = config
        self.repository = str(config["repository"])
        self._token = ""
        self._token_expiry = 0.0

    # -- authentication ----------------------------------------------------

    def app_jwt(self) -> str:
        """Sign a short-lived App JWT with `openssl` and the App private key.

        Returns:
            str: The compact JWT.

        Raises:
            BrokerRefusal: `openssl` failed to sign.
        """
        now = int(time.time())
        header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode("utf-8"))
        claims = {"iat": now - 60, "exp": now + 540, "iss": str(self.config["app_id"])}
        signing_input = f"{header}.{b64url(json.dumps(claims).encode('utf-8'))}"
        key = self.home / "keys" / "app_private_key.pem"
        done = run_command(
            ["openssl", "dgst", "-sha256", "-sign", str(key)], stdin=signing_input.encode("ascii")
        )
        if done.returncode != 0 or not done.stdout:
            raise BrokerRefusal("openssl failed to sign the App JWT")
        return f"{signing_input}.{b64url(done.stdout)}"

    def installation_token(self) -> str:
        """Return a valid installation token, minting one when needed.

        Returns:
            str: The token (held in memory only).

        Raises:
            BrokerRefusal: GitHub did not issue a token.
        """
        if self._token and time.time() < self._token_expiry - TOKEN_REFRESH_MARGIN_SECONDS:
            return self._token
        url = f"{API_ROOT}/app/installations/{self.config['installation_id']}/access_tokens"
        status, body = http_json("POST", url, self.app_jwt())
        if status != 201 or not isinstance(body, dict) or not body.get("token"):
            raise BrokerRefusal(f"installation token request failed: HTTP {status}")
        self._token = str(body["token"])
        self._token_expiry = time.time() + 3600
        return self._token

    def api(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        """Call the repository REST API with the installation token.

        Args:
            method: HTTP method.
            path: Path under `/repos/{repository}`.
            payload: Optional JSON body.

        Returns:
            Any: The decoded JSON body.

        Raises:
            BrokerRefusal: GitHub answered with a status of 400 or above.
        """
        url = f"{API_ROOT}/repos/{self.repository}{path}"
        status, body = http_json(method, url, self.installation_token(), payload)
        if status >= 400:
            message = body.get("message", "") if isinstance(body, dict) else ""
            raise BrokerRefusal(f"GitHub {method} {path} failed: HTTP {status} {message}".strip())
        return body

    def git_env(self) -> dict[str, str]:
        """Build a child environment that carries the token only as a git config header.

        Returns:
            dict[str, str]: The environment for one `git` child; never logged.
        """
        raw = f"x-access-token:{self.installation_token()}".encode()
        env = dict(os.environ)
        env.update(
            {
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
                "GIT_CONFIG_VALUE_0": "Authorization: basic " + base64.b64encode(raw).decode("ascii"),
            }
        )
        return env

    def git(self, args: list[str]) -> str:
        """Run `git` in the broker's working directory with the token in the child env.

        Args:
            args: Arguments after `git`.

        Returns:
            str: Decoded stderr and stdout, with the token redacted.

        Raises:
            BrokerRefusal: `git` exited non-zero.
        """
        done = run_command(["git", *args], env=self.git_env())
        text = (done.stdout + done.stderr).decode("utf-8", errors="replace")
        text = text.replace(self._token, "[redacted]") if self._token else text
        if done.returncode != 0:
            raise BrokerRefusal(f"git {args[0]} failed (exit {done.returncode}): {text.strip()}")
        return text.strip()

    # -- operations --------------------------------------------------------

    def push_branch(self, branch: str) -> dict[str, Any]:
        """Push `branch` to the repository, without force.

        Args:
            branch: Branch name matching `ai-sprint/*`, `hotfix/*` or `deploy-notes/*`.

        Returns:
            dict[str, Any]: The pushed branch name.

        Raises:
            BrokerRefusal: The name does not match an allowed pattern, or contains `..`.
        """
        if branch == "main" or ".." in branch or not PUSH_BRANCH_RE.fullmatch(branch):
            raise BrokerRefusal(f"push_branch refused: `{branch}` is not an allowed branch pattern")
        remote = GIT_REMOTE_TEMPLATE.format(repository=self.repository)
        self.git(["push", remote, f"refs/heads/{branch}:refs/heads/{branch}"])
        return {"pushed": branch}

    def open_pr(self, head: str, base: str, title: str, body: str = "") -> dict[str, Any]:
        """Open a pull request.

        Args:
            head: Head branch.
            base: Base branch.
            title: Pull request title.
            body: Pull request description.

        Returns:
            dict[str, Any]: The pull request number and URL.
        """
        reply = self.api("POST", "/pulls", {"head": head, "base": base, "title": title, "body": body})
        return {"number": reply.get("number"), "url": reply.get("html_url")}

    def _failing_checks(self, head_sha: str) -> list[str]:
        """List required checks that are not in `success` for a commit.

        Args:
            head_sha: The pull request head commit.

        Returns:
            list[str]: Required check names missing or not `success`.

        Raises:
            BrokerRefusal: No `required_checks` list is configured.
        """
        required = self.config.get("required_checks")
        if not isinstance(required, list) or not required:
            raise BrokerRefusal("merge_pr refused: `required_checks` is not configured")
        runs = self.api("GET", f"/commits/{head_sha}/check-runs?per_page=100").get("check_runs", [])
        conclusions = {run.get("name"): run.get("conclusion") for run in runs}
        return [name for name in required if conclusions.get(name) != "success"]

    def merge_pr(self, number: int, merge_method: str = "merge") -> dict[str, Any]:
        """Merge a pull request when head, base and required checks satisfy D4.

        Args:
            number: Pull request number.
            merge_method: `merge`, `squash` or `rebase`.

        Returns:
            dict[str, Any]: Whether it merged and the merge commit SHA.

        Raises:
            BrokerRefusal: Head, base or a required check does not satisfy D4.
        """
        if merge_method not in MERGE_METHODS:
            raise BrokerRefusal(f"merge_pr refused: merge_method must be one of {MERGE_METHODS}")
        pull = self.api("GET", f"/pulls/{number}")
        head, base = pull["head"], pull["base"]
        if not MERGE_HEAD_RE.fullmatch(str(head.get("ref", ""))) or base.get("ref") != "main":
            raise BrokerRefusal("merge_pr refused: head must be ai-sprint/* or hotfix/* and base main")
        failing = self._failing_checks(str(head["sha"]))
        if failing:
            raise BrokerRefusal(f"merge_pr refused: checks not in success: {', '.join(failing)}")
        reply = self.api("PUT", f"/pulls/{number}/merge", {"merge_method": merge_method})
        return {"merged": bool(reply.get("merged")), "sha": reply.get("sha")}

    def push_tag(self, tag: str, commit: str) -> dict[str, Any]:
        """Create an SSH-signed tag on a commit of `main` and push it, without force.

        Args:
            tag: Tag name `vX.Y.Z`.
            commit: Full 40-hex commit SHA.

        Returns:
            dict[str, Any]: The pushed tag and commit.

        Raises:
            BrokerRefusal: The tag name is not `vX.Y.Z` or the commit is not on `main`.
        """
        if not TAG_RE.fullmatch(tag):
            raise BrokerRefusal(f"push_tag refused: `{tag}` is not vX.Y.Z")
        if not SHA_RE.fullmatch(commit):
            raise BrokerRefusal("push_tag refused: commit must be a full 40-hex SHA")
        status = self.api("GET", f"/compare/main...{commit}").get("status")
        if status not in ("identical", "behind"):
            raise BrokerRefusal("push_tag refused: the commit is not on main")
        key = str(self.home / "keys" / "tag_signing")
        self.git(
            [
                "-c", "gpg.format=ssh",
                "-c", f"user.signingkey={key}",
                "-c", f"user.name={SIGNER_PRINCIPAL}",
                "-c", f"user.email={SIGNER_PRINCIPAL}",
                "tag", "-s", "-m", f"Release {tag}", tag, commit,
            ]
        )  # fmt: skip
        remote = GIT_REMOTE_TEMPLATE.format(repository=self.repository)
        self.git(["push", remote, f"refs/tags/{tag}:refs/tags/{tag}"])
        return {"pushed": tag, "commit": commit}

    def create_release(
        self, tag: str, name: str = "", body: str = "", prerelease: bool = False
    ) -> dict[str, Any]:
        """Publish a GitHub Release for a tag.

        Args:
            tag: Existing tag name.
            name: Release title; defaults to the tag.
            body: Release notes.
            prerelease: Mark the release as a pre-release.

        Returns:
            dict[str, Any]: The release id and URL.
        """
        payload = {"tag_name": tag, "name": name or tag, "body": body, "prerelease": prerelease}
        reply = self.api("POST", "/releases", payload)
        return {"id": reply.get("id"), "url": reply.get("html_url")}

    def pr_status(self, number: int) -> dict[str, Any]:
        """Read a pull request's state and its check-run conclusions.

        Args:
            number: Pull request number.

        Returns:
            dict[str, Any]: State, merged flag, refs and check conclusions.
        """
        pull = self.api("GET", f"/pulls/{number}")
        sha = str(pull["head"]["sha"])
        runs = self.api("GET", f"/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
        return {
            "state": pull.get("state"),
            "merged": bool(pull.get("merged")),
            "head": pull["head"].get("ref"),
            "base": pull["base"].get("ref"),
            "checks": {run.get("name"): run.get("conclusion") for run in runs},
        }

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Dispatch one tool call against the closed list.

        Args:
            name: Tool name.
            arguments: Tool arguments.

        Returns:
            dict[str, Any]: The operation result.

        Raises:
            BrokerRefusal: Unknown operation, `force` requested, or arguments that do not
                match the tool schema.
        """
        if name not in TOOLS:
            raise BrokerRefusal(f"unknown operation `{name}`")
        if arguments.get("force"):
            raise BrokerRefusal("force is never allowed")
        schema = TOOLS[name][1]
        unknown = set(arguments) - set(schema["properties"])
        missing = set(schema["required"]) - set(arguments)
        if unknown or missing:
            raise BrokerRefusal(f"{name} refused: unexpected {sorted(unknown)} or missing {sorted(missing)}")
        handler: Callable[..., dict[str, Any]] = getattr(self, name)
        return handler(**arguments)


# -- JSON-RPC / MCP ------------------------------------------------------------


def rpc_result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    """Build a JSON-RPC success reply.

    Args:
        request_id: The request id.
        result: The result object.

    Returns:
        dict[str, Any]: The reply message.
    """
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def rpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    """Build a JSON-RPC error reply.

    Args:
        request_id: The request id (None when unknown).
        code: JSON-RPC error code.
        message: Error text (never contains the token).

    Returns:
        dict[str, Any]: The reply message.
    """
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def tools_list() -> list[dict[str, Any]]:
    """List the closed tool set in MCP form.

    Returns:
        list[dict[str, Any]]: One entry per operation.
    """
    return [
        {"name": name, "description": text, "inputSchema": schema}
        for name, (text, schema) in TOOLS.items()
    ]


def handle_tool_call(broker: Broker, params: dict[str, Any]) -> dict[str, Any]:
    """Run a `tools/call` and wrap the outcome as an MCP tool result.

    Args:
        broker: The broker.
        params: The `tools/call` params.

    Returns:
        dict[str, Any]: A tool result with `isError` set on refusal or failure.
    """
    name = str(params.get("name", ""))
    arguments = params.get("arguments") or {}
    try:
        if not isinstance(arguments, dict):
            raise BrokerRefusal("arguments must be an object")
        text, is_error = json.dumps(broker.call(name, arguments)), False
    except BrokerRefusal as refusal:
        text, is_error = str(refusal), True
    except Exception as error:  # fault boundary: no operation failure may kill the server
        LOGGER.exception("operation %s failed", name)
        text, is_error = f"{name} failed: {type(error).__name__}", True
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def handle_message(broker: Broker, message: dict[str, Any]) -> dict[str, Any] | None:
    """Answer one JSON-RPC message.

    Args:
        broker: The broker.
        message: The decoded message.

    Returns:
        dict[str, Any] | None: The reply, or None for a notification.
    """
    method, request_id = message.get("method"), message.get("id")
    params = message.get("params") or {}
    if request_id is None:
        return None
    if method == "initialize":
        version = params.get("protocolVersion", PROTOCOL_VERSION)
        return rpc_result(
            request_id,
            {
                "protocolVersion": version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": "1"},
            },
        )
    if method == "ping":
        return rpc_result(request_id, {})
    if method == "tools/list":
        return rpc_result(request_id, {"tools": tools_list()})
    if method == "tools/call":
        if params.get("name") not in TOOLS:
            return rpc_error(request_id, -32602, f"unknown operation `{params.get('name')}`")
        return rpc_result(request_id, handle_tool_call(broker, params))
    return rpc_error(request_id, -32601, f"method not found: {method}")


def reply_for_line(broker: Broker, line: str) -> dict[str, Any] | None:
    """Decode one input line and produce the reply for it.

    Args:
        broker: The broker.
        line: One non-empty input line.

    Returns:
        dict[str, Any] | None: The reply, or None for a notification.
    """
    try:
        message = json.loads(line)
        if not isinstance(message, dict):
            return rpc_error(None, -32600, "invalid request")
        return handle_message(broker, message)
    except ValueError:
        return rpc_error(None, -32700, "parse error")
    except Exception as error:  # fault boundary: keep serving after any fault
        LOGGER.exception("message handling failed")
        return rpc_error(None, -32603, f"internal error: {type(error).__name__}")


def serve(broker: Broker, stdin: TextIO, stdout: TextIO) -> None:
    """Read JSON-RPC messages by line until stdin closes.

    Args:
        broker: The broker.
        stdin: Input stream.
        stdout: Output stream.
    """
    for line in stdin:
        reply = reply_for_line(broker, line) if line.strip() else None
        if reply is not None:
            stdout.write(json.dumps(reply) + "\n")
            stdout.flush()


def main() -> int:
    """Load the configuration and serve MCP over stdio.

    Returns:
        int: Exit code (0 on stdin close, 2 on invalid configuration).
    """
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    home = broker_home()
    try:
        config = load_config(home)
    except BrokerRefusal as refusal:
        LOGGER.error("%s", refusal)
        return 2
    serve(Broker(home, config), sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
