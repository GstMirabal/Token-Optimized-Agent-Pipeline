---
description: "Protocolo Post-Sprint de Purga y Extracción de Memoria a Largo Plazo"
version: 1.0.0
---

# 🧠 Workflow: Extractor de Amnesia y Conocimiento

Este es el **Protocolo de Cierre Obligatorio** para todos los Sprints de Universal-Agents. Dado que nuestra arquitectura dicta que las carpetas de estado temporal (`.agent_state/session_{UID}/`) deben ser destruidas para prevenir alucinaciones cruzadas y ahorro de tokens, este *Workflow* se asegura de destilar las "lecciones aprendidas" empujándolas a la memoria persistente del sistema (`/knowledge/`) antes de ejecutar el borrado físico de la Caché.

## Fase 1: Escaneo Retrospectivo (Brain Drain)
Cuando el Director ordene `/save_knowledge` o declare el Sprint como terminado, el Orquestador leerá en frío el `task.md` y su historial de comandos, e identificará:
1.  **Workarounds Críticos:** Soluciones creativas a librerías rebeldes (ej. "FastAPI chocó con Pydantic V2, se arregló haciendo X").
2.  **Arquitectura Asentada:** (ej. "Se decidió usar `envtoml` en lugar de `dotenv` por X motivo").
3.  **Bugs Complejos:** Errores de Linters o de Tipado que costaron más de 2 intentos solucionar en la sesión.

## Fase 2: Destilación en Markdown
El Orquestador creará o actualizará un archivo en la ruta del submódulo `.agents/knowledge/<tema_del_sprint>.md`.
El formato exigido por el *Agente Constitucional* es implacable:
- **Título:** Breve y descriptivo.
- **Contexto (1 párrafo):** ¿Qué estábamos intentando hacer?
- **El Bloqueo:** ¿Qué falló o qué obstáculo surgió (incluir error del traceback si aplica)?
- **La Solución (Snippets):** El código puro que lo arregló.

## Fase 3: La Purga de Sesión (Amnesia)
Una vez validados y guardados los archivos en `/knowledge/`, el Orquestador borrará implacablemente los archivos temporales (su propia mente a corto plazo):
```bash
rm -rf .agent_state/session_{UID}/
```
**Regla de Hierro:** Queda estrictamente prohibido mantener carpetas de sesión operativas de días anteriores. El proyecto debe quedar inmaculado.

## Fase 4: Actualización de la Matriz Central
Dado que `.agents/` funciona distribuyéndose a través de Submódulos Git, el Orquestador armará el comando final para que el Director consolide el nuevo conocimiento globalmente y todos los otros repositorios lo hereden:
```bash
cd .agents
git add knowledge/
git commit -m "docs(knowledge): extract bugs and heuristics from active session"
```

**Nota para el Enjambre:** Este Workflow garantiza que Universal-Agents amanezca mañana más inteligente que hoy, reteniendo el conocimiento vital sin arrastrar basura temporal, tokens muertos, ni alucinaciones operacionales a la siguiente sesión.
