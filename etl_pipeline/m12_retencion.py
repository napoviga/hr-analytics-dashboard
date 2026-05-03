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
    print("🚀 [ETL M12] RETENCIÓN & RIESGO DE FUGA")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Turnover Analysis ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_turnover_analysis CASCADE;
    CREATE MATERIALIZED VIEW business.mv_turnover_analysis AS
    SELECT snapshot_date, department_name, country_iso3, job_level_1,
        COUNT(*) FILTER (WHERE is_active_at_snapshot) as activos,
        COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date) as bajas,
        ROUND((100.0 * COUNT(*) FILTER (WHERE termination_date BETWEEN DATE_TRUNC('month', snapshot_date) AND snapshot_date)
            / NULLIF(COUNT(*) FILTER (WHERE is_active_at_snapshot), 0))::NUMERIC, 2) as tasa_rotacion_mensual
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date, department_name, country_iso3, job_level_1;

    -- ═══ MV: Manager Turnover ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_manager_turnover CASCADE;
    CREATE MATERIALIZED VIEW business.mv_manager_turnover AS
    SELECT e.snapshot_date, e.manager_employee_id,
        m.full_name as manager_name, m.department_name,
        COUNT(*) FILTER (WHERE NOT e.is_active_at_snapshot) as subordinates_lost,
        COUNT(*) as total_subordinates,
        ROUND((100.0 * COUNT(*) FILTER (WHERE NOT e.is_active_at_snapshot) / NULLIF(COUNT(*),0))::NUMERIC, 1) as manager_turnover_rate
    FROM business.v_employee_full_byNapo e
    LEFT JOIN business.v_employee_full_byNapo m 
        ON e.manager_employee_id = m.employee_id AND e.snapshot_date = m.snapshot_date
    WHERE e.manager_employee_id IS NOT NULL
    GROUP BY e.snapshot_date, e.manager_employee_id, m.full_name, m.department_name;

    CREATE INDEX IF NOT EXISTS idx_mv_turnover_snap ON business.mv_turnover_analysis(snapshot_date);
    CREATE INDEX IF NOT EXISTS idx_mv_mgr_turn_snap ON business.mv_manager_turnover(snapshot_date);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Retención...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M12 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
