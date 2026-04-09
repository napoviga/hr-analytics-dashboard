# README Update Brief — HR Analytics Dashboard
> Generado automáticamente el 2026-04-07 por Technical Writer Agent.
> Propósito: Servir como insumo estructurado para que otro agente redacte la versión final del README.md.

---

## 1. Nuevos Módulos y Scripts

### 1.1 ETL Pipeline (`/etl_pipeline`)

El README actual solo documenta 3 scripts (01–03). Desde entonces se han creado **5 archivos nuevos**:

| # | Archivo | Estado | Descripción |
|---|---------|--------|-------------|
| **NEW** | `00_full_run_pipeline.py` | ✅ Funcional | **Orquestador maestro.** Invoca secuencialmente los scripts 01→07 mediante `subprocess`. Incluye banner ejecutivo, medición de tiempo total y manejo de errores con interrupción automática si un paso falla. |
| **NEW** | `04_create_enhanced_dataset_byNapo.py` | ✅ Funcional | **Generador de datos mejorados.** Simula un dataset de snapshots mensuales (75 meses, ~450K registros) con 35 columnas HR: demográficas, jerárquicas, salariales, flags de cambio y coordenadas geográficas. Exporta `ibm_hr_monthly_snapshot_byNapo.csv`. |
| **NEW** | `05_setup_raw_enhanced_byNapo.py` | ✅ Funcional | **DDL de la capa Raw mejorada.** Crea las tablas `raw.ibm_hr_monthly_snapshot_byNapo` (35 cols TEXT + timestamp) y `raw.ibm_hr_change_reasons_byNapo` (catálogo de motivos). |
| **NEW** | `06_ingest_enhanced_byNapo.py` | ✅ Funcional | **Ingesta masiva del dataset mejorado.** Lee el CSV generado por el paso 04 y lo sube a la tabla raw en chunks de 1000 registros. |
| **NEW** | `07_setup_business_enhanced_byNapo.py` | ✅ Funcional | **Capa Business mejorada (Clean Slate).** Destruye y reconstruye el esquema `business` con 5 vistas analíticas tipadas + 1 vista materializada + índice único + permisos Supabase `anon`. |

### 1.2 Scripts Existentes Modificados

| Archivo | Cambio |
|---------|--------|
| `01_setup_raw.py` | Refactorizado con logging ejecutivo, `try/except`, medición de tiempo y enumeración de artefactos creados. |
| `02_ingest_data.py` | Ídem: logging ejecutivo con resumen de ingesta (origen, destino, volumen). |
| `03_setup_business.py` | Ídem: logging ejecutivo con enumeración de esquema, vista y permisos. |

### 1.3 Frontend (`/client/src/components`)

El README no detalla componentes individuales. Los componentes actuales son:

| Componente | Descripción |
|------------|-------------|
| `Sidebar.jsx` | Menú lateral colapsable estilo Microsoft 365 con navegación por acordeón. |
| `Overview.jsx` | Vista general con KPIs ejecutivos y gráficos de resumen. |
| `OrgStructure.jsx` | Landing page del módulo de Estructura Organizativa con submenús. |
| `OrganigramaIntegral.jsx` | Visualización jerárquica del organigrama empresarial. |
| `Compensations.jsx` | Análisis de compensaciones con visualización de tarifa diaria vs edad. |
| `EmployeeTable.jsx` | Tabla dinámica para auditoría de registros (TanStack Table). |

---

## 2. Evolución de la Arquitectura de Datos

### 2.1 Cambio de paradigma: Datos Estáticos → Series de Tiempo

| Aspecto | README actual (v1) | Estado real (v2) |
|---------|-------------------|------------------|
| **Dataset origen** | `ibm_hr.csv` (1,470 registros). Un corte estático en un solo punto del tiempo. | Se añadió `ibm_hr_monthly_snapshot_byNapo.csv` (~450K registros, 75 meses, 2020-01 a 2026-03). **Series de tiempo mensuales.** |
| **Esquema raw** | Solo `raw.ibm_hr_landing` (35 cols TEXT, ingesta plana). | Se añadieron `raw.ibm_hr_monthly_snapshot_byNapo` (35 cols TEXT) y `raw.ibm_hr_change_reasons_byNapo` (catálogo). |
| **Esquema business** | Solo `business.ibm_hr` (vista simple con casting directo). | Se añadieron **6 artefactos nuevos** en `business` (ver tabla abajo). |

### 2.2 Nuevos Artefactos en Esquema `business`

| # | Tipo | Nombre | Propósito |
|---|------|--------|-----------|
| 1 | Vista | `v_employee_full_byNapo` | Vista maestra tipada. Transforma TEXT→tipos nativos con `NULLIF` defensivo. Incluye campos calculados: `tenure_months`, `is_active_at_snapshot`. |
| 2 | Vista | `v_org_tree_byNapo` | Organigrama recursivo con CTE (Common Table Expression). Prevención de ciclos y límite de profundidad 10. Incluye nodo JSON para ECharts. |
| 3 | MatView | `mv_monthly_kpis_byNapo` | Vista materializada de KPIs mensuales agrupados por `snapshot_date`, `country_iso3`, `department_name`, `job_level_1`. Incluye headcount, salarios, attrition rate, salary change rate. Índice único para soporte de `REFRESH CONCURRENTLY`. |
| 4 | Vista | `v_kpi_summary_byNapo` | Resumen rápido globales por snapshot para tarjetas KPI del dashboard. |
| 5 | Vista | `v_compensation_analysis_byNapo` | Análisis de compensación por empleado activo (sin compa-ratio temporalmente; depende de tabla de bandas salariales futura). |
| 6 | Permisos | `GRANT ... TO anon` | Acceso de lectura Supabase `anon` sobre todo el esquema `business`. |

### 2.3 Estrategia Clean Slate

El script 07 ahora ejecuta `DROP SCHEMA IF EXISTS business CASCADE` antes de reconstruir, garantizando idempotencia total en cada ejecución del pipeline.

---

## 3. Actualizaciones de la Interfaz (Frontend)

### 3.1 Componentes y Vistas documentados en el README vs. estado real

| Módulo en README | Estado real en el código |
|------------------|------------------------|
| Estructura Organizativa | ✅ Implementado: `OrgStructure.jsx` (landing con submenú) + `OrganigramaIntegral.jsx` (visualización jerárquica). |
| Compensaciones | ✅ Implementado: `Compensations.jsx`. |
| Auditoría de Datos | ✅ Implementado: `EmployeeTable.jsx`. |
| Visión General | ✅ Implementado: `Overview.jsx` (no mencionado explícitamente como componente en el README). |
| Sidebar | ✅ Implementado: `Sidebar.jsx` con navegación por acordeón. Mencionado en README pero sin detalle de componente. |
| Fuga de Talento, Desempeño, Turnos, Reclutamiento, Capacitación, Clima, Diversidad | ⏳ Placeholders en `App.jsx` con mensaje "Módulo en Construcción". |

### 3.2 Cambios de diseño relevantes

- **Sidebar colapsable con acordeón**: El módulo "Estructura Org." tiene submenú desplegable con 3 opciones (Organigrama Integral, Dotación, Costos).
- **Estilo Microsoft 365**: Colores corporativos sobrios, diseño ejecutivo.
- **Routing por estado**: La navegación se maneja mediante `vistaActual` (state) en `App.jsx`, sin router externo.

---

## 4. Nuevas Dependencias

### 4.1 Python (Backend ETL)

> ⚠️ **No existe `requirements.txt` en el proyecto.** Las dependencias se infieren del código fuente:

| Librería | Versión | Usada en | Propósito |
|----------|---------|----------|-----------|
| `pandas` | — | 01, 02, 04, 06 | Manipulación de DataFrames y lectura/escritura CSV. |
| `numpy` | — | 04 | Generación de datos aleatorios (distribuciones, elecciones). |
| `sqlalchemy` | — | 01–03, 05–07 | Conexión ORM a PostgreSQL/Supabase. |
| `psycopg2` | — | (dependencia de SQLAlchemy) | Driver PostgreSQL nativo. |
| `python-dotenv` | — | 01–03, 05–07 | Lectura de variables de entorno desde `.env`. |
| `networkx` | — | 04 (importado, uso futuro) | Validación de grafos para organigramas. |

**Recomendación:** Crear un `requirements.txt` o `pyproject.toml` para formalizar las dependencias de Python.

### 4.2 Node.js (Frontend React)

Las dependencias en `package.json` ya están correctamente declaradas. El README las menciona de forma general pero no detalla versiones. Estado actual:

| Dependencia | Versión | Mencionada en README |
|-------------|---------|---------------------|
| `react` | ^19.2.4 | ✅ (como "React.js") |
| `react-dom` | ^19.2.4 | ✅ |
| `@supabase/supabase-js` | ^2.101.1 | ❌ No mencionada |
| `echarts` | ^6.0.0 | ✅ (como "Apache ECharts") |
| `echarts-for-react` | ^3.0.6 | ❌ No mencionada |
| `lucide-react` | ^1.7.0 | ✅ (como "Lucide-React") |
| `tailwindcss` | ^4.2.2 | ✅ (como "Tailwind CSS") |
| `prisma` | ^7.6.0 (devDep) | ❌ No mencionada — verificar si se usa activamente |
| `dotenv` | ^17.4.1 (devDep) | ❌ No mencionada |

---

## 5. Sección del README que requiere actualización urgente

### Sección 6 — Installation & Deployment Guide

El README actual indica ejecutar solo 3 scripts:

```bash
cd etl_pipeline
python 01_setup_raw.py
python 02_ingest_data.py
python 03_setup_business.py
```

**Debe actualizarse a:**

```bash
cd etl_pipeline
python 00_full_run_pipeline.py
```

O, si se prefiere ejecución individual:

```bash
python 01_setup_raw.py
python 02_ingest_data.py
python 03_setup_business.py
python 04_create_enhanced_dataset_byNapo.py
python 05_setup_raw_enhanced_byNapo.py
python 06_ingest_enhanced_byNapo.py
python 07_setup_business_enhanced_byNapo.py
```

### Sección 3 — Directory Structure

Debe reflejar los nuevos archivos en `/etl_pipeline` (00–07) y el dataset `ibm_hr_monthly_snapshot_byNapo.csv` en `/data`.

---

*Fin del brief. Listo para ser consumido por el agente redactor del README final.*
