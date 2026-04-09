# 📖 Diccionario de Datos Oficial (Data Lineage & Dictionary)

> **Actualización:** Automatizada (Basada en la lectura del código fuente ETL)
> **Alcance:** Proyecto HR Analytics Dashboard (Arquitectura Medallion)

---

## 1. Arquitectura de Datos (Visión General)

El proyecto estructura sus bases de datos en torno al patrón **Medallion Architecture (Data Mesh)**, orquestado a través del pipeline secuencial de Python (`etl_pipeline/00_full_run_pipeline.py`). El ciclo de vida de un dato se resume de la siguiente forma:

1.  **Generación Sintética (`01_generate_synthetic_data`):** Un motor probabilístico forja data base aleatoria enriquecida (historización mensual, KPIs organizativos, sueldos y geografía). El output son archivos CSV.
2.  **Capa RAW - Bronce (`02_setup_raw_layer` & `03_ingest`):** Los CSVs son ingestados brutalmente en formato 100% `TEXT` puro. El objetivo es que la fase de ingesta jamás reviente por descalce de tipos.
3.  **Capa BUSINESS CORE - Plata/Oro (`04_setup_business`):** Transforma la tabla RAW al vuelo mediante Vistas SQL puras, fundiendo (casting) campos reales (INTEGER, NUMERIC, DATE) y normalizando el linaje maestro para la UI de manera transversal.
4.  **Capa DATA MARTS - Oro Analítica (`m05_fuerza_laboral`, etc):** Convierte el Core Plata en métricas ultrarrápidas mediante Vistas Materializadas y Funciones RPC altamente cacheadas para alimentar APIs y componentes gráficos Frontend.

---

## 2. Capa RAW (Bronce - Aterrizaje)

Instanciado en el script `02_setup_raw_layer.py`. Todas las columnas son de tipo **`TEXT`**.

### `raw."ibm_hr_monthly_snapshot_byNapo"`
La inmensa matriz fotográfica mensual (snapshotting temporal).

| Grupo Lógico | Columnas Principales |
| :--- | :--- |
| **Identificadores** | `employee_id`, `employee_code`, `full_name`, `snapshot_date` |
| **Demografía** | `gender`, `nationality_iso3`, `country_iso3`, `marital_status`, `dependents_count`, `education_level`, `education_status` |
| **Puestos** | `department_name`, `job_role`, `job_level_1`, `job_level_2` |
| **Ciclo Vida** | `employment_status`, `hire_date`, `termination_date`, `termination_reason_legal`, `turnover_classification_company`, `exit_interview_completed`, `regrettable_loss_flag` |
| **Compensación** | `monthly_salary_local`, `currency_iso3`, `fx_rate_to_usd`, `monthly_salary_usd`, `salary_change_flag`, `salary_change_reason_code` |
| **Jerarquía y Op** | `manager_employee_id`, `dotted_line_manager_id`, `work_center_id`, `home_lat`, `home_lon`, `work_modality`, `job_change_flag` |

### `raw."ibm_hr_change_reasons_byNapo"`
Diccionario crudo que tipifica cambios contractuales (Promociones, Despidos, IPC). Contiene:
- `reason_code`, `reason_name_es`, `reason_name_en`, `affects_salary`, `affects_job`, `active_flag`

---

## 3. Capa BUSINESS CORE (Plata/Oro Transversal)

Desplegada en el `04_setup_business_core.py`. Limpia la escoria y estandariza las métricas.

### `business.v_employee_full_byNapo` (La Vista Maestra)
Mantiene exactamente los campos de la capa cruda, pero convertidos (`::DATE`, `::NUMERIC`, `::INTEGER`). Agrega **Lógica de Negocio Crucial SQL**:

*   **`tenure_months`**: Se calcula midiendo la distancia en edad (`AGE`) entre *hire_date* y *snapshot_date*. Si la persona ya renunció, calcula la antigüedad exacto sobre su fecha de salida (*termination_date*).
*   **`is_active_at_snapshot`**: Etiqueta como `TRUE` a la plantilla si su estado es 'Active', o si su fecha de cese es posterior o nula dentro de ese mes cronológico.

### `business.mv_ui_global_filters` (Vista de Metadatos UI)
Genera el mega-JSON que alimenta la barra lateral de filtros globales en el React Frontend (`periods`, `countries`, `departments`, `job_levels_1`, `job_levels_2`, y `work_centers`) escaneando única y velozmente a `v_employee_full_byNapo`.

---

## 4. Capa DATA MARTS (Oro Específica / Módulo M05)

Desplegada en `m05_fuerza_laboral.py`. Optimizada puramente para lectura analítica en ráfaga.

### Tablas de Agregación Clave (Data Marts)
1. **`business.v_org_tree_byNapo`**: Un motor recursivo (`WITH RECURSIVE`) que rastrea desde el CEO hacia el último obrero para alimentar visores ECharts jerárquicos (Max 10 de profundidad). Retorna la carga en nodos estructurados (`echarts_node`).
2. **`business.mv_monthly_kpis_byNapo`**: Agregador macro que agrupa por Mes + País métricas base: `headcount_active`, `headcount_terminated`, promedio de salarios USD y tenures.
3. **`business.mv_demographics_agg`**: Corazón del Dashboard de KPI M05. Acumula las Altas y Bajas (`DATE_TRUNC('month')`).
4. **Vistas Avanzadas**: `mv_diversity_pyramid`, `mv_bajas_heatmap`, `mv_country_dist`, `mv_experience_bubbles`. Tablas pre-renderizadas que sirven como insumos directos a funciones RPC, aliviando la fatiga de cómputo frontend.

---

## 5. Reglas de Simulación (Lógica de Negocio inyectada)

Analizado desde el motor core probabilístico dictado en `01_generate_synthetic_data`.

*   **Ajuste Inflacionario (Salarial IPC):** El motor lee la matriz estática (`CONFIG["IPC_CONFIG"]`). Mes a mes por cada País dictamina el índice IPC histórico real (ej. `PER` 4% en el mes 2; `ESP` 3% en mes 1). Afecta transversalmente a todos los activos en su salario local.
*   **Deserción Natural Constante (Attrition):** Aplica una tasa de rotación fotográfica mensual del `0.5%`. Extrae aleatoriamente IDs para liquidarlos, etiquetándolas como Deserción Voluntaria `TER-VOL` (70%), Injustificado (20%) o Retiro (10%).
*   **Renacimiento Organizativo (Orphans Management):** Si un mánager cesa voluntariamente, el código busca quién era su equipo subalterno (`orphans`) y aleatoriza la re-asignación de un líder de equipo activo del organigrama.
*   **Anclaje del Inmortal (El CEO Root):** El ID de empleado #1 está codificado en duro (hardcoded) para ser el gerente Root (`CEO`) invariable de inyecciones de desgaste organizativo, garantizando que todo el `v_org_tree` tenga siempre una cabeza de la cual renderizar ECharts recursivamente.
*   **Sustrato Geográfico:** Combina los países base (`PER`, `CHL`, `COL`, `MEX`, `USA`, `ESP`) cruzándoles un mapa modal. A cada empleado se le otorgan Coordenadas Domiciliarias simuladas (desviación aleatoria desde la capital del país `lat` `lon`) limitadas al porcentaje global de Presencial/Híbrido/Remoto.
