"""
🛡️ Token-Optimized Agent Pipeline: JS/TS Standardizer (Native)
Agnostic health-check script for JS/TS repositories to ensure framework compliance.
"""

import os
import json
import subprocess

def _should_skip_dir(root: str) -> bool:
    """Reports whether a walked directory is an excluded build/tooling path.

    Args:
        root: The directory path currently visited by `os.walk`.

    Returns:
        True when `root` contains one of the excluded path fragments.
    """
    return any(x in root for x in ["node_modules", ".git", ".agents", "dist", "build"])


def _js_files_in_root(root: str, files: list[str]) -> list[str]:
    """Full paths, under `root`, of every `.js`/`.ts` file in `files`.

    Args:
        root: The directory these `files` were listed from.
        files: Bare filenames as returned by `os.walk` for `root`.

    Returns:
        Full paths for the files ending in `.js` or `.ts`.
    """
    return [os.path.join(root, f) for f in files if f.endswith((".js", ".ts"))]


def _iter_js_files(directory: str):
    """Yields full paths of every `.js`/`.ts` file under `directory`.

    Args:
        directory: The root directory to walk.

    Yields:
        Full paths for files that pass `_should_skip_dir` and the `.js`/`.ts`
        suffix check.
    """
    for root, _, files in os.walk(directory):
        if _should_skip_dir(root):
            continue
        yield from _js_files_in_root(root, files)


def _file_has_jsdoc(file_path: str) -> bool:
    """Reports whether a file contains `@param` or `@returns`.

    Args:
        file_path: Path of the file to read.

    Returns:
        True when the file content contains `@param` or `@returns`, False
        otherwise, including when the file cannot be read. The bare
        `except:` below is pre-existing (ruff `E722`) and is Sprint 054's
        scope; preserved unchanged here per the Sprint 052 refactor charter.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return "@param" in content or "@returns" in content
    except:
        pass
    return False


def check_jsdoc(directory):
    print("🔍 Auditing JSDoc Compliance...")
    # Basic heuristic: check if functions in .js/.ts files have @param or @returns
    jsdoc_found = False
    for file_path in _iter_js_files(directory):
        if _file_has_jsdoc(file_path):
            jsdoc_found = True
            print(f"✅ Found JSDoc in: {os.path.basename(file_path)}")
    return jsdoc_found

def main():
    root_path = os.getcwd()
    print(f"🚀 Initializing JS/TS Standardization Audit...")

    # Ecosystem Discovery
    ecosystem = {
        "ESLint": [".eslintrc", ".eslintrc.json", ".eslintrc.js", "eslint.config.js"],
        "Prettier": [".prettierrc", "prettier.config.js"],
        "TypeScript": ["tsconfig.json"],
        "Biome": ["biome.json"]
    }

    found = []
    for name, files in ecosystem.items():
        if any(os.path.exists(f) for f in files):
            found.append(name)
    
    print(f"📁 Metadata Discovery: {found}")

    # JSDoc Check (Governance Rule)
    has_jsdoc = check_jsdoc(".")
    
    print("\n🏁 --- [Final JS/TS Summary] ---")
    if found:
        print(f"✅ Tools configured: {', '.join(found)}")
    else:
        print("⚠️ No standard JS linting tools found.")

    if has_jsdoc:
        print("✅ JSDoc implementation detected (Compliance OK).")
    else:
        print("❌ FAIL: No JSDoc patterns found. Governance Phase 1 requires JSDoc/@param usage.")

if __name__ == "__main__":
    main()
