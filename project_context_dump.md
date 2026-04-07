# Contexto de Proyecto: HR Analytics Dashboard

Este documento sirve como "Context Dump" para documentar la arquitectura, estructura y estado actual del proyecto, facilitando la sincronización con un nuevo equipo o agente de IA.

## 1. Estructura de Directorios (Tree)

A continuación, la estructura de archivos y directorios del proyecto, excluyendo directorios pesados/irrelevantes (`node_modules`, `.git`, `venv`, `.venv`, `__pycache__`, etc.):

```text
hr-analytics-dashboard
├── .env
├── .gitignore
├── project_context_dump.md
├── README.md
├── client
│   ├── .agents
│   ├── docs
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── prisma.config.ts
│   ├── public
│   ├── skills-lock.json
│   ├── src
│   │   ├── App.jsx
│   │   ├── components
│   │   │   ├── Compensations.jsx
│   │   │   ├── EmployeeTable.jsx
│   │   │   ├── OrgStructure.jsx
│   │   │   ├── OrganigramaIntegral.jsx
│   │   │   ├── Overview.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── index.css
│   │   ├── lib
│   │   └── main.jsx
│   └── vite.config.js
├── data
│   ├── ibm_hr.csv
│   └── ibm_hr_monthly_snapshot_byNapo.csv
└── etl_pipeline
    ├── 01_setup_raw.py
    ├── 02_ingest_data.py
    ├── 03_setup_business.py
    ├── 04_create_enhanced_dataset_byNapo.py
    ├── 05_setup_raw_enhanced_byNapo.py
    ├── 06_ingest_enhanced_byNapo.py
    └── 07_setup_business_enhanced_byNapo.py
```

## 2. Dependencias y Entorno

### Dependencias de Python (Backend / ETL)
Aunque no se detecta un archivo `requirements.txt` explícito, los scripts del backend (`etl_pipeline/*.py`) exigen las siguientes librerías:
```ini
pandas
numpy
sqlalchemy
python-dotenv
psycopg2-binary # Usado por URL postgresql://
networkx # Usado en simulación de data y organigrama
```

### Dependencias de Frontend (React / Vite)
Extraído de `client/package.json`:

**dependencies:**
```json
{
  "@supabase/supabase-js": "^2.101.1",
  "echarts": "^6.0.0",
  "echarts-for-react": "^3.0.6",
  "lucide-react": "^1.7.0",
  "react": "^19.2.4",
  "react-dom": "^19.2.4"
}
```

**devDependencies:**
```json
{
  "@eslint/js": "^9.39.4",
  "@tailwindcss/vite": "^4.2.2",
  "@types/react": "^19.2.14",
  "@types/react-dom": "^19.2.3",
  "@vitejs/plugin-react": "^6.0.1",
  "autoprefixer": "^10.4.27",
  "dotenv": "^17.4.1",
  "eslint": "^9.39.4",
  "eslint-plugin-react-hooks": "^7.0.1",
  "eslint-plugin-react-refresh": "^0.5.2",
  "globals": "^17.4.0",
  "postcss": "^8.5.8",
  "prisma": "^7.6.0",
  "tailwindcss": "^4.2.2",
  "vite": "^8.0.1"
}
```

## 3. Modelado de Base de Datos y Arquitectura de Datos

El diseño utiliza Supabase (PostgreSQL), donde el flujo ETL separa los datos en esquema `raw` (sin tipar) y esquema `business` (tipados/vistas/KPIs).

### Esquema: `raw` (Capa Landing)
- **`raw.ibm_hr_landing`**: Tabla de ingesta base. Todas sus columnas (`age`, `attrition`, `gender`, `jobrole`, etc.) son de tipo `TEXT`. Registra `created_at` (TIMESTAMP).
- **`raw.ibm_hr_monthly_snapshot_byNapo`**: Nueva tabla extendida. Recibe snapshots mensuales. Todo el data frame original es guardado como `TEXT` (`employee_id`, `nationality_iso3`, `manager_employee_id`, `salary_change_flag`, etc.).
- **`raw.ibm_hr_change_reasons_byNapo`**: Catálogo paramétrico de motivos de cambio.

### Esquema: `business` (Capa de Analytics/Views)
- **`business.ibm_hr`**: Vista básica (`id` INTEGER, `age` INTEGER, `dailyrate` INTEGER, etc.).
- **`business.v_employee_full_byNapo`**: Vista extendida que castea los datos RAW a nativos (`snapshot_date::DATE`, `manager_employee_id::INTEGER`, flags a `BOOLEAN`, salarios a `NUMERIC`). Añade flags de fechas (`is_active_at_snapshot`) y antigüedad (`tenure_months`).
- **`business.v_org_tree_byNapo`**: Vista RECURSIVA `WITH RECURSIVE` para deducir el árbol organizacional según `manager_employee_id`. Exporta objetos ricos `echarts_node::JSON` para los componentes de árbol en React.
- **`business.mv_monthly_kpis_byNapo`**: Vista *Materializada* de alto rendimiento para KPIs grupales agrupando por fechas, departamentos y países. Calcula retención, rotación (`attrition_rate_monthly_pct`) y promedios salariales.
- **`business.v_kpi_summary_byNapo`** y **`business.v_compensation_analysis_byNapo`**: Vistas enfocadas en tarjetas directivas y matrices de equidad salarial (`band_penetration_pct`, `compa_ratio`).

## 4. Scripts Críticos del Backend / Pipeline ETL

A continuación, los scripts íntegros ejecutables del flujo de datos en `/etl_pipeline/`:

### 01_setup_raw.py
```python
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw():
    # 1. Leer CSV para detectar cabeceras
    df = pd.read_csv('../data/ibm_hr.csv', nrows=0) 
    columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # 2. Construir el SQL Dinámico
    table_name = "raw.ibm_hr_landing"
    cols_query = ", ".join([f"{col} TEXT" for col in columns])
    sql_query = f"""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS {table_name};
    CREATE TABLE {table_name} (
        {cols_query},
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # 3. Ejecutar en la Base de Datos
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text(sql_query))
        conn.commit()
    print(f"✅ Capa RAW preparada: Tabla {table_name} creada con {len(columns)} columnas.")

if __name__ == "__main__":
    setup_raw()
```

### 02_ingest_data.py
```python
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_data():
    # 1. Cargar y Limpiar Nombres
    df = pd.read_csv('../data/ibm_hr.csv')
    df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # 2. Conectar e Inyectar
    engine = create_engine(db_url)
    print(f"🚀 Iniciando ingesta de {len(df)} registros...")
    
    df.to_sql(
        name='ibm_hr_landing',
        con=engine,
        schema='raw',
        if_exists='append',
        index=False,
        chunksize=500 # Sube de 500 en 500 para mayor estabilidad
    )
    print("✅ Ingesta completada con éxito en raw.ibm_hr_landing.")

if __name__ == "__main__":
    ingest_data()
```

### 03_setup_business.py
```python
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business():
    engine = create_engine(db_url)
    
    sql_query = """
    CREATE SCHEMA IF NOT EXISTS business;
    
    CREATE OR REPLACE VIEW business.ibm_hr AS
    SELECT 
        employeenumber::INTEGER as id,
        age::INTEGER,
        department,
        jobrole,
        attrition,
        gender,
        dailyrate::INTEGER,
        monthlyincome::INTEGER,
        totalworkingyears::INTEGER,
        yearsatcompany::INTEGER,
        distancefromhome::INTEGER
    FROM raw.ibm_hr_landing;

    -- Permisos para el Dashboard
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql_query))
        conn.commit()
    print("✅ Capa BUSINESS preparada: Vista core.ibm_hr lista y con permisos otorgados.")

if __name__ == "__main__":
    setup_business()
```

### 04_create_enhanced_dataset_byNapo.py
```python
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import networkx as nx

# ==========================================
# 🛠️ CONFIGURACIÓN DEL DATASET - NAPo HR
# ==========================================
CONFIG = {
    "RANDOM_SEED": 42,
    "DATE_RANGE": {"start": "2020-01-01", "end": "2026-03-31"},
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 8000},
    "OUTPUT_DIR": "../data/",
    "LOG_LEVEL": "INFO"
}

def generate_dataset():
    print("🚀 Iniciando generación del dataset potenciado byNapo...")
    
    # 1. Configuración de fechas
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    
    # 2. Carga base IBM (Simulación inicial)
    # Generamos DataFrame vacío base con columnas clave
    cols_snapshot = [
        "snapshot_date", "employee_id", "employee_code", "full_name", "gender", 
        "nationality_iso3", "country_iso3", "department_name", "job_role", 
        "job_level_1", "job_level_2", "employment_status", "hire_date", 
        "termination_date", "termination_reason_legal", "turnover_classification_company",
        "monthly_salary_local", "currency_iso3", "fx_rate_to_usd", "monthly_salary_usd",
        "manager_employee_id", "dotted_line_manager_id", "work_center_id", 
        "home_lat", "home_lon", "work_modality", "education_level", 
        "education_status", "marital_status", "dependents_count", 
        "salary_change_flag", "salary_change_reason_code", "job_change_flag", 
        "exit_interview_completed", "regrettable_loss_flag"
    ]
    
    # Creamos lista de DataFrames mensuales
    monthly_data = []
    
    print(f"📅 Generando snapshots desde {start.strftime('%Y-%m')} hasta {end.strftime('%Y-%m')}...")
    
    # Simulación simplificada para demostración
    for date in dates:
        n_emp = np.random.randint(CONFIG["EMPLOYEES_PER_MONTH"]["min"], CONFIG["EMPLOYEES_PER_MONTH"]["max"])
        
        data = {
            "snapshot_date": date.strftime("%Y-%m-%d"),
            "employee_id": range(1, n_emp + 1),
            "employee_code": [f"EMP-{i:05d}" for i in range(1, n_emp + 1)],
            "full_name": ["Empleado Generado" for _ in range(n_emp)],
            "gender": np.random.choice(["Male", "Female"], n_emp),
            "nationality_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "country_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "department_name": np.random.choice(["Sales", "IT", "HR", "Operations"], n_emp),
            "job_role": np.random.choice(["Analyst", "Manager", "Director"], n_emp),
            "job_level_1": np.random.choice(["Individual Contributor", "Management"], n_emp),
            "job_level_2": np.random.choice(["Junior", "Senior", "Lead"], n_emp),
            "employment_status": np.random.choice(["Active", "Terminated"], n_emp, p=[0.9, 0.1]),
            "hire_date": (date - pd.Timedelta(days=np.random.randint(1, 3650))).strftime("%Y-%m-%d"),
            "termination_date": [None] * n_emp,
            "termination_reason_legal": [None] * n_emp,
            "turnover_classification_company": [None] * n_emp,
            "monthly_salary_local": np.random.uniform(1000, 5000, n_emp).round(2),
            "currency_iso3": "PEN",
            "fx_rate_to_usd": 3.70,
            "monthly_salary_usd": 0.0,
            "manager_employee_id": [None] * n_emp,
            "dotted_line_manager_id": [None] * n_emp,
            "work_center_id": np.random.choice(["WC-001", "WC-002"], n_emp),
            "home_lat": np.random.uniform(-12.0, -11.0, n_emp),
            "home_lon": np.random.uniform(-77.0, -76.0, n_emp),
            "work_modality": "Hybrid",
            "education_level": "Bachelor",
            "education_status": "Complete",
            "marital_status": "Single",
            "dependents_count": 0,
            "salary_change_flag": 0,
            "salary_change_reason_code": None,
            "job_change_flag": 0,
            "exit_interview_completed": False,
            "regrettable_loss_flag": False
        }
        
        df = pd.DataFrame(data)
        
        # Cálculo de FX y USD
        df["monthly_salary_usd"] = (df["monthly_salary_local"] / df["fx_rate_to_usd"]).round(2)
        
        monthly_data.append(df)

    # Concatenar todo
    final_df = pd.concat(monthly_data, ignore_index=True)
    
    # Guardar CSV
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    final_df.to_csv(output_path, index=False)
    print(f"✅ Dataset guardado en: {output_path}")
    print(f"📊 Total registros generados: {len(final_df)}")

if __name__ == "__main__":
    generate_dataset()
```

### 05_setup_raw_enhanced_byNapo.py
```python
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw_enhanced():
    print("🔨 Creando tablas RAW potenciadas (byNapo)...")
    engine = create_engine(db_url)
    
    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS raw;

    -- Tabla Principal: Snapshot Mensual
    CREATE TABLE IF NOT EXISTS raw.ibm_hr_monthly_snapshot_byNapo (
        snapshot_date TEXT,
        employee_id TEXT,
        employee_code TEXT,
        full_name TEXT,
        gender TEXT,
        nationality_iso3 TEXT,
        country_iso3 TEXT,
        department_name TEXT,
        job_role TEXT,
        job_level_1 TEXT,
        job_level_2 TEXT,
        employment_status TEXT,
        hire_date TEXT,
        termination_date TEXT,
        termination_reason_legal TEXT,
        turnover_classification_company TEXT,
        monthly_salary_local TEXT,
        currency_iso3 TEXT,
        fx_rate_to_usd TEXT,
        monthly_salary_usd TEXT,
        manager_employee_id TEXT,
        dotted_line_manager_id TEXT,
        work_center_id TEXT,
        home_lat TEXT,
        home_lon TEXT,
        work_modality TEXT,
        education_level TEXT,
        education_status TEXT,
        marital_status TEXT,
        dependents_count TEXT,
        salary_change_flag TEXT,
        salary_change_reason_code TEXT,
        job_change_flag TEXT,
        exit_interview_completed TEXT,
        regrettable_loss_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Tabla de Catálogo de Motivos
    CREATE TABLE IF NOT EXISTS raw.ibm_hr_change_reasons_byNapo (
        reason_code TEXT,
        reason_name_es TEXT,
        reason_name_en TEXT,
        affects_salary TEXT,
        affects_job TEXT,
        active_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    with engine.connect() as conn:
        conn.execute(text(sql_queries))
        conn.commit()
    print("✅ Tablas RAW potenciadas creadas correctamente.")

if __name__ == "__main__":
    setup_raw_enhanced()
```

### 06_ingest_enhanced_byNapo.py
```python
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def ingest_enhanced_data():
    print("📥 Iniciando ingesta de datos potenciados (byNapo)...")
    
    engine = create_engine(db_url)
    data_dir = "../data/"
    
    files_to_ingest = {
        "ibm_hr_monthly_snapshot_byNapo.csv": "raw.ibm_hr_monthly_snapshot_byNapo",
    }
    
    for filename, table_name in files_to_ingest.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Normalizar nombres de columnas para match exacto
            df.columns = [col.strip().lower() for col in df.columns]
            
            print(f"🚀 Subiendo {len(df)} registros a {table_name}...")
            df.to_sql(
                name=table_name.split('.')[1],
                schema=table_name.split('.')[0],
                con=engine,
                if_exists='append',
                index=False,
                chunksize=1000
            )
            print(f"✅ {filename} ingestado exitosamente.")
        else:
            print(f"⚠️ Archivo no encontrado: {filepath}")

if __name__ == "__main__":
    ingest_enhanced_data()
```

### 07_setup_business_enhanced_byNapo.py
```python
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_enhanced():
    print("🏗️ Creando Capa Business (Vistas byNapo)...")
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return
    
    engine = create_engine(db_url)
    
    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- 1. ESQUEMA Y VISTA MAESTRA TIPADA
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        snapshot_date::DATE as snapshot_date,
        employee_id::INTEGER as employee_id,
        employee_code, full_name, gender, nationality_iso3, country_iso3,
        birth_date::DATE as birth_date, home_address,
        home_lat::NUMERIC(10,6) as home_lat,
        home_lon::NUMERIC(10,6) as home_lon,
        work_center_id, work_modality,
        department_name, job_role, job_level_1, job_level_2, job_family,
        employment_status,
        hire_date::DATE as hire_date,
        termination_date::DATE as termination_date,
        termination_reason_legal, termination_reason_detail, turnover_classification_company,
        monthly_salary_local::NUMERIC(12,2) as monthly_salary_local,
        currency_iso3,
        fx_rate_to_usd::NUMERIC(10,6) as fx_rate_to_usd,
        monthly_salary_usd::NUMERIC(12,2) as monthly_salary_usd,
        NULLIF(manager_employee_id, '')::INTEGER as manager_employee_id,
        NULLIF(dotted_line_manager_employee_id, '')::INTEGER as dotted_line_manager_employee_id,
        education_level, education_status, marital_status,
        dependents_count::INTEGER as dependents_count,
        (salary_change_flag = '1' OR salary_change_flag = 'true') as salary_change_flag,
        salary_change_reason_code,
        (job_change_flag = '1' OR job_change_flag = 'true') as job_change_flag,
        job_change_reason_code,
        (exit_interview_completed = '1' OR exit_interview_completed = 'true') as exit_interview_completed,
        (regrettable_loss_flag = '1' OR regrettable_loss_flag = 'true') as regrettable_loss_flag,
        
        CASE 
            WHEN termination_date::DATE IS NOT NULL THEN 
                EXTRACT(YEAR FROM AGE(termination_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(termination_date::DATE, hire_date::DATE))
            ELSE 
                EXTRACT(YEAR FROM AGE(snapshot_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(snapshot_date::DATE, hire_date::DATE))
        END as tenure_months,
        
        CASE 
            WHEN employment_status = 'Active' THEN TRUE
            WHEN termination_date::DATE IS NULL THEN TRUE
            WHEN termination_date::DATE >= snapshot_date::DATE THEN TRUE
            ELSE FALSE
        END as is_active_at_snapshot,
        NOW() as processed_at
    FROM raw.ibm_hr_monthly_snapshot_byNapo;

    -- 2. VISTA DE ORGANIGRAMA (Recursiva)
    CREATE OR REPLACE VIEW business.v_org_tree_byNapo AS
    WITH RECURSIVE org_hierarchy AS (
        SELECT 
            employee_id, full_name, job_role, job_level_1, job_level_2,
            department_name, country_iso3, work_center_id, manager_employee_id,
            0 as depth,
            ARRAY[employee_id] as path_ids,
            ARRAY[full_name] as path_names
        FROM business.v_employee_full_byNapo
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND employment_status = 'Active'
          AND (manager_employee_id IS NULL OR manager_employee_id NOT IN (
                   SELECT employee_id FROM business.v_employee_full_byNapo 
                   WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
                     AND employment_status = 'Active'))
        
        UNION ALL
        
        SELECT 
            emp.employee_id, emp.full_name, emp.job_role, emp.job_level_1, emp.job_level_2,
            emp.department_name, emp.country_iso3, emp.work_center_id, emp.manager_employee_id,
            oh.depth + 1,
            oh.path_ids || emp.employee_id,
            oh.path_names || emp.full_name
        FROM business.v_employee_full_byNapo emp
        INNER JOIN org_hierarchy oh ON emp.manager_employee_id = oh.employee_id
        WHERE emp.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND emp.employment_status = 'Active'
          AND emp.manager_employee_id IS NOT NULL
          AND NOT emp.employee_id = ANY(oh.path_ids)
          AND oh.depth < 10
    )
    SELECT 
        employee_id, full_name, job_role, job_level_1, job_level_2,
        department_name, country_iso3, work_center_id, manager_employee_id,
        depth, path_ids, path_names,
        json_build_object(
            'id', employee_id, 'name', full_name, 'role', job_role,
            'level', job_level_1, 'dept', department_name, 'country', country_iso3,
            'depth', depth, 'children', NULL
        ) as echarts_node
    FROM org_hierarchy
    ORDER BY depth, employee_id;

    -- 3. VISTA MATERIALIZADA: KPIs Mensuales
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_monthly_kpis_byNapo AS
    WITH monthly_stats AS (
        SELECT 
            snapshot_date, country_iso3, department_name, job_level_1,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
            COUNT(*) as headcount_total,
            ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
            ROUND(MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as min_salary_usd,
            ROUND(MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as max_salary_usd,
            COUNT(*) FILTER (WHERE salary_change_flag = TRUE) as salary_changes_count,
            COUNT(*) FILTER (WHERE job_change_flag = TRUE) as job_changes_count,
            COUNT(*) FILTER (WHERE turnover_classification_company = 'Undesired_Turnover') as undesired_turnovers,
            COUNT(*) FILTER (WHERE regrettable_loss_flag = TRUE) as regrettable_losses
        FROM business.v_employee_full_byNapo
        GROUP BY snapshot_date, country_iso3, department_name, job_level_1
    )
    SELECT 
        *,
        ROUND(CASE WHEN headcount_active > 0 THEN (headcount_terminated::NUMERIC / NULLIF(headcount_active + headcount_terminated, 0)) * 100 ELSE 0 END, 2) as attrition_rate_monthly_pct,
        ROUND(CASE WHEN headcount_active > 0 THEN (salary_changes_count::NUMERIC / NULLIF(headcount_active, 0)) * 100 ELSE 0 END, 2) as salary_change_rate_pct,
        NOW() as generated_at
    FROM monthly_stats;

    CREATE INDEX IF NOT EXISTS idx_mv_kpis_snapshot ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3);

    -- 4. VISTA DE RESUMEN RÁPIDO
    CREATE OR REPLACE VIEW business.v_kpi_summary_byNapo AS
    SELECT 
        snapshot_date,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as total_headcount,
        COUNT(DISTINCT country_iso3) as countries_count,
        COUNT(DISTINCT department_name) as departments_count,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as global_avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure_months,
        COUNT(*) FILTER (WHERE salary_change_flag = TRUE) as recent_salary_changes,
        COUNT(*) FILTER (WHERE turnover_classification_company = 'Undesired_Turnover') as undesired_exits
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date
    ORDER BY snapshot_date DESC;

    -- 5. VISTA DE COMPENSACIÓN
    CREATE OR REPLACE VIEW business.v_compensation_analysis_byNapo AS
    SELECT 
        e.snapshot_date, e.employee_id, e.full_name, e.country_iso3, e.department_name,
        e.job_level_1, e.job_level_2, e.monthly_salary_local, e.currency_iso3,
        e.monthly_salary_usd, e.fx_rate_to_usd, e.is_active_at_snapshot,
        ROUND(CASE WHEN e.monthly_salary_usd > 0 AND cm.grade_mid_usd > 0 THEN e.monthly_salary_usd / cm.grade_mid_usd ELSE NULL END, 3) as compa_ratio,
        ROUND(CASE WHEN cm.grade_max_usd > cm.grade_min_usd THEN ((e.monthly_salary_usd - cm.grade_min_usd) / (cm.grade_max_usd - cm.grade_min_usd)) * 100 ELSE NULL END, 1) as band_penetration_pct,
        CASE 
            WHEN e.monthly_salary_usd < cm.grade_min_usd * 0.8 THEN 'Below_Minimum'
            WHEN e.monthly_salary_usd > cm.grade_max_usd * 1.2 THEN 'Above_Maximum'
            WHEN e.monthly_salary_usd < cm.grade_mid_usd * 0.9 THEN 'Below_Market'
            WHEN e.monthly_salary_usd > cm.grade_mid_usd * 1.1 THEN 'Above_Market'
            ELSE 'In_Range'
        END as salary_position_flag
    FROM business.v_employee_full_byNapo e
    LEFT JOIN raw.ibm_hr_compensation_matrix_byNapo cm 
        ON e.job_level_1 = cm.job_level_1 AND e.country_iso3 = cm.country_iso3 AND e.snapshot_date BETWEEN cm.effective_date AND cm.expiration_date
    WHERE e.is_active_at_snapshot = TRUE;

    -- 6. PERMISOS
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    ALTER DEFAULT PRIVILEGES IN SCHEMA business GRANT SELECT ON TABLES TO anon;
    GRANT SELECT ON business.mv_monthly_kpis_byNapo TO anon;
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.commit()
            print("✅ Vistas Business creadas exitosamente")
            
        with engine.connect() as conn:
            conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY business.mv_monthly_kpis_byNapo;"))
            conn.commit()
            print("✅ Vista materializada mv_monthly_kpis_byNapo refrescada")
            
    except Exception as e:
        print(f"❌ Error creando vistas Business: {str(e)}")
        raise

if __name__ == "__main__":
    setup_business_enhanced()
```

## 5. Estado del Frontend (React/Vite)

### Componentes Activos en `/client/src/components`:
1. `Compensations.jsx`
2. `EmployeeTable.jsx`
3. `OrgStructure.jsx`
4. `OrganigramaIntegral.jsx`
5. `Overview.jsx`
6. `Sidebar.jsx`

### Enrutamiento Condicional (en `client/src/App.jsx`)
La aplicación no utiliza librerías externas de enrutamiento web (como React Router DOM). En vez de eso, muta vistas delegadas por el sidebar:
```javascript
// ... importaciones ...

function App() {
  const [empleados, setEmpleados] = useState([])
  const [errorBd, setErrorBd] = useState(null)
  const [vistaActual, setVistaActual] = useState('vision_general')

  // ... lógica de obtención de datos ...

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />

      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8 border-b border-gray-200 pb-4">
            <h1 className="text-3xl font-semibold text-gray-800 mb-8">HR Analytics</h1>
          </header>
        
        {errorBd ? (
          <div className="bg-red-900 text-red-200 p-4 rounded-lg mt-4 text-sm font-mono shadow-md">
            <strong>🚨 Error de Conexión:</strong> {errorBd}
          </div>
        ) : (
          <div className="mt-8">
            {/* Vistas Activas */}
            {vistaActual === 'vision_general' && <Overview data={empleados} />}
            {vistaActual === 'estructura' && <OrgStructure setVistaActual={setVistaActual} />} 
            {vistaActual === 'org_integral' && <OrganigramaIntegral />}
            {vistaActual === 'compensaciones' && <Compensaciones data={empleados} />}
            {vistaActual === 'auditoria' && <EmployeeTable data={empleados} />}

            {/* Placeholder para los módulos en construcción */}
            {['fuga_talento', 'desempeno', 'turnos', 'reclutamiento'].includes(vistaActual) && (
              <div className="flex flex-col items-center justify-center p-20 text-gray-400 border-2 border-dashed border-gray-300 rounded-xl mt-10">
                <h3 className="text-2xl font-bold text-gray-500 mb-2">Módulo en Construcción 🚀</h3>
                <p>Pronto conectaremos los datos para esta sección.</p>
              </div>
            )}
          </div>
        )}
        </div>
      </main>
    </div>
  )
}

export default App
```

## 6. Variables de Entorno (.env)

Las llaves expuestas para el ecosistema backend/front-end en el estado nativo:

```env
# URL y Key publicable de Supabase usada por JS -> ./client/src/lib/supabaseClient.js
VITE_SUPABASE_URL=***
VITE_SUPABASE_ANON_KEY=***

# Llaves secretas para Service Roles y ETL Python Scripts -> /etl_pipeline/*.py
SUPABASE_SERVICE_KEY=***

# URL de Postgres para inyecciones SQLAlchemy usando DB-Pool
DATABASE_URL=***
```
