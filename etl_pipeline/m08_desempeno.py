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
    print("🚀 [ETL M08] GESTIÓN DEL DESEMPEÑO")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Performance Summary ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_performance_summary CASCADE;
    CREATE MATERIALIZED VIEW business.mv_performance_summary AS
    SELECT r.review_period as review_cycle, e.department_name, e.country_iso3,
        COUNT(*) as total_reviews,
        ROUND((AVG(r.overall_score::NUMERIC))::NUMERIC, 1) as avg_rating,
        COUNT(*) FILTER (WHERE r.overall_score::NUMERIC >= 4) as high_performers,
        COUNT(*) FILTER (WHERE r.overall_score::NUMERIC < 2.5) as low_performers
    FROM raw."performance_reviews_byNapo" r
    JOIN business.v_employee_full_byNapo e ON r.employee_id = e.employee_id::TEXT AND e.is_active_at_snapshot = TRUE
    GROUP BY r.review_period, e.department_name, e.country_iso3;

    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Desempeño...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M08 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
