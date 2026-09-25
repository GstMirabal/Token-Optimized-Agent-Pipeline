"""Tests for config/artifact_registry.json and the consumers that read it.

Sprint 023 `C0.2`. The registry is the coordination matrix: a phase is defined
by the artifact it leaves, not by the agent that produces it. Three consumers
read it, so a malformed entry breaks a documentation gate, a close gate and the
generated step map at once — the same criticality bar as the gates themselves.

What these tests protect is not the file's syntax but its two contracts:
every entry declares the fields consumers index into, and every filename is
named literally in a workflow, because `map_workflows.py` matches prose by
literal filename and a deliverable described in words is invisible to it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import map_workflows  # noqa: E402

REGISTRY_PATH = ROOT / "config" / "artifact_registry.json"
REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
ARTIFACTS = REGISTRY["artifacts"]
AGENTS_DIR = ROOT / "agents"
MAKEFILE_PATH = ROOT / "Makefile"
DECLARED_FIELDS = {
    "filename", "phase", "role", "writer", "scope", "host_path", "nucleus_path", "required",
}
SPRINT_PLACEHOLDER = "docs/sprints/[Sprint_ID]-[Stack]-[Layer]/"


def profile_tools(profile: str, agents_dir: Path) -> list[str]:
    """Tools declared in `agents/<profile>.md`'s frontmatter `tools:` line.

    `profile` is a snake_case identifier matching the `agents/` filename
    stem — the same convention `config/artifact_registry.json`'s `writer`
    field uses (ADR-0015's own `<writer>` notation, e.g. `orchestrator`,
    `doc_orchestrator`), so no kebab-case/display-name conversion is needed
    for a value already in that form; a profile absent from `agents_dir`
    resolves to an empty tool list rather than raising, so callers fail
    closed instead of crashing on a typo.

    Args:
        profile: snake_case profile identifier (no `.md` suffix).
        agents_dir: Directory holding `<profile>.md` files.

    Returns:
        list[str]: Tool names from the `tools:` line, or `[]` when the
        profile file or the line is missing.
    """
    profile_path = agents_dir / f"{profile}.md"
    if not profile_path.exists():
        return []
    match = re.search(r"^tools:\s*(.+)$", profile_path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return []
    return [tool.strip() for tool in match.group(1).split(",")]


def writer_holds_write(writer: str, agents_dir: Path) -> bool:
    """Whether `agents/<writer>.md` declares `Write` among its tools.

    The assertion ADR-0015 requires of every registry `writer`
    (`docs/decisions/ADR-0015-artifact-owner-writer-separation.md` §2): the
    writer is the profile that holds `Write`/`Edit` and materializes the
    artifact — `role` alone (e.g. Principal Agent) does not satisfy it.

    Args:
        writer: snake_case profile identifier, as stored in the registry's
            `writer` field.
        agents_dir: Directory holding `<writer>.md` files.

    Returns:
        bool: `True` when `Write` is declared; `False` otherwise, including
        when the profile file does not exist (fails closed).
    """
    return "Write" in profile_tools(writer, agents_dir)


def parse_writer(writer: str) -> tuple[str, str]:
    """Split a typed `writer` field value into its kind and target.

    Sprint 052 `U9` rework: `writer` is typed so it can name a mechanism
    instead of improvising a profile over a file no profile's `Write` tool
    actually touches (`active_state.json`, `mirror.json`, `graph.json` are
    all materialized by a script or `make` target, not by an agent editing
    them directly).

    Args:
        writer: Raw `writer` field value.

    Returns:
        tuple[str, str]: `("script", <repo-relative path>)`,
        `("make", <target>)`, or `("profile", <snake_case id>)` when no
        recognised prefix is present.
    """
    if writer.startswith("script:"):
        return "script", writer[len("script:"):]
    if writer.startswith("make:"):
        return "make", writer[len("make:"):]
    return "profile", writer


def make_target_defined(target: str, makefile_path: Path) -> bool:
    """Whether `target:` is defined as a rule in `makefile_path`.

    Args:
        target: Makefile target name, without the trailing colon.
        makefile_path: Path to the Makefile to search.

    Returns:
        bool: `True` when a `<target>:` rule line is found; `False`
        otherwise, including when `makefile_path` does not exist (fails
        closed).
    """
    if not makefile_path.exists():
        return False
    text = makefile_path.read_text(encoding="utf-8")
    return re.search(rf"(?m)^{re.escape(target)}\s*:", text) is not None


def writer_resolves(
    writer: str, *, agents_dir: Path, repo_root: Path, makefile_path: Path
) -> bool:
    """Whether a typed `writer` value resolves to something real.

    Dispatches on `parse_writer`'s classification: a bare profile id must
    hold `Write` (`writer_holds_write`); `script:<path>` must exist under
    `repo_root`; `make:<target>` must be a defined Makefile rule. An
    unrecognised prefix (e.g. `docker:foo`) falls through to the profile
    branch, where `agents/docker:foo.md` does not exist — so it fails
    closed rather than being silently accepted.

    Args:
        writer: Raw `writer` field value from the registry.
        agents_dir: Directory holding `<profile>.md` files.
        repo_root: Repository root, for resolving `script:` paths.
        makefile_path: Path to the Makefile, for resolving `make:` targets.

    Returns:
        bool: `True` when the named mechanism/profile resolves; `False`
        otherwise.
    """
    kind, target = parse_writer(writer)
    if kind == "script":
        return (repo_root / target).exists()
    if kind == "make":
        return make_target_defined(target, makefile_path)
    return writer_holds_write(target, agents_dir)


def test_every_entry_declares_every_field_a_consumer_indexes():
    """Consumers index with `entry["filename"]`, not `.get`. A missing key is a
    crash in a gate rather than a warning, so the shape is pinned here."""
    for entry in ARTIFACTS:
        missing = DECLARED_FIELDS - set(entry)
        assert not missing, f"{entry.get('filename')} is missing {sorted(missing)}"


def test_scope_is_one_of_the_two_values_consumers_filter_on():
    """Both gates filter `scope == "sprint"`. A third value would silently drop
    the entry from every check while still appearing in the file."""
    assert {entry["scope"] for entry in ARTIFACTS} <= {"sprint", "repository"}


def test_sprint_scoped_paths_use_the_canonical_sprint_directory():
    """`agents.md §5 mandatory_topology` declares the path once. Four different
    forms of it were in circulation until Phase 019, which is how a file was
    persisted to a path no other document recognised."""
    for entry in ARTIFACTS:
        if entry["scope"] != "sprint":
            continue
        for field in ("host_path", "nucleus_path"):
            assert entry[field].startswith(SPRINT_PLACEHOLDER), (
                f"{entry['filename']}.{field} does not start with the canonical path"
            )


def test_a_path_ends_with_the_filename_it_declares():
    """A registry whose path and filename disagree would make one consumer look
    in the right place while another reports the wrong name."""
    for entry in ARTIFACTS:
        for field in ("host_path", "nucleus_path"):
            if entry[field] is None:
                continue
            assert entry[field].endswith(entry["filename"])


def test_filenames_are_unique():
    """Both gates build a dict keyed by filename: a duplicate would not be
    rejected, it would be silently overwritten by whichever came last."""
    names = [entry["filename"] for entry in ARTIFACTS]
    assert len(names) == len(set(names))


def test_every_entry_declares_a_writer():
    """ADR-0015 §2: every artifact entry gains `writer`, alongside `role`."""
    for entry in ARTIFACTS:
        assert entry.get("writer"), f"{entry.get('filename')} has no writer"


def test_every_writer_resolves():
    """ADR-0015 §2 (typed-writer rework, Sprint 052 `U9`): every declared
    `writer` resolves per its form — a bare profile id holds `Write`
    (the mechanism that fixed `F-051-R1`, a `role` without `Write`
    dispatched to author its own artifact); `script:`/`make:` name a real
    script path or Makefile target rather than improvising a profile over
    a file no profile's `Write` tool actually touches."""
    for entry in ARTIFACTS:
        writer = entry["writer"]
        assert writer_resolves(
            writer, agents_dir=AGENTS_DIR, repo_root=ROOT, makefile_path=MAKEFILE_PATH
        ), f"{entry['filename']}'s writer `{writer}` does not resolve"


def test_writer_resolves_script_form_fails_when_path_does_not_exist(tmp_path: Path):
    assert not writer_resolves(
        "script:scripts/does_not_exist.py",
        agents_dir=AGENTS_DIR, repo_root=tmp_path, makefile_path=MAKEFILE_PATH,
    )


def test_writer_resolves_script_form_passes_when_path_exists(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "real.py").write_text("", encoding="utf-8")
    assert writer_resolves(
        "script:scripts/real.py",
        agents_dir=AGENTS_DIR, repo_root=tmp_path, makefile_path=MAKEFILE_PATH,
    )


def test_writer_resolves_make_form_fails_when_target_is_absent(tmp_path: Path):
    fake_makefile = tmp_path / "Makefile"
    fake_makefile.write_text("verify:\n\techo ok\n", encoding="utf-8")
    assert not writer_resolves(
        "make:no-such-target",
        agents_dir=AGENTS_DIR, repo_root=ROOT, makefile_path=fake_makefile,
    )


def test_writer_resolves_make_form_passes_when_target_is_defined(tmp_path: Path):
    fake_makefile = tmp_path / "Makefile"
    fake_makefile.write_text("graphify-update:\n\techo ok\n", encoding="utf-8")
    assert writer_resolves(
        "make:graphify-update",
        agents_dir=AGENTS_DIR, repo_root=ROOT, makefile_path=fake_makefile,
    )


def test_writer_resolves_fails_closed_on_an_unknown_prefix():
    """`docker:some-target` is neither `script:` nor `make:`; it must not be
    silently accepted as a profile id (no `agents/docker:some-target.md`
    exists, so it fails — but this pins that behaviour rather than leaving
    it incidental)."""
    assert not writer_resolves(
        "docker:some-target",
        agents_dir=AGENTS_DIR, repo_root=ROOT, makefile_path=MAKEFILE_PATH,
    )


def test_parse_writer_splits_typed_forms():
    assert parse_writer("script:scripts/session_state.py") == (
        "script", "scripts/session_state.py",
    )
    assert parse_writer("make:graphify-update") == ("make", "graphify-update")
    assert parse_writer("orchestrator") == ("profile", "orchestrator")


def test_make_target_defined_fails_closed_on_a_missing_makefile(tmp_path: Path):
    assert not make_target_defined("verify", tmp_path / "no-such-Makefile")


def test_writer_holds_write_fails_closed_on_a_profile_without_write(tmp_path: Path):
    """Fixture proving the checker helper actually discriminates: a registry
    naming a writer whose `tools:` omits `Write` must fail, not pass silently
    — reproducing the exact defect `F-051-R1` found (Principal Agent, no
    `Write`, named as the artifact's writer)."""
    fake_agents = tmp_path / "agents"
    fake_agents.mkdir()
    (fake_agents / "no_write_profile.md").write_text(
        "---\nname: no-write-profile\ntools: Read, Glob, Grep, Bash\n"
        "model: haiku\ntier: mechanical\n---\n",
        encoding="utf-8",
    )
    assert writer_holds_write("no_write_profile", fake_agents) is False


def test_writer_holds_write_passes_on_a_profile_with_write(tmp_path: Path):
    fake_agents = tmp_path / "agents"
    fake_agents.mkdir()
    (fake_agents / "has_write_profile.md").write_text(
        "---\nname: has-write-profile\ntools: Read, Glob, Grep, Write, Edit\n"
        "model: sonnet\ntier: author\n---\n",
        encoding="utf-8",
    )
    assert writer_holds_write("has_write_profile", fake_agents) is True


def test_writer_holds_write_fails_closed_on_a_missing_profile_file(tmp_path: Path):
    """A `writer` naming a profile that does not exist under `agents/` must
    not be mistaken for one that silently grants `Write`."""
    fake_agents = tmp_path / "agents"
    fake_agents.mkdir()
    assert writer_holds_write("ghost_profile", fake_agents) is False


def test_implementation_plan_writer_is_orchestrator_per_adr_0015():
    """ADR-0015 §2 explicit table: the three artifacts Principal Agent owns
    (no `Write`) each get a named `writer` distinct from `role`."""
    by_filename = {entry["filename"]: entry for entry in ARTIFACTS}
    assert by_filename["IMPLEMENTATION_PLAN.md"]["writer"] == "orchestrator"
    assert by_filename["PHASE_REGISTER.md"]["writer"] == "doc_orchestrator"
    assert by_filename["CHANGELOG.md"]["writer"] == "doc_orchestrator"


def test_every_artifact_is_named_by_filename_in_some_workflow():
    """The `R2` guarantee, pinned so it cannot silently regress.

    `map_workflows.py` matches workflow prose by literal filename, so a phase
    that describes its deliverable instead of naming it produces an empty
    matrix column. That is not hypothetical: Phase 4.1 said "every step has a
    named assignee" and Phase 4.2 "every step has its tools resolved", and
    `agent_assignment.md` and `skill_assignment.md` were invisible to the map
    while four sprints were producing them.
    """
    prose = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted((ROOT / "workflows").glob("*.md"))
    )
    for entry in ARTIFACTS:
        assert entry["filename"] in prose, (
            f"{entry['filename']} is in the registry but no workflow names it, so its "
            "matrix column is empty by construction"
        )


def test_the_matrix_columns_are_every_registry_entry_in_order():
    """The columns were a fixed table of six state artifacts and zero
    documentary ones. Order is part of the contract: the registry is ordered by
    phase so the generated guide reads in execution order."""
    assert list(map_workflows.load_artifacts()) == [e["filename"] for e in ARTIFACTS]


def test_a_missing_registry_fails_loudly_in_the_map(tmp_path):
    """A matrix built from an unreadable registry would have no columns and
    would read as "no workflow touches any artifact" — a false green. The map
    raises instead, which is the opposite failure direction from the freshness
    gate on purpose: one generates a document, the other reports findings."""
    try:
        map_workflows.load_artifacts(tmp_path / "absent.json")
    except FileNotFoundError:
        return
    raise AssertionError("load_artifacts accepted a missing registry")
