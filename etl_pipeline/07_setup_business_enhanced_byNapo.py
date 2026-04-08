import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_enhanced():
    start_time = time.time()
    print("\n" + "="*50)
    print("🏢 [ETL 07] CONSTRUYENDO CAPA BUSINESS ENHANCED (byNapo)")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS business;

    DROP VIEW IF EXISTS business.v_employee_full_byNapo CASCADE;
    DROP VIEW IF EXISTS business.v_org_tree_byNapo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_monthly_kpis_byNapo CASCADE;
    DROP VIEW IF EXISTS business.v_kpi_summary_byNapo CASCADE;
    DROP VIEW IF EXISTS business.v_compensation_analysis_byNapo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_ui_global_filters CASCADE;
    
    -- 1. VISTA MAESTRA
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        snapshot_date::DATE as snapshot_date, employee_id::INTEGER as employee_id,
        employee_code, full_name, gender, country_iso3, department_name, job_role,
        job_level_1, job_level_2, employment_status, hire_date::DATE as hire_date,
        termination_date::DATE as termination_date, monthly_salary_local::NUMERIC(12,2),
        currency_iso3, fx_rate_to_usd::NUMERIC(10,4), monthly_salary_usd::NUMERIC(12,2),
        NULLIF(manager_employee_id, '')::NUMERIC::INTEGER as manager_employee_id,
        CASE WHEN termination_date::DATE IS NOT NULL THEN 
            EXTRACT(YEAR FROM AGE(termination_date::DATE, hire_date::DATE)) * 12 + EXTRACT(MONTH FROM AGE(termination_date::DATE, hire_date::DATE))
        ELSE 
            EXTRACT(YEAR FROM AGE(snapshot_date::DATE, hire_date::DATE)) * 12 + EXTRACT(MONTH FROM AGE(snapshot_date::DATE, hire_date::DATE))
        END as tenure_months,
        CASE WHEN employment_status = 'Active' THEN TRUE WHEN termination_date::DATE IS NULL THEN TRUE WHEN termination_date::DATE >= snapshot_date::DATE THEN TRUE ELSE FALSE END as is_active_at_snapshot,
        NOW() as processed_at
    FROM raw."ibm_hr_monthly_snapshot_byNapo";

    -- 2. VISTA DE ORGANIGRAMA (Con parche de seguridad para encontrar la Raíz)
    CREATE OR REPLACE VIEW business.v_org_tree_byNapo AS
    WITH RECURSIVE org_hierarchy AS (
        SELECT employee_id, full_name, job_role, job_level_1, department_name, manager_employee_id, 0 as depth, ARRAY[employee_id] as path
        FROM business.v_employee_full_byNapo
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo) AND is_active_at_snapshot = TRUE
          AND (manager_employee_id IS NULL OR manager_employee_id = employee_id OR manager_employee_id NOT IN (
              SELECT employee_id FROM business.v_employee_full_byNapo WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo) AND is_active_at_snapshot = TRUE
          ))
        UNION ALL
        SELECT emp.employee_id, emp.full_name, emp.job_role, emp.job_level_1, emp.department_name, emp.manager_employee_id, oh.depth + 1, oh.path || emp.employee_id
        FROM business.v_employee_full_byNapo emp
        INNER JOIN org_hierarchy oh ON emp.manager_employee_id = oh.employee_id
        WHERE emp.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo) AND emp.is_active_at_snapshot = TRUE
          AND NOT emp.employee_id = ANY(oh.path) AND oh.depth < 10
    )
    SELECT employee_id, full_name, job_role, job_level_1, depth,
        json_build_object('id', employee_id, 'name', full_name, 'value', job_level_1, 'children', NULL) as echarts_node
    FROM org_hierarchy ORDER BY depth, employee_id;

    -- 3. VISTA MATERIALIZADA DE KPIs
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_monthly_kpis_byNapo AS
    SELECT snapshot_date, country_iso3,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure
    FROM business.v_employee_full_byNapo GROUP BY snapshot_date, country_iso3;
    CREATE UNIQUE INDEX IF NOT EXISTS idx_kpis_unique ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3);

    -- 4. VISTA MATERIALIZADA DE METADATOS (Filtros Globales UI)
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_ui_global_filters AS
    SELECT json_build_object(
        'periods', (SELECT COALESCE(json_agg(TO_CHAR(snapshot_date, 'YYYY-MM-DD')), '[]'::json) FROM (SELECT DISTINCT snapshot_date FROM business.mv_monthly_kpis_byNapo ORDER BY snapshot_date DESC) p),
        'countries', (SELECT COALESCE(json_agg(country_iso3), '[]'::json) FROM (SELECT DISTINCT country_iso3 FROM business.mv_monthly_kpis_byNapo WHERE country_iso3 IS NOT NULL ORDER BY country_iso3) c),
        'departments', (SELECT COALESCE(json_agg(department_name), '[]'::json) FROM (SELECT DISTINCT department_name FROM business.v_employee_full_byNapo WHERE department_name IS NOT NULL ORDER BY department_name) d)
    ) as filter_options;

    GRANT USAGE ON SCHEMA business TO anon;
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_ui_global_filters;"))
            conn.commit()
            print("✅ Vistas creadas y refrescadas exitosamente.")
    except Exception as e:
        print(f"❌ Error en SQL: {e}")

if __name__ == "__main__":
    setup_business_enhanced()