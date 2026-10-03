"""
🛡️ Token-Optimized Agent Pipeline: Environment Shielding Auditor (3rd-party)
Agnostic security check script for avoiding PII leaks and hardcoded secrets.
"""

import logging
import os
import re
from collections.abc import Iterable, Iterator

logger = logging.getLogger(__name__)

# Secret Patterns (High-level samples)
SECRET_PATTERNS = {
    "Generic API Key": r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|secret[_-]?key)['\"]?\s*[:=]\s*['\"]?[a-z0-9+/=]{16,}['\"]?",
    "JWT Token": r"ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
    "Slack Webhook": r"https://hooks\.slack\.com/services/T[A-Z0-9_]{8}/B[A-Z0-9_]{8}/[A-Za-z0-9_]{24}",
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Generic Password": r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[a-z0-9@#$%^&*()_+]{8,}['\"]?"
}

# Credentials live in configuration far more often than in source, and the
# original list read source only: Compose, Helm values, Terraform, `.ini`,
# `.cfg`, `.conf` and `.toml` were all unread (F-086-S1). `.example` covers the
# `config.toml.example` form the sanctioned RA-09 pattern uses.
# `.env.example` is deliberately absent: `endswith` is suffix matching, so
# `.example` already covers it, and keeping both would be an entry that can
# never be the one that matched.
SCANNED_SUFFIXES = (
    ".py", ".js", ".ts", ".json", ".env", ".sh", ".bash",
    ".yml", ".yaml", ".toml", ".cfg", ".ini", ".conf", ".tf", ".example",
)

# Files whose whole name is the identifier: a suffix test cannot see them,
# because they have no suffix. `docker-compose.yml` is already reachable via
# `.yml` and is named anyway, so grepping this tuple answers the question of
# whether Compose is covered.
SCANNED_NAMES = ("Dockerfile", "Makefile", "docker-compose.yml")

# `Dockerfile.prod` and `api.Dockerfile`: splitting the build file leaves an
# affix that is not a format suffix, so neither test above sees it. Matched
# here so this auditor and hooks/on_commit.py agree on what a build file is
# called — the two halves of this unit disagreed until the gates said so, in
# two successive rounds.
BUILD_FILE_NAME = "dockerfile"


def is_scanned(filename: str) -> bool:
    """Reports whether a file is one this auditor reads.

    Comparison is lowercased throughout: `endswith` is case-sensitive, so
    `values.YAML` was skipped here while hooks/on_commit.py, which lowercases,
    read it — the same rule disagreeing with itself across the two halves.

    Args:
        filename: Bare filename, without its directory.

    Returns:
        True when the file matches a scanned suffix, an exact name, or one of
        the container build-file spellings.
    """
    lowered = filename.lower()
    return (
        lowered.endswith(SCANNED_SUFFIXES)
        or lowered in tuple(n.lower() for n in SCANNED_NAMES)
        or lowered == BUILD_FILE_NAME
        or lowered.startswith(f"{BUILD_FILE_NAME}.")
        or lowered.endswith(f".{BUILD_FILE_NAME}")
    )


def _should_skip_dir(root: str) -> bool:
    """Reports whether a walked directory is an excluded infrastructure path.

    Args:
        root: The directory path currently visited by `os.walk`.

    Returns:
        True when `root` contains one of the excluded path fragments.
    """
    return any(x in root for x in [".git", ".agents", "venv", "node_modules", ".agent_state"])


def _scanned_files_in_root(root: str, files: list[str]) -> list[str]:
    """Full paths, under `root`, of every file `is_scanned` accepts.

    Args:
        root: The directory these `files` were listed from.
        files: Bare filenames as returned by `os.walk` for `root`.

    Returns:
        Full paths for the files that `is_scanned` accepts.
    """
    return [os.path.join(root, f) for f in files if is_scanned(f)]


def _iter_scanned_files(directory: str) -> Iterator[str]:
    """Yields full paths of every scan-eligible file under `directory`.

    Args:
        directory: The root directory to walk.

    Yields:
        Full paths for files that pass `_should_skip_dir` and `is_scanned`.
    """
    for root, _, files in os.walk(directory):
        if _should_skip_dir(root):
            continue
        yield from _scanned_files_in_root(root, files)


def _match_patterns(file_path: str, line_no: int, line: str) -> list[str]:
    """Leak report strings for every SECRET_PATTERNS match on one line.

    Args:
        file_path: Path of the file the line was read from.
        line_no: 1-based line number of `line` within `file_path`.
        line: The line content to test against SECRET_PATTERNS.

    Returns:
        One formatted leak report string per matching pattern.
    """
    return [
        f"🚨 {name} found: {file_path} (Line {line_no})"
        for name, pattern in SECRET_PATTERNS.items()
        if re.search(pattern, line)
    ]


def _leaks_in_lines(file_path: str, lines: Iterable[str]) -> list[str]:
    """Leak report strings for every secret-pattern match across `lines`.

    Args:
        file_path: Path of the file `lines` were read from.
        lines: An iterable of line strings, 1-indexed by enumeration.

    Returns:
        The concatenated leak reports for every matching line.
    """
    found = []
    for i, line in enumerate(lines, 1):
        found.extend(_match_patterns(file_path, i, line))
    return found


def _find_leaks_in_file(file_path: str) -> list[str]:
    """Leak report strings found inside one file.

    Args:
        file_path: Path of the file to open and scan.

    Returns:
        The leak reports for `file_path`, or an empty list when the file
        cannot be read (unreadable files are silently skipped).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return _leaks_in_lines(file_path, f)
    except (OSError, ValueError) as exc:
        # Unreadable or undecodable files are skipped, not fatal.
        logger.debug("Skipping unreadable file %s: %s", file_path, exc)
    return []


def scan_files(directory):
    leaks = []
    for file_path in _iter_scanned_files(directory):
        leaks.extend(_find_leaks_in_file(file_path))
    return leaks

def _check_env_in_gitignore(content: str) -> bool:
    """Reports and prints whether `.env` appears in gitignore content.

    Args:
        content: The full text content of the `.gitignore` file.

    Returns:
        True when `.env` is present in `content`, False otherwise.
    """
    if ".env" in content:
        print("✅ .env is present in .gitignore.")
        return True
    print("❌ .env is NOT in .gitignore! This is a Major Security Risk.")
    return False


def check_gitignore():
    if not os.path.exists(".gitignore"):
        print("⚠️ .gitignore not found. Skipping check.")
        return None
    with open(".gitignore", "r") as f:
        content = f.read()
    return _check_env_in_gitignore(content)

def main():
    print("🚀 Initializing Environment Shielding Audit...")
    
    # Gitignore Validation
    check_gitignore()
    
    # Secret Scanning
    print("\n🔍 Scanning for Hardcoded Secrets (Wait brief moment)...")
    leaks = scan_files(".")
    
    if leaks:
        print(f"\n🚨 {len(leaks)} Potential Leaks Detected:")
        for leak in leaks:
            print(leak)
    else:
        print("\n✅ No hardcoded secrets found in source code.")

    print("\n🏁 --- [Final Shielding Summary] ---")
    if leaks:
        print("❌ FAIL: Secrets detected or environment is vulnerable.")
    else:
        print("🏆 Environment and Secrets are currently Certified.")

if __name__ == "__main__":
    main()
