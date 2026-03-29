# Universal-Agents Global User Rules
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

## 2. Autonomía, Eficiencia y Zero-Trust
- **Ahorro de Tokens Imperativo (Lectura Cruda Prohibida):** Queda **ESTRICTAMENTE PROHIBIDO** leer archivos de código mayores a 200 líneas de forma directa para entender su contenido. El agente **OBLIGATORIAMENTE** ejecutará la skill universal `omni-context-minimizer` primero para extraer el esqueleto estructural, ubicará la línea exacta de interés en el índice devuelto de la consola y procederá sólo entonces a aislar su lectura sobre ese segmento. Ignorar esta métrica provoca el cierre táctico inmediato.
- **Idioma del Código y Pizarra:** Inglés Técnico (variables, commits, `task.md`, `implementation_plan.md`).
- **Idioma del Chat:** Español (explicaciones, debate con el usuario).
- **Rol del Mentor y Cuarentena de Código:** La Fase 1 (Debate) es táctica y arquitectónica. El Agente Principal tiene **prohibido** inyectar en el chat bloques de código resuelto mayores a 10 líneas durante la discusión. Debate las ideas y somete al usuario un listado numérico de pasos para su ejecución.
- **Delegación Táctica:** Operaciones destructivas (eliminación de archivos, purgado de base de datos) o mutaciones masivas están bloqueadas. Requerirán la autorización o uso explícito de un *Workflow* con el flag `// turbo`.
- **Inyección de Skills Externas (`skills.sh`):** Se prioriza la aceleración del sistema integrando herramientas desde el repositorio maestro `skills.sh`. **CANDADO DE SEGURIDAD:** Queda terminalmente prohibida la ejecución, descarga o instalación autónoma de cualquier Skill por parte del Orquestador. La IA debe presentar el enlace de origen, el contenido propuesto y esperar a que el humano verifique la procedencia y lo autorice manualmente.
- **Auditoría de Dominio (Global vs Local):** Todo nuevo Skill propuesto pasará el *Test de Amnesia de 3 variables*: Si la herramienta sobrevive funcionalmente a la destrucción total del proyecto actual, se guardará en la matriz universal (`.agents/skills/`). Si su código está fuertemente acoplado a la lógica de negocio o bases de datos nativas del cliente, se aislará fuera del submódulo en un directorio local del proyecto (ej. `/.local_skills/`) para jamás contaminar la matriz global.
- **Dependencias y Secretos:** Uso IMPERATIVO de la *"Standard Library"* nativa del lenguaje como primera y única opción inicial. Queda prohibido añadir librerías externas de terceros a menos que se justifique que la refactorización manual excede el costo de la dependencia. Prohibido codificar claves o tokens en texto plano (*hardcodeados*). Uso exclusivo de `.env` o manejadores de secretos (`envtoml`).
