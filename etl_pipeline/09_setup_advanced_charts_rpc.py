import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_advanced_rpc():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧠 [ETL 09] CREANDO MOTOR RPC PARA ECHARTS AVANZADOS")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    # =========================================================
    # PASO 1: Crear MVs pre-agregadas para cada chart
    # =========================================================
    mv_sql = """
    DROP MATERIALIZED VIEW IF EXISTS business.mv_diversity_pyramid CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_bajas_heatmap CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_country_dist CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS business.mv_experience_bubbles CASCADE;

    -- MV1: Pirámide de Diversidad
    CREATE MATERIALIZED VIEW business.mv_diversity_pyramid AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
           gender, COUNT(*) as value
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, gender;

    CREATE INDEX idx_mv_div_snap ON business.mv_diversity_pyramid (snapshot_date);

    -- MV2: Heatmap de Bajas por Dept/Mes
    CREATE MATERIALIZED VIEW business.mv_bajas_heatmap AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
           COUNT(*) as count
    FROM business.v_employee_full_byNapo
    WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id;

    CREATE INDEX idx_mv_bajas_snap ON business.mv_bajas_heatmap (snapshot_date);

    -- MV3: Distribución por País
    CREATE MATERIALIZED VIEW business.mv_country_dist AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
           COUNT(*) as value
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id;

    CREATE INDEX idx_mv_country_snap ON business.mv_country_dist (snapshot_date);

    -- MV4: Burbujas de Experiencia
    CREATE MATERIALIZED VIEW business.mv_experience_bubbles AS
    SELECT snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id,
           CASE 
               WHEN tenure_months < 12 THEN '< 1 año'
               WHEN tenure_months < 36 THEN '1-3 años'
               WHEN tenure_months < 72 THEN '3-6 años'
               ELSE '6+ años' 
           END as generation,
           (ROUND(tenure_months / 6.0) * 6)::INTEGER as tenure_bucket,
           ROUND(AVG(monthly_salary_usd)::NUMERIC, 0) as avg_salary,
           COUNT(*) as emp_count
    FROM business.v_employee_full_byNapo
    WHERE is_active_at_snapshot = TRUE AND tenure_months IS NOT NULL AND monthly_salary_usd IS NOT NULL
    GROUP BY snapshot_date, country_iso3, department_name, job_level_1, job_level_2, work_center_id, generation, tenure_bucket;

    CREATE INDEX idx_mv_exp_snap ON business.mv_experience_bubbles (snapshot_date);

    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    # =========================================================
    # PASO 2: Función RPC que consulta las MVs (ultra rápido)
    # =========================================================
    rpc_sql = """
    DROP FUNCTION IF EXISTS business.get_advanced_demographics(DATE, TEXT, TEXT, TEXT, TEXT, TEXT);

    CREATE OR REPLACE FUNCTION business.get_advanced_demographics(
        p_period_date DATE,
        p_country TEXT DEFAULT NULL,
        p_department TEXT DEFAULT NULL,
        p_job_level_1 TEXT DEFAULT NULL,
        p_job_level_2 TEXT DEFAULT NULL,
        p_work_center TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE
        result JSON;
    BEGIN
        SELECT json_build_object(
            -- 1. Pirámide de Diversidad
            'diversity_pyramid', (
                SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                    SELECT job_level_2 as level, gender, SUM(value) as value
                    FROM business.mv_diversity_pyramid
                    WHERE snapshot_date = p_period_date
                      AND (p_country IS NULL OR country_iso3 = p_country)
                      AND (p_department IS NULL OR department_name = p_department)
                      AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
                      AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
                      AND (p_work_center IS NULL OR work_center_id = p_work_center)
                    GROUP BY job_level_2, gender
                    ORDER BY job_level_2
                ) t
            ),

            -- 2. Heatmap de Bajas
            'turnover_heatmap', (
                SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                    SELECT department_name as dept,
                           TO_CHAR(snapshot_date, 'YYYY.MM') as month_label,
                           SUM(count) as count
                    FROM business.mv_bajas_heatmap
                    WHERE snapshot_date > (p_period_date - INTERVAL '12 months')
                      AND snapshot_date <= p_period_date
                      AND (p_country IS NULL OR country_iso3 = p_country)
                      AND (p_department IS NULL OR department_name = p_department)
                      AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
                      AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
                      AND (p_work_center IS NULL OR work_center_id = p_work_center)
                    GROUP BY department_name, snapshot_date
                    ORDER BY snapshot_date
                ) t
            ),

            -- 3. Distribución por País
            'country_distribution', (
                SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                    SELECT country_iso3 as name, SUM(value) as value
                    FROM business.mv_country_dist
                    WHERE snapshot_date = p_period_date
                      AND (p_country IS NULL OR country_iso3 = p_country)
                      AND (p_department IS NULL OR department_name = p_department)
                      AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
                      AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
                      AND (p_work_center IS NULL OR work_center_id = p_work_center)
                    GROUP BY country_iso3
                    ORDER BY value DESC
                ) t
            ),

            -- 4. Burbujas de Experiencia
            'experience_bubbles', (
                SELECT COALESCE(json_agg(t), '[]'::json) FROM (
                    SELECT generation,
                           tenure_bucket as tenure_months,
                           ROUND(SUM(avg_salary * emp_count) / NULLIF(SUM(emp_count), 0)) as salary,
                           SUM(emp_count) as count
                    FROM business.mv_experience_bubbles
                    WHERE snapshot_date = p_period_date
                      AND (p_country IS NULL OR country_iso3 = p_country)
                      AND (p_department IS NULL OR department_name = p_department)
                      AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
                      AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
                      AND (p_work_center IS NULL OR work_center_id = p_work_center)
                    GROUP BY generation, tenure_bucket
                    ORDER BY tenure_bucket
                ) t
            )
        ) INTO result;

        RETURN result;
    END;
    $$ LANGUAGE plpgsql;

    GRANT EXECUTE ON FUNCTION business.get_advanced_demographics(DATE, TEXT, TEXT, TEXT, TEXT, TEXT) TO anon;
    """

    try:
        with engine.connect() as conn:
            print("⏳ Creando MVs pre-agregadas (esto puede tardar ~30s)...")
            conn.execute(text(mv_sql))
            conn.commit()
            print("✅ MVs creadas y refrescadas.")

            print("⏳ Desplegando función RPC...")
            conn.execute(text(rpc_sql))
            conn.commit()

            # Forzar recarga del schema de PostgREST (Supabase)
            conn.execute(text("NOTIFY pgrst, 'reload schema'"))
            conn.commit()

            elapsed = time.time() - start_time
            print(f"✅ Motor RPC avanzado listo + schema recargado ({elapsed:.1f}s)")
    except Exception as e:
        print(f"❌ Error:\n{e}")

if __name__ == "__main__":
    setup_advanced_rpc()