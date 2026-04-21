# KI: Protocolo de Orquestación de Matriz e Identidad (Fase 11)

## 📋 Resumen
Consolidación de la gobernanza de Universal-Agents mediante la centralización de roles operativos y la implementación del Triple Lock de autorización.

## 🧠 Heurísticas Destiladas
1.  **Segregación de Roles:** Fase 1 (Mentor), Fase 2 (Orchestrator), Fase 3 (DevOps), Fase 4 (Matrix), Fase 5 (Auditor/QA). Cada fase tiene prohibiciones explícitas de ejecución de herramientas.
2.  **Mandato del 100%:** Cualquier módulo táctico debe alcanzar el 100% de cobertura antes de ser integrado.
3.  **Lock de Arsenal:** Si una skill no está en el `manifest_skills.json`, debe debatirse su búsqueda mediante tablas comparativas (Regla 11).
4.  **WIP Safety Freeze:** Ejecutar `git status --porcelain` antes de cualquier provisión de entorno para detectar cambios humanos no confirmados.

## 🛠️ Comandos Clave
- `npx -y autoskills@latest`: Para auditoría de arsenal (previa autorización).
- `git status --porcelain`: Centinela de integridad de DevOps.
- `00x-00y-agent-task.md`: Nomenclatura obligatoria de aislamiento.

---
*ID: ki_011_identity_matrix_orchestration*
*Domain: Governance*
*Source Session: #7a3f4e2b*
