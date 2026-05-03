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
    print("🚀 [ETL M11] COMPLIANCE & RELACIONES LABORALES")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Compliance Dashboard ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_compliance_dashboard CASCADE;
    CREATE MATERIALIZED VIEW business.mv_compliance_dashboard AS
    SELECT c.country_iso3, c.obligation_type, c.status, c.risk_level,
        COUNT(*) as total_obligations,
        COUNT(*) FILTER (WHERE c.status = 'Overdue') as overdue_count
    FROM raw."compliance_obligations_byNapo" c
    GROUP BY c.country_iso3, c.obligation_type, c.status, c.risk_level;

    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Compliance...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M11 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
