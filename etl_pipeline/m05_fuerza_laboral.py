import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Resolver ruta absoluta al .env
ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)
db_url = os.getenv("DATABASE_URL")

def setup_fuerza_laboral():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧠 [ETL M05] CONFIGURANDO DOMINIO: FUERZA LABORAL")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_views = """
    -- ==========================================
    -- 1. VISTAS Y M-VIEWS DE DEMOGRAFÍA
    -- ==========================================
    DROP VIEW IF EXISTS business.v_org_tree_byNapo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_monthly_kpis_byNapo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_demographics_agg CASCADE;
    
    DROP MATERIALIZED VIEW IF EXISTS business.mv_diversity_pyramid CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_bajas_heatmap CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_country_dist CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_experience_bubbles CASCADE;

    -- VISTA DE ORGANIGRAMA
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

    -- MV KPIs MENSULAES
    CREATE MATERIALIZED VIEW business.mv_monthly_kpis_byNapo AS
    SELECT snapshot_date, country_iso3,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure
    FROM business.v_employee_full_byNapo GROUP BY snapshot_date, country_iso3;
    CREATE UNIQUE INDEX idx_kpis_unique_m05 ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3);

    -- MV DEMOGRAFÍA AGREGADA (Cards)
    CREATE MATERIALIZED VIEW business.mv_demographics_agg AS
    SELECT 
        snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
        COUNT(*) as total_hc,
        COUNT(*) FILTER (WHERE hire_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as altas,
        COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as bajas
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id;
    CREATE INDEX idx_demo_agg_snap_m05 ON business.mv_demographics_agg (snapshot_date);
    CREATE INDEX idx_demo_agg_filt_m05 ON business.mv_demographics_agg (snapshot_date, country_iso3, department_name);

    -- MV Pirámide Diversidad
    CREATE MATERIALIZED VIEW business.mv_diversity_pyramid AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, gender, COUNT(*) as value
    FROM business.v_employee_full_byNapo WHERE is_active_at_snapshot = TRUE
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, gender;
    CREATE INDEX idx_mv_div_snap_m05 ON business.mv_diversity_pyramid (snapshot_date);

    -- MV Heatmap Bajas
    CREATE MATERIALIZED VIEW business.mv_bajas_heatmap AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, COUNT(*) as count
    FROM business.v_employee_full_byNapo WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id;
    CREATE INDEX idx_mv_bajas_snap_m05 ON business.mv_bajas_heatmap (snapshot_date);

    -- MV País
    CREATE MATERIALIZED VIEW business.mv_country_dist AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, COUNT(*) as value
    FROM business.v_employee_full_byNapo WHERE is_active_at_snapshot = TRUE
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id;
    CREATE INDEX idx_mv_country_snap_m05 ON business.mv_country_dist (snapshot_date);

    -- MV Experiencia
    CREATE MATERIALIZED VIEW business.mv_experience_bubbles AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
           CASE WHEN tenure_months < 12 THEN '< 1 año' WHEN tenure_months < 36 THEN '1-3 años' WHEN tenure_months < 72 THEN '3-6 años' ELSE '6+ años' END as generation,
           (ROUND(tenure_months / 6.0) * 6)::INTEGER as tenure_bucket,
           ROUND(AVG(monthly_salary_usd)::NUMERIC, 0) as avg_salary,
           COUNT(*) as emp_count
    FROM business.v_employee_full_byNapo WHERE is_active_at_snapshot = TRUE AND tenure_months IS NOT NULL AND monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, generation, tenure_bucket;
    CREATE INDEX idx_mv_exp_snap_m05 ON business.mv_experience_bubbles (snapshot_date);

    -- Permisos
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    sql_rpcs = """
    -- ==========================================
    -- 2. FUNCIONES RPC (Para Supabase PostgREST)
    -- ==========================================
    DROP FUNCTION IF EXISTS business.get_demographics_dashboard(DATE, TEXT, TEXT, TEXT, TEXT, TEXT);
    DROP FUNCTION IF EXISTS business.get_advanced_demographics(DATE, TEXT, TEXT, TEXT, TEXT, TEXT);

    CREATE OR REPLACE FUNCTION business.get_demographics_dashboard(
        p_period_date DATE, p_country TEXT DEFAULT NULL, p_department TEXT DEFAULT NULL,
        p_job_level_1 TEXT DEFAULT NULL, p_job_level_2 TEXT DEFAULT NULL, p_work_center TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        WITH historical_trend AS (
            SELECT snapshot_date, TO_CHAR(snapshot_date, 'YYYY.MM') as month_lbl, SUM(total_hc) as total_hc, SUM(altas) as altas, SUM(bajas) as bajas
            FROM business.mv_demographics_agg
            WHERE snapshot_date BETWEEN (p_period_date - INTERVAL '11 months') AND p_period_date
              AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department)
              AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
              AND (p_work_center IS NULL OR work_center_id = p_work_center)
            GROUP BY snapshot_date ORDER BY snapshot_date
        ),
        yoy_point AS (
            SELECT SUM(total_hc) as total_hc, SUM(altas) as altas, SUM(bajas) as bajas
            FROM business.mv_demographics_agg
            WHERE snapshot_date = (p_period_date - INTERVAL '1 year')::DATE
              AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department)
              AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
              AND (p_work_center IS NULL OR work_center_id = p_work_center)
        ),
        card_fl AS ( SELECT COALESCE((SELECT total_hc FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr, COALESCE((SELECT total_hc FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev, COALESCE((SELECT total_hc FROM yoy_point), 0) as val_yoy ),
        card_altas AS ( SELECT COALESCE((SELECT altas FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr, COALESCE((SELECT altas FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev, COALESCE((SELECT altas FROM yoy_point), 0) as val_yoy ),
        card_bajas AS ( SELECT COALESCE((SELECT bajas FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr, COALESCE((SELECT bajas FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev, COALESCE((SELECT bajas FROM yoy_point), 0) as val_yoy )

        SELECT json_build_object(
            'total_activos_card', (SELECT json_build_object('title', 'FUERZA LABORAL', 'current_month', TO_CHAR(p_period_date, 'YYYY.MM'), 'current_value', val_curr, 'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'), 'previous_value', val_prev, 'diff_abs', val_curr - val_prev, 'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END, 'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'), 'yoy_value', val_yoy, 'yoy_diff_abs', val_curr - val_yoy, 'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END, 'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', total_hc)), '[]'::json) FROM historical_trend)) FROM card_fl),
            'altas_card', (SELECT json_build_object('title', 'ALTAS DEL MES', 'current_month', TO_CHAR(p_period_date, 'YYYY.MM'), 'current_value', val_curr, 'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'), 'previous_value', val_prev, 'diff_abs', val_curr - val_prev, 'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END, 'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'), 'yoy_value', val_yoy, 'yoy_diff_abs', val_curr - val_yoy, 'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END, 'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', altas)), '[]'::json) FROM (SELECT * FROM historical_trend WHERE snapshot_date >= (p_period_date - INTERVAL '5 months')) sub)) FROM card_altas),
            'bajas_card', (SELECT json_build_object('title', 'BAJAS DEL MES', 'current_month', TO_CHAR(p_period_date, 'YYYY.MM'), 'current_value', val_curr, 'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'), 'previous_value', val_prev, 'diff_abs', val_curr - val_prev, 'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END, 'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'), 'yoy_value', val_yoy, 'yoy_diff_abs', val_curr - val_yoy, 'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END, 'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', bajas)), '[]'::json) FROM (SELECT * FROM historical_trend WHERE snapshot_date >= (p_period_date - INTERVAL '5 months')) sub)) FROM card_bajas)
        ) INTO result;
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION business.get_advanced_demographics(
        p_period_date DATE, p_country TEXT DEFAULT NULL, p_department TEXT DEFAULT NULL,
        p_job_level_1 TEXT DEFAULT NULL, p_job_level_2 TEXT DEFAULT NULL, p_work_center TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'diversity_pyramid', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (SELECT job_level_2 as level, gender, SUM(value) as value FROM business.mv_diversity_pyramid WHERE snapshot_date = p_period_date AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department) AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2) AND (p_work_center IS NULL OR work_center_id = p_work_center) GROUP BY job_level_2, gender ORDER BY job_level_2) t),
            'turnover_heatmap', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (SELECT department_name as dept, TO_CHAR(snapshot_date, 'YYYY.MM') as month_label, SUM(count) as count FROM business.mv_bajas_heatmap WHERE snapshot_date > (p_period_date - INTERVAL '12 months') AND snapshot_date <= p_period_date AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department) AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2) AND (p_work_center IS NULL OR work_center_id = p_work_center) GROUP BY department_name, snapshot_date ORDER BY snapshot_date) t),
            'country_distribution', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (SELECT country_iso3 as name, SUM(value) as value FROM business.mv_country_dist WHERE snapshot_date = p_period_date AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department) AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2) AND (p_work_center IS NULL OR work_center_id = p_work_center) GROUP BY country_iso3 ORDER BY value DESC) t),
            'experience_bubbles', (SELECT COALESCE(json_agg(t), '[]'::json) FROM (SELECT generation, tenure_bucket as tenure_months, ROUND(SUM(avg_salary * emp_count) / NULLIF(SUM(emp_count), 0)) as salary, SUM(emp_count) as count FROM business.mv_experience_bubbles WHERE snapshot_date = p_period_date AND (p_country IS NULL OR country_iso3 = p_country) AND (p_department IS NULL OR department_name = p_department) AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1) AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2) AND (p_work_center IS NULL OR work_center_id = p_work_center) GROUP BY generation, tenure_bucket ORDER BY tenure_bucket) t)
        ) INTO result;
        RETURN result;
    END;
    $$ LANGUAGE plpgsql;

    GRANT EXECUTE ON FUNCTION business.get_demographics_dashboard(DATE, TEXT, TEXT, TEXT, TEXT, TEXT) TO anon;
    GRANT EXECUTE ON FUNCTION business.get_advanced_demographics(DATE, TEXT, TEXT, TEXT, TEXT, TEXT) TO anon;
    """

    try:
        with engine.begin() as conn:
            print("⏳ Creando Vistas y MVs Demográficas (M05)...")
            conn.execute(text(sql_views))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_demographics_agg;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_diversity_pyramid;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_bajas_heatmap;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_country_dist;"))
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_experience_bubbles;"))
            
            print("⏳ Creando Motor RPC Demográfico...")
            conn.execute(text(sql_rpcs))
            
            conn.execute(text("NOTIFY pgrst, 'reload schema'"))
            
            elapsed = time.time() - start_time
            print(f"✅ Módulo M05 (Fuerza Laboral) Refrescado Exitosamente ({elapsed:.1f}s)")
    except Exception as e:
        print(f"❌ Error en Módulo M05:\n{e}")

if __name__ == "__main__":
    setup_fuerza_laboral()
