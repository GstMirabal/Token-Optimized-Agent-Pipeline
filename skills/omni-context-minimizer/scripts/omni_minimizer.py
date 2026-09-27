import sys
import re
import ast

def _print_node_line(node: ast.AST, lines: list[str]) -> None:
    """Prints the source line for one AST node's header.

    Args:
        node: An AST node carrying a 1-based `lineno`.
        lines: The source file split into physical lines.
    """
    print(f"Line {node.lineno}: {lines[node.lineno - 1].strip()}")


def _print_class_methods(node: ast.ClassDef, lines: list[str]) -> int:
    """Prints every method header inside one class body.

    Args:
        node: The class definition to scan for methods.
        lines: The source file split into physical lines.

    Returns:
        The number of method headers printed.
    """
    matched = 0
    for subnode in node.body:
        if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
            print(f"Line {subnode.lineno}:     {lines[subnode.lineno - 1].strip()}")
            matched += 1
    return matched


def _process_top_level_node(node: ast.AST, lines: list[str]) -> int:
    """Prints and counts one top-level AST node if it is structural.

    Args:
        node: One statement from the module body.
        lines: The source file split into physical lines.

    Returns:
        The number of structural lines this node contributed (its own
        header, plus any class methods printed beneath it).
    """
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        _print_node_line(node, lines)
        matched = 1
        if isinstance(node, ast.ClassDef):
            matched += _print_class_methods(node, lines)
        return matched
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        _print_node_line(node, lines)
        return 1
    return 0


def parse_python_ast(filepath):
    """Uses native Python AST to perfectly extract classes and function signatures."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"[ERROR] Failed to parse Python AST: {e}")
        return

    print(f"--- [TOKEN-SAVER MAP] AST Skeleton of: {filepath} ---")
    lines = source.split('\n')
    print(f"[Total Physical Lines]: {len(lines)}\n")

    matched_lines = 0
    for node in tree.body:
        matched_lines += _process_top_level_node(node, lines)

    print(f"\n--- [OPTIMIZATION]: The file was reduced to {matched_lines} lines of pure AST structure. ---")

def _continue_multiline_block(
    idx: int, stripped: str, matched_lines: int, block_braces: int
) -> tuple[int, int, bool]:
    """Prints and accounts for one line while inside a multiline TS block.

    Args:
        idx: 1-based line number.
        stripped: The right-stripped line content.
        matched_lines: Running count of structural lines printed so far.
        block_braces: Running open-brace balance for the block.

    Returns:
        A 3-tuple of (new_matched_lines, new_block_braces, still_in_block).
    """
    print(f"Line {idx}: {stripped}")
    matched_lines += 1
    block_braces += stripped.count('{') - stripped.count('}')
    # Terminate block if braces close or we hit a semicolon (for types)
    still_in_block = not (block_braces <= 0 and ('{' not in stripped or '}' in stripped))
    return matched_lines, block_braces, still_in_block


def _start_ts_block(idx: int, stripped: str) -> tuple[bool, int]:
    """Prints one interface/type declaration line and opens block tracking.

    Args:
        idx: 1-based line number.
        stripped: The right-stripped line content.

    Returns:
        A 2-tuple of (in_block, block_braces) reflecting whether this
        declaration line opened a multiline block.
    """
    print(f"Line {idx}: {stripped}")
    if '{' in stripped and '}' not in stripped:
        return True, 1
    if stripped.endswith('='):  # Multiline type alias
        return True, 0
    return False, 0


def parse_heuristic(filepath):
    """Enhanced Heuristic Extractor with JS/TS/TSX State Machine for Interfaces/Types."""
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    print(f"--- [TOKEN-SAVER MAP] Structural Skeleton of: {filepath} ---")
    print(f"[Total Physical Lines]: {len(lines)}\n")

    matched_lines = 0
    in_block = False
    block_braces = 0

    # 1. Broad Declarations (functions, classes, structs)
    decl_pattern = re.compile(r'^\s*(export\s+|default\s+)*(public\s+|private\s+|protected\s+)*(static\s+)*(async\s+)*(class|function|func|fn|struct|enum)\s+\w+')
    
    # 2. JS/TS Arrow Functions (Including React Components with generics)
    arrow_pattern = re.compile(r'^\s*(export\s+)*(const|let|var)\s+\w+\s*(:\s*[A-Za-z0-9_.<>]+)?\s*=\s*(async\s*)?(\(|<)')
    
    # 3. TS Interfaces & Types (Starts block extraction)
    ts_block_pattern = re.compile(r'^\s*(export\s+)?(interface|type)\s+\w+')
    
    # 4. Imports & Decorators
    import_pattern = re.compile(r'^\s*(import|from|require|#include|using|package)\b')
    decorator_pattern = re.compile(r'^\s*@(?!.*\b(param|returns|type)\b)')

    for idx, line in enumerate(lines, 1):
        stripped = line.rstrip()
        if not stripped:
            continue

        # If inside a multiline TS Interface or Type definition
        if in_block:
            matched_lines, block_braces, in_block = _continue_multiline_block(
                idx, stripped, matched_lines, block_braces
            )
            continue

        if ts_block_pattern.search(stripped):
            matched_lines += 1
            in_block, block_braces = _start_ts_block(idx, stripped)
            continue

        if decl_pattern.search(stripped) or import_pattern.search(stripped) or arrow_pattern.search(stripped) or decorator_pattern.search(stripped):
            print(f"Line {idx}: {stripped}")
            matched_lines += 1

    print(f"\n--- [OPTIMIZATION]: The file was reduced to {matched_lines} lines of pure structure. ---")

def parse_file(filepath):
    try:
        if filepath.endswith('.py'):
            parse_python_ast(filepath)
        else:
            parse_heuristic(filepath)
    except Exception as e:
        print(f"[ERROR]: Failed to process file {filepath} - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Critical Usage: python omni_minimizer.py <absolute_file_path>")
        sys.exit(1)
    parse_file(sys.argv[1])
