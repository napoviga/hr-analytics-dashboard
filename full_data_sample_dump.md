# 📊 Full Data Sample Dump — Esquema `business`

> **Generado:** 2026-04-07 17:33  
> **Vistas encontradas:** 3  
> **Registros por vista:** 5 (muestra)

---


## 📌 `business.mv_monthly_kpis_bynapo`

> **Tipo:** MATERIALIZED VIEW | **Columnas:** 6 | **Muestra:** 5 registros

### Esquema de columnas

| Columna | Tipo (Pandas) |
|---------|---------------|
| `snapshot_date` | `object` |
| `country_iso3` | `str` |
| `headcount_active` | `int64` |
| `headcount_terminated` | `int64` |
| `avg_salary_usd` | `float64` |
| `avg_tenure` | `float64` |

### Datos de muestra

| snapshot_date | country_iso3 | headcount_active | headcount_terminated | avg_salary_usd | avg_tenure |
| --- | --- | --- | --- | --- | --- |
| 2020-01-31 | CHL | 682 | 0 | 904.48 | 35.3 |
| 2020-01-31 | COL | 695 | 0 | 922.38 | 34.3 |
| 2020-01-31 | ESP | 679 | 0 | 947.95 | 34.2 |
| 2020-01-31 | MEX | 686 | 0 | 926.67 | 35.4 |
| 2020-01-31 | PER | 685 | 0 | 910.82 | 33.8 |

---


## 📌 `business.v_employee_full_bynapo`

> **Tipo:** VIEW | **Columnas:** 21 | **Muestra:** 5 registros

### Esquema de columnas

| Columna | Tipo (Pandas) |
|---------|---------------|
| `snapshot_date` | `object` |
| `employee_id` | `int64` |
| `employee_code` | `str` |
| `full_name` | `str` |
| `gender` | `str` |
| `country_iso3` | `str` |
| `department_name` | `str` |
| `job_role` | `str` |
| `job_level_1` | `str` |
| `job_level_2` | `str` |
| `employment_status` | `str` |
| `hire_date` | `object` |
| `termination_date` | `object` |
| `monthly_salary_local` | `float64` |
| `currency_iso3` | `str` |
| `fx_rate_to_usd` | `float64` |
| `monthly_salary_usd` | `float64` |
| `manager_employee_id` | `int64` |
| `tenure_months` | `float64` |
| `is_active_at_snapshot` | `bool` |
| `processed_at` | `datetime64[us, UTC]` |

### Datos de muestra

| snapshot_date | employee_id | employee_code | full_name | gender | country_iso3 | department_name | job_role | job_level_1 | job_level_2 | employment_status | hire_date | termination_date | monthly_salary_local | currency_iso3 | fx_rate_to_usd | monthly_salary_usd | manager_employee_id | tenure_months | is_active_at_snapshot | processed_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-01-31 | 1 | EMP-00001 | Maria Rodriguez | Female | COL | IT | CTO | Management | Junior | Active | 2015-03-05 | None | 3089.87 | COP | 3.5 | 882.82 | 2939 | 58.0 | True | 2026-04-07 22:33:18.995919+00:00 |
| 2020-01-31 | 2 | EMP-00002 | Maria Silva | Female | USA | HR | HR Specialist | Individual Contributor | Senior | Active | 2014-10-26 | None | 2154.33 | USD | 3.5 | 615.52 | 2157 | 63.0 | True | 2026-04-07 22:33:18.995919+00:00 |
| 2020-01-31 | 3 | EMP-00003 | Sofia Torres | Male | USA | Operations | Logistics Coord | Individual Contributor | Senior | Active | 2016-07-31 | None | 4479.46 | USD | 3.5 | 1279.85 | 2102 | 42.0 | True | 2026-04-07 22:33:18.995919+00:00 |
| 2020-01-31 | 4 | EMP-00004 | Luis Lopez | Female | COL | HR | HR Manager | Management | Junior | Active | 2016-10-25 | None | 2610.64 | COP | 3.5 | 745.9 | 394 | 39.0 | True | 2026-04-07 22:33:18.995919+00:00 |
| 2020-01-31 | 5 | EMP-00005 | Lucia Torres | Female | USA | HR | HR Specialist | Management | Senior | Active | 2016-07-14 | None | 2635.17 | USD | 3.5 | 752.91 | 3707 | 42.0 | True | 2026-04-07 22:33:18.995919+00:00 |

---


## 📌 `business.v_org_tree_bynapo`

> **Tipo:** VIEW | **Columnas:** 6 | **Muestra:** 0 registros

### Esquema de columnas

| Columna | Tipo (Pandas) |
|---------|---------------|
| `employee_id` | `object` |
| `full_name` | `object` |
| `job_role` | `object` |
| `job_level_1` | `object` |
| `depth` | `object` |
| `echarts_node` | `object` |

### Datos de muestra

| employee_id | full_name | job_role | job_level_1 | depth | echarts_node |
| --- | --- | --- | --- | --- | --- |

---
