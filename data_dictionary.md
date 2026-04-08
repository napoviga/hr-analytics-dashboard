# 📖 Diccionario de Datos - HR Analytics (byNapo)

**Última Actualización:** 2024-05-20  
**Versión Pipeline:** v2.0 (Dual Stream: Legacy + Potenciado)

---

## 🏗️ Arquitectura de Datos

Este proyecto maneja dos flujos de datos independientes en la misma base de datos:

1.  **📦 Legacy IBM:** Datos estáticos originales (~1,470 registros). Usados para validación y estructuras base.
2.  **🚀 Potenciado (byNapo):** Simulación histórica mensual (2020-2026) con lógica de negocio (IPC, rotación, organigrama). Usado para el dashboard avanzado.

---

## 🥉 Capa 1: RAW (Bronce)

_Tablas de ingestión cruda. Columnas en formato `TEXT` para máxima tolerancia a cambios en el origen._

### 📋 Tabla: `raw.ibm_hr_landing`

_Fuente: Dataset estático original._
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `employeenumber` | TEXT | ID único del empleado. |
| `monthlyincome` | TEXT | Ingreso mensual actual. |
| `age` | TEXT | Edad del empleado. |
| `yearsatcompany` | TEXT | Antigüedad en años. |
| `attrition` | TEXT | ¿Abandonó la empresa? (Yes/No). |
| _(... otras columnas base de IBM ...)_ | TEXT | |

### 📋 Tabla: `raw.ibm_hr_monthly_snapshot_byNapo`

_Fuente: Generada por script `04_create_enhanced_dataset_byNapo.py`._
_Simulación mensual con ~4,000 - 8,000 empleados activos por corte._

| Columna                 | Tipo | Descripción                                |
| ----------------------- | ---- | ------------------------------------------ |
| `snapshot_date`         | TEXT | Fecha de corte del reporte (YYYY-MM-DD).   |
| `employee_id`           | TEXT | ID único en simulación.                    |
| `full_name`             | TEXT | Nombre completo sintético.                 |
| `employment_status`     | TEXT | `Active` o `Terminated`.                   |
| `monthly_salary_usd`    | TEXT | Salario dolarizado del mes.                |
| `manager_employee_id`   | TEXT | ID del jefe directo (Jerarquía).           |
| `tenure_months`         | TEXT | Antigüedad calculada al momento del corte. |
| `is_active_at_snapshot` | TEXT | Flag: `True` si trabaja en esa fecha.      |
| `salary_change_flag`    | TEXT | Flag: `1` si hubo aumento este mes.        |

---

## 🥇 Capa 2: BUSINESS (Oro)

_Vistas tipadas y listas para consumo de React/Vite y ECharts._

### 📊 Vista: `business.ibm_hr`

_Vista analítica del dataset original._
| Columna | Tipo | Origen | Uso |
|---------|------|--------|-----|
| `id` | INTEGER | `employeenumber` | ID numérico tipado. |
| `monthlyincome` | INTEGER | `monthlyincome` | Ingreso mensual. |
| `age` | INTEGER | `age` | Edad tipada. |
| `attrition` | TEXT | `attrition` | Rotación original. |

### 📊 Vista: `business.v_employee_full_byNapo`

_Vista Maestra Potenciada. Transforma `TEXT` a tipos nativos y calcula métricas derivadas._
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `snapshot_date` | DATE | Fecha de corte. |
| `employee_id` | INTEGER | ID del empleado. |
| `manager_employee_id`| INTEGER | ID del jefe directo. |
| `monthly_salary_usd` | NUMERIC(12,2) | Salario mensual en USD. |
| `tenure_months` | INTEGER | Antigüedad en meses (Calculado). |
| `is_active_at_snapshot`| BOOLEAN | Estado activo en esa fecha. |
| `salary_change_flag` | BOOLEAN | ¿Hubo cambio salarial? |
| `job_change_flag` | BOOLEAN | ¿Hubo cambio de puesto? |
| `processed_at` | TIMESTAMPTZ | Marca de tiempo del procesamiento. |

### 🌳 Vista: `business.v_org_tree_byNapo`

_Vista recursiva para renderizar el organigrama interactivo._
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `employee_id` | INTEGER | Nodo actual. |
| `manager_employee_id`| INTEGER | Nodo padre (Jefe). |
| `depth` | INTEGER | Nivel jerárquico (0 = CEO). |
| `echarts_node` | JSONB | Objeto JSON pre-formateado para ECharts. |

### 📈 Vista Materializada: `business.mv_monthly_kpis_byNapo`

_KPIs pre-calculados para carga instantánea del Dashboard (<50ms)._
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `snapshot_date` | DATE | Mes de referencia. |
| `headcount_active` | BIGINT | Total empleados activos. |
| `headcount_terminated`| BIGINT | Total empleados cesados en el mes. |
| `avg_salary_usd` | NUMERIC | Promedio salarial del periodo. |
| `attrition_rate_monthly_pct`| NUMERIC | % de rotación mensual. |
| `salary_change_rate_pct`| NUMERIC | % de empleados que recibieron aumento. |

### 📉 Vista: `business.v_kpi_summary_byNapo`

_Resumen global para tarjetas (KPI Cards) del dashboard._
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `total_headcount` | BIGINT | Fuerza laboral total. |
| `global_avg_salary_usd`| NUMERIC | Promedio global en USD. |
| `avg_tenure_months` | NUMERIC | Antigüedad promedio de la empresa. |
| `undesired_exits` | BIGINT | Conteo de bajas no deseadas (Renuncias clave). |

---

## 🧠 Lógica de Simulación (Script 04)

El dataset `byNapo` no es estático; evoluciona mes a mes aplicando reglas de negocio:

1.  **📈 Ajuste por IPC:** Automáticamente incrementa salarios en meses específicos según país (Ej: Perú en Feb, España en Ene).
2.  ** Rotación Natural:** 1% de la fuerza laboral es marcada como `Terminated` aleatoriamente cada mes.
3.  **👋 Contrataciones:** Se inyectan nuevos empleados (`Active`) para mantener el volumen base.
4.  **🛡️ Validación de Jerarquía:** Se asegura que todo empleado activo tenga un `manager_id` válido y existente en la base de datos (prevención de nodos huérfanos).

---

## 🔑 Permisos y Seguridad

- **Esquema `raw`**: Acceso restringido (Solo scripts de ingesta).
- **Esquema `business`**: Acceso público para el Dashboard (`anon`).
  - `GRANT SELECT ON ALL TABLES IN SCHEMA business TO anon;`
