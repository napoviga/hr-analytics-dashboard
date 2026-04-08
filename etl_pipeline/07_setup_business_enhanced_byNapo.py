import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_enhanced():
    """
    🏗️ Crea la capa Business (Oro) con vistas tipadas y analíticas.
    """
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 07] CONSTRUYENDO CAPA BUSINESS ENHANCED (byNapo)")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    print("⏳ Ejecutando sentencias SQL en Supabase...")
    engine = create_engine(db_url)

    # ==========================================
    # 📋 CONSULTAS SQL
    # ==========================================
    sql_queries = """
    -- 0. CLEAN SLATE (Reconstrucción total para idempotencia)
    DROP SCHEMA IF EXISTS business CASCADE;

    -- 1. Crear esquema
    CREATE SCHEMA business;

    -- 2. VISTA MAESTRA (Tipada y Enriquecida)
    -- Transforma TEXT crudos a tipos reales (DATE, INTEGER, NUMERIC, BOOLEAN)
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        -- Identificadores y Fechas
        snapshot_date::DATE as snapshot_date,
        employee_id::INTEGER as employee_id,
        employee_code,
        full_name,
        
        -- Demografía
        gender,
        country_iso3,
        
        -- Organización
        department_name,
        job_role,
        job_level_1,
        job_level_2,
        
        -- Estado Laboral
        employment_status,
        hire_date::DATE as hire_date,
        termination_date::DATE as termination_date,
        
        -- Compensación (Casting a NUMERIC y cálculo de USD si faltara)
        monthly_salary_local::NUMERIC(12,2) as monthly_salary_local,
        currency_iso3,
        fx_rate_to_usd::NUMERIC(10,4) as fx_rate_to_usd,
        monthly_salary_usd::NUMERIC(12,2) as monthly_salary_usd,
        
        -- Jerarquía
        NULLIF(manager_employee_id, '')::NUMERIC::INTEGER as manager_employee_id,
        
        -- Campos Calculados
        
        -- Antigüedad en meses
        CASE 
            WHEN termination_date::DATE IS NOT NULL THEN 
                EXTRACT(YEAR FROM AGE(termination_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(termination_date::DATE, hire_date::DATE))
            ELSE 
                EXTRACT(YEAR FROM AGE(snapshot_date::DATE, hire_date::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(snapshot_date::DATE, hire_date::DATE))
        END as tenure_months,
        
        -- Flag Activo (Lógica de corte)
        CASE 
            WHEN employment_status = 'Active' THEN TRUE
            WHEN termination_date::DATE IS NULL THEN TRUE
            WHEN termination_date::DATE >= snapshot_date::DATE THEN TRUE
            ELSE FALSE
        END as is_active_at_snapshot,
        
        NOW() as processed_at

    FROM raw."ibm_hr_monthly_snapshot_byNapo";

    -- 3. VISTA DE ORGANIGRAMA (Recursiva para ECharts)
    -- Construye la jerarquía para el mes más reciente
    CREATE OR REPLACE VIEW business.v_org_tree_byNapo AS
    WITH RECURSIVE org_hierarchy AS (
        -- Nivel Base: Empleados sin jefe o CEO
        SELECT 
            employee_id,
            full_name,
            job_role,
            job_level_1,
            department_name,
            manager_employee_id,
            0 as depth,
            ARRAY[employee_id] as path
        FROM business.v_employee_full_byNapo
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND is_active_at_snapshot = TRUE
          AND (manager_employee_id IS NULL OR manager_employee_id NOT IN (
              SELECT employee_id FROM business.v_employee_full_byNapo 
              WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          ))
        
        UNION ALL
        
        -- Recursión: Hijos
        SELECT 
            emp.employee_id,
            emp.full_name,
            emp.job_role,
            emp.job_level_1,
            emp.department_name,
            emp.manager_employee_id,
            oh.depth + 1,
            oh.path || emp.employee_id
        FROM business.v_employee_full_byNapo emp
        INNER JOIN org_hierarchy oh ON emp.manager_employee_id = oh.employee_id
        WHERE emp.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND emp.is_active_at_snapshot = TRUE
          AND NOT emp.employee_id = ANY(oh.path) -- Evitar ciclos
          AND oh.depth < 10 -- Límite de profundidad
    )
    SELECT 
        employee_id,
        full_name,
        job_role,
        job_level_1,
        depth,
        json_build_object(
            'id', employee_id,
            'name', full_name,
            'value', job_level_1,
            'children', NULL 
        ) as echarts_node
    FROM org_hierarchy
    ORDER BY depth, employee_id;

    -- 4. VISTA MATERIALIZADA DE KPIs (Alto Rendimiento)
    -- Pre-calcula métricas para tarjetas del dashboard
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_monthly_kpis_byNapo AS
    SELECT 
        snapshot_date,
        country_iso3,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3;

    -- Índice para acelerar filtros en la vista materializada
    CREATE UNIQUE INDEX IF NOT EXISTS idx_kpis_unique ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3);

    -- 5. PERMISOS
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.commit()
            print("✅ Vistas creadas exitosamente.")
            
        # Refrescar vista materializada
        with engine.connect() as conn:
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo;"))
            conn.commit()
            print("🔄 Vista materializada refrescada.")
            
    except Exception as e:
        print(f"❌ Error en SQL: {e}")
        return

    elapsed = time.time() - start_time
    print(f"\n🎉 [ETL 07] Completado en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    setup_business_enhanced()