---
description: "Andamiaje Modular Múltiple (Generación y Configuración Dinámica de Proyectos)"
version: 1.0.0
---

# 🏗️ Workflow: Andamiaje Modular (Scaffolding Dinámico)

Este es el **Protocolo Maestro** para inicializar cualquier repositorio nuevo. Asegura que los requisitos del proyecto queden grabados permanentemente en caché, cumpliendo con la exigencia de ahorro del [Token-Saver], e instala la topología física bajo las leyes de la Constitución [Fases 1 y 2].

El agente encargado OBLIGATORIAMENTE seguirá esta secuencia en orden:

## Fase 1: Interrogatorio del Ecosistema (Mentor Mode)

El Mentor interroga al Director (el usuario) para definir 4 pilares tecnológicos:
1.  **Tecnología Base:** ¿Python (Data/Backend) o Node/JS (Frontend/Fullstack)? ¿Qué Framework exacto (ej. Django, FastAPI, React, NextJS)?
2.  **Manejador de Dependencias:** ¿Para Python (`venv` + `requirements.txt`, `poetry`, o `uv`)? ¿Para JS (`npm`, `yarn`, `pnpm`)?
3.  **Persistencia / Docker:** ¿Se levantará base de datos en `docker-compose.yml` (ej. PostgreSQL, Redis)?
4.  **Formatters/Linters:** (ej. `ruff`, `black`, `eslint`).

## Fase 2: Blindaje de Caché (Ahorro de Tokens)

Cualquier proyecto nacido de este Workflow DEBE blindar sus dependencias inmediatas para que futuros agentes tácticos no escaneen ciegamente el proyecto gastando cientos de miles de tokens:
- **Acción:** El Orquestador crea un archivo `project_stack.md` (o lo inyecta directamente en la caché obligatoria `.agent_state/session_{UID}/context.md`) detallando el Ecosistema, la Ruta Raíz, la BD instalada, y los Comandos de Testeo elegidos en la Fase 1.
- *Nota del Token-Saver:* Nadie lee este repositorio desde cero nunca más. Se consulta la caché.

## Fase 3: Despliegue Físico de Topología

Basándose en la Fase 1 y en el archivo `project_mapping_and_context.md`, el Orquestador ejecuta de manera secuencial (*usando comandos de terminal atómicos en bash separados por SafeToAutoRun* si corresponde):

1.  **Directorio y Propagación:**
    - Hacer `mkdir` de la subcarpeta del proyecto y moverse `cd`.
    - **LEY ABSOLUTA (Git Submodules):** Ejecutar `git init` inicial, seguido inmediatamente de `git submodule add <URL_O_RUTA_RAIZ_DEL_SISTEMA>/.agents .agents` para vincular el marco constitucional sin romper la cadena de actualizaciones globales.
2.  **Topología (Src Layout):**
    - Crear `/src`, `/tests`, `/data/output`.
    - Crear `/logs` (Trazas puras) y `.gitignore` (bloqueando obligatoriamente `.DS_Store`, `.agent_state/`, `/venv/`, `.env` y `/data/`).
3.  **Caja de Arena (Sandbox Virtual):**
    - Python: Instanciar `./venv/` y blindarlo. Configurar archivo `.python-version`.
    - Node: Ejecutar `npm init -y` o el equivalente blindado, dejando el directorio `node_modules`.
4.  **El Orquestador Humano (Makefile):**
    - Redactar un `Makefile` (o `taskfile`) instanciando dependencias comunes (`test`, `lint`, `db-up`) y, **obligatoriamente**, agregar el alias `make sync-ai` que invoque asíncronamente a `git submodule update --remote` para que el humano actualice el marco lógico de la IA con un clic.
5.  **Blindaje de Datos (Docker):**
    - Si se eligió BD, inyectar el archivo `docker-compose.yml` con el mapeo del volumen forzado a `./.docker-db-data`.

## Fase 4: Cierre con Auditoría

- El Orquestador pide a los 3 Auditores (Dual Constitucional + Proyecto, y Token-Saver) que verifiquen el árbol generado sin gastar contexto, únicamente revisando `project_stack.md`.
- Presenta el comando final de instanciación Git (`git init && git add . && git commit -m "chore: init modular scaffolding"`) para que el humano pulse el Botón Final de Aprobación.
