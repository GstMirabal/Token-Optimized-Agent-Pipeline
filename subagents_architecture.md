# Arquitectura y Flujo de Subagentes (Zero-Trust)
Reglas de operación estricta LLM-Terminal. Los agentes actúan bajo confinamiento absoluto.

## 1. Ciclo Vital Jerárquico (6 Fases)
Toda interacción de código debe escalar a través de estos actores y no alterar el orden:
1. **El Mentor (Debate):** Agente principal cognitivo. Discute con el usuario en español y nunca escribe código en local.
2. **El Orquestador (Plano):** Diseña técnicamente un `implementation_plan.md` (En Inglés) y delinea perfiles de Subagentes según el consenso del Mentor.
3. **El Auditor (Supervisión):** Robot observador. Revisa el plan del Orquestador contra las reglas de la carpeta `.agent/`. Lo tumba si rompe normas (Límite: 3 rechazos continuos).
4. **La Autorización (Humano):** El usuario evalúa visualmente el plan final purificado.
5. **La Matriz (Ejecución):** El Orquestador despliega al enjambre táctico de Subagentes para codificar.
   - **El Paso Cero (DevOps):** El Orquestador instala dependencias ciegas en el `venv` *antes* de que la Matriz instanciada opere.
   - **Freno absoluto (*WIP Safety Freeze*):** Si `git status` muestra cambios humanos sin comitear, el despliegue aborta para prevenir sobreescrituras ciegas.
6. **Bucle de Fallo (Rollback):** Si los Subagentes caen 3 veces por Excepciones Python o fallo de Linters, el Orquestador ejecuta un *Rollback* mecánico (deshace los pasos) y relata el evento en `task.md`.

## 2. Límite de Jurisdicciones
- **Docs Auditor:** Corrige documentación en Markdown (Nivel 1). Operación "Solo Lectura" sobre la configuración maestra `.agent/*` (Nivel 2). Prohibido escanear lógica de negocio (`/src/`).
- **Matriz Ejecutora (Escaneo Ad-Hoc):** Prohibidos los agentes omnipotentes genéricos. El Orquestador está OBLIGADO a escanear el entorno (ej. detectar dependencias `pandas`, `django`) e instanciar *on the fly* perfiles de Subagentes hiper-especializados (ej. `[Pandas Cleaner Analyst]`, `[Postgres SQL Architect]`).
- **Micro-Límites Físicos:** El Orquestador definirá taxativamente qué archivo único tiene permitido tocar un Subagente instanciado.
- **Cola Concurrente:** Bloqueo de escritura (Write-Lock preventivo). Dos agentes jamás tocan el mismo fichero en paralelo.

## 3. Reglas de Operación Segura (Zero-Trust)
- **Pizarra Compartida:** Prohibida la conversación entre agentes (P2P). La telemetría solo se pasa grabando resultados en los Markdowns locales.
- **Límite de Retry (Kill Switch):** 3 caídas compilan un Rollback. En caso de fallos de red/modelo (HTTP 503, API Rate), el sistema no retrocede: decreta Pausa Crio-Génica y aguarda conexión.
- **Commits Atómicos y Git:** Solo tras linters y pruebas exitosas, se forma un *Conventional Commit* (`feat:`, `fix:`) en la rama `ai-sprint`.
  - Prohibición terminal de auto-commit sin flag `// turbo`.
  - Repudio de nivel host para comandos `git push`.
  - **Freno SQL Visual:** Si el modo `// turbo` detecta mutaciones de Base de Datos (`sqlmigrate`), el automatismo se desactiva obligando al humano a aprobar lógicamente el *Query*.
- **TDD Aislado:** Segregación forzosa. El subagente `[Coder]` jamás diseña los tests de su obra; recae siempre en un `[QA Tester]` exiliado.
- **Protocolo de Comunicación (Proxy Ban):** Prohibido para Subagentes tácticos alertar o preguntar dudas directamente al Usuario. Ante un obstáculo, el subagente debe fallecer y reportar su bloqueo en el `task.md` para que el Orquestador o Mentor intercedan.
- **Incolumidad del Entorno y OS (RCE Ban):**
  - Prohibido instruir comandos ciegos de Host (`os.system`).
  - Prohibido instruir migraciones de BD (`SQL`) vía scripts de IA ocultos.
  - Prohibido escudriñar claves del `.env` (Blindaje de lectura asíncrona).
  - Enmascaramiento de Trazadores (`--tb=short` restrictivo) para que excepciones crudas no vuelquen PII o claves al log leído por el modelo.
- **Ingestión Analítica Restringida (AST y PII):**
  - Prohibido ingestar archivos gigantes completos (`cat *.py`, o lectura llana de CSVs financieros).
  - Los scripts asíncronos aislarán firmas sintácticas (*ripgrep*) o exportarán perfiles estructurales de datos (`df.info()`) sin extirpar registros a la nube.
- **Estado Multisectorial (Pizarras UID):** Cada Orquestador generará su rastro en sub-carpetas irrepetibles exclusivas `.agent_state/session_{UID}/`.
- **Amnesia y Extracción (Knowledge Items):** Antes de disgregar la carpeta temporal de sesión, es OBLIGATORIO extraer metadatos útiles, *workarounds* y configuraciones exitosas y guardarlas en Markdown dentro de `.agent/knowledge/` (Cerebro Permanente). Tras el volcado, el Orquestador suprime definitivamente la pizarra efímera.
