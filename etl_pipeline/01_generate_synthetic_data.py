import pandas as pd
import numpy as np
import os
import time
from datetime import datetime

CONFIG = {
    "RANDOM_SEED": 42,
    "DATE_RANGE": {"start": "2020-01-01", "end": "2026-03-31"},
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 6000},
    "OUTPUT_DIR": "../data/",
    "IPC_CONFIG": {"PER": {"rate": 0.04, "month": 2}, "ESP": {"rate": 0.03, "month": 1}, "CHL": {"rate": 0.035, "month": 7}},
    "GEO_CONFIG": {
        "PER": {"lat": -12.0464, "lon": -77.0428}, "CHL": {"lat": -33.4489, "lon": -70.6693},
        "COL": {"lat": 4.6097, "lon": -74.0817}, "MEX": {"lat": 19.4326, "lon": -99.1332},
        "ESP": {"lat": 40.4168, "lon": -3.7038}, "USA": {"lat": 40.7128, "lon": -74.0060}
    },
    "COUNTRIES": ["PER", "CHL", "COL", "MEX", "ESP", "USA"],
    "DEPARTMENTS": ["IT", "Sales", "HR", "Finance", "Operations"],
    "ROLES_BY_DEPT": {
        "IT": ["Software Engineer", "DevOps", "Data Analyst", "CTO"],
        "Sales": ["Sales Rep", "Account Manager", "Sales Director"],
        "HR": ["HR Specialist", "HR Manager", "Recruiter"],
        "Finance": ["Accountant", "Financial Analyst", "CFO"],
        "Operations": ["Operator", "Logistics Coord", "Ops Director"]
    }
}

def generate_catalogs():
    reasons = [
        {"reason_code": "SAL-IPC", "reason_name_es": "Ajuste por Inflación (IPC)", "reason_name_en": "Inflation Adjustment", "affects_salary": "Y", "affects_job": "N", "active_flag": "Y"},
        {"reason_code": "TER-VOL", "reason_name_es": "Renuncia Voluntaria", "reason_name_en": "Voluntary Resignation", "affects_salary": "N", "affects_job": "Y", "active_flag": "Y"},
        {"reason_code": "TER-INV", "reason_name_es": "Despido Injustificado", "reason_name_en": "Involuntary Termination", "affects_salary": "N", "affects_job": "Y", "active_flag": "Y"},
        {"reason_code": "TER-RET", "reason_name_es": "Jubilación", "reason_name_en": "Retirement", "affects_salary": "N", "affects_job": "Y", "active_flag": "Y"}
    ]
    df_reasons = pd.DataFrame(reasons)
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    df_reasons.to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_change_reasons_byNapo.csv"), index=False)

def generate_dataset():
    start_time = time.time()
    print("\n" + "="*50 + "\n🧬 [ETL 01] GENERACIÓN DE DATASET (CEO FIX)\n" + "="*50)
    
    np.random.seed(CONFIG["RANDOM_SEED"])
    generate_catalogs()
    
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    n_seed = CONFIG["EMPLOYEES_PER_MONTH"]["min"]
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia"]
    last_names = ["Perez", "Gomez", "Rodriguez", "Lopez", "Martinez", "Silva", "Torres"]
    
    data = {
        "employee_id": range(1, n_seed + 1),
        "employee_code": [f"EMP-{i:05d}" for i in range(1, n_seed + 1)],
        "full_name": [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_seed)],
        "gender": np.random.choice(["Male", "Female"], n_seed),
        "country_iso3": np.random.choice(CONFIG["COUNTRIES"], n_seed),
        "department_name": np.random.choice(CONFIG["DEPARTMENTS"], n_seed),
        "job_role": ["Role"] * n_seed,
        "job_level_1": np.random.choice(["Management", "Individual Contributor"], n_seed, p=[0.15, 0.85]),
        "job_level_2": np.random.choice(["Senior", "Junior", "Lead"], n_seed),
        "employment_status": "Active",
        "hire_date": [(start - pd.Timedelta(days=int(d))).strftime("%Y-%m-%d") for d in np.random.randint(100, 2000, n_seed)],
        "termination_date": None, "termination_reason_legal": None,
        "monthly_salary_local": np.random.uniform(1500, 5000, n_seed).round(2),
        "currency_iso3": "PEN", "manager_employee_id": None,
        "work_modality": np.random.choice(["Remote", "Hybrid", "On-Site"], n_seed, p=[0.2, 0.5, 0.3]),
        "marital_status": np.random.choice(["Single", "Married", "Divorced"], n_seed, p=[0.5, 0.4, 0.1]),
        "education_level": np.random.choice(["Bachelor", "Master", "PhD", "Technical"], n_seed),
        "home_lat": 0.0, "home_lon": 0.0, "salary_change_flag": 0, "salary_change_reason_code": None
    }
    
    df = pd.DataFrame(data)
    df["job_role"] = df.apply(lambda row: np.random.choice(CONFIG["ROLES_BY_DEPT"].get(row["department_name"], ["General"])), axis=1)
    currency_map = {"PER": "PEN", "ESP": "EUR", "USA": "USD", "CHL": "CLP", "COL": "COP", "MEX": "MXN"}
    df["currency_iso3"] = df["country_iso3"].map(currency_map)
    
    # Llenando columnas fantasma para tener 100% de calidad
    df["nationality_iso3"] = df["country_iso3"]
    df["education_status"] = "Graduated"
    df["dependents_count"] = np.random.randint(0, 4, n_seed)
    df["turnover_classification_company"] = None
    df["exit_interview_completed"] = None
    df["regrettable_loss_flag"] = None
    df["dotted_line_manager_id"] = None
    df["work_center_id"] = "WC-" + df["country_iso3"]
    df["job_change_flag"] = 0

    for c_iso in CONFIG["COUNTRIES"]:
        mask = df["country_iso3"] == c_iso
        c_lat, c_lon = CONFIG["GEO_CONFIG"][c_iso]["lat"], CONFIG["GEO_CONFIG"][c_iso]["lon"]
        df.loc[mask, "home_lat"] = c_lat + np.random.uniform(-0.05, 0.05, mask.sum())
        df.loc[mask, "home_lon"] = c_lon + np.random.uniform(-0.05, 0.05, mask.sum())

    # 🔥 FIX: El nacimiento del CEO Inmortal (Raíz del Organigrama)
    df.loc[0, "job_role"] = "CEO"
    df.loc[0, "job_level_1"] = "Management"
    df.loc[0, "manager_employee_id"] = None

    monthly_snapshots = []
    
    for date in dates:
        current_month_str = date.strftime("%Y-%m-%d")
        df["salary_change_flag"] = 0
        df["salary_change_reason_code"] = None
        
        # El CEO (id=1) jamás necesita manager
        active_managers = df[(df["job_level_1"] == "Management") & (df["employment_status"] == "Active")]["employee_id"].tolist()
        needs_manager = df[(df["employment_status"] == "Active") & (df["manager_employee_id"].isnull()) & (df["employee_id"] != 1)]
        
        if not needs_manager.empty and active_managers:
            df.loc[needs_manager.index, "manager_employee_id"] = np.random.choice(active_managers, len(needs_manager))

        for country, config in CONFIG["IPC_CONFIG"].items():
            if date.month == config["month"]:
                mask = (df["country_iso3"] == country) & (df["employment_status"] == "Active")
                df.loc[mask, "monthly_salary_local"] *= (1 + config["rate"])
                df.loc[mask, "salary_change_flag"] = 1
                df.loc[mask, "salary_change_reason_code"] = "SAL-IPC"
        
        # El CEO (id=1) no entra en la rifa de despidos
        attrition_rate = 0.005
        active_employees = df[(df["employment_status"] == "Active") & (df["employee_id"] != 1)]
        leaving_count = int(len(active_employees) * attrition_rate)
        
        if leaving_count > 0:
            leaving_ids = np.random.choice(active_employees["employee_id"], size=leaving_count, replace=False)
            df.loc[df["employee_id"].isin(leaving_ids), "employment_status"] = "Terminated"
            df.loc[df["employee_id"].isin(leaving_ids), "termination_date"] = current_month_str
            df.loc[df["employee_id"].isin(leaving_ids), "termination_reason_legal"] = np.random.choice(["TER-VOL", "TER-INV", "TER-RET"], len(leaving_ids), p=[0.7, 0.2, 0.1])
            df.loc[df["employee_id"].isin(leaving_ids), "turnover_classification_company"] = np.random.choice(["Regrettable", "Non-Regrettable"], len(leaving_ids))
            df.loc[df["employee_id"].isin(leaving_ids), "exit_interview_completed"] = np.random.choice(["Y", "N"], len(leaving_ids))
            df.loc[df["employee_id"].isin(leaving_ids), "regrettable_loss_flag"] = np.random.choice(["Y", "N"], len(leaving_ids))
            active_managers = [m for m in active_managers if m not in leaving_ids]

        orphans = df[(df["employment_status"] == "Active") & (df["manager_employee_id"].isin(leaving_ids)) & (df["employee_id"] != 1)]
        if not orphans.empty and active_managers:
            df.loc[orphans.index, "manager_employee_id"] = np.random.choice(active_managers, len(orphans))

        n_new = int(CONFIG["EMPLOYEES_PER_MONTH"]["min"] * 0.01)
        new_rows = []
        for i in range(n_new):
            new_id = df["employee_id"].max() + 1 + i
            country = np.random.choice(CONFIG["COUNTRIES"])
            new_rows.append({
                "employee_id": new_id, "employee_code": f"EMP-{new_id:05d}",
                "full_name": f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
                "gender": np.random.choice(["Male", "Female"]), "country_iso3": country,
                "nationality_iso3": country, "department_name": np.random.choice(CONFIG["DEPARTMENTS"]),
                "job_role": np.random.choice(CONFIG["ROLES_BY_DEPT"].get("IT", ["General"])),
                "job_level_1": "Individual Contributor", "job_level_2": "Junior",
                "employment_status": "Active", "hire_date": current_month_str,
                "termination_date": None, "termination_reason_legal": None,
                "monthly_salary_local": np.random.uniform(1000, 3000), "currency_iso3": currency_map[country],
                "manager_employee_id": np.random.choice(active_managers) if active_managers else 1,
                "work_modality": np.random.choice(["Remote", "Hybrid", "On-Site"], p=[0.2, 0.5, 0.3]),
                "marital_status": np.random.choice(["Single", "Married", "Divorced"], p=[0.5, 0.4, 0.1]),
                "education_level": np.random.choice(["Bachelor", "Master", "PhD", "Technical"]),
                "education_status": "Graduated", "dependents_count": np.random.randint(0, 4),
                "work_center_id": "WC-" + country,
                "home_lat": CONFIG["GEO_CONFIG"][country]["lat"] + np.random.uniform(-0.05, 0.05),
                "home_lon": CONFIG["GEO_CONFIG"][country]["lon"] + np.random.uniform(-0.05, 0.05),
                "salary_change_flag": 0, "salary_change_reason_code": None, "job_change_flag": 0,
                "turnover_classification_company": None, "exit_interview_completed": None,
                "regrettable_loss_flag": None, "dotted_line_manager_id": None
            })
        if new_rows:
            df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        
        snapshot_df = df.copy()
        snapshot_df["snapshot_date"] = current_month_str
        snapshot_df["fx_rate_to_usd"] = 3.50 
        snapshot_df["monthly_salary_usd"] = (snapshot_df["monthly_salary_local"] / snapshot_df["fx_rate_to_usd"]).round(2)
        monthly_snapshots.append(snapshot_df)
    
    final_df = pd.concat(monthly_snapshots, ignore_index=True)
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    final_df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset maestro guardado. CEO asignado con éxito.")
    
    generate_phase3_data(final_df)
    generate_phase4_data(final_df)
    generate_phase5_data(final_df)

def generate_phase3_data(df):
    print("⏳ Generando datos sintéticos Fase 3 (M02 y M03)...")
    import uuid
    import random
    
    hires = df.drop_duplicates(subset=["employee_id"], keep="first").copy()
    postings = []
    candidates = []
    
    hires['hire_month'] = pd.to_datetime(hires['hire_date']).dt.to_period('M')
    for (month, dept), group in hires.groupby(['hire_month', 'department_name']):
        num_hires = len(group)
        posting_id = f"POST-{month}-{dept[:3].upper()}-{np.random.randint(1000,9999)}"
        posting_date = (month.to_timestamp() - pd.Timedelta(days=np.random.randint(30, 60))).strftime("%Y-%m-%d")
        closing_date = (month.to_timestamp() + pd.Timedelta(days=np.random.randint(0, 15))).strftime("%Y-%m-%d")
        
        country = group['country_iso3'].iloc[0]
        postings.append({
            "posting_id": posting_id, "job_title": f"Specialist {dept}", "department_name": dept, 
            "country_iso3": country, "job_level_1": "Individual Contributor", "job_level_2": "Junior",
            "salary_range_min": 1000, "salary_range_max": 3000, "posting_date": posting_date,
            "closing_date": closing_date, "status": "Closed", "positions_available": num_hires,
        })
        
        for _, emp in group.iterrows():
            candidates.append({
                "candidate_id": f"CAND-{uuid.uuid4().hex[:6].upper()}", "posting_id": posting_id,
                "full_name": emp["full_name"], "gender": emp["gender"], "age": np.random.randint(22, 50),
                "education_level": emp["education_level"], "years_experience": np.random.randint(1, 10),
                "application_date": posting_date, "stage": "Hired", "stage_change_date": emp["hire_date"],
                "interview_score": np.random.randint(70, 100), "rejection_reason": None,
                "hired_employee_id": emp["employee_id"], "nps_score": np.random.randint(7, 11)
            })
            
        num_rejected = np.random.randint(10, 31)
        stages = ["Applied", "Screening", "Interview", "Offer"]
        for _ in range(num_rejected):
            stage = np.random.choice(stages, p=[0.4, 0.3, 0.2, 0.1])
            candidates.append({
                "candidate_id": f"CAND-{uuid.uuid4().hex[:6].upper()}", "posting_id": posting_id,
                "full_name": f"Cand {np.random.randint(1000,9999)}", "gender": np.random.choice(["Male", "Female"]), 
                "age": np.random.randint(22, 50), "education_level": np.random.choice(["Bachelor", "Master"]),
                "years_experience": np.random.randint(0, 10), "application_date": posting_date,
                "stage": stage, "stage_change_date": closing_date, "interview_score": np.random.randint(40, 85) if stage in ["Interview", "Offer"] else None,
                "rejection_reason": "Not a fit" if stage != "Offer" else "Offer Rejected", "hired_employee_id": None, "nps_score": np.random.randint(3, 9)
            })

    pd.DataFrame(postings).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "job_postings_byNapo.csv"), index=False)
    pd.DataFrame(candidates).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "recruitment_pipeline_byNapo.csv"), index=False)
    
    checklists = []
    milestones = []
    checklist_items = ["Equipment Setup", "IT Access", "Orientation", "Compliance Training", "Manager Meet"]
    
    for _, emp in hires.iterrows():
        emp_id = emp["employee_id"]
        hire_date = pd.to_datetime(emp["hire_date"])
        for item in checklist_items:
            status = np.random.choice(["Completed", "Overdue"], p=[0.85, 0.15])
            checklists.append({
                "onboarding_id": f"ONB-{emp_id}-{item[:3].upper()}", "employee_id": emp_id,
                "checklist_item": item, "category": "General", 
                "due_date": (hire_date + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                "completion_date": (hire_date + pd.Timedelta(days=np.random.randint(1, 14))).strftime("%Y-%m-%d") if status == "Completed" else None,
                "status": status
            })
            
        for m_name, exp_days in [("First Project", 30), ("Independent Work", 60), ("Full Productivity", 90)]:
            actual_days = exp_days + np.random.randint(-10, 20)
            milestones.append({
                "milestone_id": f"MIL-{emp_id}-{exp_days}", "employee_id": emp_id,
                "milestone_name": m_name, "expected_days": exp_days, "actual_days": actual_days,
                "achievement_date": (hire_date + pd.Timedelta(days=actual_days)).strftime("%Y-%m-%d"),
                "performance_rating": np.random.randint(3, 6), "manager_id": emp["manager_employee_id"]
            })
            
    pd.DataFrame(checklists).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "onboarding_checklist_byNapo.csv"), index=False)
    pd.DataFrame(milestones).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "productivity_milestones_byNapo.csv"), index=False)
    print("✅ CSVs Fase 3 generados exitosamente.")

def generate_phase4_data(df):
    print("⏳ Generando datos sintéticos Fase 4 (M07, M08, M09)...")
    import uuid
    import random
    
    hires = df.drop_duplicates(subset=["employee_id"], keep="first").copy()
    
    # --- M07: Tiempo y Asistencia ---
    attendance = []
    overtime = []
    leaves = []
    incidents = []
    
    # We will generate summary data instead of daily to keep CSV sizes manageable
    # Just generating a few records per employee to simulate the metrics
    for _, emp in hires.iterrows():
        emp_id = emp["employee_id"]
        # Leaves
        leaves.append({
            "leave_id": f"LV-{emp_id}-{np.random.randint(100,999)}", "employee_id": emp_id,
            "leave_type": "Vacation", "start_date": "2024-01-10", "end_date": "2024-01-20",
            "total_days": 10, "balance_before": 30, "balance_after": 20, "approval_status": "Approved"
        })
        # Overtime
        if np.random.random() < 0.2:
            overtime.append({
                "overtime_id": f"OT-{emp_id}-{np.random.randint(100,999)}", "employee_id": emp_id,
                "date_from": "2024-02-01", "date_to": "2024-02-07", "hours_overtime": np.random.randint(2, 10),
                "overtime_type": "Weekend", "approval_status": "Approved", "cost_usd": np.random.randint(50, 200)
            })
            
        # Incidents
        if np.random.random() < 0.05:
            incidents.append({
                "incident_id": f"INC-{emp_id}-{np.random.randint(100,999)}", "employee_id": emp_id,
                "incident_date": "2024-03-15", "incident_type": "Slip", "severity": np.random.choice(["Minor", "Moderate"]),
                "body_part_affected": "Leg", "location": "Office", "lost_days": np.random.randint(0, 5),
                "investigation_status": "Closed"
            })
            
    # For attendance, generate 1 record per month per employee (aggregated simulation) to avoid 1M rows
    # The ETL actually groups by month, so we can generate monthly summaries directly into the 'attendance' table
    for (month, emp_id), group in df.groupby(['snapshot_date', 'employee_id']):
        if group['employment_status'].iloc[0] == 'Active':
            attendance.append({
                "record_id": f"ATT-{emp_id}-{month}", "employee_id": emp_id, "work_date": month,
                "check_in_time": "09:00", "check_out_time": "18:00", "scheduled_hours": 160,
                "worked_hours": 160 - np.random.randint(0, 16), 
                "absence_type": np.random.choice(["Present", "Sick", "Vacation"], p=[0.95, 0.03, 0.02]),
                "late_minutes": np.random.randint(0, 60) if np.random.random() < 0.1 else 0,
                "work_modality": "Remote"
            })

    pd.DataFrame(attendance).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "attendance_records_byNapo.csv"), index=False)
    pd.DataFrame(overtime).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "overtime_logs_byNapo.csv"), index=False)
    pd.DataFrame(leaves).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "leave_requests_byNapo.csv"), index=False)
    pd.DataFrame(incidents).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "incidents_sst_byNapo.csv"), index=False)

    # --- M08 & M09 (Desempeño y Talento) ---
    reviews = []
    courses = []
    enrollments = []
    nine_box = []
    
    for _, emp in hires.iterrows():
        emp_id = emp["employee_id"]
        score = np.random.uniform(2.5, 5.0)
        reviews.append({
            "review_id": f"REV-{emp_id}-2024", "employee_id": emp_id, "review_period": "2024-Q1",
            "reviewer_id": emp["manager_employee_id"], "overall_score": round(score, 1),
            "potential_score": np.random.randint(1, 4), "performance_score": np.random.randint(1, 4),
            "status": "Completed"
        })
        
        nine_box.append({
            "grid_id": f"9B-{emp_id}-2024", "employee_id": emp_id, "assessment_date": "2024-01-01",
            "performance_rating": np.random.randint(1, 4), "potential_rating": np.random.randint(1, 4),
            "box_category": "Core Player"
        })
        
        enrollments.append({
            "enrollment_id": f"ENR-{emp_id}", "employee_id": emp_id, "course_id": "CRS-101",
            "enrollment_date": "2024-02-01", "completion_date": "2024-02-15",
            "status": "Completed", "score": np.random.randint(70, 100), "feedback_rating": 4
        })

    courses.append({"course_id": "CRS-101", "course_name": "Leadership 101", "category": "Soft Skills", "duration_hours": 10, "provider": "Internal", "cost_usd": 0})
    
    pd.DataFrame(reviews).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "performance_reviews_byNapo.csv"), index=False)
    pd.DataFrame(nine_box).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "nine_box_grid_byNapo.csv"), index=False)
    pd.DataFrame(enrollments).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "training_enrollments_byNapo.csv"), index=False)
    pd.DataFrame(courses).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "training_courses_byNapo.csv"), index=False)
    
    # Save empty CSVs for the ones we didn't fully model but are in the tables
    pd.DataFrame(columns=["goal_id", "employee_id"]).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "goals_okrs_byNapo.csv"), index=False)
    pd.DataFrame(columns=["feedback_id", "employee_id"]).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "continuous_feedback_byNapo.csv"), index=False)
    pd.DataFrame(columns=["plan_id", "employee_id"]).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "succession_plans_byNapo.csv"), index=False)
    
    print("✅ CSVs Fase 4 generados exitosamente.")

def generate_phase5_data(df):
    print("⏳ Generando datos sintéticos Fase 5 (M10, M11, M12)...")
    import uuid
    import random
    
    hires = df.drop_duplicates(subset=["employee_id"], keep="first").copy()
    
    # --- M10: Engagement & Sentimiento ---
    surveys = []
    feedback = []
    
    for _, emp in hires.iterrows():
        emp_id = emp["employee_id"]
        # eNPS Survey
        if np.random.random() < 0.8:
            score = np.random.randint(1, 11)
            surveys.append({
                "response_id": f"SUR-{emp_id}-2024", "employee_id": emp_id,
                "survey_id": "ENPS-2024", "survey_type": "eNPS",
                "survey_date": "2024-03-01", "score_normalized": score,
                "comments": "Great place to work" if score >= 9 else "Could be better"
            })
            
        # Feedback
        if np.random.random() < 0.3:
            sentiment = np.random.choice(["Positive", "Neutral", "Negative"], p=[0.6, 0.3, 0.1])
            feedback.append({
                "feedback_id": f"FB-{emp_id}-2024", "employee_id": emp_id,
                "feedback_date": "2024-03-15", "source_channel": "Pulse Survey",
                "sentiment_label": sentiment, "sentiment_score": 0.8 if sentiment == "Positive" else (0.5 if sentiment == "Neutral" else 0.2),
                "key_topics": "Work-Life Balance"
            })

    pd.DataFrame(surveys).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "survey_responses_byNapo.csv"), index=False)
    pd.DataFrame(feedback).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "feedback_comments_byNapo.csv"), index=False)

    # --- M11: Compliance ---
    compliance = []
    unions = []
    
    countries = df["country_iso3"].unique()
    for country in countries:
        compliance.append({
            "obligation_id": f"COMP-{country}-01", "obligation_type": "Labor Law",
            "description": f"Annual HR Audit {country}", "country_iso3": country,
            "due_date": "2024-12-31", "frequency": "Annual",
            "responsible_party": "HR Director", "status": "Compliant", "risk_level": "High"
        })
        if np.random.random() < 0.5:
            unions.append({
                "agreement_id": f"UAG-{country}", "union_name": f"National Union {country}",
                "country_iso3": country, "effective_date": "2023-01-01", "expiry_date": "2025-12-31",
                "coverage_employees": np.random.randint(50, 500), "negotiation_status": "Active"
            })

    pd.DataFrame(compliance).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "compliance_obligations_byNapo.csv"), index=False)
    pd.DataFrame(unions).to_csv(os.path.join(CONFIG["OUTPUT_DIR"], "union_agreements_byNapo.csv"), index=False)
    
    print("✅ CSVs Fase 5 generados exitosamente.")

if __name__ == "__main__":
    generate_dataset()