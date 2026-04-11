# Audit Report — HR Analytics Dashboard

> **Generado automaticamente:** 2026-04-11T23:00:00Z
> **Ejecutado por:** Qwen Code Terminal
> **Alcance:** Codigo fuente frontend, scripts ETL, configuracion, documentacion

---

## Matriz de Hallazgos

| # | Severidad | Pilar | Hallazgo | Archivo | Linea (aprox.) | Solucion Propuesta |
|---|-----------|-------|----------|---------|----------------|--------------------|
| 1 | 🔴 | Hardcoding | Datos mock hardcoded en OrganigramaIntegral.jsx — KPIs fijos (1,470 empleados, 3 deptos, $6,500 salario) y estructura organizacional estatica con nombres y conteos fijos | `OrganigramaIntegral.jsx` | ~10-100 | Conectar a `v_org_tree_byNapo` y `mv_monthly_kpis_byNapo` via RPC o query Supabase |
| 2 | 🔴 | Hardcoding | Table name incorrecto en App.jsx — consulta `.from('ibm_hr')` pero la tabla raw se llama `raw."ibm_hr_monthly_snapshot_byNapo"`; ademas no usa la vista `business.v_employee_full_byNapo` | `App.jsx` | ~26 | Cambiar a `.schema('business').from('v_employee_full_byNapo').select('*')` o usar la vista tipificada |
| 3 | 🔴 | Hardcoding | Fx rate fijo en ETL — `01_generate_synthetic_data.py` usa `fx_rate_to_usd = 3.50` para todos los paises (PER, ESP, CHL, COL, MEX, USA), distorsionando salarios reales | `01_generate_synthetic_data.py` | ~174 | Usar tabla de tasas de cambio reales por moneda o al menos valores diferenciados por pais |
| 4 | 🔴 | Zombie Code | `org_dotacion` referenciado en OrgStructure.jsx pero no existe en navigation.js ni en App.jsx — el boton navega a ruta inexistente | `OrgStructure.jsx` | ~35 | Agregar subItem `org_dotacion` a navigation.js o eliminar el boton |
| 5 | 🔴 | Security | GRANT EXECUTE a `anon` en funciones RPC — `get_demographics_dashboard` y `get_advanced_demographics` otorgan acceso anonimo sin restriccion RLS | `m05_fuerza_laboral.py` | ~176-177 | Evaluar si el acceso anonimo es intencional; si hay auth, usar rol autenticado |
| 6 | 🟡 | Zombie Code | `React` importado pero nunca usado directamente en 5 archivos — JSX transform en Vite no requiere `import React` | `Demographics.jsx`, `OrganigramaIntegral.jsx`, `OrgStructure.jsx`, `SectionLanding.jsx`, `Sidebar.jsx` | ~1 | Eliminar `import React from 'react'` en todos los archivos (React 17+ JSX transform) |
| 7 | 🟡 | Zombie Code | Doble import de `lucide-react` en Sidebar.jsx — `import * as Icons` + `import { Grip, UserCircle, ... }` separados | `Sidebar.jsx` | ~2-3 | Unificar: `import * as Icons from 'lucide-react'` ya incluye todos los iconos individuales |
| 8 | 🟡 | Zombie Code | `echarts` en dependencies pero nunca importado directamente — solo se usa `echarts-for-react` | `package.json` | ~13 | Verificar si `echarts` es peer dependency requerida por `echarts-for-react` (si lo es, marcar como ok) |
| 9 | 🟡 | Zombie Code | `autoprefixer` y `postcss` en devDependencies posiblemente innecesarios con Tailwind v4 + `@tailwindcss/vite` plugin | `package.json` | ~20,24 | Verificar si son requeridos; si no, eliminar |
| 10 | 🟡 | Zombie Code | `prisma` configurado sin schema — `prisma.config.ts` apunta a `prisma/schema.prisma` que no existe | `prisma.config.ts` | ~7 | Crear schema o eliminar dependencia de Prisma si no se usa |
| 11 | 🟡 | Zombie Code | Comentario dead code en navigation.js — `// Changed to UsersIcon to differentiate... wait, 'Users' works. we will map.` | `navigation.js` | ~113 | Eliminar comentario o verificar si `UsersIcon` existe en lucide-react |
| 12 | 🟡 | UI/UX | SVG inline sin `aria-label` ni `role="img"` en App.jsx placeholder y en Overview.jsx — iconos decorativos no son accesibles | `App.jsx` ~107, `Overview.jsx` ~68,78 | Agregar `aria-label="descripcion"` y `role="img"` a cada SVG decorativo |
| 13 | 🟡 | UI/UX | Hardcoded user name en Sidebar — "JESUS VILLEGAS" / "Data y BI" hardcoded en componente de layout | `Sidebar.jsx` | ~155 | Extraer a variable de config o contexto de auth |
| 14 | 🟡 | Consistencia | App.jsx importa `SectionLanding` pero solo se usa cuando `activeModuleObj` es truthy — el estado `empleados` se consulta desde tabla incorrecta y solo se pasa a `Overview` y `EmployeeTable` | `App.jsx` | ~16-37 | Corregir tabla de consulta y considerar lazy loading de datos por vista |
| 15 | 🟡 | UI/UX | Compensations y Overview usan dark theme manual (bg-gray-900, text-gray-400) en vez de clases semanticas Tailwind o sistema de temas | `Overview.jsx`, `Compensations.jsx` | Todo el archivo | Considerar crear componente `Card` reutilizable con variantes claro/oscuro |
| 16 | 🟢 | Sugerencia | `navigation.js` usa icono `UsersIcon` que podria no existir en lucide-react (nombre correcto: `Users`) | `navigation.js` | ~113 | Verificar que `UsersIcon` se resuelve correctamente en Sidebar via `Icons[item.icon]` |
| 17 | 🟢 | Sugerencia | Sin `.env.example` en el proyecto — las variables requeridas no estan documentadas como plantilla | Raiz del proyecto | N/A | Crear `.env.example` con `VITE_SUPABASE_URL=`, `VITE_SUPABASE_ANON_KEY=`, `DATABASE_URL=` |
| 18 | 🟢 | Sugerencia | Script 91 (`91_export_data_samples.py`) comentado en el orquestador — si es util, deberia habilitarse | `00_full_run_pipeline.py` | ~13 | Descomentar o documentar razon para exclusion |
| 19 | 🟢 | Sugerencia | Sin tests automatizados — ni frontend ni ETL tienen pruebas unitarias o de integracion | Todo el proyecto | N/A | Agregar al menos tests criticos para hooks ETL y componentes principales |
| 20 | 🟢 | Sugerencia | Sin CI/CD configurado — no hay archivos `.github/`, `.gitlab-ci.yml` | Raiz del proyecto | N/A | Configurar pipeline basico de lint + build |
| 21 | 🟢 | Sugerencia | `index.html` tiene titulo generico `<title>client</title>` | `index.html` | ~7 | Cambiar a `<title>GDH Analytics</title>` |
| 22 | 🟢 | Sugerencia | 11 modulos placeholder (carpetas vacias) sin indicadores de estado — el usuario navega a subItems sin vista implementada y ve placeholder generico | `modules/01-*` a `14-*` | N/A | Agregar badge "Proximamente" en navigation o deshabilitar subItems sin componente |
| 23 | 🟢 | Buenas practicas | ECharts configs inline en componentes — configuraciones complejas de ~30-50 lineas dentro de funciones de render | `Demographics.jsx`, `Overview.jsx`, `Compensations.jsx` | Varias | Extraer a archivos de config separados o custom hooks para mejor testabilidad |

### Leyenda de Severidad
| Nivel | Significado | Accion |
|-------|-----------|--------|
| 🔴 Critico | Seguridad, hardcoding, datos mock, rutas rotas | Corregir inmediatamente |
| 🟡 Advertencia | Zombie code, deuda tecnica, accesibilidad | Planificar correccion |
| 🟢 Sugerencia | Accesibilidad, mejoras, conveniencia | Mejorar cuando sea conveniente |

---

## Score de Calidad

```
Score de Calidad del Proyecto: 52/100

Desglose:
  - Seguridad:          14/25  (GRANT anon sin restriccion, user name hardcodeado, sin .env.example)
  - Limpieza de codigo: 13/25  (5 imports React innecesarios, doble import lucide,
                                 comment dead code, prisma sin schema, deps posiblemente innecesarias)
  - Buenas practicas:   12/25  (sin aria-label en SVGs, dark theme manual, configs inline,
                                 sin tests, sin CI/CD, titulo generico)
  - Consistencia:       13/25  (table name incorrecto en App.jsx, fx rate fijo en ETL,
                                 org_dotacion ruta fantasma, datos mock en OrganigramaIntegral)
```

---

## Detalle de Analisis

### 1. Deteccion de Hardcoding

#### Datos Mock en OrganigramaIntegral.jsx [🔴]
El componente `OrganigramaIntegral.jsx` contiene datos completamente estaticos:
- KPI: "Total Empleados: 1,470" — valor fijo, no viene de ninguna query
- KPI: "Departamentos Activos: 3" — hardcodeado
- KPI: "Costo Salarial Promedio: $6,500" — hardcodeado
- Estructura org: "Ventas (Sales) — 446 Empleados — 20.6% ATR" — hardcodeado
- Estructura org: "Investigacion y Des. — 961 Empleados — 13.8% ATR" — hardcodeado
- Estructura org: "Recursos Humanos — 63 Empleados — 19.0% ATR" — hardcodeado

No hay ninguna llamada a Supabase, ni hook custom, ni props de datos. Es un mock permanente.

#### Table Name Incorrecto en App.jsx [🔴]
La consulta `supabase.schema('business').from('ibm_hr').select('*')` no corresponde a ningun objeto real en la base de datos:
- En el esquema `raw` existe: `ibm_hr_monthly_snapshot_byNapo`
- En el esquema `business` existe: `v_employee_full_byNapo`
- No existe ninguna tabla o vista llamada `ibm_hr`

Esto causa que el estado `empleados` siempre tenga error o data vacia, afectando `Overview.jsx` y `EmployeeTable.jsx`.

#### Fx Rate Fijo en ETL [🔴]
En `01_generate_synthetic_data.py` linea 174:
```python
snapshot_df["fx_rate_to_usd"] = 3.50
```
Un solo tipo de cambio para 6 paises con monedas diferentes (PEN, EUR, CLP, COP, MXN, USD) distorsiona completamente los salarios en USD y cualquier analisis de compensacion.

#### Colores Hex Hardcodeados en ECharts [🟢]
29 colores hex hardcodeados en configs de ECharts across 3 archivos. No es un problema critico (ECharts requiere colores explícitos), pero seria ideal extraerlos a un archivo de tema compartido.

---

### 2. Dependencias Fantasma y Codigo Zombie

#### Imports de React Innecesarios [🟡]
Con React 19 y el JSX transform automatico de Vite, `import React from 'react'` es innecesario. Afecta 5 archivos:
- `Sidebar.jsx`
- `SectionLanding.jsx`
- `Demographics.jsx`
- `OrganigramaIntegral.jsx`
- `OrgStructure.jsx`

#### Doble Import de Lucide [🟡]
`Sidebar.jsx` importa lucide-react dos veces:
```js
import * as Icons from 'lucide-react';
import { Grip, UserCircle, ChevronDown, ChevronRight } from 'lucide-react';
```
El segundo import es redundante porque `* as Icons` ya incluye todos los iconos.

#### Prisma sin Schema [🟡]
`prisma.config.ts` existe y referencia `prisma/schema.prisma` que no existe en el proyecto. Prisma esta en devDependencies pero no tiene uso verificado.

#### echarts vs echarts-for-react [🟡]
`echarts` esta en dependencies pero solo se importa `echarts-for-react`. Sin embargo, `echarts-for-react` requiere `echarts` como peer dependency, por lo que **si es necesario**. Marcado como verificado OK.

#### autoprefixer / postcss [🟡]
Tailwind CSS v4 con `@tailwindcss/vite` no requiere PostCSS ni autoprefixer manualmente. Probablemente innecesarios.

---

### 3. Archivos Huerfanos

#### Modulos Placeholder (11 carpetas vacias) [🟢]
| Carpeta | Archivos | Estado |
|---------|----------|--------|
| `01-vision-ejecutiva/` | 0 | Vacia |
| `02-reclutamiento/` | 0 | Vacia |
| `03-onboarding/` | 0 | Vacia |
| `04-ciclo-vida/` | 0 | Vacia |
| `07-tiempo-asistencia/` | 0 | Vacia |
| `08-gestion-desempeno/` | 0 | Vacia |
| `09-talento-desarrollo/` | 0 | Vacia |
| `10-engagement-sentimiento/` | 0 | Vacia |
| `11-compliance/` | 0 | Vacia |
| `12-retencion/` | 0 | Vacia |
| `13-calidad-datos/` | 0 | Vacia |
| `14-administracion/` | 0 | Vacia |

No hay archivos `.bak`, `.tmp`, CSVs sueltos, ni scripts Python obsoletos en `etl_pipeline/`. Todos los 8 scripts Python tienen uso verificado en el pipeline.

---

### 4. Cruce Blueprint vs Realidad

#### Rutas en App.jsx vs navigation.js

| Vista en App.jsx | Componente | Existe en navigation.js? | Funcional? |
|------------------|-----------|-------------------------|------------|
| `vision_general` | `Overview` | Si (subItem de 01) | ⚠️ Depende de tabla incorrecta |
| `demografia` | `Demographics` | Si (subItem de 05) | Si (RPC + MVs) |
| `org_posiciones` | `OrgStructure` | Si (subItem de 05) | Si (navegacion) |
| `org_integral` | `OrganigramaIntegral` | Si (subItem de 05) | 🔴 Datos mock |
| `compensaciones` | `Compensaciones` | Si (subItem de 06) | ⚠️ Depende de tabla incorrecta |
| `auditoria` | `EmployeeTable` | Si (subItem de 13) | ⚠️ Depende de tabla incorrecta |
| `roles_permisos` | Ninguno | No (hardcodeado en Sidebar) | 🔴 Sin componente |
| `conexiones_etl` | Ninguno | No (hardcodeado en Sidebar) | 🔴 Sin componente |
| `org_dotacion` | Ninguno | No | 🔴 Referenciado pero no existe |

#### Administracion hardcodeado en Sidebar
El panel de Administracion en `Sidebar.jsx` referencia `roles_permisos` y `conexiones_etl` que no estan en `navigationConfig` ni tienen componentes. App.jsx tiene soporte de breadcrumbs para estas vistas pero no hay renderizado.

---

### 5. Seguridad y Secrets

#### GRANT a anon en funciones RPC [🔴]
`m05_fuerza_laboral.py` otorga:
```sql
GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
GRANT EXECUTE ON FUNCTION business.get_demographics_dashboard(...) TO anon;
GRANT EXECUTE ON FUNCTION business.get_advanced_demographics(...) TO anon;
```
Esto permite acceso sin autenticacion a datos de empleados. Si el dashboard es publico es aceptable; si hay auth de usuarios, deberia usarse rol `authenticated`.

#### No se encontraron secrets en codigo [✅]
- No hay API keys, tokens, passwords, ni connection strings literales en el codigo frontend
- `supabaseClient.js` usa correctamente `import.meta.env.VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY`
- Scripts Python usan `python-dotenv` para cargar `DATABASE_URL`

#### .gitignore [✅]
Protege correctamente: `.env`, `.env.*` (excepto `.env.example`), `__pycache__/`, `.venv/`, `node_modules/`, `dist/`, `data/*.csv`

#### User name hardcodeado [🟡]
`Sidebar.jsx` muestra "JESUS VILLEGAS" y "Data y BI" como texto fijo. Deberia venir de contexto de autenticacion o variable configurable.

---

### 6. UI/UX y Buenas Practicas React

#### SVG sin accesibilidad [🟡]
- `App.jsx` linea ~107: SVG de placeholder sin `aria-label` ni `role="img"`
- `Overview.jsx` lineas ~68, ~78: 2 SVGs decorativos sin atributos de accesibilidad

#### Key en .map() [✅]
Todos los `.map()` usan IDs unicos (`item.id`, `subItem.id`, `tag`, `emp.employeenumber`, `name`, `opt`). No se usan indices como key.

#### Hooks bien implementados [✅]
- `useDemographicsData.js` usa correctamente `useCallback`, `useRef` para abort, y debounce
- `useDemographicsFilters` tiene cleanup adecuado en useEffect
- No hay useState declarados pero nunca leidos

#### Await dentro de return [✅]
No se encontraron llamadas `await supabase...` dentro de bloques `return`. Todas las queries estan en `useEffect` o callbacks.

#### Dark theme manual [🟢]
`Overview.jsx` y `Compensations.jsx` usan clases hardcodeadas `bg-gray-900`, `text-gray-400`, etc. en lugar de un sistema de temas. Funcional pero inconsistente con el resto de la app que usa tema claro.

---

### 7. Pipeline ETL

| Script | Estado | Dependencias | Uso verificado |
|--------|--------|-------------|----------------|
| `01_generate_synthetic_data.py` | ✅ Activo | Ninguna | pandas, numpy |
| `02_setup_raw_layer.py` | ✅ Activo | 01 | sqlalchemy, dotenv |
| `03_ingest_data.py` | ✅ Activo | 02 | pandas, sqlalchemy, dotenv |
| `04_setup_business_core.py` | ✅ Activo | 03 | sqlalchemy, dotenv |
| `m05_fuerza_laboral.py` | ✅ Activo | 04 | sqlalchemy, dotenv |
| `90_generate_data_inventory.py` | ✅ Activo | m05 | pandas, sqlalchemy, dotenv |
| `91_export_data_samples.py` | ⚠️ Comentado | m05 | psycopg2, dotenv |
| `00_full_run_pipeline.py` | ✅ Orquestador | Todos | subprocess |

Orden de ejecucion verificado: 01 → 02 → 03 → 04 → m05 → 90 (Core antes que Data Marts — correcto)

---

## Correcciones para Hallazgos Criticos

### Hallazgo #2: Table name incorrecto en App.jsx

```diff
// Antes:
  useEffect(() => {
    async function fetchEmpleados() {
      const { data, error } = await supabase
        .schema('business')
        .from('ibm_hr')
        .select('*')

// Despues:
  useEffect(() => {
    async function fetchEmpleados() {
      const { data, error } = await supabase
        .schema('business')
        .from('v_employee_full_byNapo')
        .select('*')
```

### Hallazgo #1: OrganigramaIntegral.jsx — Datos mock

```diff
// Antes:
export default function OrganigramaIntegral() {
  return (
    <div className="p-2 min-h-screen">
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-blue-100 p-3 rounded-lg text-blue-600"><Users size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Total Empleados</p>
              <p className="text-2xl font-bold text-slate-800">1,470</p>
            </div>
          </div>
          // ... mas datos hardcodeados

// Despues: conectar a Supabase via hook custom
+ import { useState, useEffect } from 'react';
+ import { supabase } from '../../lib/supabaseClient';
+
+ export default function OrganigramaIntegral() {
+   const [orgData, setOrgData] = useState(null);
+   const [kpis, setKpis] = useState(null);
+   const [loading, setLoading] = useState(true);
+
+   useEffect(() => {
+     async function fetchData() {
+       const [{ data: tree, error: treeErr }, { data: monthlyKpis, error: kpisErr }] =
+         await Promise.allSettled([
+           supabase.schema('business').from('v_org_tree_byNapo').select('*'),
+           supabase.schema('business').from('mv_monthly_kpis_byNapo').select('*').limit(1),
+         ]);
+       if (!treeErr) setOrgData(tree);
+       if (!kpisErr && monthlyKpis?.[0]) setKpis(monthlyKpis[0]);
+       setLoading(false);
+     }
+     fetchData();
+   }, []);
+
+   if (loading) return <div>Cargando organigrama...</div>;
+   if (!orgData) return <div>Sin datos del organigrama</div>;
+   // ... render dinamico basado en orgData y kpis
```

### Hallazgo #3: Fx rate fijo en ETL

```diff
# Antes:
        snapshot_df["fx_rate_to_usd"] = 3.50
        snapshot_df["monthly_salary_usd"] = (snapshot_df["monthly_salary_local"] / snapshot_df["fx_rate_to_usd"]).round(2)

# Despues: tasas diferenciadas por moneda
+ FX_RATES = {
+     "PEN": 3.70,   # Sol peruano
+     "EUR": 0.92,   # Euro
+     "CLP": 890.0,  # Peso chileno
+     "COP": 3900.0, # Peso colombiano
+     "MXN": 17.0,   # Peso mexicano
+     "USD": 1.0,    # Dolar
+ }
+ COUNTRY_CURRENCY = {"PER": "PEN", "ESP": "EUR", "CHL": "CLP", "COL": "COP", "MEX": "MXN", "USA": "USD"}
+
+ snapshot_df["currency_iso3"] = snapshot_df["country_iso3"].map(COUNTRY_CURRENCY)
+ snapshot_df["fx_rate_to_usd"] = snapshot_df["currency_iso3"].map(FX_RATES)
+ snapshot_df["monthly_salary_usd"] = (snapshot_df["monthly_salary_local"] * snapshot_df["fx_rate_to_usd"]).round(2)
```

### Hallazgo #4: Ruta org_dotacion fantasma

```diff
// Opcion A: Agregar a navigation.js como subItem de 05-fuerza-laboral
// En navigation.js, dentro de subItems de 05-fuerza-laboral:
+       {
+         id: 'org_dotacion',
+         title: 'Organigrama de Dotacion',
+         description: 'Enfoque en el conteo de personas (Headcount), vacantes y capacidad operativa por area.',
+         icon: 'Users',
+         tags: ['DESC']
+       },

// Opcion B: Eliminar el boton de OrgStructure.jsx si no se implementara
// En OrgStructure.jsx:
-           <button
-             onClick={() => setVistaActual('org_dotacion')}
-             className="flex items-center text-emerald-600 font-medium hover:text-emerald-700 transition-colors mt-auto"
-           >
-             Explorar <ArrowRight size={18} className="ml-2" />
-           </button>
```

### Hallazgo #6: Eliminar imports de React innecesarios

```diff
// Antes (en 5 archivos):
- import React from 'react';
  import ReactECharts from 'echarts-for-react';

// Despues:
  import ReactECharts from 'echarts-for-react';
```

### Hallazgo #7: Unificar imports de Lucide en Sidebar

```diff
// Antes:
- import React, { useState } from 'react';
- import * as Icons from 'lucide-react';
- import { Grip, UserCircle, ChevronDown, ChevronRight } from 'lucide-react';
  import { navigationConfig } from '../../config/navigation';

// Despues:
+ import { useState } from 'react';
+ import * as Icons from 'lucide-react';
  import { navigationConfig } from '../../config/navigation';

// Y reemplazar usos directos:
- <Grip size={22} />
+ <Icons.Grip size={22} />
- <UserCircle size={24} />
+ <Icons.UserCircle size={24} />
- <ChevronDown size={16} />
+ <Icons.ChevronDown size={16} />
- <ChevronRight size={16} />
+ <Icons.ChevronRight size={16} />
```

---

## Resumen de Estado por Pilar

| Pilar | Hallazgos Criticos | Advertencias | Sugerencias | Estado |
|-------|-------------------|-------------|-------------|--------|
| Hardcoding | 3 (#1, #2, #3) | 0 | 1 (#23) | 🔴 Critico |
| Zombie Code | 1 (#4) | 5 (#6-#11) | 0 | 🟡 Medio |
| Seguridad | 1 (#5) | 1 (#13) | 1 (#17) | 🟡 Medio |
| UI/UX | 0 | 2 (#12, #14) | 2 (#15, #22) | 🟡 Medio |
| Consistencia | 1 (#2) | 1 (#14) | 0 | 🟡 Medio |
| Buenas practicas | 0 | 0 | 3 (#19-#21) | 🟢 Aceptable |

---

*Documento generado automaticamente mediante analisis estatico del repositorio. Las secciones marcadas como `[⚠️ No verificable]` requieren verificacion en runtime o acceso a la base de datos Supabase.*
