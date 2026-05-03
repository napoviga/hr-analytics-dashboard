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
    print("🚀 [ETL M10] ENGAGEMENT & SENTIMIENTO")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: eNPS Trend ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_enps_trend CASCADE;
    CREATE MATERIALIZED VIEW business.mv_enps_trend AS
    SELECT DATE_TRUNC('quarter', s.survey_date::DATE)::DATE as periodo,
        e.department_name, e.country_iso3,
        COUNT(*) FILTER (WHERE s.score_normalized::NUMERIC >= 9) as promoters,
        COUNT(*) FILTER (WHERE s.score_normalized::NUMERIC <= 6) as detractors,
        COUNT(*) as total_responses,
        ROUND((100.0 * (COUNT(*) FILTER (WHERE s.score_normalized::NUMERIC >= 9) - COUNT(*) FILTER (WHERE s.score_normalized::NUMERIC <= 6)) / NULLIF(COUNT(*),0))::NUMERIC, 1) as enps_score
    FROM raw."survey_responses_byNapo" s
    JOIN business.v_employee_full_byNapo e ON s.employee_id = e.employee_id::TEXT AND e.is_active_at_snapshot = TRUE
    WHERE s.survey_type = 'eNPS'
    GROUP BY 1, e.department_name, e.country_iso3;

    -- ═══ MV: Sentiment Summary ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_sentiment_summary CASCADE;
    CREATE MATERIALIZED VIEW business.mv_sentiment_summary AS
    SELECT DATE_TRUNC('quarter', f.feedback_date::DATE)::DATE as periodo,
        f.sentiment_label,
        COUNT(*) as total_comments,
        ROUND((AVG(f.sentiment_score::NUMERIC))::NUMERIC, 2) as avg_sentiment
    FROM raw."feedback_comments_byNapo" f
    GROUP BY 1, f.sentiment_label;

    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Engagement...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M10 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
