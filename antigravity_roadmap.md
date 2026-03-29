# 🗺️ Roadmap de Configuración de Antigravity

Este roadmap está diseñado para configurar Antigravity paso a paso, asegurando que se adapte perfectamente a tu flujo de trabajo en macOS y tus repositorios en `/Users/gstmirabal/Developer`. 

La idea es ir comprobando cada fase uno a uno.

## Fase 1: Reglas Globales y de Comportamiento (User Rules)
**Objetivo:** Establecer una base hiper-personalizada de cómo quieres que trabaje, me comunique y qué estándares arquitectónicos y de desarrollo prefieres que utilice siempre. Esto actúa como el "cerebro principal" de nuestras interacciones.

### 1.1 Estándares de Codificación y Calidad:
- [x] Definir convenciones de nombres (Snake case, Camel case, Pascal case) para variables, clases, módulos y constantes.
- [x] Seleccionar linters o formateadores por defecto para cada lenguaje (Ej. Python: `black`, `ruff`, o `flake8`; JS/TS: `eslint`, `prettier`).
- [x] Definir expectativas sobre el tipado estricto (Ej. ¿Obligamos el uso de `typing` en Python o TypeScript estricto?).
- [x] Establecer umbrales de complejidad cognitiva: ¿Cuándo debo sugerirte refactorizar una función grande?
- [x] Preferencias sobre el manejo de errores (Try/Except agresivo, custom exceptions, patrones Option/Result).

### 1.2 Reglas de Entorno y Arquitectura:
- [x] Definir rutas o convenciones estándar donde sueles guardar proyectos y scripts (Ej. todo en `~/Developer`).
- [x] Normativas para entornos virtuales: ¿Usamos siempre `venv`, `poetry`, `pipenv` o `conda`? ¿Dónde se guardan (dentro del proyecto o de forma centralizada)?
- [x] Estándares para el manejo de dependencias (`requirements.txt`, `pyproject.toml`, etc.).
- [x] Organización de la arquitectura base: ¿Patrones MVC, arquitecturas limpias, o scripts secuenciales? (Especialmente para tus transformadores de datos).

### 1.3 Comportamiento y Comunicación de Antigravity:
- [x] Definir el grado de autonomía (Autopilot `// turbo` para tareas 100% seguras vs. pedir confirmación en cambios de código).
- [x] Establecer el Idioma de la Documentación vs. Código (Ej. Código, variables y commits en **Inglés**, explicaciones y comentarios de alto nivel en **Español**).
- [x] Nivel de detalle en las explicaciones: ¿Respuestas técnicas directas al grano o explicaciones didácticas paso a paso?
- [x] Formato de las respuestas: ¿Uso extensivo de diagramas Mermaid, tablas comparativas, o listas Markdown simples?
- [x] Limitar el uso de librerías de terceros (Ej. preferir siempre la biblioteca estándar de Python antes que sugerir una dependencia nueva a menos que haya una buena razón).

### 1.4 Testeo, Git y Despliegue:
- [x] Convenciones de commits: (Ej. Usar Conventional Commits como `feat:`, `fix:`, `chore:`).
- [x] Estándares de Testing: ¿Usamos `pytest`, `unittest`? ¿Exigimos un % mínimo de cobertura antes de dar un módulo por cerrado?
- [x] ¿Cómo manejamos los datos sensibles o contraseñas en los scripts? (Ej. uso obligatorio de archivos `.env` o gestores de secretos).

## Fase 2: Mapeo y Topología de Proyectos (Estructura Física)
**Objetivo:** Enseñar a Antigravity la topología exacta y las fronteras de los repositorios para que opere sin destruir el entorno nativo del Mac.
- [x] Definir la estructura de aislamiento Src-Layout (`/src`, `/tests`, `/data`), separando código de datos pesados (Git LFS).
- [x] Centralizar comandos con un Orquestador de Atajos (Makefiles en vez de comandos bash ciegos).
- [x] Establecer la regla del Virtual Environment nativo (`/venv/`) con ejecución binaria estricta (`./venv/bin/python`).
- [x] Blindaje de contenedores: Obligar al uso de Docker-Compose para Bases de Datos (PostgreSQL) con retención local en `.docker-db-data`.
- [x] Aislar la base de datos de los Tests Unitarios (Test DB Segregation in-memory) para que el QA de la IA no borre tus datos reales.

## Fase 3: Arquitectura Suprema de Subagentes (Zero-Trust Framework)
**Objetivo:** Construir una IA multi-agente militarizada que opere autónomamente sobre tu código usando fronteras físicas inquebrantables, impidiendo Bucles API y colisiones.
- [x] Diseñar el Flujo Operativo de 6 Pasos (Mentor > Orquestador > Auditor > Autorización Humana > Matriz Ejecutora > Rollback).
- [x] Instaurar la Matriz de Agentes Dinámicos: Creación Ad-Hoc de subagentes y segregación estricta TDD (El Coder no es Juez QA).
- [x] Capa de Supervisión Ortogonal (Docs Auditor): Agente paralelo de solo-lectura que tumba planes inarquitectónicos (Kill Switch de Planificación).
- [x] Control Transaccional: Atomic Commits manuales tas éxito, combinados con Git Branch Isolation (`ai-sprint/tarea`), o Rollback absoluto preservando humanos no trackeados (WIP Safety Freeze).
- [x] Seguridad RCE y PII: Prohibición LLM de ingestión cruda de datos sensibles (`view_file CSV`) o librerías del OS (`os.system`). Obligación de scripting enmascarado (Traceback Sanitization).
- [x] Supremacía Constitucional: Aislamiento por Sesiones UID de orquestadores (`.agent_state/uid/`) imposibilitando mentes cruzadas, y supremacía inquebrantable de las reglas base frente a futuros *Skills*. Límite cognitivo AST contra facturas masivas.

## Fase 4: Creación de Workflows y Habilidades (Skills)
**Objetivo:** Tras fabricar un motor irrompible (Fases 1-3), ahora construimos sus *Manuales Tácticos*. El Director invoca comandos personalizados y el Orquestador ejecuta bajo reglas pre-aprobadas acelerando las tareas semanales.
- [ ] Diseñar Workflow 1: Andamiaje (*Scaffolding* absoluto). Rutina interactiva o archivo base para inicializar de golpe la base `src/`, el `.env` y el entorno Docker bajo normas Fase 1 y 2.
- [ ] Diseñar Skill 1: *Data Cleaner Operator*. Un subagente experto en la estandarización y normalización de tus CSV y Excels transaccionales que opera por Python sin escupir PII.
- [ ] Definir desencadenantes técnicos (Triggers) seguros para usar delegaciones de autonomía al instante (`// turbo`) sin destruir la gobernanza o los datos Base.

## Fase 5: Consolidación del Conocimiento (Knowledge Items)
**Objetivo:** Curar el "Síndrome de Alzheimer de la IA" dotándola de un Cerebro a Largo Plazo externo a tus repos de usuario.
- [ ] Automatizar u ordenar al Orquestador para extraer lecciones heurísticas, *workarounds* descubiertos de librerías exóticas o *fixes* de bugs post-sprint.
- [ ] Dictaminar formato y alojamiento en `.agent/knowledge/` antes de que el Orquestador limpie (Amnesia Total) sus memorias operativas temporales al terminar un *Branch*.

---
**¿Cómo proceder?**
Con 3/5 fases coronadas con éxito estructural histórico, empezamos oficialmente la Fase de Producto Final: **Los Workflows (Fase 4)**.
