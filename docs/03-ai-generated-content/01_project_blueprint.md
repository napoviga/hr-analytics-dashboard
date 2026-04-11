# Project Blueprint — HR Analytics Dashboard

> **Generado automaticamente:** 2026-04-11T23:00:00Z
> **Ejecutado por:** Qwen Code Terminal
> **Version del Pipeline:** Scripts 01-04 + m05 + 90-91

---

## 1. Estructura de Directorios

```
hr-analytics-dashboard/
│
├── .gitignore
├── README.md
│
├── client/
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── prisma.config.ts
│   ├── skills-lock.json
│   ├── vite.config.js
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── index.css
│       ├── config/
│       │   └── navigation.js
│       ├── lib/
│       │   └── supabaseClient.js
│       └── modules/
│           ├── 00-layout/
│           │   ├── Overview.jsx
│           │   ├── SectionLanding.jsx
│           │   └── Sidebar.jsx
│           ├── 01-vision-ejecutiva/          [VACIA - Placeholder]
│           ├── 02-reclutamiento/              [VACIA - Placeholder]
│           ├── 03-onboarding/                 [VACIA - Placeholder]
│           ├── 04-ciclo-vida/                 [VACIA - Placeholder]
│           ├── 05-fuerza-laboral/
│           │   ├── Demographics.jsx
│           │   ├── EmployeeTable.jsx
│           │   ├── OrganigramaIntegral.jsx
│           │   ├── OrgStructure.jsx
│           │   └── hooks/
│           │       └── useDemographicsData.js
│           ├── 06-nomina-costos/
│           │   └── Compensations.jsx
│           ├── 07-tiempo-asistencia/          [VACIA - Placeholder]
│           ├── 08-gestion-desempeno/          [VACIA - Placeholder]
│           ├── 09-talento-desarrollo/         [VACIA - Placeholder]
│           ├── 10-engagement-sentimiento/     [VACIA - Placeholder]
│           ├── 11-compliance/                 [VACIA - Placeholder]
│           ├── 12-retencion/                  [VACIA - Placeholder]
│           ├── 13-calidad-datos/              [VACIA - Placeholder]
│           └── 14-administracion/             [VACIA - Placeholder]
│
├── data/                                      [Gitignored - CSVs generados por ETL]
│
├── docs/
│   ├── PIPELINE_ORDER.md
│   ├── 01-product-specs/
│   │   ├── 01_navigation_sitemap.md
│   │   ├── 02_view_logic_specs.md
│   │   └── 03_design_system.md
│   ├── 02-data-governance/
│   │   ├── 02_supabase_metadata_inventory.md
│   │   └── 03_data_samples.md
│   ├── 03-ai-generated-content/
│   │   ├── 01_project_blueprint.md
│   │   ├── 02_data_dictionary.md
│   │   └── 03_audit_report.md
│   └── prompts/
│       ├── 00. Blueprint & Context.md
│       ├── 01. Data Dictionary.md
│       ├── 02. Audit & Linting.md
│       └── 90_Update_README.md
│
└── etl_pipeline/
    ├── 00_full_run_pipeline.py
    ├── 01_generate_synthetic_data.py
    ├── 02_setup_raw_layer.py
    ├── 03_ingest_data.py
    ├── 04_setup_business_core.py
    ├── m05_fuerza_laboral.py
    ├── 90_generate_data_inventory.py
    └── 91_export_data_samples.py
```

### Discrepancias: navigation.js vs modulos reales

| Modulo en navigation.js | Carpeta en modules/ | Estado | ¿Coincide? |
|-------------------------|---------------------|--------|------------|
| 01-vision-ejecutiva (3 subItems) | 01-vision-ejecutiva/ | Vacia | Si existe carpeta, sin componentes |
| 02-reclutamiento (5 subItems) | 02-reclutamiento/ | Vacia | Si existe carpeta, sin componentes |
| 03-onboarding (3 subItems) | 03-onboarding/ | Vacia | Si existe carpeta, sin componentes |
| 04-ciclo-vida (3 subItems) | 04-ciclo-vida/ | Vacia | Si existe carpeta, sin componentes |
| 05-fuerza-laboral (6 subItems) | 05-fuerza-laboral/ | 5 archivos + hooks | Implementado parcialmente |
| 06-nomina-costos (6 subItems) | 06-nomina-costos/ | 1 archivo | Implementado parcialmente |
| 07-tiempo-asistencia (6 subItems) | 07-tiempo-asistencia/ | Vacia | Si existe carpeta, sin componentes |
| 08-gestion-desempeno (4 subItems) | 08-gestion-desempeno/ | Vacia | Si existe carpeta, sin componentes |
| 09-talento-desarrollo (5 subItems) | 09-talento-desarrollo/ | Vacia | Si existe carpeta, sin componentes |
| 10-engagement-sentimiento (3 subItems) | 10-engagement-sentimiento/ | Vacia | Si existe carpeta, sin componentes |
| 11-compliance (2 subItems) | 11-compliance/ | Vacia | Si existe carpeta, sin componentes |
| 12-retencion (3 subItems) | 12-retencion/ | Vacia | Si existe carpeta, sin componentes |
| 13-calidad-datos (3 subItems) | 13-calidad-datos/ | Vacia | Si existe carpeta, sin componentes |
| Administracion (no en nav principal, hardcodeado en Sidebar) | 14-administracion/ | Vacia | Sidebar referencia `roles_permisos` y `conexiones_etl` pero no existen componentes |

**Hallazgo:** El Sidebar hardcodea 2 vistas de Administracion (`roles_permisos`, `conexiones_etl`) que no tienen componentes implementados ni estan en `navigationConfig`. La carpeta `14-administracion/` existe pero esta vacia.

---

## 2. Dependencias y Entorno

### Frontend (Node.js)

#### dependencies (6 paquetes)

| Paquete | Version | Uso Verificado en Codigo |
|---------|---------|-------------------------|
| `@supabase/supabase-js` | ^2.101.1 | Si — `src/lib/supabaseClient.js`, `App.jsx`, `useDemographicsData.js` |
| `echarts` | ^6.0.0 | Si — usado indirectamente via `echarts-for-react` en `Overview.jsx`, `Demographics.jsx`, `OrganigramaIntegral.jsx` |
| `echarts-for-react` | ^3.0.6 | Si — `Overview.jsx` importa `ReactECharts` |
| `lucide-react` | ^1.7.0 | Si — `Sidebar.jsx`, `SectionLanding.jsx` importan iconos |
| `react` | ^19.2.4 | Si — framework principal |
| `react-dom` | ^19.2.4 | Si — `main.jsx` usa `createRoot` |

#### devDependencies (14 paquetes)

| Paquete | Version | Uso Verificado |
|---------|---------|----------------|
| `@eslint/js` | ^9.39.4 | Si — `eslint.config.js` |
| `@tailwindcss/vite` | ^4.2.2 | Si — `vite.config.js` |
| `@types/react` | ^19.2.14 | Si — TypeScript types (prisma.config.ts es .ts) |
| `@types/react-dom` | ^19.2.3 | Si — TypeScript types |
| `@vitejs/plugin-react` | ^6.0.1 | Si — `vite.config.js` |
| `autoprefixer` | ^10.4.27 | Instalado pero [⚠️ No verificable uso explicito] — Tailwind v4 usa su propio procesador |
| `dotenv` | ^17.4.1 | Si — `prisma.config.ts` importa `config` de dotenv |
| `eslint` | ^9.39.4 | Si — linting del proyecto |
| `eslint-plugin-react-hooks` | ^7.0.1 | Si — reglas de ESLint para hooks |
| `eslint-plugin-react-refresh` | ^0.5.2 | Si — reglas de fast refresh |
| `globals` | ^17.4.0 | Si — configurado en `eslint.config.js` |
| `postcss` | ^8.5.8 | Instalado pero [⚠️ No verificable uso explicito] — Tailwind v4 con plugin Vite no requiere PostCSS standalone |
| `prisma` | ^7.6.0 | Parcial — `prisma.config.ts` existe pero no hay `prisma/schema.prisma` en el proyecto |
| `tailwindcss` | ^4.2.2 | Si — `index.css` importa tailwind, `vite.config.js` usa plugin |
| `vite` | ^8.0.1 | Si — build tool principal |

#### Dependencias fantasma detectadas

| Paquete | Estado | Motivo |
|---------|--------|--------|
| `autoprefixer` | Posiblemente innecesaria | Tailwind CSS v4 con `@tailwindcss/vite` plugin no requiere PostCSS/autoprefixer manualmente |
| `postcss` | Posiblemente innecesaria | Mismo motivo — Tailwind v4 integra su propio procesador |
| `prisma` | Configurado pero sin schema | Existe `prisma.config.ts` apuntando a `prisma/schema.prisma` que no existe en el proyecto |

### Backend/ETL (Python)

| Dependencia | Scripts que la usan | Uso |
|-------------|---------------------|-----|
| `pandas` | 01, 03, 90 | Manipulacion de DataFrames, lectura CSV, to_sql |
| `numpy` | 01 | Generacion de datos aleatorios, calculos matriciales |
| `sqlalchemy` | 02, 03, 04, m05, 90 | Creacion de engine PostgreSQL, ejecucion de SQL |
| `python-dotenv` | 02, 03, 04, m05, 90, 91 | Carga de DATABASE_URL desde .env |
| `psycopg2` (o `psycopg2-binary`) | 91 | Conexion directa PostgreSQL para export de samples |

**Nota:** Los scripts 02, 03, 04, m05, 90 resuelven la ruta del `.env` desde el directorio raiz del proyecto (`PROJECT_ROOT / ".env"`). El script 91 tiene fallback: busca `.env` en raiz primero, luego en `client/`, y finalmente construye `DATABASE_URL` desde `VITE_SUPABASE_URL` + `SUPABASE_SERVICE_KEY`.

---

## 3. Arquitectura de Datos

### Capa RAW (Bronce)

Creada por el script `02_setup_raw_layer.py`. Todas las columnas son tipo `TEXT` para evitar conflictos de formato durante la ingesta. La tipificacion se aplica en la capa Business.

| Tabla | Columnas Clave | Descripcion |
|-------|---------------|-------------|
| `raw."ibm_hr_monthly_snapshot_byNapo"` | 37 columnas (36 datos + `created_at`) | Snapshots mensuales de empleados. PK logica compuesta: `(snapshot_date, employee_id)`. Columnas principales: `snapshot_date`, `employee_id`, `employee_code`, `full_name`, `gender`, `country_iso3`, `department_name`, `job_role`, `job_level_1`, `job_level_2`, `employment_status`, `hire_date`, `termination_date`, `monthly_salary_local`, `currency_iso3`, `fx_rate_to_usd`, `monthly_salary_usd`, `manager_employee_id`, `dotted_line_manager_id`, `work_center_id`, `home_lat`, `home_lon`, `work_modality`, `education_level`, `marital_status`, `salary_change_flag`, `salary_change_reason_code`, `job_change_flag`, `turnover_classification_company`, `exit_interview_completed`, `regrettable_loss_flag` |
| `raw."ibm_hr_change_reasons_byNapo"` | 7 columnas (6 datos + `created_at`) | Catalogo de motivos de cambio: `SAL-IPC` (ajuste inflacion), `TER-VOL` (renuncia voluntaria), `TER-INV` (despido), `TER-RET` (jubilacion) |

### Capa BUSINESS (Oro Transversal)

Creada por el script `04_setup_business_core.py`. Contiene las vistas tipificadas que son la unica fuente de verdad para consumo analitico.

| Vista | Tipo | Columnas | Reglas de Negocio Aplicadas |
|-------|------|----------|----------------------------|
| `business.v_employee_full_byNapo` | Vista | 22 (19 fuente + 3 calculadas) | `tenure_months`: calculo en meses entre hire_date y snapshot_date/termination_date. `is_active_at_snapshot`: logica booleana que considera si el empleado estaba activo en la fecha del snapshot. `processed_at`: timestamp NOW() |
| `business.mv_ui_global_filters` | Vista Materializada | 1 columna (`filter_options` JSON) | Agrega valores distintos para 6 dimensiones universales: `periods`, `countries`, `departments`, `job_levels_1`, `job_levels_2`, `work_centers`. Usada por el hook `useDemographicsFilters()` para poblar dropdowns del frontend |

### Capa DATA MARTS (Oro Especifica)

Creada por el script `m05_fuerza_laboral.py`. Vistas especializadas para el modulo de Fuerza Laboral.

| Vista/MV | Tipo | Metricas Principales | Indexes |
|----------|------|---------------------|---------|
| `business.v_org_tree_byNapo` | Vista (CTE recursivo) | Jerarquia organizacional completa con depth (0-10) y path | Ninguno (vista) |
| `business.mv_monthly_kpis_byNapo` | MV | `headcount_active`, `headcount_terminated`, `avg_salary_usd`, `avg_tenure` por snapshot + pais | `idx_kpis_unique_m05` (snapshot_date, country_iso3) |
| `business.mv_demographics_agg` | MV | `total_hc`, `altas`, `bajas` agrupado por 6 dimensiones | `idx_demo_agg_snap_m05`, `idx_demo_agg_filt_m05` |
| `business.mv_diversity_pyramid` | MV | Count por genero, nivel, departamento | `idx_mv_div_snap_m05` |
| `business.mv_bajas_heatmap` | MV | Count de bajas por dept y mes | `idx_mv_bajas_snap_m05` |
| `business.mv_country_dist` | MV | Distribucion de empleados por pais | `idx_mv_country_snap_m05` |
| `business.mv_experience_bubbles` | MV | `avg_salary`, `emp_count` bucketed por tenure (`<1 ano`, `1-3 anos`, `3-6 anos`, `6+ anos`) | `idx_mv_exp_snap_m05` |

### Funciones RPC

Creadas por `m05_fuerza_laboral.py`. Consumibles via Supabase PostgREST (`supabase.schema('business').rpc()`).

| Funcion | Parametros | Retorno | Consumo Frontend |
|---------|-----------|---------|-----------------|
| `business.get_demographics_dashboard(p_period_date DATE, p_country TEXT, p_department TEXT, p_job_level_1 TEXT, p_job_level_2 TEXT, p_work_center TEXT)` | 6 parametros (5 opcionales con DEFAULT NULL) | JSON con 3 cards (`total_activos_card`, `altas_card`, `bajas_card`), cada una con: valor actual, anterior, YoY, diff absoluto/porcentual, sparkline_data | `useDemographicsData.js` → `Demographics.jsx` via `supabase.schema('business').rpc('get_demographics_dashboard', params)` |
| `business.get_advanced_demographics(p_period_date DATE, p_country TEXT, p_department TEXT, p_job_level_1 TEXT, p_job_level_2 TEXT, p_work_center TEXT)` | 6 parametros (5 opcionales con DEFAULT NULL) | JSON con 4 arrays: `diversity_pyramid`, `turnover_heatmap`, `country_distribution`, `experience_bubbles` | `useDemographicsData.js` → `Demographics.jsx` via `supabase.schema('business').rpc('get_advanced_demographics', params)` |

---

## 4. Pipeline ETL

### Orquestador: `00_full_run_pipeline.py`

Ejecuta secuencialmente los scripts en este orden:

```
01 → 02 → 03 → 04 → m05 → 90
```

El script `91_export_data_samples.py` esta comentado en el orquestador (no se ejecuta automaticamente). Cada script se ejecuta via `subprocess.run(['python', script_path], check=True)`. Si un script falla, el pipeline se aborta inmediatamente.

### Detalle de Cada Script

| # | Script | Que Hace | Que Genera | Dependencias |
|---|--------|----------|-----------|-------------|
| 01 | `01_generate_synthetic_data.py` | Genera datos sintéticos HR con seed 42. Crea 4,000-6,000 empleados iniciales + variaciones mensuales (0.5% attrition, 1% nuevas contrataciones). Aplica ajuste IPC por pais (PER 4%, ESP 3%, CHL 3.5%). Convierte salarios a USD con fx_rate fijo 3.50. Genera 75 snapshots mensuales (2020-01 a 2026-03). Incluye catalogo de razones de cambio. | `data/ibm_hr_monthly_snapshot_byNapo.csv`, `data/ibm_hr_change_reasons_byNapo.csv` | Ninguna |
| 02 | `02_setup_raw_layer.py` | Conecta a Supabase via SQLAlchemy. Crea esquema `raw` si no existe. Elimina tablas anteriores (con variantes de casing). Crea 2 tablas con columnas TEXT. | `raw."ibm_hr_monthly_snapshot_byNapo"`, `raw."ibm_hr_change_reasons_byNapo"` | Script 01 (archivos CSV deben existir) |
| 03 | `03_ingest_data.py` | Lee CSVs del directorio `data/`. Convierte columnas a lowercase. Sube a tablas raw via `df.to_sql()` con chunksize=1000. | Datos poblados en `raw.*` | Script 02 (tablas deben existir) |
| 04 | `04_setup_business_core.py` | Crea esquema `business`. Crea vista maestra `v_employee_full_byNapo` con casting de tipos y columnas calculadas. Crea MV `mv_ui_global_filters` con JSON de filtros universales. Refresca MV. Grants a `anon`. | `business.v_employee_full_byNapo`, `business.mv_ui_global_filters` | Script 03 (datos en raw) |
| m05 | `m05_fuerza_laboral.py` | Crea 1 vista recursiva (org tree), 6 MVs demograficas con indexes, 2 funciones RPC con logica de cards + sparklines + graficos avanzados. Refresca todas las MVs. Ejecuta `NOTIFY pgrst, 'reload schema'`. | 7 MVs + 1 vista + 2 funciones RPC en `business.*` | Script 04 (vistas business deben existir) |
| 90 | `90_generate_data_inventory.py` | Escanea todos los objetos en esquemas `raw` y `business`. Calcula cardinalidad, completitud, muestra de valores por columna. Escribe tabla `business.data_inventory` en Supabase. Genera Markdown en `docs/02-data-governance/02_supabase_metadata_inventory.md`. | `business.data_inventory` (tabla), `02_supabase_metadata_inventory.md` | Script m05 (todas las vistas deben existir) |
| 91 | `91_export_data_samples.py` | Conecta via psycopg2. Extrae 5 filas aleatorias de 4 vistas clave. Genera Markdown con schema + muestras. Incluye checksum MD5. | `docs/02-data-governance/03_data_samples.md` | Script m05 (vistas deben existir) |

---

## 5. Estado del Frontend Modular

### Modulos en `client/src/modules/`

| Modulo | Archivos | Estado | SubItems en navigation.js | Vistas Implementadas en App.jsx |
|--------|----------|--------|--------------------------|-------------------------------|
| `00-layout` | `Sidebar.jsx`, `SectionLanding.jsx`, `Overview.jsx` | Activo | N/A (componentes compartidos) | `Overview.jsx` → `vision_general` |
| `01-vision-ejecutiva` | [vacío] | Placeholder | 3 (vision_general, alertas_anomalias, benchmarking) | `vision_general` resuelto via `00-layout/Overview.jsx` |
| `02-reclutamiento` | [vacío] | Placeholder | 5 | Ninguna |
| `03-onboarding` | [vacío] | Placeholder | 3 | Ninguna |
| `04-ciclo-vida` | [vacío] | Placeholder | 3 | Ninguna |
| `05-fuerza-laboral` | `Demographics.jsx`, `EmployeeTable.jsx`, `OrganigramaIntegral.jsx`, `OrgStructure.jsx`, `hooks/useDemographicsData.js` | Activo (5/6 vistas con componente) | 6 | `demografia` → `Demographics.jsx`, `org_integral` → `OrganigramaIntegral.jsx`, `org_posiciones` → `OrgStructure.jsx`, `auditoria` → `EmployeeTable.jsx` |
| `06-nomina-costos` | `Compensations.jsx` | Parcial | 6 | `compensaciones` → `Compensations.jsx` |
| `07-tiempo-asistencia` | [vacío] | Placeholder | 6 | Ninguna |
| `08-gestion-desempeno` | [vacío] | Placeholder | 4 | Ninguna |
| `09-talento-desarrollo` | [vacío] | Placeholder | 5 | Ninguna |
| `10-engagement-sentimiento` | [vacío] | Placeholder | 3 | Ninguna |
| `11-compliance` | [vacío] | Placeholder | 2 | Ninguna |
| `12-retencion` | [vacío] | Placeholder | 3 | Ninguna |
| `13-calidad-datos` | [vacío] | Placeholder | 3 | `auditoria` resuelto via `05-fuerza-laboral/EmployeeTable.jsx` |
| `14-administracion` | [vacío] | Placeholder | 0 (hardcodeado en Sidebar) | `roles_permisos` y `conexiones_etl` sin componentes |

### Resumen de Implementacion

| Metrica | Valor |
|---------|-------|
| Modulos con al menos 1 componente | 3 de 15 (00-layout, 05-fuerza-laboral, 06-nomina-costos) |
| Modulos placeholder (carpetas vacias) | 11 de 15 |
| SubItems de navigation con vista renderizada | 6 de ~50 |
| Componentes funcionales JSX | 8 (Sidebar, SectionLanding, Overview, Demographics, EmployeeTable, OrganigramaIntegral, OrgStructure, Compensations) |
| Custom hooks | 1 (`useDemographicsData` + `useDemographicsFilters` en mismo archivo) |

### Componentes Compartidos

| Componente | Archivo | Funcion |
|------------|---------|---------|
| `Sidebar` | `modules/00-layout/Sidebar.jsx` | Navegacion lateral colapsable con arbol de modulos + subItems + panel de administracion |
| `SectionLanding` | `modules/00-layout/SectionLanding.jsx` | Landing page generica para cada modulo (grid de cards con iconos, descripciones, tags) |
| `navigationConfig` | `config/navigation.js` | Definicion completa de 13 modulos + 50 subItems con iconos, descripciones, tags metodologicos |

### Sistema de Routing

El routing es **state-based** (sin `react-router`). El estado `vistaActual` en `App.jsx` controla que vista se renderiza. La logica:
1. Si `vistaActual` coincide con un `module.id` de `navigationConfig` → renderiza `SectionLanding`
2. Si `vistaActual` coincide con un `subItem.id` → renderiza el componente mapeado o el placeholder generico
3. Vistas hardcodeadas en `App.jsx`: `vision_general`, `demografia`, `org_posiciones`, `org_integral`, `compensaciones`, `auditoria`

---

## 6. Variables de Entorno

### Detectadas en Codigo

| Variable | Archivo Origen | Usada en Codigo | Valor |
|----------|---------------|-----------------|-------|
| `DATABASE_URL` | `.env` (raiz del proyecto) | Si — `02_setup_raw_layer.py`, `03_ingest_data.py`, `04_setup_business_core.py`, `m05_fuerza_laboral.py`, `90_generate_data_inventory.py`, `91_export_data_samples.py`, `prisma.config.ts` (como `DIRECT_URL` fallback) | `***` |
| `VITE_SUPABASE_URL` | `client/.env` o `client/.env.local` | Si — `src/lib/supabaseClient.js` via `import.meta.env`, `91_export_data_samples.py` (fallback) | `***` |
| `VITE_SUPABASE_ANON_KEY` | `client/.env` o `client/.env.local` | Si — `src/lib/supabaseClient.js` via `import.meta.env` | `***` |
| `SUPABASE_SERVICE_KEY` | `client/.env` | Si — `91_export_data_samples.py` (fallback para construir `DATABASE_URL`) | `***` |
| `DIRECT_URL` | `.env` o `.env.local` (client) | Si — `prisma.config.ts` como fallback para `datasource.url` | `***` |

### Hallazgos

- **No se encontraron archivos `.env`** en el repositorio (correctamente ignorados por `.gitignore`)
- El `.gitignore` excluye `.env`, `.env.*` excepto `.env.example` — correcto
- **No existe `.env.example`** en el proyecto — [⚠️ Variable faltante] Se recomienda crear plantillas de ejemplo
- `client/.env` es la convencion inferida por los scripts ETL (91 busca ahi como fallback) y por `prisma.config.ts` que carga `.env.local`
- Todas las variables detectadas tienen consumo verificado en codigo — no hay variables fantasma

---

## 7. Score de Madurez del Proyecto

| Metrica | Valor | Score | Detalle |
|---------|-------|-------|---------|
| **Modulos implementados vs totales** | 3 de 15 modulos con codigo | 20% | Solo `00-layout`, `05-fuerza-laboral`, `06-nomina-costos` tienen componentes. 11 modulos son placeholders vacios |
| **SubItems con vista funcional** | 6 de ~50 | 12% | `vision_general`, `demografia`, `org_integral`, `org_posiciones`, `compensaciones`, `auditoria` |
| **Pipeline ETL completo** | 7 de 8 scripts activos | 88% | Pipeline 01→02→03→04→m05→90 funcional. Script 91 comentado en orquestador (ejecutable manualmente) |
| **Capa de datos implementada** | 13 objetos DB | 100% | 2 tablas raw + 2 vistas business + 7 MVs + 1 vista org + 2 RPCs + 1 tabla inventory |
| **Dependencias limpias (frontend)** | 3 fantasma detectadas | 75% | `autoprefixer`, `postcss` posiblemente innecesarias (Tailwind v4). `prisma` configurado sin schema |
| **Dependencias limpias (Python)** | Todas usadas | 100% | Las 5 dependencias Python tienen consumo verificado |
| **Variables de entorno OK** | 5 keys, todas usadas | 80% | Todas las variables tienen uso verificado. Falta `.env.example` como plantilla |
| **Documentacion al dia** | 6 documentos generados | 75% | Existen: PIPELINE_ORDER.md, metadata inventory, data samples, blueprint, data dictionary, audit report. Pendiente: regenerar tras cambios |
| **Tests automatizados** | 0 | 0% | No existen tests unitarios ni de integracion en frontend ni ETL |
| **CI/CD** | No detectado | 0% | No hay archivos `.github/`, `.gitlab-ci.yml`, ni config de CI |

### Score Global Ponderado

| Categoria | Peso | Score | Ponderado |
|-----------|------|-------|-----------|
| Backend/Datos (ETL + DB) | 30% | 95% | 28.5 |
| Frontend (componentes) | 25% | 20% | 5.0 |
| Infraestructura (env, deps) | 20% | 75% | 15.0 |
| Documentacion | 15% | 75% | 11.25 |
| Calidad (tests, CI/CD) | 10% | 0% | 0.0 |
| **TOTAL** | **100%** | | **59.75 / 100** |

**Estado general:** [⚠️ No verificable con precision absoluta] — El score es una aproximacion basada en analisis estatico de codigo. El pipeline ETL y la capa de datos estan maduros; el frontend esta en fase temprana de implementacion con el modulo 05 como referencia de arquitectura a seguir.

---

## 8. Observaciones y Recomendaciones

### Criticas

1. **Prisma configurado sin schema:** `prisma.config.ts` referencia `prisma/schema.prisma` que no existe. O se elimina la dependencia de Prisma (el proyecto usa Supabase client directamente) o se crea el schema.
2. **Dependencias potencialmente innecesarias:** `autoprefixer` y `postcss` en devDependencies pueden eliminarse si Tailwind v4 con `@tailwindcss/vite` los reemplaza completamente.
3. **Script 91 deshabilitado del pipeline:** `91_export_data_samples.py` esta comentado en `00_full_run_pipeline.py`. Si es util, deberia habilitarse.
4. **11 modulos placeholder:** Requieren plan de implementacion priorizado. El modulo 05 sirve como blueprint de arquitectura (componente + hook custom + RPC + MVs).

### Arquitectonicas

5. **Sin react-router:** El routing state-based funciona pero no soporta bookmarks, sharing de URLs, ni browser history. Considerar `react-router-dom` si el proyecto escala.
6. **`OrganigramaIntegral.jsx` usa datos mock:** [⚠️ No verificable] Segun analisis del README existente, este componente usa datos de prueba en lugar de `v_org_tree_byNapo`. Verificar implementacion real.
7. **Fx rate hardcodeado:** `01_generate_synthetic_data.py` usa `fx_rate_to_usd = 3.50` fijo para todos los paises. No refleja tasas reales por moneda.

### Positivas

8. **Medallion architecture bien implementada:** Capas Raw → Business → Data Marts con separacion clara de responsabilidades.
9. **RPC functions bien disenadas:** Las funciones aceptan los 6 filtros universales con valores DEFAULT NULL, permitiendo consultas flexibles desde el frontend.
10. **Materialized views con indexes:** Cada MV tiene indexes apropiados por `snapshot_date` para optimizar consultas filtradas.
11. **Sistema de navegacion escalable:** `navigationConfig` como archivo de configuracion permite agregar modulos sin tocar el router.

---

*Documento generado automaticamente mediante analisis estatico del repositorio. Las secciones marcadas como `[⚠️ No verificable]` requieren verificacion en runtime o acceso a la base de datos Supabase.*
