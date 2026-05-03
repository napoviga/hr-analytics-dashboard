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
    print("🚀 [ETL M07] TIEMPO, ASISTENCIA & BIENESTAR")
    print("="*50)

    engine = create_engine(db_url)
    
    sql = """
    CREATE SCHEMA IF NOT EXISTS business;

    -- ═══ MV: Ausentismo ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_absenteeism CASCADE;
    CREATE MATERIALIZED VIEW business.mv_absenteeism AS
    SELECT DATE_TRUNC('month', a.work_date::DATE)::DATE as periodo,
        e.department_name, e.country_iso3,
        COUNT(*) as total_dias,
        COUNT(*) FILTER (WHERE a.absence_type != 'Present') as dias_ausencia,
        ROUND((100.0 * COUNT(*) FILTER (WHERE a.absence_type != 'Present') / NULLIF(COUNT(*),0))::NUMERIC, 1) as tasa_ausentismo,
        SUM(a.late_minutes::INT) as total_minutos_tarde
    FROM raw."attendance_records_byNapo" a
    JOIN business.v_employee_full_byNapo e ON a.employee_id = e.employee_id::TEXT AND DATE_TRUNC('month', e.snapshot_date::DATE) = DATE_TRUNC('month', a.work_date::DATE)
    GROUP BY 1, e.department_name, e.country_iso3;

    -- ═══ MV: Overtime Summary ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_overtime_summary CASCADE;
    CREATE MATERIALIZED VIEW business.mv_overtime_summary AS
    SELECT DATE_TRUNC('month', o.date_from::DATE)::DATE as periodo,
        e.department_name, e.country_iso3,
        SUM(o.hours_overtime::NUMERIC) as total_horas_extra,
        SUM(o.cost_usd::NUMERIC) as costo_total_extra,
        COUNT(DISTINCT o.employee_id) as empleados_con_extra
    FROM raw."overtime_logs_byNapo" o
    JOIN business.v_employee_full_byNapo e ON o.employee_id = e.employee_id::TEXT
    GROUP BY 1, e.department_name, e.country_iso3;

    -- ═══ MV: SST Incidents ═══
    DROP MATERIALIZED VIEW IF EXISTS business.mv_sst_incidents CASCADE;
    CREATE MATERIALIZED VIEW business.mv_sst_incidents AS
    SELECT DATE_TRUNC('month', i.incident_date::DATE)::DATE as periodo,
        i.severity, i.incident_type,
        COUNT(*) as total_incidentes,
        SUM(i.lost_days::INT) as dias_perdidos
    FROM raw."incidents_sst_byNapo" i
    GROUP BY 1, i.severity, i.incident_type;

    CREATE INDEX IF NOT EXISTS idx_mv_absent_per ON business.mv_absenteeism(periodo);
    CREATE INDEX IF NOT EXISTS idx_mv_ot_per ON business.mv_overtime_summary(periodo);
    CREATE INDEX IF NOT EXISTS idx_mv_sst_per ON business.mv_sst_incidents(periodo);
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    """

    with engine.begin() as conn:
        print("⏳ Creando MVs de Tiempo y Asistencia...")
        conn.execute(text(sql))
        conn.execute(text("NOTIFY pgrst, 'reload schema';"))
        
    elapsed = time.time() - start_time
    print(f"\n✅ ETL M07 completado exitosamente en {elapsed:.2f} segundos.")

if __name__ == "__main__":
    run()
