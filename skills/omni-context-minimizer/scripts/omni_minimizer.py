import sys
import re

def parse_file(filepath):
    """
    Universal Heuristic Extractor. Scans a file and returns a cognitive "skeleton"
    composed solely of Imports, Function Signatures (Def, Arrow, Func, Fn), and Structures (Classes, Structs).
    Saves 90% of context by not loading the logical blocks of function bodies.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Regex Patterns to hunt main architectures ignoring bodies
        patterns = [
            # 1. Declaration keywords (Python, JS/TS, Go, Rust, Java, C++)
            r'^\s*(export\s+|default\s+)*(public\s+|private\s+|protected\s+)*(static\s+)*(async\s+)*(class|def|function|func|fn|struct|interface|type|enum)\s+\w+',
            # 2. Arrow Functions (JS/TS) e.g., const myFunction = async (args) => {
            r'^\s*(export\s+)*(const|let|var)\s+\w+\s*=\s*(async\s*)?(\([^)]*\)|\w+)\s*=>',
            # 3. Imports / Dependencies
            r'^\s*(import|from|require|#include|using|package)\b',
            # 4. Decorators (e.g., @app.route, @Component) excluding JSDoc
            r'^\s*@(?!.*\b(param|returns|type)\b)'
        ]
        
        master_regex = re.compile('|'.join(patterns))
        
        print(f"--- [TOKEN-SAVER MAP] Architectural Skeleton of: {filepath} ---")
        print(f"[Total Physical Lines]: {len(lines)}\n")
        
        matched_lines = 0
        for idx, line in enumerate(lines, 1):
            # Clean newline for processing
            stripped = line.rstrip()
            if master_regex.search(stripped):
                print(f"Line {idx}: {stripped}")
                matched_lines += 1
                
        print(f"\n--- [OPTIMIZATION]: The file was reduced to {matched_lines} lines of pure structure. ---")
                
    except UnicodeDecodeError:
        print(f"[ERROR]: The file {filepath} appears to be binary or has an incomprehensible encoding.")
    except Exception as e:
        print(f"[ERROR]: Failed to read file {filepath} - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Critical Usage: python omni_minimizer.py <absolute_file_path>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    parse_file(target_file)
