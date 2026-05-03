import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")
db_url = os.getenv("DATABASE_URL")

def run():
    start_time = time.time()
    print("\n" + "="*50)
    print("🚀 [ETL M06] NÓMINA, COSTOS & EQUIDAD")
    print("="*50)

    engine = create_engine(db_url)
    
    # 1. Crear mv_salary_bands
    sql_part1 = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV 1: Bandas Salariales ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_salary_bands CASCADE;
    CREATE MATERIALIZED VIEW business.mv_salary_bands AS
    SELECT 
        snapshot_date, department_name, job_level_1, job_level_2, job_role, country_iso3,
        PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_salary_usd) as p10,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_salary_usd) as p25,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_salary_usd) as p50_median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_salary_usd) as p75,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_salary_usd) as p90,
        AVG(monthly_salary_usd)::NUMERIC(12,2) as avg_salary,
        STDDEV(monthly_salary_usd)::NUMERIC(12,2) as stddev_salary,
        COUNT(*) as employee_count
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE AND monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, department_name, job_level_1, job_level_2, job_role, country_iso3;

    CREATE INDEX IF NOT EXISTS idx_mv_sal_bands_snap ON business.mv_salary_bands(snapshot_date);
    """

    # 2. Crear las demás MVs y RPC
    sql_part2 = """
    -- ═══ MV 2: Compa-Ratio ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_compa_ratio CASCADE;
    CREATE MATERIALIZED VIEW business.mv_compa_ratio AS
    SELECT 
        e.snapshot_date, e.employee_id, e.full_name, e.department_name, e.job_role,
        e.job_level_1, e.job_level_2, e.country_iso3,
        e.monthly_salary_usd,
        b.p50_median as band_median,
        ROUND(((e.monthly_salary_usd / NULLIF(b.p50_median, 0)) * 100)::NUMERIC, 1) as compa_ratio_pct,
        CASE 
            WHEN e.monthly_salary_usd / NULLIF(b.p50_median,0) < 0.8 THEN 'Below Range'
            WHEN e.monthly_salary_usd / NULLIF(b.p50_median,0) > 1.2 THEN 'Above Range'
            ELSE 'In Range'
        END as range_status
    FROM business.v_employee_full_byNapo e
    LEFT JOIN business.mv_salary_bands b 
        ON e.snapshot_date = b.snapshot_date
        AND e.department_name = b.department_name
        AND e.job_role = b.job_role
        AND e.country_iso3 = b.country_iso3
    WHERE e.is_active_at_snapshot = TRUE;

    CREATE INDEX IF NOT EXISTS idx_mv_compa_snap ON business.mv_compa_ratio(snapshot_date);

    -- ═══ MV 3: Masa Salarial ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_payroll_mass CASCADE;
    CREATE MATERIALIZED VIEW business.mv_payroll_mass AS
    SELECT 
        snapshot_date, department_name, country_iso3, job_level_1,
        SUM(monthly_salary_usd)::NUMERIC(14,2) as total_payroll_usd,
        COUNT(*) as headcount,
        AVG(monthly_salary_usd)::NUMERIC(12,2) as avg_salary_usd
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE AND monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, department_name, country_iso3, job_level_1;

    CREATE INDEX IF NOT EXISTS idx_mv_payroll_snap ON business.mv_payroll_mass(snapshot_date);

    -- ═══ MV 4: Impacto Financiero de Rotación ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_turnover_cost CASCADE;
    CREATE MATERIALIZED VIEW business.mv_turnover_cost AS
    SELECT 
        snapshot_date, department_name, country_iso3,
        COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as bajas_mes,
        SUM(monthly_salary_usd) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date)::NUMERIC(14,2) as costo_bajas_usd,
        SUM(monthly_salary_usd * 3) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date)::NUMERIC(14,2) as costo_reemplazo_estimado
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, department_name, country_iso3;

    CREATE INDEX IF NOT EXISTS idx_mv_turnover_cost_snap ON business.mv_turnover_cost(snapshot_date);

    -- ═══ Permisos MVs ═══
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;

    -- ═══ RPC: get_nomina_dashboard ═══
    CREATE OR REPLACE FUNCTION business.get_nomina_dashboard(
        p_period_date DATE, p_country TEXT DEFAULT NULL, p_department TEXT DEFAULT NULL
    ) RETURNS JSON LANGUAGE plpgsql SECURITY DEFINER AS $$
    DECLARE result JSON;
    BEGIN
        SELECT json_build_object(
            'salary_bands', (SELECT json_agg(row_to_json(t)) FROM (
                SELECT * FROM business.mv_salary_bands 
                WHERE snapshot_date = p_period_date
                AND (p_country IS NULL OR country_iso3 = p_country)
                AND (p_department IS NULL OR department_name = p_department)
            ) t),
            'payroll_summary', (SELECT json_agg(row_to_json(t)) FROM (
                SELECT * FROM business.mv_payroll_mass
                WHERE snapshot_date = p_period_date
                AND (p_country IS NULL OR country_iso3 = p_country)
                AND (p_department IS NULL OR department_name = p_department)
            ) t)
        ) INTO result;
        RETURN result;
    END; $$;

    GRANT EXECUTE ON FUNCTION business.get_nomina_dashboard(DATE, TEXT, TEXT) TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MV 1: Bandas Salariales...")
        conn.execute(text(sql_part1))
        
        # 🔥 REFRESH CRÍTICO INTERCALADO 🔥
        print("🔄 Refrescando mv_salary_bands (Requisito para Compa-Ratio)...")
        conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_salary_bands;"))
        
        print("⏳ Creando MVs 2, 3, 4 y Funciones RPC...")
        conn.execute(text(sql_part2))
        
        print("🔄 Refrescando resto de vistas materializadas...")
        conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_compa_ratio;"))
        conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_payroll_mass;"))
        conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_turnover_cost;"))
        
        print("📡 Notificando a PostgREST para recargar schema...")
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M06 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run()
