import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_rpc():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧠 [ETL 08] REPARANDO MOTOR RPC - SNAPSHOT CARDS")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    engine = create_engine(db_url)

    sql_query = """
    -- 1. Limpieza de funciones antiguas
    DROP FUNCTION IF EXISTS business.get_demographics_dashboard(DATE, TEXT, TEXT);
    DROP FUNCTION IF EXISTS business.get_demographics_dashboard(DATE, TEXT, TEXT, TEXT, TEXT, TEXT);

    -- 2. Crear índice para acelerar los filtros si no existe
    CREATE INDEX IF NOT EXISTS idx_emp_snapshot_filters 
        ON raw."ibm_hr_monthly_snapshot_byNapo" (snapshot_date, country_iso3, department_name);

    -- 3. Función RPC optimizada con 12 meses + YoY
    CREATE OR REPLACE FUNCTION business.get_demographics_dashboard(
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
        -- ========================================
        -- TODAS las queries usan la MV pre-agregada (ultra rápido)
        -- ========================================
        WITH historical_trend AS (
            SELECT 
                snapshot_date,
                TO_CHAR(snapshot_date, 'YYYY.MM') as month_lbl,
                SUM(total_hc) as total_hc,
                SUM(altas) as altas,
                SUM(bajas) as bajas
            FROM business.mv_demographics_agg
            WHERE snapshot_date BETWEEN (p_period_date - INTERVAL '11 months') AND p_period_date
              AND (p_country IS NULL OR country_iso3 = p_country)
              AND (p_department IS NULL OR department_name = p_department)
              AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
              AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
              AND (p_work_center IS NULL OR work_center_id = p_work_center)
            GROUP BY snapshot_date
            ORDER BY snapshot_date
        ),
        yoy_point AS (
            SELECT SUM(total_hc) as total_hc, SUM(altas) as altas, SUM(bajas) as bajas
            FROM business.mv_demographics_agg
            WHERE snapshot_date = (p_period_date - INTERVAL '1 year')::DATE
              AND (p_country IS NULL OR country_iso3 = p_country)
              AND (p_department IS NULL OR department_name = p_department)
              AND (p_job_level_1 IS NULL OR job_level_1 = p_job_level_1)
              AND (p_job_level_2 IS NULL OR job_level_2 = p_job_level_2)
              AND (p_work_center IS NULL OR work_center_id = p_work_center)
        ),
        card_fl AS (
            SELECT 
                COALESCE((SELECT total_hc FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr,
                COALESCE((SELECT total_hc FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev,
                COALESCE((SELECT total_hc FROM yoy_point), 0) as val_yoy
        ),
        card_altas AS (
            SELECT
                COALESCE((SELECT altas FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr,
                COALESCE((SELECT altas FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev,
                COALESCE((SELECT altas FROM yoy_point), 0) as val_yoy
        ),
        card_bajas AS (
            SELECT
                COALESCE((SELECT bajas FROM historical_trend WHERE snapshot_date = p_period_date), 0) as val_curr,
                COALESCE((SELECT bajas FROM historical_trend WHERE snapshot_date = (p_period_date - INTERVAL '1 month')::DATE), 0) as val_prev,
                COALESCE((SELECT bajas FROM yoy_point), 0) as val_yoy
        )

        SELECT json_build_object(
            'total_activos_card', (
                SELECT json_build_object(
                    'title', 'FUERZA LABORAL',
                    'current_month', TO_CHAR(p_period_date, 'YYYY.MM'),
                    'current_value', val_curr,
                    'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'),
                    'previous_value', val_prev,
                    'diff_abs', val_curr - val_prev,
                    'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END,
                    'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'),
                    'yoy_value', val_yoy,
                    'yoy_diff_abs', val_curr - val_yoy,
                    'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END,
                    'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', total_hc)), '[]'::json) FROM historical_trend)
                ) FROM card_fl
            ),
            'altas_card', (
                SELECT json_build_object(
                    'title', 'ALTAS DEL MES',
                    'current_month', TO_CHAR(p_period_date, 'YYYY.MM'),
                    'current_value', val_curr,
                    'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'),
                    'previous_value', val_prev,
                    'diff_abs', val_curr - val_prev,
                    'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END,
                    'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'),
                    'yoy_value', val_yoy,
                    'yoy_diff_abs', val_curr - val_yoy,
                    'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END,
                    'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', altas)), '[]'::json) FROM (SELECT * FROM historical_trend WHERE snapshot_date >= (p_period_date - INTERVAL '5 months')) sub)
                ) FROM card_altas
            ),
            'bajas_card', (
                SELECT json_build_object(
                    'title', 'BAJAS DEL MES',
                    'current_month', TO_CHAR(p_period_date, 'YYYY.MM'),
                    'current_value', val_curr,
                    'previous_month', TO_CHAR(p_period_date - INTERVAL '1 month', 'YYYY.MM'),
                    'previous_value', val_prev,
                    'diff_abs', val_curr - val_prev,
                    'diff_pct', CASE WHEN val_prev > 0 THEN ROUND(((val_curr::NUMERIC - val_prev::NUMERIC) / val_prev::NUMERIC) * 100, 1) ELSE 0 END,
                    'yoy_month', TO_CHAR(p_period_date - INTERVAL '1 year', 'YYYY.MM'),
                    'yoy_value', val_yoy,
                    'yoy_diff_abs', val_curr - val_yoy,
                    'yoy_diff_pct', CASE WHEN val_yoy > 0 THEN ROUND(((val_curr::NUMERIC - val_yoy::NUMERIC) / val_yoy::NUMERIC) * 100, 1) ELSE 0 END,
                    'sparkline_data', (SELECT COALESCE(json_agg(json_build_object('label', month_lbl, 'value', bajas)), '[]'::json) FROM (SELECT * FROM historical_trend WHERE snapshot_date >= (p_period_date - INTERVAL '5 months')) sub)
                ) FROM card_bajas
            )
        ) INTO result;

        RETURN result;
    END;
    $$ LANGUAGE plpgsql;

    GRANT EXECUTE ON FUNCTION business.get_demographics_dashboard(DATE, TEXT, TEXT, TEXT, TEXT, TEXT) TO anon;
    """

    try:
        with engine.begin() as conn:
            conn.execute(text(sql_query))
            print("✅ Motor RPC actualizado y conflicto de sobrecarga resuelto.")
    except Exception as e:
        print(f"❌ Error reconstruyendo el motor RPC:\n{e}")

if __name__ == "__main__":
    setup_rpc()