import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_raw_enhanced():
    print("🔨 Creando tablas RAW potenciadas (byNapo)...")
    engine = create_engine(db_url)
    
    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS raw;

    -- Tabla Principal: Snapshot Mensual
    CREATE TABLE IF NOT EXISTS raw.ibm_hr_monthly_snapshot_byNapo (
        snapshot_date TEXT,
        employee_id TEXT,
        employee_code TEXT,
        full_name TEXT,
        gender TEXT,
        nationality_iso3 TEXT,
        country_iso3 TEXT,
        department_name TEXT,
        job_role TEXT,
        job_level_1 TEXT,
        job_level_2 TEXT,
        employment_status TEXT,
        hire_date TEXT,
        termination_date TEXT,
        termination_reason_legal TEXT,
        turnover_classification_company TEXT,
        monthly_salary_local TEXT,
        currency_iso3 TEXT,
        fx_rate_to_usd TEXT,
        monthly_salary_usd TEXT,
        manager_employee_id TEXT,
        dotted_line_manager_id TEXT,
        work_center_id TEXT,
        home_lat TEXT,
        home_lon TEXT,
        work_modality TEXT,
        education_level TEXT,
        education_status TEXT,
        marital_status TEXT,
        dependents_count TEXT,
        salary_change_flag TEXT,
        salary_change_reason_code TEXT,
        job_change_flag TEXT,
        exit_interview_completed TEXT,
        regrettable_loss_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Tabla de Catálogo de Motivos
    CREATE TABLE IF NOT EXISTS raw.ibm_hr_change_reasons_byNapo (
        reason_code TEXT,
        reason_name_es TEXT,
        reason_name_en TEXT,
        affects_salary TEXT,
        affects_job TEXT,
        active_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    with engine.connect() as conn:
        conn.execute(text(sql_queries))
        conn.commit()
    print("✅ Tablas RAW potenciadas creadas correctamente.")

if __name__ == "__main__":
    setup_raw_enhanced()