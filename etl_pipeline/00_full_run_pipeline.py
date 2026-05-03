import subprocess
import time
import os
from datetime import datetime

SCRIPTS = [
    "01_generate_synthetic_data.py",
    "02_setup_raw_layer.py",
    "03_ingest_data.py",
    "04_setup_business_core.py",
    "m01_vision_ejecutiva.py",
    "m02_reclutamiento.py",
    "m03_onboarding.py",
    "m04_ciclo_vida.py",
    "m05_fuerza_laboral.py",
    "m06_nomina_costos.py",
    "m07_tiempo_bienestar.py",
    "m08_desempeno.py",
    "m09_talento_desarrollo.py",
    "m10_engagement.py",
    "m11_compliance.py",
    "m12_retencion.py",
    "m13_calidad_datos.py",
    "90_generate_data_inventory.py",
    "91_export_data_samples.py",
    "92_generate_lineage.py",       # Auto-actualiza 92_dashboard_lineage.md con row counts reales
]

def run_pipeline():
    print("="*60)
    print("🚀 INICIANDO PIPELINE ETL (MODULAR ARCHITECTURE)")
    print(f"📅 Inicio: {datetime.now().isoformat()}")
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
    print(f"📅 Fin: {datetime.now().isoformat()}")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()