import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Resolver ruta absoluta al .env
ETL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ETL_DIR.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)
db_url = os.getenv("DATABASE_URL")

def setup_raw_enhanced():
    start_time = time.time()
    print("\n" + "="*50)
    print("🛠️  [ETL 02] CONSTRUYENDO CAPA RAW (byNapo)")
    print("="*50)

    print("⏳ Ejecutando DDL sobre esquema [raw]...")
    engine = create_engine(db_url)
    
    sql_queries = """
    CREATE SCHEMA IF NOT EXISTS raw;

    -- Limpiar versiones anteriores (ambas variantes de casing por seguridad)
    DROP TABLE IF EXISTS raw."ibm_hr_monthly_snapshot_byNapo" CASCADE;
    DROP TABLE IF EXISTS raw."ibm_hr_monthly_snapshot_bynapo" CASCADE;

    -- Tabla Principal: Snapshot Mensual (nombre citado para preservar case)
    CREATE TABLE raw."ibm_hr_monthly_snapshot_byNapo" (
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
    DROP TABLE IF EXISTS raw."ibm_hr_change_reasons_byNapo" CASCADE;
    DROP TABLE IF EXISTS raw."ibm_hr_change_reasons_bynapo" CASCADE;
    CREATE TABLE raw."ibm_hr_change_reasons_byNapo" (
        reason_code TEXT,
        reason_name_es TEXT,
        reason_name_en TEXT,
        affects_salary TEXT,
        affects_job TEXT,
        active_flag TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Phase 3 Tables
    DROP TABLE IF EXISTS raw."job_postings_byNapo" CASCADE;
    CREATE TABLE raw."job_postings_byNapo" (
        posting_id TEXT, job_title TEXT, department_name TEXT, country_iso3 TEXT,
        job_level_1 TEXT, job_level_2 TEXT, salary_range_min TEXT, salary_range_max TEXT,
        posting_date TEXT, closing_date TEXT, status TEXT, positions_available TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    DROP TABLE IF EXISTS raw."recruitment_pipeline_byNapo" CASCADE;
    CREATE TABLE raw."recruitment_pipeline_byNapo" (
        candidate_id TEXT, posting_id TEXT, full_name TEXT, gender TEXT, age TEXT,
        education_level TEXT, years_experience TEXT, application_date TEXT, stage TEXT,
        stage_change_date TEXT, interview_score TEXT, rejection_reason TEXT,
        hired_employee_id TEXT, nps_score TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    DROP TABLE IF EXISTS raw."onboarding_checklist_byNapo" CASCADE;
    CREATE TABLE raw."onboarding_checklist_byNapo" (
        onboarding_id TEXT, employee_id TEXT, checklist_item TEXT, category TEXT,
        due_date TEXT, completion_date TEXT, status TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    DROP TABLE IF EXISTS raw."productivity_milestones_byNapo" CASCADE;
    CREATE TABLE raw."productivity_milestones_byNapo" (
        milestone_id TEXT, employee_id TEXT, milestone_name TEXT, expected_days TEXT,
        actual_days TEXT, achievement_date TEXT, performance_rating TEXT, manager_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Phase 4 M07
    DROP TABLE IF EXISTS raw."attendance_records_byNapo" CASCADE;
    CREATE TABLE raw."attendance_records_byNapo" (
        record_id TEXT, employee_id TEXT, work_date TEXT,
        check_in_time TEXT, check_out_time TEXT, scheduled_hours TEXT,
        worked_hours TEXT, absence_type TEXT, late_minutes TEXT, work_modality TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."overtime_logs_byNapo" CASCADE;
    CREATE TABLE raw."overtime_logs_byNapo" (
        overtime_id TEXT, employee_id TEXT, date_from TEXT, date_to TEXT,
        hours_overtime TEXT, overtime_type TEXT, approval_status TEXT, cost_usd TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."leave_requests_byNapo" CASCADE;
    CREATE TABLE raw."leave_requests_byNapo" (
        leave_id TEXT, employee_id TEXT, leave_type TEXT,
        start_date TEXT, end_date TEXT, total_days TEXT,
        balance_before TEXT, balance_after TEXT, approval_status TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."incidents_sst_byNapo" CASCADE;
    CREATE TABLE raw."incidents_sst_byNapo" (
        incident_id TEXT, employee_id TEXT, incident_date TEXT,
        incident_type TEXT, severity TEXT, body_part_affected TEXT,
        location TEXT, lost_days TEXT, investigation_status TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Phase 4 M08
    DROP TABLE IF EXISTS raw."performance_reviews_byNapo" CASCADE;
    CREATE TABLE raw."performance_reviews_byNapo" (
        review_id TEXT, employee_id TEXT, review_period TEXT,
        reviewer_id TEXT, overall_score TEXT, potential_score TEXT,
        performance_score TEXT, status TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."goals_okrs_byNapo" CASCADE;
    CREATE TABLE raw."goals_okrs_byNapo" (
        goal_id TEXT, employee_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."continuous_feedback_byNapo" CASCADE;
    CREATE TABLE raw."continuous_feedback_byNapo" (
        feedback_id TEXT, employee_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Phase 4 M09
    DROP TABLE IF EXISTS raw."training_courses_byNapo" CASCADE;
    CREATE TABLE raw."training_courses_byNapo" (
        course_id TEXT, course_name TEXT, category TEXT,
        duration_hours TEXT, provider TEXT, cost_usd TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."training_enrollments_byNapo" CASCADE;
    CREATE TABLE raw."training_enrollments_byNapo" (
        enrollment_id TEXT, employee_id TEXT, course_id TEXT,
        enrollment_date TEXT, completion_date TEXT, status TEXT,
        score TEXT, feedback_rating TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."succession_plans_byNapo" CASCADE;
    CREATE TABLE raw."succession_plans_byNapo" (
        plan_id TEXT, employee_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."nine_box_grid_byNapo" CASCADE;
    CREATE TABLE raw."nine_box_grid_byNapo" (
        grid_id TEXT, employee_id TEXT, assessment_date TEXT,
        performance_rating TEXT, potential_rating TEXT, box_category TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Phase 5 M10
    DROP TABLE IF EXISTS raw."survey_responses_byNapo" CASCADE;
    CREATE TABLE raw."survey_responses_byNapo" (
        response_id TEXT, employee_id TEXT, survey_id TEXT,
        survey_type TEXT, survey_date TEXT, score_normalized TEXT,
        comments TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."feedback_comments_byNapo" CASCADE;
    CREATE TABLE raw."feedback_comments_byNapo" (
        feedback_id TEXT, employee_id TEXT, feedback_date TEXT,
        source_channel TEXT, sentiment_label TEXT, sentiment_score TEXT,
        key_topics TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Phase 5 M11
    DROP TABLE IF EXISTS raw."compliance_obligations_byNapo" CASCADE;
    CREATE TABLE raw."compliance_obligations_byNapo" (
        obligation_id TEXT, obligation_type TEXT, description TEXT,
        country_iso3 TEXT, due_date TEXT, frequency TEXT,
        responsible_party TEXT, status TEXT, risk_level TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    DROP TABLE IF EXISTS raw."union_agreements_byNapo" CASCADE;
    CREATE TABLE raw."union_agreements_byNapo" (
        agreement_id TEXT, union_name TEXT, country_iso3 TEXT,
        effective_date TEXT, expiry_date TEXT, coverage_employees TEXT,
        negotiation_status TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(sql_queries))
            conn.commit()
    except Exception as e:
        print(f"❌ Error en base de datos:\n{e}")
        return
        
    print("\n📌 Enumerando artefactos creados:")
    print("  1. Tabla: [raw.ibm_hr_monthly_snapshot_byNapo]")
    print("  2. Tabla: [raw.ibm_hr_change_reasons_byNapo]")
    print("  3. Tabla: [raw.job_postings_byNapo]")
    print("  4. Tabla: [raw.recruitment_pipeline_byNapo]")
    print("  5. Tabla: [raw.onboarding_checklist_byNapo]")
    print("  6. Tabla: [raw.productivity_milestones_byNapo]")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 05 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_raw_enhanced()