import subprocess
import time
import os

SCRIPTS = [
    "01_generate_synthetic_data.py",
    "02_setup_raw_layer.py",
    "03_ingest_data.py",
    "04_setup_business_core.py",
    "m05_fuerza_laboral.py",
    "90_generate_data_inventory.py"
]

def run_pipeline():
    print("="*60)
    print("🚀 INICIANDO PIPELINE ETL (MODULAR ARCHITECTURE)")
    print("="*60)
    start_total = time.time()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for script in SCRIPTS:
        script_path = os.path.join(current_dir, script)
        if not os.path.exists(script_path):
            print(f"\n⚠️  Script no encontrado: {script}. Saltando...")
            continue
            
        print(f"\n▶️  Ejecutando: {script}")
        try:
            result = subprocess.run(['python', script_path], check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error fatal al ejecutar {script}.")
            print("🛑 Abortando Pipeline.")
            break

    elapsed = time.time() - start_total
    print("\n" + "="*60)
    print(f"🏁 PIPELINE FINALIZADO EN {elapsed:.1f} SEGUNDOS")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()