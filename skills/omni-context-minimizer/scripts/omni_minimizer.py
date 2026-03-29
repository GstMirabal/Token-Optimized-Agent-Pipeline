import sys
import re

def parse_file(filepath):
    """
    Extrator Heurístico Universal. Escanea un archivo y devuelve un "esqueleto" cognitivo
    compuesto únicamente de Imports, Firmas de Funciones (Def, Arrow, Func, Fn) y Estructuras (Classes, Structs).
    Ahorra el 90% del contexto al no cargar los bloques lógicos de los cuerpos de las funciones.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Patrones Regex para cazar las arquitecturas principales ignorando los cuerpos
        patterns = [
            # 1. Palabras clave de declaración (Python, JS/TS, Go, Rust, Java, C++)
            r'^\s*(export\s+|default\s+)*(public\s+|private\s+|protected\s+)*(static\s+)*(async\s+)*(class|def|function|func|fn|struct|interface|type|enum)\s+\w+',
            # 2. Funciones Flecha / Arrow Functions (JS/TS) e.g., const myFunction = async (args) => {
            r'^\s*(export\s+)*(const|let|var)\s+\w+\s*=\s*(async\s*)?(\([^)]*\)|\w+)\s*=>',
            # 3. Importaciones / Dependencias
            r'^\s*(import|from|require|#include|using|package)\b',
            # 4. Decoradores (ej. @app.route, @Component) excluyendo JSDoc
            r'^\s*@(?!.*\b(param|returns|type)\b)'
        ]
        
        master_regex = re.compile('|'.join(patterns))
        
        print(f"--- [TOKEN-SAVER MAP] Esqueleto Arquitectónico de: {filepath} ---")
        print(f"[Total Líneas Físicas]: {len(lines)}\n")
        
        matched_lines = 0
        for idx, line in enumerate(lines, 1):
            # Limpiamos el salto de línea para procesar
            stripped = line.rstrip()
            if master_regex.search(stripped):
                print(f"Línea {idx}: {stripped}")
                matched_lines += 1
                
        print(f"\n--- [OPTIMIZACIÓN]: Se redujo el archivo a {matched_lines} líneas de estructura pura. ---")
                
    except UnicodeDecodeError:
        print(f"[ERROR]: El archivo {filepath} parece ser binario o tener una codificación incomprensible.")
    except Exception as e:
        print(f"[ERROR]: Fallo en la lectura del archivo {filepath} - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso Crítico: python omni_minimizer.py <ruta_absoluta_del_archivo>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    parse_file(target_file)
