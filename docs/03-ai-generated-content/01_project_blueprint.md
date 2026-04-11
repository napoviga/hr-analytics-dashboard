# Project Blueprint — HR Analytics Dashboard

> **Generado automáticamente:** 2026-04-11T06:30:00Z
> **Ejecutado por:** Qwen Code Terminal
> **Versión del Pipeline:** Scripts 01-04 + m05 + 90-91
> **Propósito:** Contexto maestro para asistencia de AI en este proyecto.

---

## 1. Estructura de Directorios

```
📁 hr-analytics-dashboard/
├── .env
├── .gitignore
├── README.md
├── docs/
│   ├── PIPELINE_ORDER.md
│   ├── 01-product-specs/
│   │   ├── 01_navigation_sitemap.md
│   │   ├── 02_view_logic_specs.md
│   │   └── 03_design_system.md
│   ├── 02-data-governance/
│   │   ├── 02_supabase_metadata_inventory.md
│   │   └── 03_data_samples.md
│   ├── 03-ai-context/
│   ├── ai-generated-content/
│   └── prompts/
│       ├── 00. Blueprint & Context.md
│       ├── 01. Data Dictionary.md
│       └── 02. Audit & Linting.md
├── data/
│   ├── ibm_hr.csv
│   ├── ibm_hr_change_reasons_byNapo.csv
│   └── ibm_hr_monthly_snapshot_byNapo.csv
├── etl_pipeline/
│   ├── 00_full_run_pipeline.py
│   ├── 01_generate_synthetic_data.py
│   ├── 02_setup_raw_layer.py
│   ├── 03_ingest_data.py
│   ├── 04_setup_business_core.py
│   ├── m05_fuerza_laboral.py
│   ├── 90_generate_data_inventory.py
│   └── 91_export_data_samples.py
└── client/
    ├── .env
    ├── .gitignore
    ├── eslint.config.js
    ├── index.html
    ├── package.json
    ├── prisma.config.ts
    ├── vite.config.js
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── config/
        │   └── navigation.js
        ├── lib/
        │   └── supabaseClient.js
        └── modules/
            ├── 00-layout/
            │   ├── Overview.jsx
            │   ├── SectionLanding.jsx
            │   └── Sidebar.jsx
            ├── 01-vision-ejecutiva/          🔴 Vacío
            ├── 02-reclutamiento/             🔴 Vacío
            ├── 03-onboarding/                🔴 Vacío
            ├── 04-ciclo-vida/                🔴 Vacío
            ├── 05-fuerza-laboral/
            │   ├── Demographics.jsx
            │   ├── EmployeeTable.jsx
            │   ├── OrgStructure.jsx
            │   ├── OrganigramaIntegral.jsx
            │   └── hooks/useDemographicsData.js
            ├── 06-nomina-costos/
            │   └── Compensations.jsx
            ├── 07-tiempo-asistencia/         🔴 Vacío
            ├── 08-gestion-desempeno/         🔴 Vacío
            ├── 09-talento-desarrollo/        🔴 Vacío
            ├── 10-engagement-sentimiento/    🔴 Vacío
            ├── 11-compliance/                🔴 Vacío
            ├── 12-retencion/                 🔴 Vacío
            ├── 13-calidad-datos/             🔴 Vacío
            └── 14-administracion/            🔴 Vacío
```

### Validación Cruzada: Navigation.js vs Carpetas

| Módulo en navigation.js | Carpeta existe | Componentes | Estado |
|------------------------|---------------|-------------|--------|
| 01-vision-ejecutiva | ✅ | ❌ Ninguno | 🔴 Vacío |
| 02-reclutamiento | ✅ | ❌ Ninguno | 🔴 Vacío |
| 03-onboarding | ✅ | ❌ Ninguno | 🔴 Vacío |
| 04-ciclo-vida | ✅ | ❌ Ninguno | 🔴 Vacío |
| 05-fuerza-laboral | ✅ | ✅ 4 componentes + 1 hook | 🟢 Activo |
| 06-nomina-costos | ✅ | ✅ 1 componente | 🟡 Parcial |
| 07-tiempo-asistencia | ✅ | ❌ Ninguno | 🔴 Vacío |
| 08-gestion-desempeno | ✅ | ❌ Ninguno | 🔴 Vacío |
| 09-talento-desarrollo | ✅ | ❌ Ninguno | 🔴 Vacío |
| 10-engagement-sentimiento | ✅ | ❌ Ninguno | 🔴 Vacío |
| 11-compliance | ✅ | ❌ Ninguno | 🔴 Vacío |
| 12-retencion | ✅ | ❌ Ninguno | 🔴 Vacío |
| 13-calidad-datos | ✅ | ❌ Ninguno | 🔴 Vacío |
| [Admin] roles_permisos | ✅ (14-administracion) | ❌ Ninguno | 🔴 Vacío |
| [Admin] conexiones_etl | ✅ (14-administracion) | ❌ Ninguno | 🔴 Vacío |

**[⚠️ Discrepancia detectada]:** 12 de 14 módulos están vacíos. Solo `05-fuerza-laboral` está completamente implementado y `06-nomina-costos` tiene 1 componente.

---

## 2. Dependencias y Entorno

### Frontend (Node.js)

**Dependencies:**

| Paquete | Versión |
|---------|---------|
| `@supabase/supabase-js` | `^2.101.1` |
| `echarts` | `^6.0.0` |
| `echarts-for-react` | `^3.0.6` |
| `lucide-react` | `^1.7.0` |
| `react` | `^19.2.4` |
| `react-dom` | `^19.2.4` |

**DevDependencies:**

| Paquete | Versión |
|---------|---------|
| `@eslint/js` | `^9.39.4` |
| `@tailwindcss/vite` | `^4.2.2` |
| `@types/react` | `^19.2.14` |
| `@types/react-dom` | `^19.2.3` |
| `@vitejs/plugin-react` | `^6.0.1` |
| `autoprefixer` | `^10.4.27` |
| `dotenv` | `^17.4.1` |
| `eslint` | `^9.39.4` |
| `eslint-plugin-react-hooks` | `^7.0.1` |
| `eslint-plugin-react-refresh` | `^0.5.2` |
| `globals` | `^17.4.0` |
| `postcss` | `^8.5.8` |
| `prisma` | `^7.6.0` |
| `tailwindcss` | `^4.2.2` |
| `vite` | `^8.0.1` |

### Backend/ETL (Python)

| Paquete | Usado en |
|---------|----------|
| `pandas` | 01, 03, 90 |
| `numpy` | 01 |
| `sqlalchemy` | 02, 03, 04, m05, 90 |
| `python-dotenv` | 02, 03, 04, m05, 90, 91 |
| `psycopg2` | 91 |

**Dependencias fantasma:** No detectadas — todos los paquetes importados se usan activamente.

---

## 3. Arquitectura de Datos

### Capa RAW (Bronce)

| Tabla | Script Origen | Descripción |
|-------|--------------|-------------|
| `raw."ibm_hr_monthly_snapshot_byNapo"` | `02_setup_raw_layer.py` | Landing de snapshots mensuales (37 columnas TEXT) |
| `raw."ibm_hr_change_reasons_byNapo"` | `02_setup_raw_layer.py` | Catálogo de códigos de cambio (7 columnas TEXT) |

### Capa BUSINESS (Oro Transversal)

| Objeto | Tipo | Script Origen | Descripción |
|--------|------|--------------|-------------|
| `business.v_employee_full_bynapo` | Vista | `04_setup_business_core.py` | Vista maestra tipada con tenure_months, is_active_at_snapshot |
| `business.mv_ui_global_filters` | MV | `04_setup_business_core.py` | JSON con valores de 6 filtros universales |

### Capa DATA MARTS (Oro Específica)

| Objeto | Tipo | Script Origen | Descripción |
|--------|------|--------------|-------------|
| `business.v_org_tree_bynapo` | Vista Recursiva | `m05_fuerza_laboral.py` | Organigrama jerárquico con formato ECharts (depth ≤ 10) |
| `business.mv_monthly_kpis_bynapo` | MV | `m05_fuerza_laboral.py` | KPIs mensuales por país (headcount, salario, tenure) |
| `business.mv_demographics_agg` | MV | `m05_fuerza_laboral.py` | Agregados demográficos para tarjetas KPI |
| `business.mv_diversity_pyramid` | MV | `m05_fuerza_laboral.py` | Conteos por género y nivel (pirámide) |
| `business.mv_bajas_heatmap` | MV | `m05_fuerza_laboral.py` | Bajas por mes/departamento (heatmap) |
| `business.mv_country_dist` | MV | `m05_fuerza_laboral.py` | Distribución por país |
| `business.mv_experience_bubbles` | MV | `m05_fuerza_laboral.py` | Burbujas de experiencia con tenure buckets |

### Funciones RPC

| Función | Parámetros | Retorno | Consumo Frontend |
|---------|-----------|---------|-----------------|
| `get_demographics_dashboard` | date, country, dept, jl1, jl2, work_center | JSON (3 cards + sparklines) | Módulo 05 Demografía |
| `get_advanced_demographics` | date, country, dept, jl1, jl2, work_center | JSON (4 gráficos) | Módulo 05 Demografía |

---

## 4. Pipeline ETL

### Secuencia de Ejecución

```
00_full_run_pipeline.py (orquestador)
  └─ 01_generate_synthetic_data.py    → CSV files
  └─ 02_setup_raw_layer.py            → raw tables (TEXT)
  └─ 03_ingest_data.py                → CSV → raw tables
  └─ 04_setup_business_core.py        → business views
  └─ m05_fuerza_laboral.py            → data marts + RPCs
  └─ 90_generate_data_inventory.py    → metadata inventory MD
  └─ 91_export_data_samples.py        → data samples MD (opcional)
```

### Detalle de Scripts

| # | Script | Genera | Depende de |
|---|--------|--------|-----------|
| 01 | `01_generate_synthetic_data.py` | `data/*.csv` | Nada |
| 02 | `02_setup_raw_layer.py` | Tablas `raw.*` | 01 |
| 03 | `03_ingest_data.py` | Datos en `raw.*` | 01, 02 |
| 04 | `04_setup_business_core.py` | `business.v_employee_full_bynapo`, `mv_ui_global_filters` | 03 |
| m05 | `m05_fuerza_laboral.py` | 6 MVs + 1 vista + 2 RPCs | 04 |
| 90 | `90_generate_data_inventory.py` | `02_supabase_metadata_inventory.md` | m05 |
| 91 | `91_export_data_samples.py` | `03_data_samples.md` | m05 |

---

## 5. Estado del Frontend Modular

### Routing

- **Sin react-router**: usa estado `vistaActual` (string) controlado por Sidebar
- **Data fetch inicial**: consulta `business.ibm_hr` via Supabase client
- **Vistas implementadas:**
  - `vision_general` → `<Overview />`
  - `demografia` → `<Demographics />`
  - `org_posiciones` → `<OrgStructure />`
  - `org_integral` → `<OrganigramaIntegral />`
  - `compensaciones` → `<Compensaciones />`
  - `auditoria` → `<EmployeeTable />`
  - Resto → "Desarrollo en Progreso" placeholder

### Módulos Detectados

| Módulo | Archivos | Estado |
|--------|---------|--------|
| `00-layout` | 3 archivos | 🟢 Layout base |
| `05-fuerza-laboral` | 4 componentes + 1 hook | 🟢 Activo |
| `06-nomina-costos` | 1 componente | 🟡 Parcial |
| `01-vision-ejecutiva` | 0 | 🔴 Vacío |
| `02-reclutamiento` | 0 | 🔴 Vacío |
| `03-onboarding` | 0 | 🔴 Vacío |
| `04-ciclo-vida` | 0 | 🔴 Vacío |
| `07-tiempo-asistencia` | 0 | 🔴 Vacío |
| `08-gestion-desempeno` | 0 | 🔴 Vacío |
| `09-talento-desarrollo` | 0 | 🔴 Vacío |
| `10-engagement-sentimiento` | 0 | 🔴 Vacío |
| `11-compliance` | 0 | 🔴 Vacío |
| `12-retencion` | 0 | 🔴 Vacío |
| `13-calidad-datos` | 0 | 🔴 Vacío |
| `14-administracion` | 0 | 🔴 Vacío |

---

## 6. Variables de Entorno

### `.env` (root)

| Variable | Valor |
|----------|-------|
| `VITE_SUPABASE_URL` | `***` |
| `VITE_SUPABASE_ANON_KEY` | `***` |
| `SUPABASE_SERVICE_KEY` | `***` |
| `DATABASE_URL` | `***` |

### `.env` (client)

| Variable | Valor |
|----------|-------|
| `VITE_SUPABASE_URL` | `***` |
| `VITE_SUPABASE_ANON_KEY` | `***` |

**[✅ Sin variables huérfanas]** Todas las variables declaradas se referencian en código.

---

## 7. Score de Madurez del Proyecto

| Métrica | Score | Detalle |
|---------|-------|---------|
| Scripts ETL funcionales | 8/8 | Todos los scripts 01-04, m05, 90, 91 operativos |
| Módulos frontend | 2/14 | Solo fuerza-laboral completo, nomina-costos parcial |
| Vistas/MVs en BD | 9 | 2 vistas + 6 MVs + 1 tabla inventario |
| Funciones RPC | 2 | get_demographics_dashboard, get_advanced_demographics |
| Documentación generada | 5 archivos .md | Blueprint, Pipeline Order, Metadata Inventory, Data Samples, este doc |
| .gitignore | ✅ OK | Todo protegido: .env, __pycache__, venv, node_modules, dist, logs |
| Dependencias limpias | ✅ OK | Sin dependencias fantasma en Python ni Node.js |
| Variables de entorno | ✅ OK | Sin claves faltantes ni hardcodeadas |

---

## 8. Resumen de Archivos del Proyecto

| Extensión | Cantidad |
|-----------|----------|
| `.jsx` | 10 |
| `.md` | 10 |
| `.py` | 8 |
| `.js` | 5 |
| `.csv` | 3 |
| `.json` | 3 |
| `.gitignore` | 2 |
| `.svg` | 2 |
| `.env` | 2 |
| `.ts` | 1 |
| `.html` | 1 |
| `.css` | 1 |

**Total: 48 archivos** (excluyendo node_modules, .git, dist, __pycache__)

---

## 9. Tech Stack

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Frontend UI | React + Vite | 19.2.4 + 8.0.1 |
| Estilos | TailwindCSS | 4.2.2 |
| Gráficos | ECharts + echarts-for-react | 6.0.0 + 3.0.6 |
| Iconos | Lucide React | 1.7.0 |
| Backend DB | Supabase (PostgreSQL) | Latest |
| ETL | SQLAlchemy + pandas + psycopg2 | Latest |
| Build/Lint | ESLint + PostCSS | 9.39.4 + 8.5.8 |

---

> **Checksum MD5:** [auto-generated]
