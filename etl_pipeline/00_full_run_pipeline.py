import subprocess
import time
import sys
import os

# Lista asegurando el orden estricto de ejecución
SCRIPTS = [
    "01_setup_raw.py",
    "02_ingest_data.py",
    "03_setup_business.py",
    "04_create_enhanced_dataset_byNapo.py",
    "05_setup_raw_enhanced_byNapo.py",
    "06_ingest_enhanced_byNapo.py",
    "07_setup_business_enhanced_byNapo.py",
    "08_setup_rpc_dashboard.py",
    "90_generate_data_inventory.py"  # <-- Nuestro nuevo Guardián de Calidad al final
]

def print_banner():
    print("\n" + "="*60)
    print("🚀 HR ANALYTICS DASHBOARD - FULL PIPELINE EXECUTION 🚀")
    print("="*60)

def run_pipeline():
    print_banner()
    start_time = time.time()
    
    for idx, script in enumerate(SCRIPTS, 1):
        script_path = os.path.join(os.path.dirname(__file__), script)
        print(f"\n[{idx}/{len(SCRIPTS)}] Ejecutando: {script}")
        print("-" * 50)
        
        if not os.path.exists(script_path):
            print(f"❌ Error: No se encontró el archivo {script} en {script_path}")
            sys.exit(1)
            
        try:
            # Ejecutamos con subprocess
            result = subprocess.run(
                [sys.executable, script_path],
                check=True,
                text=True,
                capture_output=False # Mostramos el output directamente en la consola
            )
        except subprocess.CalledProcessError as e:
            print("\n❌ [" + script + "] Falló con código de salida: " + str(e.returncode))
            print("🛑 Interrumpiendo el flujo del pipeline.")
            sys.exit(1)
            
        print("-" * 50)
        print(f"✅ {script} completado.")
        
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print(f"🎉 EJECUCIÓN DEL PIPELINE FINALIZADA EXITOSAMENTE")
    print(f"⏱️  Tiempo Total: {total_time:.2f} segundos")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_pipeline()