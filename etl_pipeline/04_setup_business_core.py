import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_core():
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 04] CONSTRUYENDO CAPA BUSINESS CORE")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- Limpieza
    DROP VIEW IF EXISTS business.v_employee_full_byNapo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_ui_global_filters CASCADE;
    
    -- 1. VISTA MAESTRA (Única base de verdad)
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        snapshot_date::DATE as snapshot_date, employee_id::INTEGER as employee_id,
        employee_code, full_name, gender, country_iso3, department_name, job_role,
        job_level_1, job_level_2, employment_status, hire_date::DATE as hire_date,
        termination_date::DATE as termination_date, monthly_salary_local::NUMERIC(12,2),
        currency_iso3, fx_rate_to_usd::NUMERIC(10,4), monthly_salary_usd::NUMERIC(12,2),
        work_center_id,
        NULLIF(manager_employee_id, '')::NUMERIC::INTEGER as manager_employee_id,
        CASE WHEN termination_date::DATE IS NOT NULL THEN 
            EXTRACT(YEAR FROM AGE(termination_date::DATE, hire_date::DATE)) * 12 + EXTRACT(MONTH FROM AGE(termination_date::DATE, hire_date::DATE))
        ELSE 
            EXTRACT(YEAR FROM AGE(snapshot_date::DATE, hire_date::DATE)) * 12 + EXTRACT(MONTH FROM AGE(snapshot_date::DATE, hire_date::DATE))
        END as tenure_months,
        CASE WHEN employment_status = 'Active' THEN TRUE WHEN termination_date::DATE IS NULL THEN TRUE WHEN termination_date::DATE >= snapshot_date::DATE THEN TRUE ELSE FALSE END as is_active_at_snapshot,
        NOW() as processed_at
    FROM raw."ibm_hr_monthly_snapshot_byNapo";

    -- 2. VISTA MATERIALIZADA DE METADATOS (¡Los 6 Filtros Universales!)
    -- Modificada para depender de v_employee_full_byNapo garantizando total independencia
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_ui_global_filters AS
    SELECT json_build_object(
        'periods', (SELECT COALESCE(json_agg(TO_CHAR(snapshot_date, 'YYYY-MM-DD')), '[]'::json) FROM (SELECT DISTINCT snapshot_date FROM business.v_employee_full_byNapo ORDER BY snapshot_date DESC) p),
        'countries', (SELECT COALESCE(json_agg(country_iso3), '[]'::json) FROM (SELECT DISTINCT country_iso3 FROM business.v_employee_full_byNapo WHERE country_iso3 IS NOT NULL ORDER BY country_iso3) c),
        'departments', (SELECT COALESCE(json_agg(department_name), '[]'::json) FROM (SELECT DISTINCT department_name FROM business.v_employee_full_byNapo WHERE department_name IS NOT NULL ORDER BY department_name) d),
        'job_levels_1', (SELECT COALESCE(json_agg(job_level_1), '[]'::json) FROM (SELECT DISTINCT job_level_1 FROM business.v_employee_full_byNapo WHERE job_level_1 IS NOT NULL ORDER BY job_level_1) jl1),
        'job_levels_2', (SELECT COALESCE(json_agg(job_level_2), '[]'::json) FROM (SELECT DISTINCT job_level_2 FROM business.v_employee_full_byNapo WHERE job_level_2 IS NOT NULL ORDER BY job_level_2) jl2),
        'work_centers', (SELECT COALESCE(json_agg(work_center_id), '[]'::json) FROM (SELECT DISTINCT work_center_id FROM business.v_employee_full_byNapo WHERE work_center_id IS NOT NULL ORDER BY work_center_id) wc)
    ) as filter_options;

    -- Permisos Base
    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_ui_global_filters;"))
            conn.commit()
            print("✅ Core Business (Vistas y Filtros) inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error en SQL Core: {e}")

if __name__ == "__main__":
    setup_business_core()
