import pandas as pd
import numpy as np
import os
import time
from datetime import datetime, timedelta
import networkx as nx

# ==========================================
# 🛠️ CONFIGURACIÓN DEL DATASET - NAPo HR
# ==========================================
CONFIG = {
    "RANDOM_SEED": 42,
    "DATE_RANGE": {"start": "2020-01-01", "end": "2026-03-31"},
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 6000},
    "OUTPUT_DIR": "../data/",
    
    # Configuración de IPC por país (Simulación anual)
    "IPC_CONFIG": {
        "PER": {"rate": 0.04, "month": 2}, # 4% en Febrero
        "ESP": {"rate": 0.03, "month": 1}, # 3% en Enero
        "CHL": {"rate": 0.035, "month": 7}, # 3.5% en Julio
    },
    
    # Listas de datos para generación realista
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

def generate_dataset():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧬 [ETL 04] GENERACIÓN DE DATASET POTENCIADO (byNapo)")
    print("="*50)
    
    # Configuración de fechas
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    
    # Generamos datos iniciales (Seed)
    n_seed = CONFIG["EMPLOYEES_PER_MONTH"]["min"]
    
    # Listas auxiliares
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Pedro", "Lucia"]
    last_names = ["Perez", "Gomez", "Rodriguez", "Lopez", "Martinez", "Silva", "Torres"]
    
    # Crear DataFrame inicial
    data = {
        "employee_id": range(1, n_seed + 1),
        "employee_code": [f"EMP-{i:05d}" for i in range(1, n_seed + 1)],
        "full_name": [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_seed)],
        "gender": np.random.choice(["Male", "Female"], n_seed),
        "country_iso3": np.random.choice(CONFIG["COUNTRIES"], n_seed),
        "department_name": np.random.choice(CONFIG["DEPARTMENTS"], n_seed),
        "job_role": ["Role"] * n_seed, # Se actualizará luego
        "job_level_1": np.random.choice(["Management", "Individual Contributor"], n_seed),
        "job_level_2": np.random.choice(["Senior", "Junior", "Lead"], n_seed),
        "employment_status": "Active",
        "hire_date": [(start - pd.Timedelta(days=int(d))).strftime("%Y-%m-%d") for d in np.random.randint(100, 2000, n_seed)],
        "termination_date": None,
        "monthly_salary_local": np.random.uniform(1500, 5000, n_seed).round(2),
        "currency_iso3": "PEN", # Default
        "manager_employee_id": None
    }
    
    # Asignar roles correctos según departamento
    df = pd.DataFrame(data)
    df["job_role"] = df.apply(lambda row: np.random.choice(CONFIG["ROLES_BY_DEPT"].get(row["department_name"], ["General"])), axis=1)
    
    # Asignar Moneda por país
    currency_map = {"PER": "PEN", "ESP": "EUR", "USA": "USD", "CHL": "CLP", "COL": "COP", "MEX": "MXN"}
    df["currency_iso3"] = df["country_iso3"].map(currency_map)
    
    # Organigrama Inicial (Managers son los primeros 10% de empleados)
    managers = df[df["job_level_1"] == "Management"]["employee_id"].tolist()
    df["manager_employee_id"] = df["employee_id"].apply(
        lambda x: np.random.choice(managers) if x not in managers else None
    )
    
    # Lista para guardar snapshots mensuales
    monthly_snapshots = []
    
    print(f"📅 Iniciando simulación desde {start.strftime('%Y-%m')}...")
    
    for date in dates:
        current_month_str = date.strftime("%Y-%m-%d")
        
        # --- 1. LÓGICA DE EVENTOS DEL MES ---
        
        # A. Ajuste Salarial por IPC
        for country, config in CONFIG["IPC_CONFIG"].items():
            if date.month == config["month"]:
                mask = (df["country_iso3"] == country) & (df["employment_status"] == "Active")
                df.loc[mask, "monthly_salary_local"] *= (1 + config["rate"])
                print(f"   📈 IPC aplicado a {country}: +{config['rate']*100}%")
        
        # B. Rotación (Bajas aleatorias 1%)
        attrition_rate = 0.01
        active_employees = df[df["employment_status"] == "Active"]
        leaving_ids = np.random.choice(active_employees["employee_id"], size=int(len(active_employees) * attrition_rate), replace=False)
        df.loc[df["employee_id"].isin(leaving_ids), "employment_status"] = "Terminated"
        df.loc[df["employee_id"].isin(leaving_ids), "termination_date"] = current_month_str
        
        # C. Contrataciones (Para mantener volumen)
        n_new = int(CONFIG["EMPLOYEES_PER_MONTH"]["min"] * 0.02) # 2% nueva contratación
        for i in range(n_new):
            new_id = df["employee_id"].max() + 1
            country = np.random.choice(CONFIG["COUNTRIES"])
            new_row = {
                "employee_id": new_id,
                "employee_code": f"EMP-{new_id:05d}",
                "full_name": f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
                "gender": np.random.choice(["Male", "Female"]),
                "country_iso3": country,
                "department_name": np.random.choice(CONFIG["DEPARTMENTS"]),
                "job_role": np.random.choice(CONFIG["ROLES_BY_DEPT"].get("IT", ["General"])),
                "job_level_1": "Individual Contributor",
                "job_level_2": "Junior",
                "employment_status": "Active",
                "hire_date": current_month_str,
                "termination_date": None,
                "monthly_salary_local": np.random.uniform(1000, 3000),
                "currency_iso3": currency_map[country],
                "manager_employee_id": np.random.choice(managers)
            }
            # Agregar al DataFrame (pd.concat es lento en bucles, pero ok para este volumen)
            # Para optimizar, en prod se usaría lista y concat final.
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # --- 2. VALIDACIÓN DE ORGANIGRAMA (NetworkX) ---
        # Validar que no haya ciclos ni managers fantasmas
        valid_ids = set(df[df["employment_status"] == "Active"]["employee_id"])
        
        # Corregir managers fantasmas
        for idx, row in df.iterrows():
            if row["employment_status"] == "Active" and row["manager_employee_id"] is not None:
                if row["manager_employee_id"] not in valid_ids:
                    # Asignar a un manager válido al azar
                    df.at[idx, "manager_employee_id"] = np.random.choice(managers)
        
        # --- 3. GUARDAR SNAPSHOT ---
        snapshot_df = df.copy()
        snapshot_df["snapshot_date"] = current_month_str
        
        # Calcular USD (simulado fx fijo 1:3.5 para simplificar, en prod usar tabla FX)
        snapshot_df["fx_rate_to_usd"] = 3.50 
        snapshot_df["monthly_salary_usd"] = (snapshot_df["monthly_salary_local"] / snapshot_df["fx_rate_to_usd"]).round(2)
        
        # Flags placeholder (se llenarían con lógica de eventos)
        snapshot_df["salary_change_flag"] = 0
        snapshot_df["job_change_flag"] = 0
        
        monthly_snapshots.append(snapshot_df)
    
    # Concatenar todos los meses
    final_df = pd.concat(monthly_snapshots, ignore_index=True)
    
    # Guardar CSV
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    final_df.to_csv(output_path, index=False)
    
    elapsed = time.time() - start_time
    print(f"\n✅ Dataset guardado en: {output_path}")
    print(f"📊 Total registros generados: {len(final_df):,}")
    print(f"⏱️ Tiempo: {elapsed:.2f} segundos")

if __name__ == "__main__":
    generate_dataset()