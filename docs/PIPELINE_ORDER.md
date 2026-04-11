# 📋 Orden de Ejecución del Pipeline ETL y Prompts

> **Última actualización:** 2026-04-11
> **Propósito:** Documentar la secuencia lógica de ejecución de scripts ETL y prompts, sus dependencias cruzadas y los artefactos que generan.

---

## 🗺️ Resumen Visual del Flujo Completo

```
FASE 0: PIPELINE ETL (ejecución automática)
│  Comando: python etl_pipeline/00_full_run_pipeline.py
│
├─ 01_generate_synthetic_data.py
│  └─ Genera: data/ibm_hr_monthly_snapshot_byNapo.csv
│  └─ Genera: data/ibm_hr_change_reasons_byNapo.csv
│
├─ 02_setup_raw_layer.py
│  └─ Genera: raw."ibm_hr_monthly_snapshot_byNapo" (tabla en Supabase)
│  └─ Genera: raw."ibm_hr_change_reasons_byNapo" (tabla en Supabase)
│  └─ Depende de: 01 (tablas deben existir antes de ingest)
│
├─ 03_ingest_data.py
│  └─ Carga: CSV → raw tables
│  └─ Depende de: 02
│
├─ 04_setup_business_core.py
│  └─ Genera: business.v_employee_full_bynapo (vista)
│  └─ Genera: business.mv_ui_global_filters (vista materializada)
│  └─ Depende de: 03 (datos deben existir en raw)
│
├─ m05_fuerza_laboral.py
│  └─ Genera: 6 materialized views + 1 vista + 2 funciones RPC
│  └─ Depende de: 04 (v_employee_full_bynapo debe existir)
│
├─ 90_generate_data_inventory.py
│  └─ Genera: business.data_inventory (tabla en Supabase)
│  └─ Genera: docs/02-data-governance/02_supabase_metadata_inventory.md ✅ con timestamp ISO 8601
│  └─ Depende de: m05 (todas las vistas deben existir)
│
└─ 91_export_data_samples.py  (opcional, descomentar en orchestrator)
   └─ Genera: docs/02-data-governance/03_data_samples.md ✅ con timestamp ISO 8601
   └─ Depende de: m05 (vistas deben existir)

FASE 1: PROMPTS DE CONTEXTO (ejecutados por Qwen Code Terminal)
│
├─ Prompt 00: Blueprint & Context
│  └─ Comando: "Ejecuta el prompt 00 para generar el Blueprint"
│  └─ Genera: docs/03-ai-generated-content/01_project_blueprint.md ✅ con timestamp
│  └─ Requiere: Pipeline ETL completo (para tener datos reales que documentar)
│
├─ Prompt 01: Data Dictionary
│  └─ Comando: "Ejecuta el prompt 01 para generar el Data Dictionary"
│  └─ Genera: docs/03-ai-generated-content/02_data_dictionary.md ✅ con timestamp
│  └─ Requiere: Pipeline ETL completo (analiza scripts reales)
│
├─ Prompt 02: Audit & Linting
│  └─ Comando: "Ejecuta el prompt 02 para generar el Audit Report"
│  └─ Genera: docs/03-ai-generated-content/03_audit_report.md ✅ con timestamp
│  └─ Requiere: Blueprint + Data Dictionary generados + Pipeline completo
│  └─ ES SIEMPRE el último paso de auditoría
│
└─ Prompt 90: Update README
   └─ Comando: "Ejecuta el prompt 90 para actualizar el README"
   └─ Genera: README.md ✅ con timestamp y métricas actualizadas
   └─ Requiere: Pipeline ETL + Prompts 00-02 ejecutados (para tener contexto completo)
   └─ SE EJECUTA AL FINAL para tener documentación maestro actualizada

FASE 2: DOCUMENTOS DE GOBERNANZA (generados por scripts Python)
│
├─ Script 90: generate_data_inventory.py → 02_supabase_metadata_inventory.md
└─ Script 91: export_data_samples.py → 03_data_samples.md
```

---

## 📁 Estructura de Archivos por Carpeta

### `etl_pipeline/` — Scripts Ejecutables

| # | Archivo | Qué Hace | Artefacto Generado |
|---|---------|----------|-------------------|
| 00 | `00_full_run_pipeline.py` | Orquestador secuencial | Logs en consola con timestamps |
| 01 | `01_generate_synthetic_data.py` | Genera datos sintéticos HR | `data/*.csv` |
| 02 | `02_setup_raw_layer.py` | Crea tablas raw en Supabase | Tablas en `raw.*` |
| 03 | `03_ingest_data.py` | Carga CSV → raw tables | Datos en `raw.*` |
| 04 | `04_setup_business_core.py` | Crea vistas business core | `business.v_employee_full_bynapo`, `business.mv_ui_global_filters` |
| m05 | `m05_fuerza_laboral.py` | Data mart fuerza laboral | 6 MVs + 1 vista + 2 RPCs |
| 90 | `90_generate_data_inventory.py` | Inventario de metadatos | `02_supabase_metadata_inventory.md` ✅ timestamp ISO 8601 |
| 91 | `91_export_data_samples.py` | Export de samples | `03_data_samples.md` ✅ timestamp ISO 8601 |

### `docs/prompts/` — Instrucciones para Qwen Code Terminal

| # | Archivo | Qué Genera | Destino del Documento | Ejecución |
|---|---------|-----------|----------------------|-----------|
| 00 | `00. Blueprint & Context.md` | Contexto maestro del proyecto | `docs/03-ai-generated-content/01_project_blueprint.md` | "Ejecuta el prompt 00" |
| 01 | `01. Data Dictionary.md` | Diccionario de datos + linaje | `docs/03-ai-generated-content/02_data_dictionary.md` | "Ejecuta el prompt 01" |
| 02 | `02. Audit & Linting.md` | Reporte de auditoría completa | `docs/03-ai-generated-content/03_audit_report.md` | "Ejecuta el prompt 02" |
| 90 | `90_Update_README.md` | README.md actualizado con métricas | `README.md` (raíz del proyecto) | "Ejecuta el prompt 90" |

### `docs/02-data-governance/` — Documentos de Gobernanza (scripts Python)

| Archivo | Generado Por | Timestamp |
|---------|-------------|-----------|
| `02_supabase_metadata_inventory.md` | Script 90 | ✅ ISO 8601 UTC |
| `03_data_samples.md` | Script 91 | ✅ ISO 8601 UTC |

### `docs/03-ai-generated-content/` — Contexto AI (Qwen Code Terminal)

| Archivo | Generado Por | Timestamp |
|---------|-------------|-----------|
| `01_project_blueprint.md` | Prompt 00 (Qwen Code) | ✅ ISO 8601 UTC |
| `02_data_dictionary.md` | Prompt 01 (Qwen Code) | ✅ ISO 8601 UTC |
| `03_audit_report.md` | Prompt 02 (Qwen Code) | ✅ ISO 8601 UTC |

### `docs/01-product-specs/` — Especificaciones de Producto (manuales, referencia)

| Archivo | Propósito |
|---------|-----------|
| `01_navigation_sitemap.md` | Arquitectura de navegación del sistema |
| `02_view_logic_specs.md` | Especificaciones de cada vista/módulo |
| `03_design_system.md` | Guía de estilos Tailwind y patrones UI |

---

## 🔗 Matriz de Dependencias Cruzadas

| Paso | Tipo | Depende de | Genera para |
|------|------|-----------|------------|
| Script 01 | Python | Nada | Script 02 |
| Script 02 | Python | Script 01 | Script 03 |
| Script 03 | Python | Script 02 | Script 04 |
| Script 04 | Python | Script 03 | Script m05 |
| Script m05 | Python | Script 04 | Scripts 90, 91 |
| Script 90 | Python | Script m05 | Documentación |
| Script 91 | Python | Script m05 | Documentación |
| Prompt 00 | Qwen Code | Pipeline ETL completo | Prompt 02 |
| Prompt 01 | Qwen Code | Pipeline ETL completo | Prompt 02 |
| Prompt 02 | Qwen Code | Prompt 00 + Prompt 01 + Pipeline | Prompt 90 |
| Prompt 90 | Qwen Code | Todos los prompts anteriores + Pipeline completo | README.md actualizado |

---

## 🚀 Comandos de Ejecución

### Pipeline ETL Completo
```bash
python etl_pipeline/00_full_run_pipeline.py
```

### Script Individual
```bash
python etl_pipeline/90_generate_data_inventory.py
python etl_pipeline/91_export_data_samples.py
```

### Prompts (Qwen Code Terminal)
```
"Ejecuta el prompt 00 para generar el Blueprint"
"Ejecuta el prompt 01 para generar el Data Dictionary"
"Ejecuta el prompt 02 para generar el Audit Report"
"Ejecuta el prompt 90 para actualizar el README"
```

### Incluir Export Samples en el Pipeline Automático
Editar `00_full_run_pipeline.py` y descomentar:
```python
"91_export_data_samples.py",
```

---

## 📌 Reglas de Oro

1. **Orden obligatorio del pipeline:** 01 → 02 → 03 → 04 → m05 → 90 → 91
2. **Los prompts se ejecutan DESPUÉS del pipeline completo** — necesitan los scripts reales para analizar.
3. **El Prompt 02 (Audit) es SIEMPRE el último paso de auditoría** — requiere Blueprint + Data Dictionary.
4. **El Prompt 90 (README) es SIEMPRE el paso final** — requiere todos los prompts anteriores y el pipeline completo.
5. **Todos los documentos generados incluyen fecha y hora ISO 8601 UTC.**
6. **m05 es modular:** puedes agregar m06, m07, etc. entre m05 y 90 sin romper el pipeline.
7. **90 y 91 son post-pipeline:** dependen de que todas las vistas existan.

---

## 🔧 Nomenclatura

| Prefijo | Significado | Ejemplo |
|---------|------------|---------|
| `00` | Orquestador / Master | `00_full_run_pipeline.py` |
| `01-04` | Core del pipeline | `01_generate_synthetic_data.py` |
| `m05+` | Módulos de dominio | `m05_fuerza_laboral.py` |
| `90-99` | Post-pipeline / Metadata | `90_generate_data_inventory.py` |
| `00-02` (prompts) | Prompts para Qwen Code Terminal | `00. Blueprint & Context.md` |
| `90` (prompts) | Actualización de README | `90_Update_README.md` |

---

## ✅ Checklist de Ejecución Completa

- [ ] Pipeline ETL: 01→02→03→04→m05→90→91
- [ ] Prompt 00 → `01_project_blueprint.md` generado con timestamp
- [ ] Prompt 01 → `02_data_dictionary.md` generado con timestamp
- [ ] Prompt 02 → `03_audit_report.md` generado con timestamp
- [ ] Prompt 90 → `README.md` actualizado con timestamp y métricas

---

## 📊 Estado de Documentos Generados

| Documento | Ubicación | Timestamp | Última Generación |
|-----------|----------|-----------|------------------|
| Metadata Inventory | `docs/02-data-governance/02_supabase_metadata_inventory.md` | ✅ | 2026-04-11T06:25:54Z |
| Data Samples | `docs/02-data-governance/03_data_samples.md` | ✅ | 2026-04-11T06:15:50Z |
| Blueprint | `docs/03-ai-generated-content/01_project_blueprint.md` | ✅ | Pendiente |
| Data Dictionary | `docs/03-ai-generated-content/02_data_dictionary.md` | ✅ | Pendiente |
| Audit Report | `docs/03-ai-generated-content/03_audit_report.md` | ✅ | Pendiente |
| README | `README.md` (raíz del proyecto) | ✅ | Pendiente |
