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
    "EMPLOYEES_PER_MONTH": {"min": 4000, "max": 8000},
    "OUTPUT_DIR": "../data/",
    "LOG_LEVEL": "INFO"
}

def generate_dataset():
    start_time = time.time()
    print("\n" + "="*50)
    print("🧬 [ETL 04] GENERACIÓN DE DATASET MEJORADO (byNapo)")
    print("="*50)
    print("⏳ Configurando rangos de fecha y simulando datos...")
    # 1. Configuración de fechas
    start = pd.to_datetime(CONFIG["DATE_RANGE"]["start"])
    end = pd.to_datetime(CONFIG["DATE_RANGE"]["end"])
    dates = pd.date_range(start=start, end=end, freq="ME")
    
    # 2. Carga base IBM (Simulación inicial)
    # Nota: En un entorno real, leeríamos el CSV. Aquí simulamos la estructura.
    # Para mantener el script ligero, asumimos que generaremos datos desde cero 
    # basados en patrones, pero manteniendo la firma IBM.
    
    # Generamos DataFrame vacío base con columnas clave
    cols_snapshot = [
        "snapshot_date", "employee_id", "employee_code", "full_name", "gender", 
        "nationality_iso3", "country_iso3", "department_name", "job_role", 
        "job_level_1", "job_level_2", "employment_status", "hire_date", 
        "termination_date", "termination_reason_legal", "turnover_classification_company",
        "monthly_salary_local", "currency_iso3", "fx_rate_to_usd", "monthly_salary_usd",
        "manager_employee_id", "dotted_line_manager_id", "work_center_id", 
        "home_lat", "home_lon", "work_modality", "education_level", 
        "education_status", "marital_status", "dependents_count", 
        "salary_change_flag", "salary_change_reason_code", "job_change_flag", 
        "exit_interview_completed", "regrettable_loss_flag"
    ]
    
    # Creamos lista de DataFrames mensuales
    monthly_data = []
    
    print(f"📅 Generando snapshots desde {start.strftime('%Y-%m')} hasta {end.strftime('%Y-%m')}...")
    
    # Simulación simplificada para demostración (Reemplazar con tu lógica completa de simulación si la tienes externa)
    # Aquí creamos 100 empleados de prueba por mes para validar la estructura
    for date in dates:
        # Generar datos dummy para el mes
        n_emp = np.random.randint(CONFIG["EMPLOYEES_PER_MONTH"]["min"], CONFIG["EMPLOYEES_PER_MONTH"]["max"])
        
        # Datos básicos
        data = {
            "snapshot_date": date.strftime("%Y-%m-%d"),
            "employee_id": range(1, n_emp + 1),
            "employee_code": [f"EMP-{i:05d}" for i in range(1, n_emp + 1)],
            "full_name": ["Empleado Generado" for _ in range(n_emp)], # Reemplazar con generador de nombres
            "gender": np.random.choice(["Male", "Female"], n_emp),
            "nationality_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "country_iso3": np.random.choice(["PER", "CHL", "COL", "MEX", "USA", "ESP"], n_emp),
            "department_name": np.random.choice(["Sales", "IT", "HR", "Operations"], n_emp),
            "job_role": np.random.choice(["Analyst", "Manager", "Director"], n_emp),
            "job_level_1": np.random.choice(["Individual Contributor", "Management"], n_emp),
            "job_level_2": np.random.choice(["Junior", "Senior", "Lead"], n_emp),
            "employment_status": np.random.choice(["Active", "Terminated"], n_emp, p=[0.9, 0.1]),
            "hire_date": (date - pd.Timedelta(days=np.random.randint(1, 3650))).strftime("%Y-%m-%d"),
            "termination_date": [None] * n_emp, # Lógica de cese necesaria aquí
            "termination_reason_legal": [None] * n_emp,
            "turnover_classification_company": [None] * n_emp,
            "monthly_salary_local": np.random.uniform(1000, 5000, n_emp).round(2),
            "currency_iso3": "PEN",
            "fx_rate_to_usd": 3.70,
            "monthly_salary_usd": 0.0, # Se calculará
            "manager_employee_id": [None] * n_emp,
            "dotted_line_manager_id": [None] * n_emp,
            "work_center_id": np.random.choice(["WC-001", "WC-002"], n_emp),
            "home_lat": np.random.uniform(-12.0, -11.0, n_emp),
            "home_lon": np.random.uniform(-77.0, -76.0, n_emp),
            "work_modality": "Hybrid",
            "education_level": "Bachelor",
            "education_status": "Complete",
            "marital_status": "Single",
            "dependents_count": 0,
            "salary_change_flag": 0,
            "salary_change_reason_code": None,
            "job_change_flag": 0,
            "exit_interview_completed": False,
            "regrettable_loss_flag": False
        }
        
        df = pd.DataFrame(data)
        
        # Cálculo de FX y USD
        df["monthly_salary_usd"] = (df["monthly_salary_local"] / df["fx_rate_to_usd"]).round(2)
        
        # Validación Organigrama (Ejemplo simple con NetworkX)
        # En producción: G = nx.DiGraph(); G.add_edges_from(...); assert nx.is_directed_acyclic_graph(G)
        
        monthly_data.append(df)

    # Concatenar todo
    final_df = pd.concat(monthly_data, ignore_index=True)
    
    # Guardar CSV
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], "ibm_hr_monthly_snapshot_byNapo.csv")
    try:
        final_df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"❌ Error al guardar CSV:\n{e}")
        return

    print("\n📌 Resumen de Generación:")
    print(f"  ➜ Archivo CSV:    {output_path}")
    print(f"  ➜ Total Meses:    {len(dates)}")
    print(f"  ➜ Total Registros:{len(final_df):,}")

    elapsed = time.time() - start_time
    print(f"\n✅ ETL 04 completado exitosamente en {elapsed:.2f} segundos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    generate_dataset()