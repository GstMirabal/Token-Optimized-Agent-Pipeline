"""Config-driven README tag-substitution engine.

Renders a README template (any file containing the `{{TAG}}` placeholders
documented below) by resolving its tags against a host's identity.config.json
— or, when this script is running from inside the `.agents` nucleus itself
(the framework's own repo, not a submodule checkout), against
config/framework_identity.json instead, remapped through NUCLEUS_FIELD_MAP.

Usage:
    python3 render_readme.py <template_path> --out <path> [--host-config <path>]

Tags substituted (host- or nucleus-resolved):
    {{OWNER_NAME}} {{OWNER_EMAIL}} {{OWNER_LINKEDIN_URL}} {{OWNER_X_URL}}
    {{REPO_SLUG}} {{REPO_URL}} {{PROJECT_NAME}} {{PROJECT_DESCRIPTION}}
    {{PROJECT_HOOK}} {{INSTITUTIONAL_IDENTITY}} {{GOVERNED_BY_AGENTS}}
    {{BANNER_PATH}} {{CREDIT_LINE}}

Tags substituted always from config/framework_identity.json, regardless of
host:
    {{FRAMEWORK_AUTHOR_NAME}} {{FRAMEWORK_REPO_URL}}

Conditional blocks (marker comments, stripped or removed wholesale):
    <!-- BANNER_START --> ... <!-- BANNER_END -->
    <!-- GOVERNED_BLOCK_START --> ... <!-- GOVERNED_BLOCK_END -->
"""
import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCRIPT_DIR.parent

BANNER_START = "<!-- BANNER_START -->"
BANNER_END = "<!-- BANNER_END -->"
GOVERNED_BLOCK_START = "<!-- GOVERNED_BLOCK_START -->"
GOVERNED_BLOCK_END = "<!-- GOVERNED_BLOCK_END -->"

# Maps a HOST-shaped identity field to its FRAMEWORK-shaped equivalent, used
# only when this script detects it is running inside the .agents nucleus.
NUCLEUS_FIELD_MAP = {
    "owner_name": "framework_author_name",
    "owner_email": "framework_author_email",
    "owner_linkedin_url": "framework_author_linkedin_url",
    "owner_x_url": "framework_author_x_url",
    "repo_slug": "framework_repo_slug",
    "banner_path": "framework_banner_path",
    "project_name": "framework_project_name",
    "project_description": "framework_project_description",
    "project_hook": "framework_project_hook",
}

REQUIRED_FIELDS = ("owner_name", "repo_slug", "project_name")


def is_nucleus_mode() -> bool:
    """Detects whether this script runs inside the .agents nucleus itself.

    Uses the exact criterion install_claude.py's main() applies: the repo
    root that contains this script (AGENTS_DIR) has its OWN real `.git`
    directory, as opposed to being checked out as a submodule (where `.git`
    is a plain gitlink file, not a directory).

    Returns:
        True if AGENTS_DIR owns a real `.git` directory (nucleus checkout).
    """
    return (AGENTS_DIR / ".git").is_dir()


def load_json(path: Path) -> dict:
    """Loads and parses a JSON file, failing loudly on any error.

    Args:
        path: Path to the JSON file to load.

    Returns:
        The parsed JSON content as a dict.
    """
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: could not read/parse {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def resolve_host_data(host_config_path: Path, framework_data: dict) -> dict:
    """Resolves the host-shaped identity dict, from a real host config or,
    in nucleus mode, remapped from framework_identity.json.

    Args:
        host_config_path: Where identity.config.json would live for a real
            host; ignored in nucleus mode.
        framework_data: Parsed content of config/framework_identity.json.

    Returns:
        A dict shaped like IDENTITY_TEMPLATE.json (host fields).
    """
    if is_nucleus_mode():
        mapped = {host_key: framework_data.get(fw_key, "")
                  for host_key, fw_key in NUCLEUS_FIELD_MAP.items()}
        mapped["governed_by_agents"] = False
        return mapped

    if not host_config_path.exists():
        print(f"ERROR: host config not found at {host_config_path}. "
              "Run install_claude.py first, or pass --host-config.", file=sys.stderr)
        sys.exit(1)
    return load_json(host_config_path)


def validate_required_fields(host_data: dict) -> None:
    """Aborts loudly if any mandatory identity field resolved empty.

    Args:
        host_data: The resolved host-shaped identity dict.
    """
    missing = [f for f in REQUIRED_FIELDS if not host_data.get(f)]
    if missing:
        print(f"ERROR: required field(s) empty after resolution: {', '.join(missing)}. "
              "Refusing to render a README with broken URLs.", file=sys.stderr)
        sys.exit(1)


def build_credit_line(nucleus: bool, framework_author_name: str, framework_repo_url: str) -> str:
    """Builds the fixed framework-credit line, in short or full wording.

    The short wording is used when nucleus mode was detected — the nucleus's
    own README already names its author elsewhere (e.g. a Contact section),
    so repeating the full name here would be redundant. The decision is
    driven directly by the nucleus-detection result, never by comparing
    owner/author name strings.

    Args:
        nucleus: Result of is_nucleus_mode().
        framework_author_name: framework_identity.json's framework_author_name.
        framework_repo_url: Derived https://github.com/{framework_repo_slug}.

    Returns:
        A single-line Markdown credit string.
    """
    if nucleus:
        return f"Built with the [Token-Optimized Agent Pipeline]({framework_repo_url}) framework."
    return (f"Built with the [Token-Optimized Agent Pipeline]({framework_repo_url}) framework, "
            f"by {framework_author_name}.")


def strip_marker_lines(text: str, start_marker: str, end_marker: str) -> str:
    """Removes only the marker comment lines, keeping the block's content.

    Args:
        text: The template text.
        start_marker: Opening marker comment, e.g. "<!-- BANNER_START -->".
        end_marker: Closing marker comment, e.g. "<!-- BANNER_END -->".

    Returns:
        The text with both marker lines deleted.
    """
    for marker in (start_marker, end_marker):
        text = re.sub(re.escape(marker) + r"\n?", "", text)
    return text


def strip_whole_block(text: str, start_marker: str, end_marker: str) -> str:
    """Removes a marker-delimited block entirely, markers included.

    No-op if the markers are absent from the template.

    Args:
        text: The template text.
        start_marker: Opening marker comment.
        end_marker: Closing marker comment.

    Returns:
        The text with the whole block (if present) removed.
    """
    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker) + r"\n?"
    return re.sub(pattern, "", text, flags=re.DOTALL)


def apply_banner_block(text: str, banner_path: str) -> str:
    """Resolves the conditional BANNER_START/BANNER_END block.

    Args:
        text: The template text.
        banner_path: Resolved banner_path, relative to the OUTPUT repo root.

    Returns:
        The text with the banner block resolved.
    """
    if banner_path:
        text = text.replace("{{BANNER_PATH}}", banner_path)
        return strip_marker_lines(text, BANNER_START, BANNER_END)
    return strip_whole_block(text, BANNER_START, BANNER_END)


def apply_governed_block(text: str, governed_by_agents: bool, framework_repo_url: str) -> str:
    """Resolves the conditional GOVERNED_BLOCK_START/END block and tag.

    Args:
        text: The template text.
        governed_by_agents: Resolved governed_by_agents flag.
        framework_repo_url: Derived https://github.com/{framework_repo_slug}.

    Returns:
        The text with the governed-by block/tag resolved.
    """
    if governed_by_agents:
        text = strip_marker_lines(text, GOVERNED_BLOCK_START, GOVERNED_BLOCK_END)
        badge = (f"> Governed by the [Token-Optimized Agent Pipeline]({framework_repo_url}) "
                 "governance framework.")
        return text.replace("{{GOVERNED_BY_AGENTS}}", badge)
    text = strip_whole_block(text, GOVERNED_BLOCK_START, GOVERNED_BLOCK_END)
    return text.replace("{{GOVERNED_BY_AGENTS}}", "")


def build_tag_map(host_data: dict, framework_data: dict, nucleus: bool) -> dict:
    """Builds the flat {{TAG}} -> value map for the plain (non-block) tags.

    Args:
        host_data: Resolved host-shaped identity dict.
        framework_data: Parsed config/framework_identity.json.
        nucleus: Result of is_nucleus_mode().

    Returns:
        A dict mapping literal `{{TAG}}` strings to their replacement text.
    """
    repo_url = f"https://github.com/{host_data['repo_slug']}"
    framework_repo_url = f"https://github.com/{framework_data.get('framework_repo_slug', '')}"
    return {
        "{{OWNER_NAME}}": host_data.get("owner_name", ""),
        "{{OWNER_EMAIL}}": host_data.get("owner_email", ""),
        "{{OWNER_LINKEDIN_URL}}": host_data.get("owner_linkedin_url", ""),
        "{{OWNER_X_URL}}": host_data.get("owner_x_url", ""),
        "{{REPO_SLUG}}": host_data.get("repo_slug", ""),
        "{{REPO_URL}}": repo_url,
        "{{PROJECT_NAME}}": host_data.get("project_name", ""),
        "{{PROJECT_DESCRIPTION}}": host_data.get("project_description", ""),
        "{{PROJECT_HOOK}}": host_data.get("project_hook", ""),
        "{{INSTITUTIONAL_IDENTITY}}": host_data.get("project_name", ""),
        "{{FRAMEWORK_AUTHOR_NAME}}": framework_data.get("framework_author_name", ""),
        "{{FRAMEWORK_REPO_URL}}": framework_repo_url,
        "{{CREDIT_LINE}}": build_credit_line(
            nucleus, framework_data.get("framework_author_name", ""), framework_repo_url),
    }


def render(template_text: str, host_data: dict, framework_data: dict, nucleus: bool) -> str:
    """Renders the full template: conditional blocks first, then flat tags.

    Args:
        template_text: Raw template file content.
        host_data: Resolved host-shaped identity dict.
        framework_data: Parsed config/framework_identity.json.
        nucleus: Result of is_nucleus_mode().

    Returns:
        The fully rendered README text.
    """
    framework_repo_url = f"https://github.com/{framework_data.get('framework_repo_slug', '')}"
    text = apply_banner_block(template_text, host_data.get("banner_path", ""))
    text = apply_governed_block(text, bool(host_data.get("governed_by_agents", False)),
                                 framework_repo_url)
    for tag, value in build_tag_map(host_data, framework_data, nucleus).items():
        text = text.replace(tag, value)
    return text


def main() -> int:
    """CLI entry point.

    Returns:
        Process exit code (0 on success, 1 on validation/IO failure).
    """
    parser = argparse.ArgumentParser(description="Render a README template from identity config.")
    parser.add_argument("template_path", help="Path to the README template to render.")
    parser.add_argument("--out", required=True, help="Path to write the rendered README to.")
    parser.add_argument("--host-config", help="Path to identity.config.json (default: ./identity.config.json).")
    args = parser.parse_args()

    template_path = Path(args.template_path)
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        return 1

    nucleus = is_nucleus_mode()
    framework_data = load_json(AGENTS_DIR / "config" / "framework_identity.json")
    host_config_path = Path(args.host_config) if args.host_config else Path.cwd() / "identity.config.json"
    host_data = resolve_host_data(host_config_path, framework_data)
    validate_required_fields(host_data)

    rendered = render(template_path.read_text(), host_data, framework_data, nucleus)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_path.write_text(rendered)
    except OSError as exc:
        print(f"ERROR: could not write {out_path}: {exc}", file=sys.stderr)
        return 1

    print(f"README rendered to {out_path} (nucleus_mode={nucleus})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
