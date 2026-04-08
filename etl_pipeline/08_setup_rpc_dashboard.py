import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_rpc():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧠 [ETL 08] CREANDO MOTOR RPC PARA DASHBOARD")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return

    print("⏳ Inyectando función get_demographics_dashboard en Supabase...")
    engine = create_engine(db_url)

    # El código SQL de la Función RPC
    sql_query = """
    -- 1. Crear la función RPC
    CREATE OR REPLACE FUNCTION business.get_demographics_dashboard(
        p_period_date DATE,
        p_country TEXT DEFAULT NULL,
        p_department TEXT DEFAULT NULL
    ) RETURNS JSON AS $$
    DECLARE
        result JSON;
    BEGIN
        -- CTE 1: Fotografía estática del mes seleccionado
        WITH current_snapshot AS (
            SELECT * FROM business.v_employee_full_byNapo
            WHERE snapshot_date = p_period_date
              AND is_active_at_snapshot = TRUE
              AND (p_country IS NULL OR country_iso3 = p_country)
              AND (p_department IS NULL OR department_name = p_department)
        ),
        -- CTE 2: Evolución histórica (12 meses hacia atrás desde el mes seleccionado)
        historical_trend AS (
            SELECT 
                TO_CHAR(snapshot_date, 'YYYY-MM') as month_lbl,
                COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as active_hc,
                COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as terminated_hc
            FROM business.v_employee_full_byNapo
            WHERE snapshot_date BETWEEN (p_period_date - INTERVAL '11 months') AND p_period_date
              AND (p_country IS NULL OR country_iso3 = p_country)
              AND (p_department IS NULL OR department_name = p_department)
            GROUP BY snapshot_date
            ORDER BY snapshot_date
        )
        -- Ensamblar el JSON maestro
        SELECT json_build_object(
            'kpis', (
                SELECT json_build_object(
                    'total_active', COUNT(*),
                    'avg_salary_usd', ROUND(AVG(monthly_salary_usd), 2),
                    'avg_tenure_months', ROUND(AVG(tenure_months), 1)
                ) FROM current_snapshot
            ),
            'gender_dist', (
                SELECT COALESCE(json_agg(row_to_json(t)), '[]'::json) 
                FROM (SELECT gender as name, COUNT(*) as value FROM current_snapshot GROUP BY gender) t
            ),
            'level_dist', (
                SELECT COALESCE(json_agg(row_to_json(t)), '[]'::json) 
                FROM (SELECT job_level_1 as name, COUNT(*) as value FROM current_snapshot GROUP BY job_level_1) t
            ),
            'trend_12m', (
                SELECT COALESCE(json_agg(row_to_json(t)), '[]'::json) 
                FROM historical_trend t
            )
        ) INTO result;

        RETURN result;
    END;
    $$ LANGUAGE plpgsql;

    -- 2. Dar permisos al frontend (Vite/React) para ejecutar esta función
    GRANT EXECUTE ON FUNCTION business.get_demographics_dashboard(DATE, TEXT, TEXT) TO anon;
    """

    try:
        # Usamos un bloque transaccional
        with engine.begin() as conn:
            conn.execute(text(sql_query))
            print("✅ Función RPC creada y permisos otorgados exitosamente.")
    except Exception as e:
        print(f"❌ Error creando la función RPC:\n{e}")

if __name__ == "__main__":
    setup_rpc()