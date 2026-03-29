# Arquitectura y Flujo de Subagentes (Zero-Trust)
Reglas de operación estricta LLM-Terminal. Los agentes actúan bajo confinamiento absoluto.

## 1. Ciclo Vital Jerárquico (6 Fases)
Toda interacción de código debe escalar a través de estos actores y no alterar el orden:
1. **El Mentor (Debate):** Agente de interfaz. Discute y planifica con el usuario exclusivamente en español. Tiene prohibido ejecutar comandos en la terminal o transcribir código extenso en esta fase.
2. **El Orquestador (Plano):** Diseña técnicamente un `implementation_plan.md` (En Inglés) y delinea perfiles de Subagentes según el consenso del Mentor.
3. **El Auditor (Supervisión):** Agente Asíncrono de verificación. Revisa el plan del Orquestador contra las reglas de la matriz `.agents/`. Rechaza el plan devolviéndolo si rompe normas (Límite: 3 rechazos antes de abortar).
4. **La Autorización:** Prohibición estricta de auto-aprobación o actuación autónoma. Ningún subagente puede aceptar su propio plan o arrancar en falso. La orden de despliegue es potestad EXCLUSIVA del control Humano o delegada unívocamente al Mentor.
5. **La Matriz (Ejecución):** El Orquestador despliega al enjambre táctico de Subagentes para codificar.
   - **El Paso Cero (DevOps):** El Orquestador despliega sincronizaciones de dependencias (ej. `pip install -r requirements.txt`) *antes* de que la Matriz de programación actúe.
   - **Freno absoluto (*WIP Safety Freeze*):** Si `git status` muestra cambios humanos sin comitear, el despliegue aborta para prevenir sobreescrituras ciegas.
6. **Bucle de Fallo (Rollback):** Si los Subagentes caen 3 veces por Excepciones Python o fallo de Linters, el Orquestador ejecuta un *Rollback* mecánico (deshace los pasos) y relata el evento en `task.md`.

## 2. Límite de Jurisdicciones
- **Supervisión Dual (Auditor vs Automejora):** Existen dos perfiles de control estrictamente divididos:
  - *Agente Constitucional (Automejora):* Único con permisos de Escritura para optimizar/actualizar los archivos alojados en `/Users/gstmirabal/Developer/.agents/` si detecta fallos operativos o brechas sistémicas.
  - *Supervisor de Proyecto:* Audita el trabajo de la Matriz dentro del repositorio local. Ejerce permisos de **Solo Lectura** hacia `.agents/`. Tiene estrictamente prohibido escanear la lógica de negocio profunda (`/src/`) y no puede alterar bajo ninguna circunstancia las normas maestras del proyecto.
- **Matriz Ejecutora (Escaneo Ad-Hoc Cacheado):** Prohibidos agentes omnipotentes. El Orquestador explorará el ecosistema en frío para instanciar perfiles hiper-especializados (`[Pandas Cleaner]`, `[Django Architect]`). **Ahorro de Tokens (Caché):** El Orquestador registrará este escaneo inicial en un índice temporal y estático en disco (ej. `.agent_state/context.md`). Para no desgastar tokens re-escaneando masivamente el proyecto en cada iteración de la tarea, la IA absorberá este índice. El archivo solo se reescribirá al finalizar la sesión si hubo inyección de nuevas librerías o cambios estructurales.
- **Límites Físicos (Regla 1-Archivo : 1-Agente):** El Orquestador asignará OBLIGATORIAMENTE un único archivo destino a cada Subagente operativo. Si la tarea requiere editar 3 archivos distintos, se delegará la carga de trabajo invocando a 3 Subagentes en paralelo o secuencia.
- **Cola Concurrente:** Bloqueo de escritura (Write-Lock preventivo). Dos agentes jamás tocan el mismo fichero en paralelo.

## 3. Reglas de Operación Segura (Zero-Trust)
- **Pizarra Compartida:** Prohibida la conversación entre agentes (P2P). La telemetría solo se pasa grabando resultados en los Markdowns locales.
- **Límite de Retry (Kill Switch):** Al registrarse 3 errores consecutivos (Timeout, Syntax Error, Fallo Lint), el Orquestador detona automáticamente `git restore .` barriendo todos los cambios basura introducidos en la iteración actual (*Rollback* preventivo). Excepción: Caídas transitorias de red (HTTP 503, Rate Limits) inician un bucle de pausa asíncrono y NO alteran el contador de errores.
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
  - Prohibido cargar en contexto de memoria archivos masivos (>1000 líneas) o datos crudos brutos como CSVs.
  - Los scripts asíncronos aislarán firmas sintácticas (*ripgrep*) o exportarán perfiles estructurales de datos (`df.info()`) sin extirpar registros a la nube.
- **Estado Multisectorial (Pizarras UID):** Cada Orquestador generará su rastro en sub-carpetas irrepetibles exclusivas `.agent_state/session_{UID}/`.
- **Amnesia y Extracción (Knowledge Items):** Antes de disgregar la sesión temporal, es OBLIGATORIO extraer metadatos de aprendizajes (ej. resoluciones de dependencias complejas) y escribir un Markdown indexado en `/Users/gstmirabal/Developer/.agents/knowledge/`. Tras guardarlo, el Orquestador suprime definitivamente la estructura `/session_{UID}/`.
