import sys
import re
import ast

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
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            print(f"Line {node.lineno}: {lines[node.lineno-1].strip()}")
            matched_lines += 1
            if isinstance(node, ast.ClassDef):
                for subnode in node.body:
                    if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        print(f"Line {subnode.lineno}:     {lines[subnode.lineno-1].strip()}")
                        matched_lines += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            print(f"Line {node.lineno}: {lines[node.lineno-1].strip()}")
            matched_lines += 1
            
    print(f"\n--- [OPTIMIZATION]: The file was reduced to {matched_lines} lines of pure AST structure. ---")

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
            print(f"Line {idx}: {stripped}")
            matched_lines += 1
            block_braces += stripped.count('{') - stripped.count('}')
            # Terminate block if braces close or we hit a semicolon (for types)
            if block_braces <= 0 and (not '{' in stripped or '}' in stripped):
                in_block = False
            continue

        if ts_block_pattern.search(stripped):
            print(f"Line {idx}: {stripped}")
            matched_lines += 1
            if '{' in stripped and not '}' in stripped:
                in_block = True
                block_braces = 1
            elif stripped.endswith('='): # Multiline type alias
                in_block = True
                block_braces = 0
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
