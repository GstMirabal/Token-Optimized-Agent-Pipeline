# Implementation Plan: Sprint 059 — efficiency-and-sandbox-regime

**Canonical path**: `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/059` · **Base**: `main` at `08c669c`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Sprint 059 nació como el sprint del régimen de sandbox, en el orden decidido el
2026-10-22 (`docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md:322-323`,
`docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md:383-387`). El 2026-11-02 el
humano amplió el alcance a la cola completa y le sumó la eficiencia del propio
framework, con este principio: **el núcleo es la matriz que se adhiere a cualquier
módulo; el framework existe para optimizar la gestión, y su propio coste es un
defecto de definición.** El orden de las waves sigue ese principio: primero lo que
abarata y acelera todo lo que viene después.

**Intake triage (Phase 1, `agents.md §4 feedback_upstream`).**

| Canal | Resultado | Comando | Exit |
| :--- | :--- | :--- | :--- |
| A | vacío: no hay `.upstream_hosts.json` registrado | `python3 scripts/session_start.py --boot --tool claude-code --session-id <id>` | 0 |
| B | vacío: ningún issue `host-finding` abierto | `gh issue list --label host-finding --state open` (sin sandbox: `HTTPS_PROXY` sin definir) | 0 |
| `F-116-N1` | **accept** (reproducido) — 11 de 33 transcripts del núcleo tienen `first_turn` = 0 en el ciclo 1, así que `ratio` es `None` | bucle de `python3 -I scripts/session_cost.py --session <id> --json` sobre `~/.claude/projects/<proyecto del núcleo>/*.jsonl` | 0 por sesión; recuento `sessions=33 first_turn_zero_cycle1=11` |
| `F-116-N2` | **accept** (reproducido) — ningún hook invoca `session_cost.py` ni `session_probe.py` | `grep -rn -e session_cost -e session_probe hooks/` | 1 (sin salida) |

**Problemas medidos, agrupados por lo que cuestan.**

| # | Problema | Medida |
| :--- | :--- | :--- |
| P1 | `agents.md` se carga en cada petición, también en cada subagente | `wc -c agents.md` → 53.907 bytes (~12k tokens); 14 filas suman 25.736 bytes, casi todo historia y precedentes |
| P2 | `qa-agent` corre en `opus` y es la primera recomendación de ahorro de `/usage` | `agents/qa_agent.md:5` `model: opus`; despachado en 13 sesiones de un host y 10 del núcleo (`grep -rl '"subagent_type":"qa-agent"'` sobre los transcripts) |
| P3 | Phase 6 ejecuta las unidades de una en una aunque `jurisdictional_lock` ya garantiza archivos disjuntos | `workflows/pipeline_workflow.md` Phase 6 no nombra paralelismo; `task_scope.md` no tiene columna de dependencias |
| P4 | Autorizaciones de Bash constantes en el núcleo: el núcleo no tiene la plantilla de sandbox con `autoAllowBashIfSandboxed` que sí reciben los hosts | `.claude/` del núcleo solo tiene `settings.local.json` con 7 permisos sueltos; `claude/settings.hooks.json:45` tiene `autoAllowBashIfSandboxed: true` solo para hosts; `scripts/install.py` `install_nucleus_bridge` no instala sandbox |
| P5 | `/clear` no suspende la sesión en el núcleo: el hook `SessionEnd` ejecuta `.agents/scripts/session_end_hook.py`, ruta que solo existe en un host | `claude/settings.hooks.json:129` |
| P6 | La cota §3.1 se mide contra una baseline 0 en 11 de 33 sesiones (cifra del plan desde `88d8a51`, con el `session_cost.py` de `08c669c`, igual al de `a014f4f`; `ef490cd` la repite) y nadie la mide mientras la sesión corre (`F-116-N1`, `F-116-N2`, `KI-058-3`); el ecosistema token-saver solo mide al arrancar | sesión `7204cadc` a **9.2×** con `session_cost.py` de `08c669c` y 3.6× con el de `919d4f2` (D19), sin señal (`python3 -I scripts/session_cost.py --session 7204cadc-d44b-4226-a000-597c17b52b33 --json`, exit 0, da la cifra de `919d4f2`; la de `08c669c` sale de `git show 08c669c:scripts/session_cost.py`) |
| P7 | Régimen de sandbox: `KI-056-1` (absorbe D-1, D-3, D-12, `KI-054-5`), `KI-056-6` (absorbe D-8), `F-055-N1`, `KI-057-1` (TCP a `127.0.0.1` denegado), D-4, D-10 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:2137-2151`, `docs/roadmaps/core/pipeline/021-030-program-queue.md:380-395` |
| P8 | `KI-057-2`: `SessionEnd` puede suspender otra sesión | `docs/roadmaps/core/pipeline/021-030-program-queue.md:396` |
| P9 | MCP de GitHub remoto con OAuth; actions de `ci.yml` con tags móviles | `.github/workflows/ci.yml:24`, `:28`, `:39` (`@v4`, `@v5`, `@v2`) |
| P10 | C-7: la separación owner/writer (`ADR-0017`) cuesta un dispatch por paso trivial | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:2137` |
| P11 | Residuos del 058 (decisión humana 2026-11-02: cerrar en este sprint todo lo que depende del núcleo): `KI-058-1` (`check_absolute_paths.py` solo mira archivos trackeados), `KI-058-4` (`read_text_file` sin chequeo de archivo regular), `KI-058-5` (cuatro residuos S3), y los puntos 3-5 de la propuesta E — su texto no está en el repositorio; decisión humana 2026-11-02 en Phase 5: se enruta a un `KI-059-n` (Z-02) con condición de desbloqueo "recuperar su texto" | `docs/roadmaps/core/pipeline/021-030-program-queue.md:407-411`; `scripts/upstream_outbox.py:94` (`PIN_PATTERN`), `:136` (`read_regular_bytes`), `:197` (`read_text_file`) |

**Hecho en Phase 1, fuera de los repositorios.** Los symlinks
`.claude/commands/agents/` (ignorados por git, recreables con `install.py`) se
borraron en tres hosts del mantenedor: 0
sesiones con `/agents:` en sus transcripts. Otro host (24 sesiones) y el núcleo (19)
los conservan.

**Hecho cuando**: `agents.md` ≤ 20.000 bytes; prueba de `qa_agent` en `sonnet` ejecutada y
revertida por su criterio de vuelta (D20); Phase 6 despacha lotes paralelos calculados por script; el núcleo trabaja con
sandbox y `autoAllowBashIfSandboxed`, con un recuento de autorizaciones antes y
después; la cota §3.1 tiene baseline no nula y un invocador en sesión decidido por
ADR; la enumeración `RA-19` está re-medida; cada ítem restante está entregado o
enrutado con destino nombrado.

---

## Design

| ID | Decisión | Alternativa rechazada y por qué |
| :--- | :--- | :--- |
| D0 | **Orden por apalancamiento**: las waves 1-2 abaratan (P1, P2) y aceleran (P3, P4, P5) todo lo que viene después; por eso van antes que el resto aunque el sprint se llamara "régimen de sandbox" | Orden de la cola original (sandbox primero): cada wave posterior pagaría el `agents.md` de 54 KB, las autorizaciones y la ejecución en serie |
| D1 | Baseline del ciclo = tamaño de contexto del primer turno: `cache_read + cache_creation + input` (`F-116-N1`, decidido en triage) | Mínimo `cache_read` no nulo (propuesta del host): descarta el turno real de arranque |
| D2 | El medidor en sesión es un **paso de workflow** en Phase 6 (decisión humana 2026-11-02). **Provisional**: ADR-0018 (A-07) puede sustituirlo por el método del debate (D8); si el debate no cierra, D2 se implementa tal cual | Hook periódico: corre fuera del sandbox y obliga a re-medir `RA-19` |
| D3 | En hard (15×) el medidor **solo avisa** (exit 0) mientras la calibración sea n=1 (decisión humana 2026-11-02) | Exit 2 en hard: con n=1 el riesgo de bloqueo falso es alto |
| D4 | Las autorizaciones se cuentan **desde transcripts** con un script determinista antes de cambiar `RA-09` o la configuración del núcleo | Revisar por impresión: es lo que produjo 055/056 |
| D5 | `make verify` deja de escribir dentro de `./.agents`: compilar en memoria y comparar el manifiesto sin reescribirlo | Excluir esos pasos en host: deja el host sin verificar |
| D6 | Cualquier cambio a `RA-09`/`RA-19` (D-12, `KI-057-1`) y la instalación de hooks en el núcleo se deciden por ADR-0019 **después** de la re-medición C-01 | Amendment directo: `RA-19` prohíbe afirmar límites sin enumeración medida |
| D7 | C-7 se resuelve con ADR-0020 que enmienda `ADR-0017`; la implementación del registro solo si el ADR se aprueba | Implementar sin ADR: C-7 se aceptó "para debate" |
| D8 | Estudio → debate → ADR antes de tocar el instrumental token-saver: A-00 inventaría qué mide cada pieza (`skills/token-saver-auditor`, `skills/omni-context-minimizer`, `scripts/session_probe.py`, `scripts/session_cost.py`) y **cuándo**, y los mecanismos de Claude Code (auto-compact y `/compact`, `/context`, `statusLine`, hooks `PostToolUse`/`PreCompact`/`Stop`, subagentes como aislamiento de contexto, carga progresiva de skills y `rules/`, prompt caching), cada uno con coste, dentro o fuera del sandbox y si es determinista; incluye si `install.py` debe instalar los comandos `agents:*` solo por opt-in | Implementar `--bound` directamente: resuelve el síntoma de `F-116-N2` y deja sin estudiar el ecosistema |
| D9 | `qa_agent` pasa al tier `author` (`sonnet`) como **prueba** con criterio de vuelta (abort 4). `tester_agent` y `principal_agent` siguen en `opus` | Bajar también a Tester: deja el sprint sin revisor `opus`; el `basis` del tier `gate` documenta que los defectos centrales los halló un gate |
| D10 | `agents.md` queda como índice: una o dos frases por fila más un puntero; medición, historia y precedentes se mueven a archivos que ya se cargan bajo demanda. Objetivo ≤ 20.000 bytes. Destinos primero, recorte después, `make verify` por fila | Borrar la historia: los precedentes son la razón de cada regla y `RA-14` exige rastrearlos |
| D11 | **Paralelismo en Phase 6**: `task_scope.md` gana la columna `Depends on`; `scripts/check_task_scope.py` calcula los lotes (unidades cuyas dependencias aterrizaron y cuyos archivos son disjuntos); cada lote se despacha en paralelo, **máximo 4 subagentes**, cada uno con `isolation: "worktree"`; el orchestrator integra los commits en el orden de la tabla. Los gates de Phase 7 siguen en serie al final de cada wave (`RA-13`); Phase 5 sigue siendo manual | Paralelismo por criterio del agente: no es reproducible ni auditable. Más de 4: la integración cuesta más de lo que ahorra, y el límite se puede subir en `/config` |
| D12 | **Autonomía en el núcleo sin abrir una vía fuera del sandbox**: B-06 instala en el núcleo solo el bloque `sandbox` con `autoAllowBashIfSandboxed: true`, sin hooks; los hooks del núcleo (que corren fuera del sandbox código que el agente puede escribir, clase `F-055-N1` `Q1`) esperan a ADR-0019 (E-01b). Coste conocido: bajo sandbox, `gh` falla por TLS (D-3) y pasa al humano | Instalar la plantilla completa de host en el núcleo: en el núcleo `scripts/` y `hooks/` no tienen write-deny, así que cada hook ejecutaría fuera del sandbox código escribible por el agente |
| D13 | `/clear` es el gesto de fin de sesión; `suspend` ocurre solo por `SessionEnd`. Requiere E-01 (suspender solo la sesión que termina) y E-01b (el hook en el núcleo). Hasta entonces, en el núcleo `suspend` se corre a mano antes de `/clear` | Cambiar la naturaleza de `suspend`: `/clear` libera contexto y `suspend` registra estado en el ancla; son dos funciones distintas y hacen falta las dos |
| D14 | **Presupuesto por unidad y puntos de suspend planificados**: `task_scope.md` gana dos columnas: `Est. cost` (tokens estimados de la unidad, según su tipo y su riesgo) y `Suspend after` (`yes` en la unidad tras la cual se suspende). La tabla de estimación sale de lo medido en A-00: coste real por unidad de sprints anteriores, cruzando los commits `✅ <sha>` de cada `task_scope.md` con los turnos de `session_cost.py`. `check_task_scope.py` acumula `Est. cost` en orden de ejecución y exige un `Suspend after: yes` antes de que el acumulado proyecte el ciclo por encima de soft (5×) sobre la baseline D1; una wave más grande que eso se parte en la planificación, no a mitad de la ejecución | Suspender solo por la medición en sesión (D2): avisa cuando el ciclo ya creció. Con el presupuesto, la sesión larga se evita al planificar, y la medición en sesión sirve para comprobar la estimación |
| D15 | **Destino para la historia sin dueño** (decisión humana 2026-11-02, Phase 6 wave 1): A-13 crea `docs/guides/RULE_PRECEDENTS_GUIDE.md` porque llegar a 20.000 bytes exige ~51 de 131 filas en ≤ 200 bytes y ~40 de ellas no tenían destino para su historia | Bajar la meta a ~30.000 (solo los 9 términos planificados): deja `agents.md` en ~12k→~7k tokens en vez de ~5k. Repartir en los archivos existentes: 6-10 unidades más en la wave 1 |
| D16 | **Desviación registrada, no decisión de diseño** (2026-11-04, Phase 6 wave 1): el orchestrator despachó A-11, A-13, A-08 y A-01 a la vez tras leer como orden una pregunta del humano sobre paralelismo; `agent_assignment.md` declaraba la wave 1 en serie y ninguna norma lo permitía. El humano lo detuvo y decidió conservar el trabajo tras comprobarlo y volver al orden aprobado. **No es precedente**: A-12 y la wave 2 van en serie, y los lotes solo existen desde la wave 3 con G-01 y G-02 (D11). Los agentes no tocaron git; el orchestrator comprobó cada unidad y la integró una a una | Descartar el trabajo y repetirlo en serie: mismo resultado en archivos independientes, con más coste |
| D17 | **La prueba D9 necesita un ADR que sustituya a `ADR-0003`** (decisión humana 2026-11-04, Phase 6 wave 1): `ADR-0003` prohíbe mover `qa_agent` del tier `gate` sin un ADR nuevo que lo sustituya, y ni este plan ni la auditoría de Phase 4 lo nombraron. A-14 crea `ADR-0021`, que sustituye solo esa cláusula para `qa_agent` durante la prueba, con el criterio de vuelta del abort 4; `tester_agent` y `principal_agent` siguen bajo `ADR-0003` | Descartar A-08: `qa_agent` sigue en `opus` y se pierde el ahorro de D9 |
| D18 | **Reparto de `agents.md` por riesgo** (decisión humana 2026-11-04, Phase 6 wave 1): regla con script que bloquea: una línea; general sin script: completa en `agents.md`; de una tarea concreta sin script: en un archivo `rules/` con disparador (A-15, A-16, A-17); historia y precedentes: `RULE_PRECEDENTS_GUIDE.md`. Objetivo sin cambios: ≤ 20.000 bytes. Límite asumido: un disparador lo sigue el agente, no bloquea; los scripts para reglas sin instrumento pasan a `KI-059-5` | Autosuficiente en ~29.000 bytes: revierte D15 por ~2.000 tokens por carga. Índice sin disparador: reglas vigentes en un archivo que nada obliga a leer |
| D19 | **`segment_cycles` también mide tamaño de contexto** (decisión humana 2026-11-05, tras Tester Gate 2 ronda 1, S1): con baseline en contexto y cortes en `cache_read`, 50 de 52 cortes sobre 35 transcripts no son colapsos y el ratio que alimenta el límite duro cae (un 20× sintético se lee 2,5×). A-01 se amplía a `segment_cycles`, con tests de `probe_cost` y del campo de corte. Cierra `KI-059-4` | Mantener el corte en `cache_read` (decisión del 2026-11-04, ya rectificada): apaga el límite duro |
| D20 | **La prueba D9 termina: se revierte A-08** (decisión humana 2026-11-05): dispara el abort 4 porque `pipeline_workflow.md:25` presenta `--resolve gate` y `--resolve qa_agent` como equivalentes, A-08 los hizo divergir y QA Gate 1 en `sonnet` tenía esa línea en su procedimiento. `qa_agent` vuelve a `opus` y al tier `gate`; `ADR-0021` queda cumplido por su propio criterio de vuelta, sin edición. Volver a probar exige un ADR nuevo que cubra Cursor | Mantener la prueba: exige sostener que F2 no era algo que QA debía ver |
| D21 | **Totales de `session_cost.py` sin duplicados antes del estudio** (decisión humana 2026-11-05, tras QA Gate 1 ronda 3, F4): `read_turns` cuenta cada mensaje de la API una vez por registro del transcript, así que los totales salen altos por un factor de 1,66 a 2,51 (mediana 2,17; 20 transcripts cerrados de la sesión principal, 2026-11-07; comando en `KI-059-10` de `SPRINT_LOG.md`); `ratio` y cortes no cambian. A-18 deduplica por `message.id` antes de A-00, porque A-00, H-01 y H-03 calibran sobre esos totales | Corregirlo solo en el análisis de A-00: el script seguiría dando cifras falsas a cualquier otro uso |
| D22 | **El nombre de host sale del árbol ahora** (decisión humana 2026-11-07, tras QA Gate 1 ronda 5, F3): A-19 a A-24 lo genericizan en los 6 archivos históricos, con anotación en cada sitio; la historia pública sigue en Sprint 060 (`KI-059-12`) | Dejarlo hasta el 060: contradice la decisión del 2026-11-05 y mantiene un S0 que bloquea merge y deploy |
| D23 | **Sustituida en parte por D32** (A-25 sin copia de texto). **Texto soft de §3.1 con check determinista** (decisión humana 2026-11-07, tras QA Gate 1 ronda 5, F1, segunda ocurrencia de la familia de N3; `family_check`): manda la fila soft, el agente actualiza Cost y ningún instrumento lo registra; A-25 fija ese texto por igualdad contra copia revisada | Solo reescribir el texto: rechaza el juicio de QA sin medir y deja la familia sin check |
| D24 | **Sustituida en parte por D29** (`scenarios.json`). **Datos de host como propiedad, no como lista de nombres** (decisión humana 2026-11-07, tras QA Gate 1 ronda 6, F1): A-26 a A-30 retiran el slug del perfil y el dominio de negocio; A-31 fija la propiedad por `profiles/<slug>` sin guardar nombres de host en el repositorio y declara su límite: los nombres sueltos siguen en el escáner de Sprint 060 (`KI-059-12`). `skills/skillopt/data/scenarios.json:58-59` no nombra proyecto y es un dataset: se mantiene y se enruta como `KI-059-14` | Otra lista de nombres: es la comprobación de subconjunto que falló en D22 (`fail_closed_claims`) |
| D25 | **Sustituida por D30.** **`RA-19` tras S0 sin aplazamiento abierto** (decisión humana 2026-11-07): C-01 salda las rondas 3, 4 y 6; sigue en la wave 4 porque mide el sandbox de B-06. Una fila de Verification lo exige, de modo que `check_plan_closure.py` no deja cerrar sin ella; A-32 fija el momento en la regla. Retirar el nombre del árbol no lo retira de la historia pública (`KI-059-12`, Sprint 060). El S0 queda abierto en cuanto a `RA-19` hasta C-01 | Adelantar C-01: saldría incompleta y habría que repetirla; aplazar sin más: se puede olvidar, y ya se saltó tres veces |
| D26 | **Ampliada por D32** (no cubre las enmiendas `RA-XX` de `skills/compliance-checker`). **El aprendizaje va donde corresponde, sin agente nuevo** (decisión humana 2026-11-07): `governance_learner` decide el destino con una tabla (test o script si se puede comprobar; `rules/` si tiene contexto; `agents.md` solo si aplica en cada sesión y nada lo cubre; solo citar si ya está cubierto) y `rule_validator` lo audita (A-33 a A-36, A-37) | Agente nuevo: suma coste fijo y conserva las instrucciones contradictorias |
| D27 | **Ampliada por D32.** **Se retira la instrucción `forced: true`** (decisión humana 2026-11-07, QA Gate 1 ronda 6, F2): nada la lee. La señal "too tight" se lee de `task_scope.md`; la calibración sigue en A-00, A-06 y A-03; la copia de A-25 se actualiza | Definir un destino para el campo: añade un mecanismo que nadie consume |
| D28 | **La regla nueva se carga donde ocurrió el fallo** (decisión humana 2026-11-07, hueco de A-37 confirmado por `rule_validator`): A-38 añade `rules/*.md` a los globs de `rules/documentation_standard.md` y A-39 ajusta su fila de `agents.md` §0 con +2 bytes | Enrutarlo por Z-02: la regla no se cargaría al editar `rules/` |
| D29 | **Inventario único de datos de host** (decisión humana 2026-11-07, tras QA Gate 1 ronda 7, F1; un dominio de negocio cuenta como dato de host): se buscaron una vez, en árbol e historia de `origin/main`, los nombres de todos los repositorios del humano, sus componentes y su dominio, con la lista fuera del repositorio (`RA-15`). A-40 a A-45 retiran lo que quedaba y sustituyen a D24 en `scenarios.json`. `tests/test_profile_references.py` cubre solo referencias `profiles/<slug>`; un término fuera de la lista no se detecta. La historia pública se decide tras el merge (D31) | Otra búsqueda por rondas: es lo que no convergió |
| D30 | **`RA-19` solo si el S0 toca sandbox o ejecución** (decisión humana 2026-11-07): sustituye a D25. Medir el sandbox no dice nada de una filtración en documentación, así que la frase de A-32, la fila de Verification de D25 y el añadido en C-01 se retiran y C-01 vuelve a su alcance | Mantener D25: añade una deuda que no aporta seguridad |
| D31 | **Historia pública, decisión aparte tras el merge** (decisión humana 2026-11-07): reescribirla cambia los SHA de 58 tags, rompe los pines de submódulo de los hosts y no garantiza que GitHub deje de servir commits antiguos por SHA. Se decide con el humano presente, a partir del inventario de D29 | Reescribir en este sprint: mezcla una operación irreversible con una rama abierta |
| D32 | **Remediar quitando** (decisión humana 2026-11-07): antes de tocar una afirmación se ejecuta el comando que la comprueba; sin instrumento, se borra. Sustituye a D27 en esto: el párrafo de calibración de `rules/token_economy.md` se borra entero, y A-25 se reduce a la conducta de `probe_cost` a 6×, sin copia de texto. D26 no cubre las enmiendas `RA-XX` de `skills/compliance-checker`, que son un destino legítimo | Otra reescritura de la misma línea: es la causa del bloqueo |
| D33 | **Remediación de la ronda 8** (decisión humana 2026-11-07, tras QA Gate 1 ronda 8, N1 a N5): N1 se corrige en `HOTFIX_TEMPLATE.md:25` (A-46); N2, N3 y N5 se corrigen en este plan y en `SPRINT_LOG.md` (A-47); N4 reduce lo que afirma el docstring (A-48). Las notas S3 N6 a N8 solo se registran | Descartar N1 o enrutar N2 a N5 como KI: deja una instrucción contradicha y arrastra deuda por una corrección mínima |
| D34 | **Sustituida por D35** (check retirado tras QA Gate 1 ronda 10; `KI-059-15`). **Check determinista de la familia de N3** (decisión humana 2026-11-07; convergencia, regla 3): `scripts/check_log_append_only.py` (A-49 a A-51) rechaza palabras perdidas en filas KI, frases perdidas tras `error_mining` y filas de decisión sustituidas sin marca. Excepción declarada: trailer `Log-Rewrite: <motivo>`. `make verify` lo aplica desde el Sprint 060; en el 059, QA lo ejecuta sobre `60383e3..HEAD`. Límites: solo esas zonas; no ve palabras reordenadas ni cambios de sentido; el patrón de sustitución depende de la redacción en español | Enrutarlo a Z-02: aplaza un check que la regla exige y que se midió viable |
| D35 | **Remediación de la ronda 9** (decisión humana 2026-11-07, tras QA Gate 1 ronda 9, R9-1 a R9-3): A-53 corrige en un commit `fix(` con test pareado la raíz de `--current-sprint` y la resolución de `--sprint-dir`, y falla con exit 2 ante un directorio inexistente, una base de rango vacía o un registro ausente pasados a mano; A-54 marca D23 y D26. Las notas S3 R9-N1 a R9-N3 solo se registran. Límite decidido por adelantado: otro S0 o S1 en este script en la ronda 10 lo retira (revierte A-49 a A-53 y el contador del README) y envía el check a Z-02, sin otra ronda de arreglos. **Aplicado el 2026-11-07**: la ronda 10 reportó R10-1 y R10-2 (S1); revertidos con `873fb1e`, `f328923`, `a4493b8`, `51016e2`, `2c55575` y `120860b`; la regla 3 queda sin cumplir para esta familia por decisión humana (`KI-059-15`) | Retirar el check ahora: incumple la regla 3 por dos defectos con corrección conocida |
| D36 | **Acotada por D37**: I-08 a I-10 quedan sustituidas por M-01 a M-05, y la frase sobre los saltos en silencio se sustituye por el test de M-05. **Remediación de la ronda 11** (decisión humana 2026-11-07, tras QA Gate 1 ronda 11, R11-1 y su medición): Z-02 deja de enumerar IDs y remite a la tabla KI de `SPRINT_LOG.md`, lo que reduce la afirmación (regla 3) sin mecanismo nuevo. Los saltos en silencio de los checks anteriores al sprint se corrigen antes del merge en I-08 a I-10, no en Z-02. Un clon sin anchor sigue omitiendo, porque el anchor no se versiona. El número de unidades es una estimación y se fija al abrir la wave 6 | Dejarlos en Z-02: el merge llevaría un gate que pasa en silencio (S1). Corregirlos en la wave 1: añade código al bloque que no converge |
| D37 | Tras QA Gate 1 ronda 13 (decisión humana 2026-11-07): la wave 1b (M-01 a M-12) se ejecuta antes de volver a pasar los gates, que revisan las waves 1 y 1b juntas. Un hallazgo se cierra con código, test o eliminación; una re-planificación solo añade filas de unidad. Cada hecho del sprint vive en un sitio y el resto cita su id. La celda Notes de Quality Gate lleva como máximo 400 caracteres y el detalle va a Gate findings (M-11). Criterio para llevarlo a `rules/` y `workflows/`: waves 2 a 6 sin hallazgos de la familia de R12-1 y como máximo 2 rondas de gate por wave. **Check**: `python3 scripts/check_sprint_refs.py --current-sprint` → exit 0; `venv_skillopt/bin/python -m pytest -q tests/test_current_sprint_matrix.py` → exit 0 | YAML/JSON ahora: migración sin medir si esto basta. Más filas I-n: enumera casos a mano. Un sprint aparte: `open-sprint` sale 2 con el 059 sin sellar (`scripts/session_state.py:765-777`) |

---

## Work

Una tabla por wave, en orden de ejecución. `tras X` en Operation es la dependencia
que G-01 convierte en la columna `Depends on` de `task_scope.md`. Desde la wave 3,
las unidades sin dependencia pendiente van en lotes paralelos (D11). La wave 1 registra una desviación: D16.

### Wave 1 — Palancas de coste (abaratan cada petición posterior)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-05 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — veredictos de triage de esta Context (`F-116-N1`, `F-116-N2`: `accept` con su comando y exit); el cierre de ambos lo marca C-02 | low | `doc_orchestrator` | ✅ `1dbe533` |
| A-09 | `rules/code_craft.md` | modify — recibe medición e historia de `linter_command` (Python, JS/TS), `max_indentation`, `max_lines_per_func`, `fail_closed_claims`, `exception_handling` (D10) | medium | `rule_validator` | ✅ `0c7a9b2` |
| A-10 | `rules/project_topology.md` | modify — recibe historia y precedentes de `RA-09`, `RA-19`, `jurisdiction` (D10) | medium | `rule_validator` | ✅ `a694ffe` |
| A-11 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify — recibe transporte, canales, triage y cierre de `feedback_upstream` (D10) | low | `doc_orchestrator` | ✅ `72ac88b` |
| A-13 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | create — recibe la historia, la medición y los precedentes de cada fila de `agents.md` que A-12 recorta y cuyo detalle no reciben A-09, A-10 ni A-11, indexados por sección y clave de la regla (D10); texto movido literal, sin reescribir | medium | `doc_orchestrator` | ✅ `a014f4f` |
| A-15 | `rules/skills_and_integrations.md` | modify — recibe literal `three_file_standard`, `topological_order`, `enforcement` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero en su lugar | low | `rule_validator` | ✅ `18b692e` |
| A-16 | `rules/qa_and_testing.md` | modify — recibe literal `local_testing` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero en su lugar | low | `rule_validator` | ✅ `9b8db89` |
| A-17 | `rules/project_topology.md` | modify — recibe literal `min_release_age`, `only_built_deps`, `config_file` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero y `config/rule_triggers.json` añade `pnpm-workspace.yaml`, `package.json` y `.npmrc` a los `globs` de ese archivo | low | `rule_validator` | ✅ `d133bc2` |
| A-12 | `agents.md` | modify — tras A-09, A-10, A-11, A-13, A-15, A-16, A-17, con el reparto D18: filas recortadas a regla + puntero, ≤ 20.000 bytes; `make verify` exit 0. Antes de recortar, `grep -n "agents.md" tests/*.py` lista las cadenas que un test fija en `agents.md` (p. ej. `RA-18` en `tests/test_cursor_phase1.py`, la línea `EMITTED` de `tests/test_gate_row_wording.py`, la fila `Command paths`) y cada una se conserva. `RA-14`: por cada término cuyo detalle se mueve (`feedback_upstream`, `jurisdiction`, `RA-09`, `RA-19`, `linter_command`, `max_indentation`, `max_lines_per_func`, `fail_closed_claims`, `exception_handling`), `grep -rn "<término>" agents.md rules/ workflows/ docs/guides/ docs/standards/ scripts/ hooks/ tests/` y cada cita que apunte al texto movido se actualiza al nuevo destino en el mismo commit | high | `rule_validator` | ✅ `d6f5756` |
| A-14 | `docs/decisions/ADR-0021-qa-agent-tier-trial.md` | create — tras A-12: sustituye la cláusula de `ADR-0003` solo para `qa_agent` durante la prueba D9, con el criterio de vuelta del abort 4 (D17); `ADR-0003` no se edita; companion obligatorio `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (`:19`, que repite la regla, y `:140`) | medium | `doc_orchestrator` | ✅ `ed96115` |
| A-08 | `agents/qa_agent.md` | modify — tras A-14: `model: sonnet`, `tier: author` (D9); companion obligatorio `config/model_tiers.json` (mover `qa_agent` a `author.profiles`; añadir al `basis` de `gate` la prueba y su criterio de vuelta), porque `scripts/check_model_tiers.py` exige que coincidan; companion `tests/test_agent_profile_census.py` (fija la lista `gate` y mantiene a `qa_agent` sin `Write`/`Edit`) | medium | `implementer_agent` | ✅ `80518b4`, reverted `8e8a566` (D20) |
| A-01 | `scripts/session_cost.py` | modify — `fix(`: baseline D1 en `cycle_summary` y cortes en `segment_cycles` por tamaño de contexto (D19); paired test `tests/test_session_cost.py` (nuevo) con un turno `cache_read` 0 / `cache_creation` > 0 | medium | `implementer_agent` | ✅ `ef490cd`, `919d4f2` |
| A-19 | `CHANGELOG.md` | modify — D22: reemplaza el nombre de host por `a host project`, con anotación en el sitio; `git grep -c -i` del nombre sobre el archivo → 0 | low | `doc_orchestrator` | ✅ `4fb09a9` |
| A-20 | `docs/roadmaps/core/pipeline/014-identity-branding-hardening.md` | modify — D22: igual que A-19 | low | `doc_orchestrator` | ✅ `28242ff` |
| A-21 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify — D22: igual que A-19 | low | `doc_orchestrator` | ✅ `a3c5a14` |
| A-22 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify — D22: igual que A-19 | low | `doc_orchestrator` | ✅ `f72983e` |
| A-23 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify — D22: igual que A-19 | low | `doc_orchestrator` | ✅ `b6adb90` |
| A-24 | `docs/sprints/023-core-pipeline/task_scope.md` | modify — D22: igual que A-19 | low | `doc_orchestrator` | ✅ `ff69f15` |
| A-25 | `tests/test_token_economy_soft_bound.py` | create — D23: igualdad contra copia revisada de la fila soft y de la frase de calibración de `rules/token_economy.md §3.1`, y `probe_cost` devuelve `None` con un ciclo a 6×; falla con el texto de `d192075` (N3) y con el de `7779e7f` (F1) | low | `implementer_agent` | ✅ `1e1deda`, reducida `d059aac` (D32) |
| A-26 | `CHANGELOG.md` | modify — D24: reemplaza el slug del perfil en las líneas 800, 811 y 934 y el dominio de la 764, con anotación | low | `doc_orchestrator` | ✅ `4e34b49` |
| A-27 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify — D24: reemplaza el slug de la línea 52, con anotación | low | `doc_orchestrator` | ✅ `59e6950` |
| A-28 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify — D24: reemplaza el slug de la línea 33 y deja legibles las líneas 33 y 38 (F6 de la ronda 6) | low | `doc_orchestrator` | ✅ `271ee11` |
| A-29 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify — D24: reemplaza el slug de las líneas 21, 29, 39 y 48, con anotación | low | `doc_orchestrator` | ✅ `fe48d2f` |
| A-30 | `workflows/reverse_documentation_workflow.md` | modify — D24: reemplaza el dominio de negocio de la línea 28 por una descripción genérica | low | `doc_orchestrator` | ✅ `af55026` |
| A-31 | `tests/test_profile_references.py` | create — D24: toda referencia `profiles/<slug>` trackeada resuelve a un directorio real o a un marcador revisado; falla en `d06c939` por cada uno de los 4 archivos; declara que no detecta nombres sueltos | low | `implementer_agent` | ✅ `dbe243a` |
| A-32 | `rules/qa_and_testing.md` | modify — D25: la repetición de `RA-19` tras un S0 ocurre antes del merge del sprint que lo remedia | low | `rule_validator` | ✅ `9382b80`, sustituida `022924f` (D30) |
| A-33 | `agents/governance_learner.md` | modify — D26: tabla de destinos del aprendizaje; quita el destino fijo `agents.md` Section 7 | low | `rule_validator` | ✅ `2d0d39b` |
| A-34 | `agents/rule_validator.md` | modify — D26: audita el destino que da `governance_learner`; quita el destino fijo `agents.md` | low | `rule_validator` | ✅ `24de04e` |
| A-35 | `workflows/remediation_workflow.md` | modify — D26: `negative_ki` enruta por la tabla de `governance_learner` en vez de inyectar en `agents.md` | low | `rule_validator` | ✅ `f052ea9` |
| A-36 | `agents.md` | modify — D26: `constitutional_escalation` enruta por `governance_learner`; `wc -c agents.md` ≤ 20000 | low | `rule_validator` | ✅ `dc53642` |
| A-37 | `rules/documentation_standard.md` | modify — D26: `negative_ki` de este bloqueo: no describir una conducta que ningún instrumento realiza; si la tabla da otro destino, se enmienda esta fila antes de escribir | low | `rule_validator` | ✅ `d6b388c` |
| A-38 | `config/rule_triggers.json` | modify — D28: añade `rules/*.md` a los globs de `rules/documentation_standard.md` | low | `rule_validator` | ✅ `408ad02` |
| A-39 | `agents.md` | modify — D28: fila §0 de `rules/documentation_standard.md`: `Editing any document under docs/ or rules/`; `wc -c agents.md` ≤ 20000 | low | `rule_validator` | ✅ `de19dad` |
| A-40 | `docs/roadmaps/core/pipeline/018-post-publication-field-hardening.md` | modify — D29: reemplaza el dominio de negocio de la línea 36, con anotación | low | `doc_orchestrator` | ✅ `6256efd` |
| A-41 | `skills/skillopt/data/scenarios.json` | modify — D29: reemplaza el dominio de negocio de las líneas 58 y 59 | low | `doc_orchestrator` | ✅ `e6f27cb` |
| A-42 | `docs/roadmaps/core/pipeline/008-session-close-governance.md` | modify — D29: reemplaza el dominio de la línea 23, con anotación | low | `doc_orchestrator` | ✅ `4bdcc49` |
| A-43 | `skills/mcp-registry/README.md` | modify — D29: reemplaza el ejemplo de dominio de la línea 5 | low | `doc_orchestrator` | ✅ `f4d20dd` |
| A-44 | `profiles/example-project/mcp/registry.json` | modify — D29: reemplaza el ejemplo de dominio de la línea 7 | low | `doc_orchestrator` | ✅ `66a4438` |
| A-45 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | modify — D29: reemplaza los roles heredados de un host en la línea 205 | low | `doc_orchestrator` | ✅ `699eac3` |
| A-46 | `docs/standards/templates/HOTFIX_TEMPLATE.md` | modify — D33: línea 25 (N1): enruta por `constitutional_escalation` y enlaza el destino asignado, sin fijar `RA-XX` | low | `doc_orchestrator` | ✅ `05a6dab` |
| A-47 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify — D33: anota las filas de D23 y D25 en Documentary impact (N2), marca D24 (N3) y quita la cifra de la fila de coste de sesión de `7a037351` (N5) | low | `doc_orchestrator` | ✅ `1473570` |
| A-48 | `tests/test_profile_references.py` | modify — D33: docstring (N4): reduce lo afirmado a lo que el test comprueba y declara los archivos omitidos; sin cambio de lógica | low | `implementer_agent` | ✅ `8923501` |
| A-49 | `scripts/check_log_append_only.py` | create — D34: falla (exit 2) en `10c88f4` (N3), `1dbb43e` (F6) y `60383e3` (D24); exit 0 en `60383e3..HEAD` tras A-47 | low | `implementer_agent` | ✅ `251717d`, revertida `120860b` (D35) |
| A-50 | `tests/test_check_log_append_only.py` | create — D34: repositorios git desechables para cada zona, el trailer, sus límites y los errores | low | `implementer_agent` | ✅ `3368dc5`, revertida `2c55575` (D35) |
| A-51 | `Makefile` | modify — D34: `verify` ejecuta `check_log_append_only.py --current-sprint` | low | `implementer_agent` | ✅ `de239b7`, revertida `a4493b8` (D35) |
| A-52 | `rules/documentation_standard.md` | modify — D34: nombra el instrumento y sus límites junto a la fila `annotated in place` | low | `rule_validator` | ✅ `d40183d`, revertida `f328923` (D35) |
| A-53 | `scripts/check_log_append_only.py` | modify — D35: `fix(` con `tests/test_check_log_append_only.py` pareado: raíz de `--current-sprint` como `check_gate_log.py`; `--sprint-dir` resuelto desde la raíz de git; exit 2 ante directorio inexistente, base vacía o registro ausente a mano; `Repro:` falla en el padre | low | `implementer_agent` | ✅ `f273f93`, revertida `873fb1e` (D35) |
| A-54 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify — D35: marca D23 y D26 como acotadas por D32 (R9-3) | low | `doc_orchestrator` | ✅ `822c047` |

### Wave 1b — Método: una casa por hecho y afirmaciones con comprobación (D37)

Sin columna Status: el estado vive en `task_scope.md`. Orden: M-11, M-01 a M-04, M-12, M-05 a M-10, M-13 a M-16.

| # | File | Operation | Risk | Assignee (proposed) |
| :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/_current_sprint.py` | create — resolver de `--current-sprint`: la raíz es el ancestro más cercano del cwd con `.git`, o el cwd si no hay ninguno; acepta el id entero o en texto con ceros; omite solo cuando falta `docs/active_state.json` o su bloque `current_sprint`; devuelve un error que el llamador convierte en exit 2 con anchor ilegible o truncado, id ausente o de otro tipo, o directorio inexistente; test `tests/test_current_sprint.py` | medium | `implementer_agent` |
| M-02 | `scripts/check_task_scope.py` | modify — tras M-01: `fix(` `current_sprint_dir` usa M-01; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` |
| M-03 | `scripts/check_gate_log.py` | modify — tras M-01: `fix(` usa M-01 y sale 2 con un `--sprint-dir` inexistente; paired test en `tests/test_check_gate_log.py` | low | `implementer_agent` |
| M-04 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify — tras M-01: `fix(` R12-2: usa M-01 y sale 2 con una ruta de plan inexistente; paired test en `tests/test_token_saver_auditor.py` | low | `skill_architect` |
| M-12 | `scripts/loop_guard.py` | modify — tras M-01: `fix(` R13-1: `check --sprint-dir` con un directorio inexistente sale 2; paired test en `tests/test_loop_guard.py` | low | `implementer_agent` |
| M-05 | `tests/test_current_sprint_matrix.py` | create — tras M-02 a M-04 y M-12: localiza por grep cada script de `scripts/` y `skills/*/scripts/` con `--current-sprint` y falla si alguno sale 0 con: cwd en un subdirectorio, id `"059"`, directorio del sprint borrado, anchor truncado, `--sprint-dir` inexistente; falla también si el grep no encuentra ninguno | low | `implementer_agent` |
| M-06 | `scripts/check_sprint_refs.py` | create — tras M-01: comprueba en los artefactos del sprint las reglas B, C y D de D37: cada id citado existe en su casa; cada fila de Design desde D37 tiene `**Check**:`; cada celda Notes de Quality Gate desde la ronda 13 tiene como máximo 400 caracteres; sale 2 con cada violación; test `tests/test_check_sprint_refs.py` | medium | `implementer_agent` |
| M-07 | `Makefile` | modify — tras M-06: `verify` ejecuta `python3 scripts/check_sprint_refs.py --current-sprint` (invocador `RA-16`) | low | `implementer_agent` |
| M-08 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify — Design con columna `Check`; tablas Work sin Status; regla B en el encabezado | low | `doc_orchestrator` |
| M-09 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify — tabla Gate findings (`Round`, `ID`, `Severity`, `File:line`, `Check`); tope de 400 caracteres en Notes; un "Next Phase" sustituido ocupa una línea | low | `doc_orchestrator` |
| M-10 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify — Operation lleva solo el verbo, no el texto del plan; Target y el verbo se quedan porque los lee `scripts/check_forge_ladder.py:159-160` | low | `doc_orchestrator` |
| M-11 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify — añade la tabla Gate findings (`Round`, `ID`, `Severity`, `File:line`, `Check`) | low | `orchestrator` |
| M-13 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify — `fix(` R14-1: el id sale solo del directorio del sprint; paired test: caso `numbered_parent` en `tests/test_current_sprint_matrix.py` | low | `skill_architect` |
| M-14 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify — R14-2: la fila M-01 enuncia la raíz y las omisiones de `scripts/_current_sprint.py` | low | `orchestrator` |
| M-15 | `scripts/_current_sprint.py` | modify — R14-3: retira `scripts/loop_guard.py` de `invoked_by:` | low | `implementer_agent` |
| M-16 | `scripts/check_task_scope.py` | modify — `fix(`: `sprint_id_from_dir` acepta un prefijo de 3 o más dígitos; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` |

### Wave 2 — Ritmo y autonomía (aceleran el resto del sprint)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M-17 | `scripts/_current_sprint.py` | modify — `fix(` T2-1: más de un directorio para el número del sprint lanza `CurrentSprintError`; paired test en `tests/test_current_sprint.py` | low | `implementer_agent` | ✅ `92bb5e7` |
| G-01 | `scripts/check_task_scope.py` | modify — columna `Depends on` y subcomando que imprime los lotes paralelos (dependencias aterrizadas, archivos disjuntos, máximo 4); tests en `tests/test_check_task_scope.py` | medium | `implementer_agent` | ✅ `21080e9` |
| G-02 | `workflows/pipeline_workflow.md` | modify — tras G-01: Phase 6 despacha cada lote en paralelo con `isolation: "worktree"` e integra en orden; Phase 7 sigue en serie por wave (D11). Tras integrar cada lote, el orchestrator borra cada worktree y su rama (`git worktree remove <path>`, `git branch -D <rama>`) antes del lote siguiente, porque `scripts/branch_sovereignty.py` niega el sello de cierre con una rama sin integrar; y re-ejecuta sobre `ai-sprint/[ID]` las comprobaciones de `hooks/on_commit.py` que el commit en el worktree no vio (`python3 scripts/check_task_scope.py --sprint-dir <dir>`), exit 0 antes del lote siguiente | medium | `orchestrator` | ✅ `808d098` |
| B-01 | `scripts/prompt_count.py` | create — cuenta autorizaciones por sesión desde transcripts, `--json`; test `tests/test_prompt_count.py` | medium | `implementer_agent` | ✅ `4952195` |
| B-02 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | create — tras B-01: recuento base de una sesión real de núcleo y una de host (genericizada, `RA-15`) | low | `doc_orchestrator` | ✅ `7fc8ae5` |
| B-07 | `workflows/close_workflow.md` | modify — tras B-01: paso advisory que corre `python3 scripts/prompt_count.py --session <id> --json` sobre la sesión que cierra e imprime el recuento; es el invocador `RA-16` de B-01 | low | `orchestrator` | ✅ `2d40946` |
| B-06 | `scripts/install.py` | modify — tras B-02: `install_nucleus_bridge` instala el bloque `sandbox` con `autoAllowBashIfSandboxed: true`, sin hooks y sin `excludedCommands` (D12); test nuevo `tests/test_install_nucleus_sandbox.py` | high | `implementer_agent` | ✅ `92fddf8` |
| E-01 | `scripts/session_state.py` | modify — `fix(`: `suspend` desde `SessionEnd` solo actúa si el `session_id` del hook coincide con el del anchor (`KI-057-2`); paired test `tests/test_session_end_hook.py`. Reproducir primero; si no se reproduce, `RECORD` | medium | `implementer_agent` | ✅ `c10f8bd` |
| E-01c | `scripts/session_state.py` | modify — tras E-01: `fix(` del hueco medido en Phase 1: entre sprints (sprint sellado, sesión `IN_PROGRESS`) `suspend` imprime "Sprint is sealed — nothing was suspended", exit 0, y deja el lock tomado, así que el boot siguiente sale 2 y exige `--takeover`; `suspend` libera el lock de la sesión sin tocar el sprint sellado; paired test en `tests/test_session_state.py` | medium | `implementer_agent` | ✅ `3a3136b` |
| M-18 | `scripts/check_task_scope.py` | modify — `fix(` R16-1: `--batches` programa solo unidades con estado `⏳`; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` | ✅ `c5fbf5f` |
| M-19 | `scripts/prompt_count.py` | modify — `fix(` R16-2: suma `<session>/subagents/*.jsonl` al recuento de la sesión; paired test en `tests/test_prompt_count.py` | medium | `implementer_agent` | ✅ `d534c04` |
| M-20 | `scripts/prompt_count.py` | modify — tras M-19: `fix(` R16-4: parte el JSONL solo por `\n`; paired test en `tests/test_prompt_count.py` | low | `implementer_agent` | ✅ `10c8e1a` |
| M-21 | `docs/plans/README.md` | modify — R16-5: declara que el self-bridge escribe `.claude/settings.json` con el bloque `sandbox`, y lo mismo en `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | low | `doc_orchestrator` | ✅ `e6caffc` |
| B-08 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | modify — tras M-20, B-06: R16-3: rehace la línea base con M-19 y M-20; el instalador del núcleo se ejecuta sobre este checkout (decisión humana 2026-11-08) y una sesión real bajo sandbox rellena `Re-measurement after B-06` | medium | `doc_orchestrator` | ✅ `9e55888` |
| B-09 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify — R17-2: transcribe QA Gate 1 ronda 17 y sus hallazgos, añade las notas de remediación de la ronda 16 con comandos y exit codes, y actualiza `Next Phase` | low | `orchestrator` | ✅ `0cbf261` |
| M-22 | `scripts/check_task_scope.py` | modify — `fix(` R17-1: un `Status` desconocido hace que `--batches` termine con exit distinto de 0; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` | ✅ `639fd05` |
| M-23 | `scripts/install.py` | modify — S3 de la ronda 17: el docstring de `install_nucleus` incluye el bloque `sandbox` en el contenido del self-bridge | low | `implementer_agent` | ✅ `104467f` |
| B-10 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify — R18-2: transcribe QA Gate 1 ronda 18, la decisión A-1 y las notas de remediación de la ronda 17 con exit codes desde la base de la rama | low | `orchestrator` | ✅ `1b99872` |
| M-24 | `scripts/check_task_scope.py` | modify — `fix(` R18-3: elimina de la auditoría la comprobación de `Status` y su texto; `--batches` sigue rechazando un `Status` desconocido; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` | ✅ `16b1dc6` |

### Wave 3 — Token economy en sesión (estudio, debate, decisión)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-18 | `scripts/session_cost.py` | modify — tras A-01, antes de A-00: `fix(` `read_turns` cuenta una vez cada `message.id` (D21); paired test en `tests/test_session_cost.py`, que además añade las anotaciones de tipo que faltan; `ratio` y cortes no cambian sobre los transcripts reales | medium | `implementer_agent` | ⏳ |
| A-00 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | create — estudio D8: tabla por pieza y por mecanismo con fuente; crecimiento de contexto boot→cierre en las sesiones del núcleo (`session_cost.py --json`); **coste real por unidad** en los sprints 056-058 (commits `✅ <sha>` de `task_scope.md` cruzados con turnos del transcript), agrupado por operación (create/modify, script/doc/rule) y riesgo, como base de la tabla de estimación D14; plantea si la cota hard de 15× sigue valiendo con la baseline en tamaño de contexto (`KI-059-9`); 2-4 métodos candidatos | medium | `token_economy_agent` | ⏳ |
| A-06 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | modify — tras A-00: sección `Debate` con opciones, objeciones y decisión del humano, incluida la de la cota hard de 15× (`KI-059-9`) | low | `doc_orchestrator` | ⏳ |
| A-07 | `docs/decisions/ADR-0018-in-session-token-economy.md` | create — tras A-06: método elegido; confirma o sustituye D2; lo que no entra pasa a `KI-059-n` | medium | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| A-02 | `scripts/session_cost.py` | modify — tras A-01, A-07: `feat(` flag `--bound` (`OK`/`SOFT`/`HARD`, exit 0, D3) o la forma que fije ADR-0018; test en `tests/test_session_cost.py` | medium | `implementer_agent` | ⏳ |
| A-03 | `rules/token_economy.md` | modify — tras A-07: §3.1 invocador en sesión (la unidad de D1 y D19 ya se corrigió en la remediación de QA Gate 1 ronda 3) y el presupuesto por unidad con puntos de suspend planificados (D14) | low | `rule_validator` | ⏳ |
| H-01 | `config/unit_cost_estimates.json` | create — tras A-07: tabla de estimación por tipo de unidad y riesgo, con la fuente de cada cifra (A-00) y su `measured_at` | low | `token_economy_agent` | ⏳ |
| H-02 | `scripts/check_task_scope.py` | modify — tras G-01, H-01: columnas `Est. cost` y `Suspend after`; acumula el coste en orden y sale 2 si el acumulado proyecta el ciclo por encima de soft (5×) sin un `Suspend after: yes` previo (D14); tests en `tests/test_check_task_scope.py` | medium | `implementer_agent` | ⏳ |
| H-03 | `workflows/close_workflow.md` | modify — tras H-01, B-07: paso advisory que compara el coste medido de cada unidad del sprint (`session_cost.py --json`) con su `Est. cost` e imprime la diferencia; es el invocador `RA-16` de la recalibración de `config/unit_cost_estimates.json`, que `token_economy_agent` aplica en el sprint siguiente | low | `orchestrator` | ⏳ |
| A-04 | `workflows/pipeline_workflow.md` | modify — tras G-02, A-02, H-02: Phase 4.3 rellena `Est. cost`/`Suspend after`; Phase 6 corre la medición en cada unidad (invocador `RA-16` de A-02), compara lo medido con `Est. cost` y ejecuta `session_state.py suspend` en cada `Suspend after: yes` | low | `orchestrator` | ⏳ |

### Wave 4 — Medición del sandbox

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B-03 | `scripts/py_compile_tree.py` | modify — compilar sin escribir `.pyc` (D5); test en `tests/test_verify_py_compile.py` | medium | `implementer_agent` | ⏳ |
| B-04 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify — modo `--check` que compara sin reescribir `skills/manifest_skills.json` (D5): exit 0 si coincide, exit 2 si difiere, y el archivo queda con el mismo hash; test en `tests/test_mass_standardizer.py` | medium | `skill_architect` | ⏳ |
| B-05 | `Makefile` | modify — tras B-03, B-04: `verify` usa ambos modos sin escritura | low | `implementer_agent` | ⏳ |
| C-01 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | create — re-medición `RA-19` para el CLI actual: miembros `E16` sin probar, subárboles inferidos por contención, `Edit(/.git/modules/.agents/**)`, D-8; incluye el núcleo con el sandbox de B-06, y la viabilidad de que `devops_agent` ejecute `gh` bajo el sandbox sin entrada en `excludedCommands` ni otra vía fuera del sandbox (`RA-09`, `RA-19`), con comandos `gh` de solo lectura y su salida literal. `devops_agent` mide con `model: sonnet` (escalado desde `mechanical` por riesgo high) y entrega la salida literal; `doc_orchestrator` escribe | high | `devops_agent` | ⏳ |
| C-02 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — tras C-01, A-02: `F-055-N1` pasa a cerrado si C-01 mide su vector sin punto escribible por el agente, o queda abierto con la medida de C-01 citada; `F-116-N1` se marca cerrado citando los commits de A-01 (`ef490cd`, `919d4f2`) y `F-116-N2` citando el de A-02 | low | `doc_orchestrator` | ⏳ |

### Wave 5 — Régimen (decisiones con las medidas en la mano)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `docs/decisions/ADR-0019-sandbox-regime.md` | create — tras B-02, C-01: `RA-09`, fila `gh`, D-12, ruta BD (`KI-057-1`) y hooks en el núcleo (D6, D12). Requisito (decisión humana 2026-11-08): `devops_agent` ejecuta `gh` en lugar del humano si C-01 mide que es posible sin abrir una vía fuera del sandbox; si C-01 mide que no, el ADR lo registra y `gh` sigue en manos del humano | high | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| D-02 | `agents.md` | modify — tras A-12, D-01: `RA-09` y `§2 graph_sync` (D-10); `wc -c agents.md` ≤ 20000 tras el cambio, y el detalle nuevo va a `rules/project_topology.md` (D-03), no a `agents.md` | high | `rule_validator` | ⏳ |
| D-03 | `rules/project_topology.md` | modify — tras A-10, D-01: §4 fila `gh` (D-3), D-1, D-4, coste de `git -C .agents fetch` (QA2-3) | medium | `rule_validator` | ⏳ |
| D-04 | `claude/settings.hooks.json` | modify — tras D-01: bloque `sandbox` (ruta BD local, `KI-057-1`) solo si ADR-0019 aprueba una ruta medida; si no, `RECORD` | high | `implementer_agent` | ⏳ |
| E-01b | `claude/settings.hooks.json` | modify — tras E-01, D-01, D-04 (mismo archivo que D-04, en serie): el comando `SessionEnd` resuelve la ruta en núcleo y en host, si ADR-0019 aprueba hooks en el núcleo (D13); si no, `RECORD` y `suspend` manual sigue documentado | medium | `implementer_agent` | ⏳ |

### Wave 6 — Endurecimiento, roles y residuos del 058

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E-02 | `claude/mcp.json` | modify — servidor MCP de GitHub remoto con OAuth (sin token en archivo) | medium | `implementer_agent` | ⏳ |
| E-03 | `.github/workflows/ci.yml` | modify — fijar `actions/checkout`, `actions/setup-python`, `errata-ai/vale-action` por SHA | low | `implementer_agent` | ⏳ |
| F-01 | `docs/decisions/ADR-0020-owner-writer-dispatch.md` | create — C-7: cuándo el owner escribe un artefacto trivial sin dispatch (enmienda `ADR-0017`) | medium | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| F-02 | `config/artifact_registry.json` | modify — tras F-01: si ADR-0020 se aprueba, registra la excepción owner-escribe con la condición que fije el ADR y `python3 scripts/check_role_artifact.py` exit 0; si no se aprueba, `RECORD` sin cambio | medium | `implementer_agent` | ⏳ |
| I-01 | `scripts/check_absolute_paths.py` | modify — `fix(` `KI-058-1`: escanear también el índice y los archivos sin trackear; paired test nuevo `tests/test_check_absolute_paths.py` | low | `implementer_agent` | ⏳ |
| I-02 | `scripts/upstream_outbox.py` | modify — `fix(` `KI-058-4`: `read_text_file` pasa por `read_regular_bytes`, así un FIFO sale 2 en vez de colgarse; paired test con un FIFO en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-03 | `scripts/upstream_outbox.py` | modify — tras I-02: `fix(` `KI-058-5` a: `deltas` sale 2 con un directorio `--rules` inexistente; paired test en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-04 | `scripts/upstream_outbox.py` | modify — tras I-03: `fix(` `KI-058-5` b: `export --out` a un directorio inexistente sale 2 con mensaje en vez de traceback; paired test en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-05 | `scripts/upstream_outbox.py` | modify — tras I-04: `fix(` `KI-058-5` c: `PIN_PATTERN` solo acepta dígitos ASCII (`[0-9]`); paired test con dígitos no ASCII en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-06 | `hooks/on_commit.py` | modify — `fix(` `KI-058-5` d: un asunto `FIX:` en mayúsculas se trata como `fix(`; paired test en `tests/test_on_commit.py` | low | `implementer_agent` | ⏳ |
| I-07 | `scripts/check_fix_reproduces.py` | modify — `fix(` `KI-058-5` d: el mismo caso que I-06 en la reproducción; paired test en `tests/test_check_fix_reproduces.py` | low | `implementer_agent` | ⏳ |
| I-08 | `scripts/check_task_scope.py` | modify — `fix(` D36: `--current-sprint` sale 2 cuando el anchor nombra un sprint cuyo directorio falta; `current_sprint_dir` distingue ese caso de la ausencia de anchor; paired test en `tests/test_check_task_scope.py` | low | `implementer_agent` | sustituida por M-02 (D37) |
| I-09 | `scripts/check_gate_log.py` | modify — tras I-08: `fix(` D36: sale 2 con un `--sprint-dir` inexistente y con el caso de I-08 en `--current-sprint`; paired test en `tests/test_check_gate_log.py` | low | `implementer_agent` | sustituida por M-03 (D37) |
| I-10 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify — tras I-08: `fix(` D36: el caso de I-08 en `--current-sprint` sale 2; paired test junto a los de `audit_plan.py` | low | `skill_architect` | sustituida por M-04 (D37) |

### Cierre

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `CHANGELOG.md` | modify — entrada `[Unreleased]` del sprint; cita `host:F-116-N1` y `host:F-116-N2` (`agents.md §4 feedback_upstream`, cierre) | low | `doc_orchestrator` | ⏳ |
| Z-02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — cerrar o re-enrutar `KI-056-1`, `KI-056-6`, `KI-057-1`, `KI-057-2`, `KI-058-1`, `KI-058-3`, `KI-058-4`, `KI-058-5`; `KI-058-2` y los condicionados de Out of scope quedan con su condición de desbloqueo; nuevos `KI-059-n`, incluido uno para los puntos 3-5 de la propuesta E (P11); enruta o cierra con evidencia cada fila `KI-059-n` de la tabla de `SPRINT_LOG.md` que siga abierta; esa tabla es la lista (D36) | low | `doc_orchestrator` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | — |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Cálculo de lotes paralelos (`check_task_scope.py`, G-01) | script | `workflows/pipeline_workflow.md` Phase 6 (G-02) |
| Presupuesto por unidad y puntos de suspend (`check_task_scope.py` con `config/unit_cost_estimates.json`, H-02) | script | `workflows/pipeline_workflow.md` Phase 4.3 (A-04); recalibración de la tabla: paso advisory en `workflows/close_workflow.md` (H-03) |
| Medición en sesión de la cota §3.1 (`session_cost.py --bound` o lo que fije ADR-0018) | script | `workflows/pipeline_workflow.md` Phase 6 (A-04) |
| Recuento de autorizaciones (`scripts/prompt_count.py`) | script | advisory en `workflows/close_workflow.md` (B-07); `PROMPT_MEASUREMENT.md` registra la medida, no la invoca |
| Comprobación del manifiesto sin escritura (`generate_manifest.py --check`) | script | `Makefile` `verify` (B-05) |
| Referencias de sprint, comprobaciones y tope de Notes (`scripts/check_sprint_refs.py`, D37) | script | `Makefile` `verify` (M-07) |
| Criterio de éxito de D37 (rondas por wave y familia de R12-1, waves 2 a 6) | agent judgment | `principal_agent` al cierre, desde las tablas Quality Gate y Gate findings |
| Retirado por D35: registros de sprint sin borrado (`scripts/check_log_append_only.py`, D34) | script | `Makefile` `verify` (A-51); QA Gate 1 en el Sprint 059 |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 119 (D37: 92 + 16 de la wave 1b + M-17 + M-18 a M-21 y B-08 + B-09, M-22 y M-23 + B-10 y M-24; I-08 a I-10 siguen contadas como sustituidas) | Count of rows in Work tables |
| Subagents dispatched | lotes de hasta 4 en paralelo desde la wave 3 (D11), más QA + Tester por wave | `agent_assignment.md` |
| Session ratio (2026-11-08, QA rondas 12 y 13, wave 1b) | Sesión `e9a7a9bf`, ciclo único: 5.4× durante la sesión, sobre soft (5×); `suspend` antes de QA Gate 1 ronda 14 | `python3 -I scripts/session_cost.py --session e9a7a9bf-bf5b-4800-bd46-edd6c8fc46c5 --json` |
| Session ratio (2026-11-07, QA rondas 8 a 11) | Sesión `93b61aea`, ciclo único: lectura de 5.0× durante la sesión, en soft (5×); el valor final lo da el comando. Quedan 44 unidades en 5 waves más cierre y los gates de la wave 1; delegación `native`; `suspend` antes de QA Gate 1 ronda 12 | `python3 -I scripts/session_cost.py --session 93b61aea-d168-4293-97f5-340681b5c33a --json` |
| Session ratio (2026-11-07) | Sesión `7a037351`, ciclo único, `session_cost.py` de `919d4f2` — supera soft (5×). Quedan 41 unidades en 5 waves más cierre y los gates de la wave 1; delegación `native`; `suspend` antes de QA Gate 1 ronda 8 | `python3 -I scripts/session_cost.py --session 7a037351-d2f6-4ff2-8ca0-1e6a82e612cc --json` |
| Session ratio (2026-11-05) | **6.1×** sesión `9679503b`, ciclo único, medida completa con `session_cost.py` de `919d4f2` (corte de D19; durante la sesión se leyó 5.4× y 5.9×) — supera soft (5×). Quedan 41 unidades en 5 waves más cierre; delegación `native`; tras los gates de la wave 1, `suspend` | `python3 -I scripts/session_cost.py --session 9679503b-5e2c-4a1a-b3dd-a42dacd42cd6 --json` |
| Prior session ratio | **9.2×** (ciclo 2; ciclo 1 4.6×), de `session_cost.py` en `08c669c` sobre la sesión `7204cadc`, cifra inflada por `F-116-N1`; con el `session_cost.py` de `919d4f2` (D19) es 3.6×; entonces superaba soft (5×). Coste restante declarado: 53 unidades en 6 waves más cierre, una wave por sesión, `suspend` entre waves | `python3 -I scripts/session_cost.py --session 7204cadc-d44b-4226-a000-597c17b52b33 --json` da la cifra de `919d4f2`; la de `08c669c` sale de `git show 08c669c:scripts/session_cost.py` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `tests/test_session_cost.py`: un ciclo cuyo primer turno tiene `cache_read` 0 y `cache_creation` > 0 devuelve `ratio` numérico | **Yes** — this is the defect | `unverified`: el test no existe todavía (A-01). Defecto observado en datos: `sessions=33 first_turn_zero_cycle1=11`, exit 0 |
| `check_task_scope.py` imprime lotes que respetan `Depends on` y archivos disjuntos | **Yes** — la columna no existe | `unverified`: funcionalidad nueva (G-01) |
| `install.py` en modo núcleo escribe `sandbox.autoAllowBashIfSandboxed: true` | **Yes** — `install_nucleus_bridge` no instala sandbox | `unverified`: se mide al abrir la wave 2 con un fixture de núcleo |
| `check_task_scope.py` sale 2 cuando el `Est. cost` acumulado supera soft sin un `Suspend after: yes` previo | **Yes** — las columnas no existen | `unverified`: funcionalidad nueva (H-02) |
| `session_cost.py --bound` imprime `HARD` y sale 0 en un ciclo de 16× | **Yes** — el flag no existe | `unverified`: flag nuevo (A-02) |
| `scripts/py_compile_tree.py` no crea `__pycache__` | **Yes** — escribe `.pyc` | `unverified`: se mide al abrir la wave 4 con `find` antes/después |
| `tests/test_session_end_hook.py`: `SessionEnd` de otra sesión no suspende | **Yes** según `KI-057-2` | `unverified`: `KI-057-2` dice "not reproducible as specified (W13)"; E-01 reproduce primero o se cierra como `RECORD` |
| `tests/test_session_state.py`: `suspend` con sprint sellado y sesión `IN_PROGRESS` libera el lock (E-01c) | **Yes** — deja el lock tomado | `unverified`: observado en Phase 1 (el boot siguiente salió 2 y exigió `--takeover`); el test se escribe y se ve fallar al abrir la wave 2 |
| `tests/test_mass_standardizer.py`: `generate_manifest.py --check` sale 2 ante un manifiesto distinto y no reescribe el archivo (B-04) | **Yes** — el flag no existe | `grep -c -- '--check' skills/mass-standardizer/scripts/generate_manifest.py` → 0, exit 1 |
| Paired tests de I-01..I-07 (`KI-058-1`, `KI-058-4`, `KI-058-5` a-d) | **Yes** — cada uno es un defecto registrado | `unverified`: cada test se escribe y se ve fallar en el padre al abrir la wave 6; `scripts/check_fix_reproduces.py` lo exige en Gate 1 |
| Sustituida por D37: paired tests de I-08..I-10 (D36) | **Yes** — medido en QA Gate 1 ronda 11 | `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/059-typo` → exit 0 con `(skip)`; cada test se ve fallar en el padre |
| `tests/test_token_economy_soft_bound.py` (A-25) | **Yes** — segunda ocurrencia de la familia de N3 (D23) | tras D32 cubre la conducta de `probe_cost` a 6× y a 16×; sin copia de texto |
| `tests/test_profile_references.py` (A-31) | **Yes** — familia de datos de host (D24) | el test se ve fallar en `d06c939` por cada uno de los 4 archivos |
| Retirado por D35: `tests/test_check_log_append_only.py` (A-50) | **Yes** — segunda ocurrencia de la familia de F6 (D34) | `unverified`: el check no existe todavía; A-49 lo ve fallar en `10c88f4`, `1dbb43e` y `60383e3` |
| `tests/test_current_sprint_matrix.py` (M-05): ningún script con `--current-sprint` sale 0 en la batería de M-05 | **Yes** — medido el 2026-11-07 | desde `docs/`, `check_gate_log.py`, `check_task_scope.py` y `audit_plan.py` con `--current-sprint` → `(skip)`, exit 0; `audit_plan.py` con id `"059"` → exit 0; `loop_guard.py --current-sprint` → exit 2; `loop_guard.py check --sprint-dir` inexistente → exit 0 (R13-1) |
| `tests/test_check_sprint_refs.py` (M-06): un id citado sin casa sale 2 | **Yes** — el script no existe | `unverified`: script nuevo; se ve fallar al abrir la wave 1b |
| Suite completa `make verify` | **No** — regresión a proteger | `make verify` → exit 0 en `08c669c` |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `wc -c agents.md` | ≤ 20000 | exit 0; 53907 | la propia corrida de base es el control positivo |
| `grep -n "^model:" agents/qa_agent.md` | `model: opus` (D20: prueba revertida) | exit 0; `model: opus` | la propia corrida de base es el control positivo |
| `python3 -I scripts/session_cost.py --from-anchor --json` | exit 0, todos los `ratio` numéricos | exit 0; ratios 4.6 y 9.2 (esta sesión no tiene ciclo frío) | bucle sobre los 33 transcripts: 11 con `first_turn` 0 |
| `grep -rn -e session_cost -e session_probe hooks/` | sin salida (D2: el invocador es un workflow, no un hook) | exit 1, sin salida | `grep -n -e session_cost -e session_probe scripts/session_start.py` → líneas 444, 679, exit 0 |
| `grep -n "isolation" workflows/pipeline_workflow.md` | una línea en Phase 6 (G-02) | exit 1 (aún no existe) | n/a: la salida esperada no es vacía |
| `make verify` | exit 0 | exit 0 en `08c669c` | n/a |
| `python3 scripts/check_sprint_refs.py --current-sprint` | exit 0 tras M-11 | `unverified`: el script no existe (M-06) | el mismo comando sobre un fixture que cita un KI del sprint ausente de su tabla → exit 2 (`tests/test_check_sprint_refs.py`) |
| `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | exit 0 | exit 0 en `08c669c`; 1527 passed | n/a |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | exit 0 | run at close: se ejecuta sobre el borrador antes de Phase 5 | n/a |
| `grep -n "@v[0-9]" .github/workflows/ci.yml` | sin salida tras E-03 | exit 0, líneas 24, 28, 39 | la propia corrida de base es el control positivo |
| Retirada por D35, el script ya no existe: `python3 scripts/check_log_append_only.py --sprint-dir docs/sprints/059-core-pipeline --range 60383e3..HEAD` | exit 0 tras A-47 (D34) | `unverified`: el check no existe todavía (A-49) | el mismo comando con `--range 10c88f4^..10c88f4` → exit 2 |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | recortado a índice de reglas (D10); `RA-09`, `graph_sync` según ADR-0019 |
| `rules/code_craft.md`, `rules/project_topology.md`, `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | reciben el detalle movido desde `agents.md`; §4 de `project_topology.md` según ADR-0019 |
| `agents/qa_agent.md`, `config/model_tiers.json` | sin cambio neto: la prueba D9 se revirtió (D20) |
| `workflows/pipeline_workflow.md` | Phase 6: lotes paralelos (D11) y paso de medición |
| `rules/token_economy.md` | §3.1 unidad y invocador |
| `CHANGELOG.md`, roadmaps 014 a 017, `docs/sprints/023-core-pipeline/task_scope.md` | nombre de host genericizado con anotación (D22) |
| `tests/test_token_economy_soft_bound.py` | nuevo: fija el texto soft de §3.1 (D23); reducido por D32 a la conducta de `probe_cost`, sin copia de texto |
| Roadmaps 008 y 018, `skills/skillopt/data/scenarios.json`, `skills/mcp-registry/README.md`, `profiles/example-project/mcp/registry.json`, `docs/guides/RULE_PRECEDENTS_GUIDE.md` | dominio y roles genericizados (D29) |
| `tests/test_profile_references.py`, `workflows/reverse_documentation_workflow.md` | nuevo check de referencias a perfiles; dominio genericizado (D24) |
| `scripts/check_log_append_only.py`, `tests/test_check_log_append_only.py`, `Makefile`, `README.md`, `rules/documentation_standard.md`, `docs/standards/templates/HOTFIX_TEMPLATE.md` | retirado por D35, sin cambio neto salvo `HOTFIX_TEMPLATE.md`: nuevo check de registros sin borrado (D34), con el contador de scripts que exige `check_readme_counts.py`; destino de la escalada en la plantilla (D33) |
| `config/rule_triggers.json` | carga `rules/documentation_standard.md` al editar `rules/*.md` (D28) |
| `rules/qa_and_testing.md`, `agents/governance_learner.md`, `agents/rule_validator.md`, `workflows/remediation_workflow.md`, `rules/documentation_standard.md` | momento de `RA-19` (D25; sustituida por D30: la repetición solo tras un S0 que toque sandbox o ejecución) y destino del aprendizaje (D26) |
| `docs/guides/RULE_PRECEDENTS_GUIDE.md` | nuevo: historia y precedentes de las filas de `agents.md` sin otro destino (A-13) |
| `docs/decisions/ADR-0021-qa-agent-tier-trial.md`, `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | nuevo ADR de la prueba D9 y su cita en la guía (A-14) |
| `rules/skills_and_integrations.md`, `rules/qa_and_testing.md`, `config/rule_triggers.json` | reciben reglas de una tarea concreta desde la guía de precedentes (A-15, A-16, A-17) |
| `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md`, `PROMPT_MEASUREMENT.md`, `SANDBOX_ENUMERATION.md` | nuevos |
| `config/unit_cost_estimates.json` | nuevo: tabla de estimación de coste por unidad |
| `docs/decisions/ADR-0018-*`, `ADR-0019-*`, `ADR-0020-*` | nuevos: token economy en sesión, régimen de sandbox, owner/writer |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | triage y estado de `F-116-N1/N2`, `F-055-N1` |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | cierre/re-enrutado de KIs, incluidos `KI-058-1`, `KI-058-4`, `KI-058-5` |
| `CHANGELOG.md` | entrada `[Unreleased]` |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `KI-058-2` (bump de `graphifyy`) | Condicionado: espera a un release upstream con `--include-json` |
| Auditoría de prompts | Sprint 060 completo: depende del recorte de `agents.md` y del resultado de `qa_agent` en `sonnet`, y meterla aquí retrasaría el despliegue del ahorro de la wave 1 a los hosts |
| Bloquear en hard (exit 2) | Cuando la calibración de §3.1 tenga n > 1 (D3) |
| `install.py` instala los comandos `agents:*` en todo host sin preguntar, así que el borrado de Phase 1 se revierte al reinstalar | Pregunta del estudio A-00 (comandos opt-in por host); si no se decide, `KI-059-n` |
| Más de 4 subagentes en paralelo | Se reevalúa con la medición de integración de la wave 3; el límite vive en `/config` |

---

## Abort criterion

1. Si C-01 mide un punto de entrada sin sandbox escribible por el agente que no
   estaba en `SANDBOX_ENUMERATION.md` (056), la wave 5 no cambia `RA-09`/`RA-19` ni
   instala hooks en el núcleo: la fila pasa a `KI-059-n` y el resto sigue. Si ese
   punto lo abre el bloque `sandbox` que instaló B-06 (adelantado a la wave 2 antes
   de esta medición), B-06 se revierte en el mismo paso.
2. Si B-02 no puede contar autorizaciones desde transcripts, ninguna regla se relaja
   por "menos autorizaciones" y el instrumento se re-planifica con el humano.
3. Si el debate de A-06 no cierra una decisión en la sesión de la wave 3, A-02..A-04
   se implementan con D2/D3 tal como están y el método pasa a `KI-059-n`.
4. Si un gate posterior encuentra un defecto que QA Gate 1 en `sonnet` debía haber
   visto, A-08 se revierte (`qa_agent` vuelve a `opus`) y se registra en
   `SPRINT_LOG.md`.
5. Si con B-06 aplicado `make verify` o un paso de Phase 6 falla en el núcleo por el
   sandbox, B-06 se revierte y el bloqueo medido pasa a C-01.
6. Si integrar un lote paralelo produce un conflicto de git, ese lote se re-ejecuta
   en serie y G-02 se revisa antes del siguiente lote.
7. Si A-00 no puede atribuir coste a unidades (los transcripts no permiten cruzar
   turnos con commits), H-01 arranca con estimaciones marcadas `unmeasured`,
   H-02 solo avisa (exit 0) y la calibración pasa a `KI-059-n`.
8. Más de 3 `REJECTED` consecutivos del mismo bloque → `remediation_workflow.md`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal («Aprobado», Phase 5, session `b1572a48`) |
| **Date** | 2026-11-02 |
| **Plan commit at approval** | `65c86d3` (this block and the P11/Z-02 routing of proposal E were added after approval, as recorded) |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
