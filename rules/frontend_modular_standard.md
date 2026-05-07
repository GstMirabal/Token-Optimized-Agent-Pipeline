# 🛡️ Rule 041: Frontend Modular Standard (Matrix V2)

## 1. Directory Anatomy (Rule 41.1)
Todo módulo dentro de `frontend/src/modules/` debe adherirse a la siguiente estructura mínima para garantizar la interoperabilidad y el aislamiento:
- `pages/`: Contiene exclusivamente las vistas de nivel de ruta (Sufijo: `View.tsx`).
- `components/`: Componentes atómicos o moleculares específicos del dominio del módulo.
- `api/`: Definiciones de interfaces y servicios de comunicación con el backend.
- `hooks/`: Lógica de estado y efectos encapsulada.
- `store/`: (Opcional) Definiciones de estado global específicas del módulo (Zustand/Redux).
- `index.ts`: La **Public API** del módulo. Solo lo exportado aquí es accesible desde fuera del módulo.

## 2. Cross-Module Communication (Rule 41.2)
- **Zero-Leaking**: Está estrictamente **PROHIBIDO** importar archivos directamente desde las subcarpetas de otro módulo (ej. `import { UserCard } from "@/modules/users/components/UserCard"` es ILEGAL).
- **Public Access**: Las importaciones entre módulos deben realizarse a través del punto de entrada raíz del módulo (ej. `import { UserCard } from "@/modules/users"`).

## 3. UI Consistency (Rule 41.3)
- **Sovereign Aesthetic**: Todos los componentes del módulo deben heredar los tokens de diseño definidos en `SovereignLayout` y utilizar `framer-motion` para transiciones de estado de vista.
- **Loading States**: Toda `View.tsx` debe implementar un estado de carga (Skeleton o Loader premium) mientras se resuelven las promesas de la API.

---
*Vigente desde: 2026-05-07*
*Estado: ACTIVE*
