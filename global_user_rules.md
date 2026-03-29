# Antigravity Global User Rules
Reglas de sintaxis, calidad y comunicación.

## 1. Código y Dialecto
- **Nomenclatura Estándar:** Usar PEP 8 para Python (`snake_case` en variables/funciones, `PascalCase` en clases, `UPPER_SNAKE_CASE` en constantes) y el estándar nativo para JS/TS (`camelCase` en funciones/variables).
- **Linters:** `ruff` (Python), `eslint/prettier` (JS/TS).
- **Tipado:** Tipado estricto obligatorio (`Type Hinting`, TypeScript).
- **Documentación de Código:** Uso de *Google Style Docstrings* para Python (`Args:`, `Returns:`) y *JSDoc* obligatorio para JS/TS (`@param`, `@returns`).
- **Rutas:** Prohibido usar rutas absolutas (hardcoded). Usar `pathlib` dinámico.
- **Manejo de Excepciones:** Prohibida la captura genérica (`except Exception:`). Instanciar forzosamente la excepción específica al origen (ej. `except ValueError:`). Prohibido silenciar errores con `pass`.
- **Salida:** Usar `logging` nativo (`INFO`, `ERROR`). Prohibido `print()` en producción u operaciones automatizadas.
- **Complejidad Cognitiva y Refactorización:** El Agente debe disparar una "Alerta de Refactorización" en su informe si revisa un módulo cuyo anidamiento de código sea > 3 niveles (`if` en un `for` en un `while`) o cuyas funciones superen las 50 líneas.
- **Modularidad (DRY):** Extraer código repetido a funciones/clases genéricas.

## 2. Comunicación y Autonomía
- **Idioma del Código y Pizarra:** Inglés Técnico (variables, commits, `task.md`, `implementation_plan.md`).
- **Idioma del Chat:** Español (explicaciones, debate con el usuario).
- **Rol del Mentor y Cuarentena de Código:** La Fase 1 (Debate) es táctica y arquitectónica. El Agente Principal tiene **prohibido** inyectar en el chat bloques de código resuelto mayores a 10 líneas durante la discusión. Debate las ideas y somete al usuario un listado numérico de pasos para su ejecución.
- **Delegación Táctica:** Operaciones destructivas (eliminación de archivos, purgado de base de datos) o mutaciones masivas están bloqueadas. Requerirán la autorización o uso explícito de un *Workflow* con el flag `// turbo`.
- **Dependencias y Secretos:** Priorizar siempre la *"Standard Library"* nativa del lenguaje. Prohibido codificar claves o tokens en texto plano (*hardcodeados*). Uso exclusivo de `.env` o manejadores de secretos (`envtoml`).
