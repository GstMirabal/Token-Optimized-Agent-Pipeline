"""Reference-integrity linter — immunizes the framework against the
"Master Ledger class" of inconsistency: normative references whose target
no longer exists or can never be reached.

Checks (run from the .agents root; CI fails the PR on any violation):
  (a) Every rules/*.md is reachable — referenced by name from agents.md,
      a workflow, or a command (lazy-loading requires a pointer somewhere).
  (b) Every *_TEMPLATE.md cited in agents.md/workflows/ exists in
      docs/standards/templates/.
  (c) Every numbered "Rule NN" citation resolves to an entry in
      rules/LEGACY_RULE_CONCORDANCE.md (the numbering system was abolished
      by the tabular refactor; unmapped numbers are phantom references).
  (d) Every workflow, script and executable skill has a declared invoker, or a
      declared exception (RA-16 INVOCATION_COVERAGE, agents.md §7).
  (e) config/rule_triggers.json mirrors rules/*.md.
  (f) Living docs (guides, decisions, audits) that cite ``path:line`` point at a
      file whose line count is at least that line — Sprint 029 J6. Does **not**
      scan docs/sprints/ or docs/roadmaps/ (historical records).
  (g) Every ``agents/*.md`` with frontmatter ``tier:`` has ``model:`` equal to
      ``config/model_tiers.json`` → ``tiers[tier]["claude_code"]["model"]``
      (Claude Code side only, D15). Plan 035 called this ``(f)``; letter ``(f)``
      is already ``check_file_line_citations`` (Sprint 029), so this is ``(g)``.

invoked_by: Makefile `verify` target (and therefore .github/workflows/ci.yml).
"""
import ast
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

CONCORDANCE = Path("rules/LEGACY_RULE_CONCORDANCE.md")
TEMPLATES_DIR = Path("docs/standards/templates")
EXCEPTIONS_FILE = Path("config/invocation_exceptions.json")
MODEL_TIERS_FILE = Path("config/model_tiers.json")

# Living documentary corpus for check (f). Historical sprint/roadmap prose is
# excluded by construction — abort criterion 3 of Sprint 029.
FILE_LINE_CORPUS = (
    Path("docs/guides"),
    Path("docs/decisions"),
    Path("docs/audits"),
)

# Leading YAML frontmatter for check (g). Only ``model:`` / ``tier:`` are read.
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
AGENT_TIER_MODEL_RE = re.compile(r"^(model|tier):\s*(\S+)\s*$", re.MULTILINE)

# ``path/to/file.ext:123`` inside backticks or as a bare token. Requires a
# known text/code suffix so bare ``12:34`` clocks and URL ports do not match.
FILE_LINE_RE = re.compile(
    r"(?<![\w./-])"  # not mid-token
    r"((?:[\w.-]+/)*[\w.-]+\.(?:md|py|json|sh|yml|yaml|toml|txt|mdc))"
    r":(\d+)"
    r"(?![\w./-])"
)
# Reasons an artifact may legitimately have no invoker inside the framework.
# A free-text reason is rejected: an exception nobody can categorise is an
# exception nobody will ever revisit.
VALID_EXCEPTION_REASONS = frozenset({
    "model-invoked",       # Claude invokes it by name from a conversation.
    "vendored-reference",  # Third-party material kept as reference, not wired.
    "human-entry-point",   # A person runs it directly; no framework caller.
    "one-time",            # A migration already consumed; kept for the record.
})

# History is never rewritten — legacy logs keep their citations un-audited.
# Generated/vendored runtime dirs are not normative material (absent in CI
# checkouts, but present locally: venvs, graph output, linked .claude trees).
SCAN_EXCLUDE = ("docs/roadmaps/", "docs/sprints/", "node_modules/", ".git/",
                "venv_skillopt/", "venv/", "graphify-out/", ".claude/",
                "CHANGELOG.md", str(CONCORDANCE))

def loadable() -> list[Path]:
    """Every document a session can load: the ruleset, the protocols, the commands.

    A function rather than a module constant, because the globs used to run at
    import — before `main()` sets the framework root — so the list was built
    against whatever directory the caller was standing in and came back empty
    from anywhere but the repository root.

    Returns:
        list[Path]: Paths relative to the framework root.
    """
    return [Path("agents.md"), *Path("workflows").glob("*.md"), *Path("commands").glob("*.md")]


def loadable_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in loadable())


def scan_files():
    for pattern in ("**/*.md", "**/*.py"):
        for p in Path(".").glob(pattern):
            sp = str(p)
            if any(x in sp for x in SCAN_EXCLUDE):
                continue
            yield p


def check_rules_reachable(corpus: str) -> list[str]:
    errors = []
    for rule in sorted(Path("rules").glob("*.md")):
        if rule.name not in corpus:
            errors.append(f"(a) rules/{rule.name} is unreachable — nothing loadable references it.")
    return errors


# Filenames GitHub defines, which this framework does not own and never ships
# in docs/standards/templates/. Any workflow describing repository setup has to
# name them, and doing so is not a dangling reference.
PLATFORM_TEMPLATES = frozenset({
    "PULL_REQUEST_TEMPLATE.md",
    "ISSUE_TEMPLATE.md",
})


def check_templates_exist(corpus: str) -> list[str]:
    """Every framework template cited in a loadable document must exist.

    Args:
        corpus: Concatenated text of agents.md and every workflow.

    Returns:
        list[str]: One error per template cited without a file behind it.
    """
    errors = []
    for name in set(re.findall(r"([A-Z][A-Z_]*_TEMPLATE\.md)", corpus)):
        if name in PLATFORM_TEMPLATES:
            continue
        if not (TEMPLATES_DIR / name).exists():
            errors.append(f"(b) {name} is cited but missing from {TEMPLATES_DIR}/.")
    return errors


def check_rule_citations() -> list[str]:
    if not CONCORDANCE.exists():
        return [f"(c) {CONCORDANCE} missing — numbered citations cannot be resolved."]
    mapped = set(re.findall(r"\*\*Rule (\d+)", CONCORDANCE.read_text(encoding="utf-8")))
    # 41 covers 041/41.x style; normalize citations to their integer part.
    errors = []
    for p in scan_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for num in re.findall(r"Rule[s]? 0*(\d+)(?:\.\d+)?", text):
            if num not in mapped:
                errors.append(f"(c) {p}: cites Rule {num}, not mapped in the concordance.")
    return sorted(set(errors))


def load_exceptions() -> tuple[dict[str, str], list[str]]:
    """Read the declared-exception registry and validate it against the tree.

    Exceptions live in a data file rather than in each artifact's frontmatter
    because vendored skills cannot be edited at all (Skill Documentation Veto,
    rules/skills_and_integrations.md §3).

    Returns:
        tuple[dict[str, str], list[str]]: path -> reason, plus registry errors.
    """
    if not EXCEPTIONS_FILE.exists():
        return {}, [f"(d) {EXCEPTIONS_FILE} missing — RA-16 cannot be evaluated."]

    errors: list[str] = []
    exceptions: dict[str, str] = {}
    for entry in json.loads(EXCEPTIONS_FILE.read_text(encoding="utf-8"))["exceptions"]:
        path, reason = entry["path"], entry["reason"]
        exceptions[path] = reason
        if reason not in VALID_EXCEPTION_REASONS:
            errors.append(
                f"(d) {EXCEPTIONS_FILE}: '{path}' has reason '{reason}', "
                f"not one of {sorted(VALID_EXCEPTION_REASONS)}."
            )
        # A stale exemption is worse than no exemption: it silently excuses an
        # artifact that no longer exists, and hides the next one to take its name.
        if not Path(path).exists():
            errors.append(f"(d) {EXCEPTIONS_FILE}: '{path}' does not exist — stale exemption.")
    return exceptions, errors


def imported_modules() -> set[str]:
    """Module names imported by any tracked Python file.

    A script imported as a module has an invoker even though its filename is
    never written anywhere. Missing this is not theoretical: `merge_json.py`
    looked orphaned to a filename-only scan while `scripts/install.py`
    depends on it, and deleting it would have broken the bridge installer.
    """
    modules: set[str] = set()
    for path in [*Path("scripts").glob("*.py"), *Path("hooks").glob("*.py")]:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[-1])
    return modules


def check_invocation_coverage(corpus: str) -> list[str]:
    """(d) Every mechanism declares an invoker, or a typed exception (RA-16).

    Args:
        corpus: Concatenated text of agents.md, workflows and commands.

    Returns:
        list[str]: One error per mechanism nothing invokes and nothing excuses.
    """
    exceptions, errors = load_exceptions()
    governance = corpus + "\n".join(
        p.read_text(encoding="utf-8")
        for p in [*Path("rules").glob("*.md"), *Path("agents").glob("*.md")]
    )
    modules = imported_modules()

    # Workflows, scripts and hooks are framework-owned: they declare their own
    # invoker. Package markers (``__init__.py``) are not mechanisms.
    for path in [
        *sorted(Path("workflows").glob("*.md")),
        *sorted(Path("scripts").glob("*.py")),
        *sorted(Path("hooks").glob("*.py")),
    ]:
        key = str(path)
        if key in exceptions:
            continue
        if path.name == "__init__.py":
            continue
        if path.suffix == ".py" and path.stem in modules:
            continue
        if "invoked_by:" not in path.read_text(encoding="utf-8"):
            errors.append(
                f"(d) {key} declares no `invoked_by:` and has no exception — "
                f"a mechanism nothing calls is a regression, not a pending feature."
            )

    # Skills are not edited here: vendored SKILL.md files are under the
    # Documentation Veto, so a skill counts as invoked when governance names it.
    for skill in sorted(p for p in Path("skills").iterdir() if (p / "scripts").is_dir()):
        key = str(skill)
        if key in exceptions or skill.name in governance:
            continue
        errors.append(f"(d) {key} is an executable skill nothing invokes and nothing excuses.")

    return errors


def check_rule_triggers_sync() -> list[str]:
    """(e) config/rule_triggers.json must mirror rules/*.md exactly."""
    triggers_path = Path("config/rule_triggers.json")
    if not triggers_path.exists():
        return ["(e) config/rule_triggers.json is missing."]
    data = json.loads(triggers_path.read_text(encoding="utf-8"))
    declared = {entry["path"] for entry in data.get("rules", [])}
    on_disk = {f"rules/{p.name}" for p in sorted(Path("rules").glob("*.md"))}
    errors: list[str] = []
    missing = on_disk - declared
    extra = declared - on_disk
    for path in sorted(missing):
        errors.append(f"(e) rules/{Path(path).name} has no entry in config/rule_triggers.json.")
    for path in sorted(extra):
        errors.append(f"(e) config/rule_triggers.json lists {path}, which is not in rules/.")
    return errors


def resolve_cited_path(cited: str) -> Path | None:
    """Map a citation path to a real file under the framework root.

    Bare basenames (``qa_agent.md``) resolve under ``agents/`` when unique there;
    otherwise only an exact relative path that exists is accepted. Missing files
    are skipped — check (f) is a **range** gate, not an existence gate (J6).
    """
    direct = Path(cited)
    if direct.is_file():
        return direct
    matches = list(Path("agents").glob(cited)) if "/" not in cited else []
    if len(matches) == 1 and matches[0].is_file():
        return matches[0]
    return None


def check_file_line_citations() -> list[str]:
    """(f) ``path:line`` citations in living docs must be inside the file.

    Scans only ``docs/guides``, ``docs/decisions``, and ``docs/audits``. Does not
    catch wrong-but-in-range line numbers — that mitigation is T5 (figure +
    command), not this check.
    """
    errors: list[str] = []
    for root in FILE_LINE_CORPUS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in FILE_LINE_RE.finditer(text):
                cited, line_s = match.group(1), match.group(2)
                line_no = int(line_s)
                target = resolve_cited_path(cited)
                if target is None:
                    continue
                try:
                    n_lines = sum(1 for _ in target.open(encoding="utf-8", errors="ignore"))
                except OSError:
                    continue
                if line_no < 1 or line_no > n_lines:
                    errors.append(
                        f"(f) {path}: cites `{cited}:{line_no}` but "
                        f"{target} has {n_lines} lines."
                    )
    return sorted(set(errors))


def parse_agent_frontmatter_fields(text: str) -> dict[str, str]:
    """Return ``model`` / ``tier`` from the leading ``---`` YAML fence, if any."""
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return {}
    return dict(AGENT_TIER_MODEL_RE.findall(match.group(1)))


def check_agents_model_tier_map() -> list[str]:
    """(g) ``agents/*.md`` frontmatter ``model:`` must match the Claude tier map.

    Plan 035 named this check ``(f)``; letter ``(f)`` is already
    ``check_file_line_citations`` (Sprint 029). Implemented as ``(g)``.
    Claude Code side only (D15) — Cursor cells are not checked.
    """
    if not MODEL_TIERS_FILE.is_file():
        return [f"(g) {MODEL_TIERS_FILE} is missing."]
    tiers = json.loads(MODEL_TIERS_FILE.read_text(encoding="utf-8")).get("tiers", {})
    errors: list[str] = []
    agents_dir = Path("agents")
    if not agents_dir.is_dir():
        return errors
    for path in sorted(agents_dir.glob("*.md")):
        fields = parse_agent_frontmatter_fields(
            path.read_text(encoding="utf-8", errors="ignore")
        )
        tier = fields.get("tier")
        model = fields.get("model")
        if tier is None and model is None:
            continue
        if tier is not None and model is None:
            errors.append(
                f"(g) {path}: has tier `{tier}` but no model: "
                f"(required when tier is present)."
            )
            continue
        if tier is None:
            # model without tier — skip (both required only when tier is set).
            continue
        spec = tiers.get(tier)
        if spec is None:
            errors.append(
                f"(g) {path}: unknown tier `{tier}` "
                f"(not in {MODEL_TIERS_FILE})."
            )
            continue
        expected = spec.get("claude_code", {}).get("model")
        if expected is None:
            errors.append(
                f"(g) {path}: tier `{tier}` has no claude_code.model in "
                f"{MODEL_TIERS_FILE}."
            )
            continue
        if model != expected:
            errors.append(
                f"(g) {path}: frontmatter model `{model}` != map `{expected}` "
                f"for tier `{tier}`."
            )
    return errors


def main() -> int:
    # Framework-scoped: every path below is this repository's. See
    # `scripts/_root.py` — the cwd is set once so the messages stay relative and
    # a path added later cannot silently reintroduce the cwd dependency.
    os.chdir(agents_root())

    corpus = loadable_text()
    errors = (
        check_rules_reachable(corpus)
        + check_templates_exist(corpus)
        + check_rule_citations()
        + check_invocation_coverage(corpus)
        + check_rule_triggers_sync()
        + check_file_line_citations()
        + check_agents_model_tier_map()
    )
    if errors:
        for e in errors:
            print(f"❌ {e}", file=sys.stderr)
        return 2
    print(
        "✅ Reference integrity OK — rules reachable, templates exist, "
        "citations resolve, every mechanism has an invoker, "
        "living file:line citations in range, "
        "profile model↔tier map."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
