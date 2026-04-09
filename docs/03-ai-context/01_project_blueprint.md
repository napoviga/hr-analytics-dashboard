# 🏗️ Contexto Maestro y Blueprint del Proyecto (Project Blueprint)

> **Actualización:** Automatizada
> **Propósito:** Entregar a cualquier agente técnico o equipo externo un mapa exhaustivo de la arquitectura "Docs-as-Code" (ETL + React Vite) del HR Analytics Dashboard.

---

## 1. Estructura de Directorios (Tree)

El repositorio está fuertemente enfocado en el modelo *Feature-Sliced Design* (Módulos por dominio) y *Data Mesh* (ETL particionado). Esta es la radiografía limpia del proyecto:

```text
hr-analytics-dashboard/
├── .env                  # (Oculto en git - Contiene credenciales maestras)
├── README.md
├── client/               # Entorno FrontEnd (UI)
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── config/
│       │   └── navigation.js    # 📍 SOURCE OF TRUTH de la navegación
│       ├── lib/
│       │   └── supabaseClient.js
│       └── modules/             # 🧱 ARQUITECTURA MODULAR
│           ├── 00-layout/       (Sidebar, SectionLanding, Overview)
│           ├── 05-fuerza-laboral/ (Organigramas, Demographics, Tablas)
│           ├── 06-nomina-costos/  (Compensations)
│           └── (01 al 14 - Directorios vacíos preparados)
├── docs/                 # Documentación Técnica (Docs as Code)
│   ├── 01-product-specs/
│   ├── 02-data-governance/
│   └── 03-ai-context/    # <-- Este Blueprint Vive Aquí
└── etl_pipeline/         # ⚙️ Data Engineering & Backend Automation
    ├── 00_full_run_pipeline.py
    ├── 01_generate_synthetic_data.py
    ├── 02_setup_raw_layer.py
    ├── 03_ingest_data.py
    ├── 04_setup_business_core.py
    ├── m05_fuerza_laboral.py
    └── 90_generate_data_inventory.py
```

---

## 2. Dependencias y Entorno

### Dependencias Python (Backend & ETL Pipeline)
La suite asume Python 3.11+. Sus librerías base (inferidas del orquestador) son:
- `pandas` (Limpieza y consolidación tabular en memoria)
- `SQLAlchemy` (ORM y conector de consultas estructurado)
- `psycopg2-binary` (Driver robusto PostgreSQL)
- `python-dotenv` (Gestión segura de credenciales locales)

### Dependencias Node.js (Frontend Client)
Extraídas del `package.json` (`React 19` + `Vite`):
- **Core:** `react`, `react-dom`, `@vitejs/plugin-react`
- **Backend (BaaS):** `@supabase/supabase-js`
- **Visualización:** `echarts`, `echarts-for-react`, `lucide-react` (iconografía corporativa)
- **Estilos:** `@tailwindcss/vite`, `tailwindcss` (v4), `autoprefixer`

---

## 3. Modelado de Base de Datos y Arquitectura de Datos

El modelo sigue el framework de capas arquitectónicas Medallion:

### 🥉 Capa RAW (Bronce) -> Generada por `02` y `03`
- `raw.ibm_hr_monthly_snapshot_byNapo` (Carga principal transaccional)
- `raw.ibm_hr_change_reasons_byNapo` (Diccionarios y razones maestras)
*(Todos sus tipos se inyectan crudos para evitar cuellos de botella `COPY`).*

### 🥇 Capa BUSINESS CORE (Oro Central) -> Generada en el script `04`
- `business.v_employee_full_byNapo` **[VISTA]**: Granularidad 1:1 limpiando la RAW (calculando antigüedades nativas).
- `business.mv_ui_global_filters` **[M-VIEW]**: Vista materializada que indexa todas las fechas, países y departamentos basándose única y exclusivamente en `v_employee_full` (rompiendo dependencias cíclicas con otros módulos).

### 🏆 Capa DATA MARTS (Oro Dominio) -> Generada en `m05` (Fuerza Laboral)
Vistas e indexaciones pre-calculadas pesadas exclusivas para el motor demográfico del Dashboard:
- **Árbol Jerárquico**: `business.v_org_tree_byNapo`
- **Agregaciones**: `business.mv_monthly_kpis_byNapo` y `business.mv_demographics_agg`
- **Gráficos Avanzados**: `mv_diversity_pyramid`, `mv_bajas_heatmap`, `mv_country_dist` y `mv_experience_bubbles`.

### 🛡️ Funciones Base de Datos (RPC Supabase)
Funciones PostgreSQL alojadas y consumidas pasivamente (sin ORM excesivo local) para retornar JSON asíncronos rápidos:
- `get_demographics_dashboard` (Consume `mv_demographics_agg` para tarjetas Sparkline y YoY).
- `get_advanced_demographics` (Agrupa de manera global gráficos avanzados de país, retenciones, etc).

---

## 4. Scripts Críticos (ETL Domain-Driven)

El orquestador maestro absoluto es: **`00_full_run_pipeline.py`**
Invocado de esta manera, ejecuta este orden inquebrantable que escala fácilmente:

| Secuencia | Script | Rol | Dominio |
| :--- | :--- | :--- | :--- |
| **01** | `01_generate_synthetic_data.py` | Genera y enriquece métricas temporales (synthetic snapshotting) construyéndolas en `/data`. | Base/Core |
| **02** | `02_setup_raw_layer.py` | Crea/Limpia de cero la estructura del esquema *Raw* (Tablas Aterrizaje). | Base/Core |
| **03** | `03_ingest_data.py` | Inyecta pesadamente las +414,000 líneas a base de lotes usando SQLAlchemy. | Base/Core |
| **04** | `04_setup_business_core.py` | Crea el esquema de negocio y funda el "Master Data" y las variables (filtros UI) transversales a todos. | Base/Core |
| **M05**| `m05_fuerza_laboral.py` | **Primer script de Dominio.** DDLs para M-Views demográficas y compila las 2 funciones RPC. | Modular |
| **90** | `90_generate_data_inventory.py` | Escanea los esquemas finales de Postgres y autodocumenta el entorno en `/docs/02-data-governance/`. | Governance |

---

## 5. Estado del Frontend Modular (React/Vite)

- **El Cerebro (`src/config/navigation.js`):** Es el Source of Truth. No se hardcodean tarjetas ni sub-menús en los componentes. Todo es manejado mediante este diccionario json mapeando `id`, `icon`, titulo y descripciones metodológicas a renderizar.
- **Mapeo de UI (`src/modules/*`):** La carpeta plana de componentes no existe.
  - El layout usa `00-layout/Sidebar.jsx` (acordeón y paneles admin) y `00-layout/SectionLanding.jsx`.
  - El dominio demográfico (`05-fuerza-laboral`) alberga las vistas aisladas como `OrganigramaIntegral`, `OrgStructure` o el Dashboard general `Demographics`.
- **RPC Consumption:** Todos los grids en `05-fuerza-laboral` (como `Demographics.jsx`) usan el cliente supabase para gatillar `rpc('get_demographics_dashboard', {...filters})`.

---

## 6. Variables de Entorno (.env)

El archivo `.env` maestro (oculto) en la raíz exige estrictamente estas *Keys*:

```env
VITE_SUPABASE_URL=***
VITE_SUPABASE_ANON_KEY=***
SUPABASE_SERVICE_KEY=***
DATABASE_URL=***
```

Las llaves `VITE_` son permitidas para la compilación del Dashboard, mietras que `DATABASE_URL` funciona como cadena de conexión nativa psycopg2 para el pipeline de Data Engineering. NUNCA DEBEN hacer Check-In en Control de Versiones.
