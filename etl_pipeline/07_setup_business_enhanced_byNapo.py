# 07_setup_business_enhanced_byNapo.py
# ==========================================
# 🏗️ CAPA BUSINESS - Vistas Analíticas byNapo
# Transforma datos RAW (TEXT) en vistas tipadas listas para ECharts/React
# ==========================================

import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('../.env')
db_url = os.getenv("DATABASE_URL")

def setup_business_enhanced():
    """
    Crea la capa Business con vistas tipadas y optimizadas para analytics.
    - Casting seguro de tipos de dato
    - Vistas recursivas para organigramas
    - Vistas materializadas para KPIs de alto rendimiento
    - Permisos para acceso anon (Supabase)
    """
    start_time = time.time()
    print("\n" + "="*50)
    print("🏗️  [ETL 07] CONSTRUYENDO CAPA BUSINESS (byNapo)")
    print("="*50)
    
    if not db_url:
        print("❌ Error: DATABASE_URL no encontrada en .env")
        return
        
    print("⏳ Ejecutando macro-script DDL sobre capa 'business'...")
    
    engine = create_engine(db_url)
    
    # ==========================================
    # 📋 CONSULTAS SQL - CAPA BUSINESS
    # ==========================================
    sql_queries = """
    -- ==========================================
    -- 0. LIMPIEZA TOTAL (CLEAN SLATE)
    -- ==========================================
    DROP SCHEMA IF EXISTS business CASCADE;
    
    -- ==========================================
    -- 1. ESQUEMA Y VISTA MAESTRA TIPADA
    -- ==========================================
    CREATE SCHEMA business;

    -- Vista maestra: Transforma TEXT → tipos nativos + campos calculados
    CREATE OR REPLACE VIEW business.v_employee_full_byNapo AS
    SELECT 
        -- Identificadores
        snapshot_date::DATE as snapshot_date,
        employee_id::INTEGER as employee_id,
        employee_code,
        full_name,
        
        -- Demografía
        gender,
        nationality_iso3,
        country_iso3,
        NULLIF(home_lat, '')::NUMERIC(10,6) as home_lat,
        NULLIF(home_lon, '')::NUMERIC(10,6) as home_lon,
        
        -- Ubicación laboral
        work_center_id,
        work_modality,
        
        -- Organización
        department_name,
        job_role,
        job_level_1,
        job_level_2,
        
        -- Estado laboral
        employment_status,
        NULLIF(hire_date, '')::DATE as hire_date,
        NULLIF(termination_date, '')::DATE as termination_date,
        termination_reason_legal,
        turnover_classification_company,
        
        -- Compensación (moneda local + USD)
        NULLIF(monthly_salary_local, '')::NUMERIC(12,2) as monthly_salary_local,
        currency_iso3,
        NULLIF(fx_rate_to_usd, '')::NUMERIC(10,6) as fx_rate_to_usd,
        NULLIF(monthly_salary_usd, '')::NUMERIC(12,2) as monthly_salary_usd,
        
        -- Jerarquía (con NULLIF para manejar strings vacíos)
        NULLIF(manager_employee_id, '')::INTEGER as manager_employee_id,
        NULLIF(dotted_line_manager_id, '')::INTEGER as dotted_line_manager_id,
        
        -- Educación y familia
        education_level,
        education_status,
        marital_status,
        NULLIF(dependents_count, '')::INTEGER as dependents_count,
        
        -- Flags de cambio (cast a BOOLEAN)
        (salary_change_flag = '1' OR lower(salary_change_flag) = 'true') as salary_change_flag,
        salary_change_reason_code,
        (job_change_flag = '1' OR lower(job_change_flag) = 'true') as job_change_flag,
        
        -- Calidad de salida
        (exit_interview_completed = '1' OR lower(exit_interview_completed) = 'true') as exit_interview_completed,
        (regrettable_loss_flag = '1' OR lower(regrettable_loss_flag) = 'true') as regrettable_loss_flag,
        
        -- Campos calculados derivados
        -- Antigüedad en meses al cierre del snapshot
        CASE 
            WHEN NULLIF(termination_date, '') IS NOT NULL THEN 
                EXTRACT(YEAR FROM AGE(NULLIF(termination_date, '')::DATE, NULLIF(hire_date, '')::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(NULLIF(termination_date, '')::DATE, NULLIF(hire_date, '')::DATE))
            ELSE 
                EXTRACT(YEAR FROM AGE(snapshot_date::DATE, NULLIF(hire_date, '')::DATE)) * 12 + 
                EXTRACT(MONTH FROM AGE(snapshot_date::DATE, NULLIF(hire_date, '')::DATE))
        END as tenure_months,
        
        -- Flag de empleado activo en esa fecha
        CASE 
            WHEN employment_status = 'Active' THEN TRUE
            WHEN NULLIF(termination_date, '') IS NULL THEN TRUE
            WHEN NULLIF(termination_date, '')::DATE >= snapshot_date::DATE THEN TRUE
            ELSE FALSE
        END as is_active_at_snapshot,
        
        -- Timestamp de procesamiento
        NOW() as processed_at
        
    FROM raw.ibm_hr_monthly_snapshot_byNapo;


    -- ==========================================
    -- 2. VISTA DE ORGANIGRAMA (Recursiva con prevención de ciclos)
    -- ==========================================
    CREATE OR REPLACE VIEW business.v_org_tree_byNapo AS
    WITH RECURSIVE org_hierarchy AS (
        -- Nivel base: Empleados sin jefe (CEO/Directores) o con jefe inexistente
        SELECT 
            employee_id,
            full_name,
            job_role,
            job_level_1,
            job_level_2,
            department_name,
            country_iso3,
            work_center_id,
            manager_employee_id,
            0 as depth,
            ARRAY[employee_id] as path_ids,
            ARRAY[full_name] as path_names
        FROM business.v_employee_full_byNapo
        WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND employment_status = 'Active'
          AND (manager_employee_id IS NULL 
               OR manager_employee_id NOT IN (
                   SELECT employee_id FROM business.v_employee_full_byNapo 
                   WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
                     AND employment_status = 'Active'
               ))
        
        UNION ALL
        
        -- Nivel recursivo: Empleados con jefe válido
        SELECT 
            emp.employee_id,
            emp.full_name,
            emp.job_role,
            emp.job_level_1,
            emp.job_level_2,
            emp.department_name,
            emp.country_iso3,
            emp.work_center_id,
            emp.manager_employee_id,
            oh.depth + 1,
            oh.path_ids || emp.employee_id,
            oh.path_names || emp.full_name
        FROM business.v_employee_full_byNapo emp
        INNER JOIN org_hierarchy oh ON emp.manager_employee_id = oh.employee_id
        WHERE emp.snapshot_date = (SELECT MAX(snapshot_date) FROM business.v_employee_full_byNapo)
          AND emp.employment_status = 'Active'
          AND emp.manager_employee_id IS NOT NULL
          AND NOT emp.employee_id = ANY(oh.path_ids)  -- Prevención de ciclos
          AND oh.depth < 10  -- Límite de profundidad para seguridad
    )
    SELECT 
        employee_id,
        full_name,
        job_role,
        job_level_1,
        job_level_2,
        department_name,
        country_iso3,
        work_center_id,
        manager_employee_id,
        depth,
        path_ids,
        path_names,
        -- Campos útiles para ECharts
        json_build_object(
            'id', employee_id,
            'name', full_name,
            'role', job_role,
            'level', job_level_1,
            'dept', department_name,
            'country', country_iso3,
            'depth', depth,
            'children', NULL  -- Se populate en frontend o con otra query
        ) as echarts_node
    FROM org_hierarchy
    ORDER BY depth, employee_id;


    -- ==========================================
    -- 3. VISTA MATERIALIZADA: KPIs Mensuales (Alto Rendimiento)
    -- ==========================================
    CREATE MATERIALIZED VIEW IF NOT EXISTS business.mv_monthly_kpis_byNapo AS
    WITH monthly_stats AS (
        SELECT 
            snapshot_date,
            country_iso3,
            department_name,
            job_level_1,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as headcount_active,
            COUNT(*) FILTER (WHERE is_active_at_snapshot = FALSE) as headcount_terminated,
            COUNT(*) as headcount_total,
            ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as avg_salary_usd,
            ROUND(MIN(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as min_salary_usd,
            ROUND(MAX(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as max_salary_usd,
            COUNT(*) FILTER (WHERE salary_change_flag = TRUE) as salary_changes_count,
            COUNT(*) FILTER (WHERE job_change_flag = TRUE) as job_changes_count,
            COUNT(*) FILTER (WHERE turnover_classification_company = 'Undesired_Turnover') as undesired_turnovers,
            COUNT(*) FILTER (WHERE regrettable_loss_flag = TRUE) as regrettable_losses
        FROM business.v_employee_full_byNapo
        GROUP BY snapshot_date, country_iso3, department_name, job_level_1
    )
    SELECT 
        *,
        -- Attrition Rate mensual (salidas / promedio headcount)
        ROUND(
            CASE 
                WHEN headcount_active > 0 THEN 
                    (headcount_terminated::NUMERIC / NULLIF(headcount_active + headcount_terminated, 0)) * 100 
                ELSE 0 
            END, 2
        ) as attrition_rate_monthly_pct,
        
        -- % de cambios salariales
        ROUND(
            CASE 
                WHEN headcount_active > 0 THEN 
                    (salary_changes_count::NUMERIC / NULLIF(headcount_active, 0)) * 100 
                ELSE 0 
            END, 2
        ) as salary_change_rate_pct,
        
        -- Timestamp de generación
        NOW() as generated_at
    FROM monthly_stats;

    -- Índice único (Requisito para REFRESH CONCURRENTLY)
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_kpis_snapshot_unique 
    ON business.mv_monthly_kpis_byNapo (snapshot_date, country_iso3, department_name, job_level_1);


    -- ==========================================
    -- 4. VISTA DE RESUMEN RÁPIDO (Para KPI Cards del Dashboard)
    -- ==========================================
    CREATE OR REPLACE VIEW business.v_kpi_summary_byNapo AS
    SELECT 
        snapshot_date,
        COUNT(*) FILTER (WHERE is_active_at_snapshot = TRUE) as total_headcount,
        COUNT(DISTINCT country_iso3) as countries_count,
        COUNT(DISTINCT department_name) as departments_count,
        ROUND(AVG(monthly_salary_usd) FILTER (WHERE is_active_at_snapshot = TRUE), 2) as global_avg_salary_usd,
        ROUND(AVG(tenure_months) FILTER (WHERE is_active_at_snapshot = TRUE), 1) as avg_tenure_months,
        COUNT(*) FILTER (WHERE salary_change_flag = TRUE) as recent_salary_changes,
        COUNT(*) FILTER (WHERE turnover_classification_company = 'Undesired_Turnover') as undesired_exits
    FROM business.v_employee_full_byNapo
    GROUP BY snapshot_date
    ORDER BY snapshot_date DESC;


    -- ==========================================
    -- 5. VISTA DE COMPENSACIÓN (Para análisis de bandas y equidad)
    -- ==========================================
    CREATE OR REPLACE VIEW business.v_compensation_analysis_byNapo AS
    SELECT 
        e.snapshot_date,
        e.employee_id,
        e.full_name,
        e.country_iso3,
        e.department_name,
        e.job_level_1,
        e.job_level_2,
        e.monthly_salary_local,
        e.currency_iso3,
        e.monthly_salary_usd,
        e.fx_rate_to_usd,
        e.is_active_at_snapshot
        
        -- NOTA: compa_ratio, band_penetration_pct y salary_position_flag
        -- se han omitido temporalmente ya que raw.ibm_hr_compensation_matrix_byNapo
        -- no existe en el flujo actual.
        
    FROM business.v_employee_full_byNapo e
    WHERE e.is_active_at_snapshot = TRUE;


    -- ==========================================
    -- 6. PERMISOS PARA SUPABASE ANON
    -- ==========================================
    -- Grant usage on schema
    GRANT USAGE ON SCHEMA business TO anon;
    
    -- Grant select on all current and future tables/views in business schema
    GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;
    ALTER DEFAULT PRIVILEGES IN SCHEMA business GRANT SELECT ON TABLES TO anon;
    
    -- Grant select specifically on materialized views
    GRANT SELECT ON business.mv_monthly_kpis_byNapo TO anon;
    """

    # ==========================================
    # 🚀 EJECUCIÓN DE CONSULTAS
    # ==========================================
    try:
        with engine.connect() as conn:
            # Ejecutar todas las consultas
            result = conn.execute(text(sql_queries))
            conn.commit()
            print("✅ Vistas Business creadas exitosamente")
            
        # Refrescar vista materializada (sin CONCURRENTLY para setup inicial)
        with engine.connect() as conn:
            conn.execute(text("REFRESH MATERIALIZED VIEW business.mv_monthly_kpis_byNapo;"))
            conn.commit()
            print("✅ Vista materializada mv_monthly_kpis_byNapo refrescada")
            
        # Validación rápida
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM business.v_employee_full_byNapo LIMIT 1")).fetchone()[0]
            print(f"📊 Validación: Vista maestra accesible ({count:,}+ registros)")
            
    except Exception as e:
        print(f"\n❌ Error creando vistas Business:\n{str(e)}")
        raise
    
    print("\n📌 Enumerando artefactos reconstruidos/creados:")
    print("  1. Esquema: [business]")
    print("  2. Vista:   [business.v_employee_full_byNapo]")
    print("  3. Vista:   [business.v_org_tree_byNapo]")
    print("  4. MatView: [business.mv_monthly_kpis_byNapo]")
    print("  5. Vista:   [business.v_kpi_summary_byNapo]")
    print("  6. Vista:   [business.v_compensation_analysis_byNapo]")
    print("  🔑 Permisos [anon] asignados correctamente (Supabase).")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 07 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    setup_business_enhanced()