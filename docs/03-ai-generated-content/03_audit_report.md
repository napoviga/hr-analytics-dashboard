# Audit Report — HR Analytics Dashboard

> **Generado automáticamente:** 2026-04-11T06:35:00Z
> **Ejecutado por:** Qwen Code Terminal
> **Alcance:** Código fuente frontend (10 archivos), scripts ETL (8 archivos), configuración, documentación
> **Baseline:** Blueprint + Data Dictionary generados el 2026-04-11

---

## Matriz de Hallazgos

| # | Severidad | Pilar | Hallazgo | Archivo | Línea (aprox.) | Solución Propuesta |
|---|-----------|-------|----------|---------|----------------|--------------------|
| 1 | 🔴 | Seguridad | `.env` con credenciales expuestas — posible commit al repo | `client/.env` | 1-2 | Agregar `.env` al `.gitignore`, crear `.env.example`, rotar key |
| 2 | 🔴 | Hardcoding | `OrganigramaIntegral.jsx` es 100% datos estáticos mock | `OrganigramaIntegral.jsx` | 8-100 | Conectar a Supabase RPC o marcar como placeholder |
| 3 | 🔴 | Accesibilidad | **CERO** `aria-label` en TODOS los íconos Lucide del proyecto (~30+ íconos) | Todos los `.jsx` | Múltiples | Agregar `aria-hidden="true"` a íconos decorativos |
| 4 | 🟡 | Zombie Code | `import React` no usado (React 19 usa JSX runtime automático) | `Sidebar.jsx`, `SectionLanding.jsx`, `Demographics.jsx` | 1 | Eliminar `import React` |
| 5 | 🟡 | Hardcoding | Botones navegan a `org_dotacion` que no existe en navigationConfig | `OrgStructure.jsx` | 34, 46 | Agregar `org_dotacion` al config o eliminar botón |
| 6 | 🟡 | Hardcoding | Nombre "JESUS VILLEGAS" hardcodeado en footer del Sidebar | `Sidebar.jsx` | 161-162 | Usar `supabase.auth.getUser()` o prop |
| 7 | 🟡 | Best Practice | `fetchEmpleados()` carga TODA la tabla en mount sin importar la vista activa | `App.jsx` | 22-38 | Lazy-load solo cuando la vista lo necesite |
| 8 | 🟡 | Seguridad | Tooltip de ECharts usa `innerHTML` con template literal — riesgo XSS | `Compensations.jsx` | 30-35 | Usar rich text formatter o sanitizar valores |
| 9 | 🟡 | Best Practice | Hook `useDemographicsFilters` no maneja error de fetch — dropdowns vacíos sin feedback | `useDemographicsData.js` | 84-97 | Agregar estado de error y mostrarlo en UI |
| 10 | 🟡 | Consistencia | `Compensaciones` importado con nombre español pero archivo es `Compensations.jsx` | `App.jsx` | 9-13 | Renombrar import a `Compensations` |
| 11 | 🟡 | Consistencia | Dos temas visuales: oscuro (`bg-gray-900`) en Overview/Compensations vs claro (`bg-white`) en Demographics | Múltiples | — | Unificar tema o documentar diferencia intencional |
| 12 | 🟡 | Best Practice | IDs de vistas hardcodeados en condicionales JSX de App.jsx | `App.jsx` | 93-99, 101 | Extraer a constantes o derivar de navigationConfig |
| 13 | 🟢 | Zombie Code | Doble import de `lucide-react` (namespace + named) | `Sidebar.jsx` | 2-3 | Consolidar en un solo import (menor) |
| 14 | 🟢 | Best Practice | `EmployeeTable` usa `employeenumber` como key — posible duplicado | `EmployeeTable.jsx` | 16 | Verificar unicidad o usar UUID |
| 15 | 🟢 | Best Practice | Sin PropTypes ni JSDoc en `EmployeeTable` | `EmployeeTable.jsx` | 1 | Agregar validación de props |
| 16 | 🟢 | Mejora | `Demographics.jsx` (~270 líneas) con configs de ECharts inline | `Demographics.jsx` | 19-197 | Extraer a `chartConfigs.js` o custom hooks |
| 17 | 🟢 | Mejora | Mezcla de idiomas: UI en español, identificadores en inglés | Múltiples | — | Documentar estrategia de i18n futura |
| 18 | 🟢 | Seguridad | `.gitignore` del root protege bien, pero el de `client/` NO incluye `.env` | `client/.gitignore` | — | Agregar `.env` al gitignore del client |

---

## Score de Calidad

```
Score de Calidad del Proyecto: 76/100

Desglose:
  - Seguridad:          18/25  (.env expuesto, falta RLS awareness, tooltip XSS risk)
  - Limpieza de código: 20/25  (OrganigramaIntegral mock completo, imports React no usados)
  - Buenas prácticas:   17/25  (aria-label ausente en todos los íconos, fetch eager, error handling)
  - Consistencia:       21/25  (naming español/inglés, temas visuales mixtos, view IDs hardcodeados)
```

---

## Correcciones para Hallazgos Críticos

### R-1: SEGURIDAD — `.env` expuesto en version control

**Archivo:** `client/.gitignore`

```diff
  /src/generated/prisma
+
+# Environment variables (secrets)
+.env
+*.env
+*.env.*
+!.env.example
```

Crear `client/.env.example`:
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_your-key-here
```

**Y en el root `.gitignore`**, verificar que ya incluya `.env` (el actual tiene 160+ líneas, confirmar que `.env` esté cubierto).

---

### R-2: HARDCODING — OrganigramaIntegral es stub completo

**Archivo:** `client/src/modules/05-fuerza-laboral/OrganigramaIntegral.jsx`

Opción A — Conectar a datos reales (recomendado):
```jsx
// TODO: Implementar fetch desde business.v_org_tree_bynapo
// o RPC dedicada
```

Opción B — Marcar como placeholder:
```diff
  export default function OrganigramaIntegral() {
    return (
      <div className="p-2 min-h-screen">
        <div className="mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
              <div className="bg-blue-100 p-3 rounded-lg text-blue-600"><Users size={24} aria-hidden="true" /></div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Total Empleados</p>
-               <p className="text-2xl font-bold text-slate-800">1,470</p>
+               <p className="text-2xl font-bold text-slate-800">--</p>
              </div>
            </div>
```

---

### R-3: ACCESIBILIDAD — `aria-hidden` en todos los íconos

**Afecta:** 5 archivos, ~30+ íconos

**Sidebar.jsx** (representativo):
```diff
- <Grip size={22} />
+ <Grip size={22} aria-hidden="true" />

- <IconComponent size={20} strokeWidth={isModuleActive ? 2.5 : 2} className="text-current" />
+ <IconComponent size={20} strokeWidth={isModuleActive ? 2.5 : 2} className="text-current" aria-hidden="true" />

- {isModuleOpen ? <ChevronDown size={16} ... /> : <ChevronRight size={16} ... />}
+ {isModuleOpen ? <ChevronDown size={16} aria-hidden="true" ... /> : <ChevronRight size={16} aria-hidden="true" ... />}

- <Icons.Lock size={20} ... />
+ <Icons.Lock size={20} aria-hidden="true" ... />

- <UserCircle size={24} />
+ <UserCircle size={24} aria-hidden="true" />
```

**SectionLanding.jsx:**
```diff
- <ModuleIcon size={24} />
+ <ModuleIcon size={24} aria-hidden="true" />
```

**OrgStructure.jsx** (8 íconos):
```diff
- <Icon size={20} />
+ <Icon size={20} aria-hidden="true" />
```

**App.jsx** (SVG inline):
```diff
- <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
+ <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true" role="img">
```

**Overview.jsx** (2 SVGs):
```diff
- <svg className="w-8 h-8 text-blue-400" ...>
+ <svg className="w-8 h-8 text-blue-400" aria-hidden="true" role="img" ...>
```

---

## Correcciones para Hallazgos Moderados (🟡)

### M-1: Eliminar `import React` no usado

```diff
  // Sidebar.jsx
- import React, { useState } from 'react';
+ import { useState } from 'react';

  // SectionLanding.jsx
- import React from 'react';
+ // React import removed — JSX runtime is automatic in React 19

  // Demographics.jsx
- import React from 'react';
+ // React import removed
```

### M-2: Agregar `org_dotacion` al navigationConfig

```diff
  // client/src/config/navigation.js — en subItems de 05-fuerza-laboral:
+ { id: 'org_dotacion', title: 'Organigrama de Posiciones', icon: 'Network', description: '...' },
```

### M-3: Fetch lazy de empleados en App.jsx

```diff
- useEffect(() => { fetchEmpleados(); }, []);
+ // Mover fetch a los componentes que lo necesitan:
+ // Overview, Compensations, EmployeeTable
```

---

## Resumen

| Severidad | Count |
|-----------|-------|
| 🔴 Crítico | 3 |
| 🟡 Moderado | 10 |
| 🟢 Menor | 5 |
| **Total** | **18** |

### Top 3 Prioridades

1. **Proteger `.env`** — Agregar al `.gitignore` del client y root, crear `.env.example`, rotar la anon key expuesta
2. **Conectar OrganigramaIntegral a datos reales** — O marcar claramente como placeholder
3. **Agregar `aria-hidden="true"` a todos los íconos** — 30+ cambios en 5 archivos, impacto directo en accesibilidad WCAG 2.1

---
