# Memory Log: Sprint 034 - Sovereign Identity Hardening

## Technical Friction Points & Lessons Learned

### 1. TypeScript: Verbatim Module Syntax Compliance
**Context**: The project has `verbatimModuleSyntax` enabled.
**Problem**: Mixing value imports (instances) and type imports (interfaces) in a single de-structuring line without the `type` qualifier leads to absolute compiler failure.
**Resolution**: Enforce split import lines:
```typescript
import { valueInstance } from "./module";
import type { InterfaceType } from "./module";
```

### 2. Governance: Rule 1.3 (Cognitive Limits)
**Context**: Complex UI flows (handshakes, wizards).
**Lesson**: Inline implementation of wizards within main pages invariably causes cognitive complexity violations (>50 lines per logical block). 
**Resolution**: Atomic extraction of wizards to `frontend/src/components/` is a mandatory architectural pattern.

### 3. Governance: Rule 2.1 (Error Trapping)
**Context**: Global state management (Zustand).
**Lesson**: Relying on "error handled by store" to justify silent `catch` blocks in components is a violation. Explicit institutional logging (`console.error`) is required at every capture point.

## Certification
**EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED**
