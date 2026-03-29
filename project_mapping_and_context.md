# Mapeo y Contexto de Proyectos
Reglas exclusivas del sistema de archivos y topología local del SO.

## 1. Ubicación y Espacio Base
- **Raíz Única:** Todos los repositorios residen forzosamente en `/Users/gstmirabal/Developer/`.

## 2. Entornos Virtuales (venv)
- **Aislamiento:** Cada proyecto aloja su propio directorio `./venv/` en la raíz. Prohibida toda instalación global (`pip install`).
- **Path Anchor:** Los agentes deben posicionarse obligatoriamente con `cd` en la raíz del proyecto antes de ejecutar cualquier herramienta.
- **Ejecución Binaria:** Prohibido usar comandos globales (`python`, `pip`). Llamar imperativamente a los binarios locales (ej. `./venv/bin/python`, o `./node_modules/.bin/`).

## 3. Disposición del Código (Src Layout)
- **Lógica Central:** `/src/`
- **Framework de Pruebas:** `/tests/`
- **Componentes Web:** En arquitecturas web: `/static/` (recursos públicos) y `/media/` (archivos subidos de clientes, prohibidos en control de versiones).
- **Jupyter Notebooks:** Pruebas computacionales en Jupyter deben aislarse en `/notebooks/`.

## 4. Persistencia y Bases de Datos
- **Motor Exclusivo:** Uso estricto de `docker-compose.yml` para levantar PostgreSQL u otras infraestructuras.
- **Bind Mounts:** Mapeo de volúmenes de Bases de Datos obligatorio hacia directorios locales ocultos (ej. `./.docker-db-data`) para garantizar la persistencia de datos.
- **Archivos Temporales/Reportes:** La generación de archivos en masa (ETLs, PDFs) debe aislarse en `./data/output/` o `./tmp/`.
- **Git LFS:** Archivos pesados (>50MB, ej. modelos, grandes datasets CSV) deben forzosamente rastrearse mediante `git lfs track`.

## 5. Gobernanza de Repositorio
- `.python-version` anclado a la raíz del proyecto, especificando la versión base de Pyenv.
- `.gitignore` estricto, excluyendo inherentemente: `/venv/`, `.env`, `.agent_state/`, temporales, logs, y datasets (`/data/`).
- `Makefile` (o orquestador homólogo) mandatorio para centralizar comandos repetitivos (`make test`, `make db-up`).
- Directorio `/logs/` exclusivo para volcar trazas de ejecución en producción.
