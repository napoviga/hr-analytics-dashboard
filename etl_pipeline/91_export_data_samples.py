#!/usr/bin/env python3
"""
Export Data Samples — GDH Analytics Dashboard
================================================
Genera un archivo Markdown con muestras reales de las vistas clave
de la base de datos Supabase/PostgreSQL.

Requisitos: pip install supabase python-dotenv

Uso: python etl_pipeline/91_export_data_samples.py
"""

import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ python-dotenv no está instalado. Ejecuta: pip install python-dotenv")
    sys.exit(1)

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("❌ psycopg2 no está instalado. Ejecuta: pip install psycopg2-binary")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

# Resolver ruta del .env (prioridad: raíz del proyecto > client/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ETL_DIR = PROJECT_ROOT / "etl_pipeline"

# Intentar cargar .env desde la raíz primero, luego desde client/
env_path = PROJECT_ROOT / ".env"
if not env_path.exists():
    env_path = PROJECT_ROOT / "client" / ".env"

if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env cargado desde: {env_path}")
else:
    print("⚠️  No se encontró .env en la raíz del proyecto ni en client/.")
    print("   Asegúrate de que DATABASE_URL esté definida como variable de entorno.")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Fallback: construir desde variables de Supabase si están disponibles
    supabase_url = os.environ.get("VITE_SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("VITE_SUPABASE_ANON_KEY")
    
    if supabase_url and supabase_key:
        # Construir conexión PostgreSQL desde URL de Supabase
        # Formato: postgresql://postgres.[project-ref]:[service-role-key]@db.[project-ref].supabase.co:5432/postgres
        project_ref = supabase_url.replace("https://", "").replace(".supabase.co", "")
        DATABASE_URL = f"postgresql://postgres.{project_ref}:{supabase_key}@db.{project_ref}.supabase.co:5432/postgres"
        print("✅ DATABASE_URL construida desde credenciales de Supabase.")
    else:
        print("❌ DATABASE_URL no está definida y no hay credenciales de Supabase.")
        sys.exit(1)

# Vistas a consultar
VISTAS = [
    "business.v_employee_full_bynapo",
    "business.v_org_tree_bynapo",
    "business.mv_monthly_kpis_bynapo",
    "business.mv_demographics_agg",
]

# Archivo de salida
OUTPUT_DIR = PROJECT_ROOT / "docs" / "02-data-governance"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "03_data_samples.md"

# ---------------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------------

def get_connection():
    """Establece conexión con PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)


def get_column_types(cursor, schema, table):
    """Obtiene los tipos de dato de cada columna de una tabla/vista."""
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
    """
    cursor.execute(query, (schema, table))
    return cursor.fetchall()


def get_sample_rows(cursor, schema, table, limit=5):
    """Extrae registros aleatorios de una vista/tabla."""
    # Extraer solo el nombre sin schema para la consulta
    table_name = table
    
    query = f"""
        SELECT * FROM "{schema}"."{table_name}"
        ORDER BY RANDOM()
        LIMIT %s
    """
    cursor.execute(query, (limit,))
    
    # Obtener nombres de columnas
    colnames = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    return colnames, rows


def markdown_escape(value):
    """Escapa un valor para renderizado seguro en Markdown."""
    if value is None:
        return "*NULL*"
    s = str(value)
    # Escapar pipes en tablas markdown
    s = s.replace("|", "\\|")
    # Truncar si es muy largo
    if len(s) > 80:
        return s[:77] + "..."
    return s


def generate_md5(content):
    """Genera hash MD5 del contenido."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  GDH Analytics — Data Samples Export")
    print("=" * 60)
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    md_lines = []
    md_lines.append("# Data Samples Dump — Volcado de Muestras Reales")
    md_lines.append("")
    md_lines.append(f"> **Generado automáticamente:** {timestamp}")
    md_lines.append(f"> **Source:** Supabase — Schema `business`")
    md_lines.append("")
    md_lines.append("---")
    
    for vista in VISTAS:
        schema, table = vista.split(".")
        
        print(f"📊 Consultando {vista}...")
        
        # Obtener schema de columnas
        try:
            columns = get_column_types(cursor, schema, table)
        except Exception as e:
            md_lines.append("")
            md_lines.append(f"## {vista}")
            md_lines.append("")
            md_lines.append(f"[⚠️ Error obteniendo schema: {e}]")
            md_lines.append("")
            md_lines.append("---")
            continue
        
        # Obtener muestras
        try:
            colnames, rows = get_sample_rows(cursor, schema, table, limit=5)
        except Exception as e:
            if "does not exist" in str(e).lower() or "not found" in str(e).lower():
                md_lines.append("")
                md_lines.append(f"## {vista}")
                md_lines.append("")
                md_lines.append(f"[⚠️ Vista no encontrada en el schema business]")
                md_lines.append("")
                md_lines.append("---")
            else:
                md_lines.append("")
                md_lines.append(f"## {vista}")
                md_lines.append("")
                md_lines.append(f"[⚠️ Error consultando vista: {e}]")
                md_lines.append("")
                md_lines.append("---")
            print(f"   ⚠️ {vista}: {e}")
            continue
        
        if not rows:
            md_lines.append("")
            md_lines.append(f"## {vista}")
            md_lines.append("")
            md_lines.append(f"[⚠️ Vista existe pero no tiene registros]")
            md_lines.append("")
            md_lines.append("---")
            print(f"   ⚠️ {vista}: sin registros")
            continue
        
        # Generar sección Markdown
        md_lines.append("")
        md_lines.append(f"## {vista}")
        md_lines.append("")
        md_lines.append("### Schema")
        md_lines.append("")
        md_lines.append("| Columna | Tipo de Dato (SQL) |")
        md_lines.append("|---------|--------------------|")
        
        for col_name, data_type in columns:
            md_lines.append(f"| {col_name} | {data_type} |")
        
        md_lines.append("")
        md_lines.append(f"### Muestra ({len(rows)} registros)")
        md_lines.append("")
        
        # Header de la tabla
        md_lines.append("| " + " | ".join(colnames) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(colnames)) + " |")
        
        # Filas de datos
        for row in rows:
            escaped = [markdown_escape(v) for v in row]
            md_lines.append("| " + " | ".join(escaped) + " |")
        
        md_lines.append("")
        md_lines.append("---")
        print(f"   ✅ {vista}: {len(rows)} registros, {len(columns)} columnas")
    
    cursor.close()
    conn.close()
    
    # Agregar checksum
    md_lines.append("")
    
    # Generar contenido final
    content = "\n".join(md_lines)
    checksum = generate_md5(content)
    content += f"\n> **Checksum MD5:** {checksum}\n"
    
    # Escribir archivo
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    
    print()
    print("=" * 60)
    print(f"  ✅ Archivo generado: {OUTPUT_FILE}")
    print(f"  📋 Checksum MD5: {checksum}")
    print("=" * 60)


if __name__ == "__main__":
    main()
