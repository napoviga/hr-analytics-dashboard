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
    print("\n" + "="*50 + "\n🧬 [ETL 04] GENERACIÓN DE DATASET (CEO FIX)\n" + "="*50)
    
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

if __name__ == "__main__":
    generate_dataset()