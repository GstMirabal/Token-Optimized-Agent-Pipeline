# Mapeo y Contexto de Proyectos
Reglas exclusivas del sistema de archivos y topología local del SO.

## 1. Ubicación y Espacio Base
- **Raíz Única:** Todos los repositorios deben residir forzosamente bajo un único directorio raíz u organizativo definido por el humano (ej. `$HOME/Developer/`).
- **Propagación del Repositorio `.agents` (Copia Bloqueada):** El directorio maestro de la IA (este repositorio) debe tratarse como el origen de verdad. Todo nuevo proyecto requiere integrar esta matriz obligatoriamente como **Submódulo de Git** (`git submodule add <url_o_path_del_repo_maestro>`). **LEY ABSOLUTA:** Queda rotundamente prohibido usar copia plana (`cp -R`); si se usa copia, los proyectos quedan desconectados de las mejoras globales.
- **Automejora y Centralización (Git):** Toda refactorización de estas reglas y manuales por parte del agente Auditor **ESTÁ ESTRICTAMENTE PROHIBIDA** sobre las copias locales de cada proyecto. Cualquier automejora a la constitución o habilidades debe ejecutarse y versionarse obligatoriamente sobre el repositorio maestro original para garantizar su herencia global.

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
- **Motor Exclusivo:** Despliegue de infraestructura (ej. PostgreSQL, Redis) mandatoriamente blindado a través de `docker-compose.yml`. Queda rotundamente prohibida la instalación de motores físicos de bases de datos en la capa del SO macOS.
- **Bind Mounts:** Mapeo de volúmenes de Bases de Datos obligatorio hacia directorios locales ocultos (ej. `./.docker-db-data`) para garantizar la persistencia de datos.
- **Archivos Temporales/Reportes:** La generación de archivos en masa (ETLs, PDFs) debe aislarse en `./data/output/` o `./tmp/`.
- **Git LFS:** Archivos pesados (>50MB, ej. modelos, grandes datasets CSV) deben forzosamente rastrearse mediante `git lfs track`.

## 5. Gobernanza de Repositorio
- `.python-version` anclado a la raíz del proyecto, especificando la versión base de Pyenv.
- `.gitignore` estricto, excluyendo inherentemente: `/venv/`, `.env`, `.agent_state/`, temporales, logs, y datasets (`/data/`).
- `Makefile` (u orquestador homólogo como `Taskfile`) es mandatorio para centralizar flujos repetitivos (`make test`, `make db-up`).
- Directorio `/logs/` exclusivo para volcar trazas de ejecución en producción.
