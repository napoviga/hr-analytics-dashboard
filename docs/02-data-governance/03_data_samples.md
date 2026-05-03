# Data Samples Dump — Volcado de Muestras Reales

> **Generado automáticamente:** 2026-05-03T16:56:14Z
> **Source:** Supabase — Schema `business`

---

## business.v_employee_full_bynapo

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|
| snapshot_date | date |
| employee_id | integer |
| employee_code | text |
| full_name | text |
| gender | text |
| country_iso3 | text |
| department_name | text |
| job_role | text |
| job_level_1 | text |
| job_level_2 | text |
| employment_status | text |
| hire_date | date |
| termination_date | date |
| monthly_salary_local | numeric |
| currency_iso3 | text |
| fx_rate_to_usd | numeric |
| monthly_salary_usd | numeric |
| work_center_id | text |
| manager_employee_id | integer |
| tenure_months | numeric |
| is_active_at_snapshot | boolean |
| processed_at | timestamp with time zone |

### Muestra (5 registros)

| snapshot_date | employee_id | employee_code | full_name | gender | country_iso3 | department_name | job_role | job_level_1 | job_level_2 | employment_status | hire_date | termination_date | monthly_salary_local | currency_iso3 | fx_rate_to_usd | monthly_salary_usd | work_center_id | manager_employee_id | tenure_months | is_active_at_snapshot | processed_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021-04-30 | 1002 | EMP-01002 | Pedro Perez | Female | ESP | HR | HR Manager | Individual Contributor | Lead | Active | 2016-06-26 | *NULL* | 3237.67 | EUR | 3.5000 | 925.05 | WC-ESP | 2684 | 58 | True | 2026-05-03 16:56:15.474341+00:00 |
| 2025-04-30 | 4940 | EMP-04940 | Luis Martinez | Female | CHL | HR | Data Analyst | Individual Contributor | Junior | Active | 2021-12-31 | *NULL* | 2503.18 | CLP | 3.5000 | 715.20 | WC-CHL | 466 | 39 | True | 2026-05-03 16:56:15.474341+00:00 |
| 2022-03-31 | 4622 | EMP-04622 | Maria Martinez | Female | USA | Sales | Software Engineer | Individual Contributor | Junior | Active | 2021-04-30 | *NULL* | 2811.70 | USD | 3.5000 | 803.34 | WC-USA | 3617 | 11 | True | 2026-05-03 16:56:15.474341+00:00 |
| 2025-11-30 | 5978 | EMP-05978 | Ana Gomez | Male | MEX | Sales | Software Engineer | Individual Contributor | Junior | Terminated | 2024-02-29 | 2025-07-31 | 1274.77 | MXN | 3.5000 | 364.22 | WC-MEX | 2618 | 17 | False | 2026-05-03 16:56:15.474341+00:00 |
| 2025-05-31 | 1642 | EMP-01642 | Luis Martinez | Female | PER | Operations | Operator | Management | Senior | Active | 2016-05-03 | *NULL* | 2095.77 | PEN | 3.5000 | 598.79 | WC-PER | 2794 | 108 | True | 2026-05-03 16:56:15.474341+00:00 |

---

## business.v_org_tree_bynapo

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|
| employee_id | integer |
| full_name | text |
| job_role | text |
| job_level_1 | text |
| depth | integer |
| echarts_node | json |

### Muestra (5 registros)

| employee_id | full_name | job_role | job_level_1 | depth | echarts_node |
| --- | --- | --- | --- | --- | --- |
| 1960 | Luis Torres | CFO | Management | 8 | {'id': 1960, 'name': 'Luis Torres', 'value': 'Management', 'children': None} |
| 1831 | Ana Lopez | CTO | Individual Contributor | 7 | {'id': 1831, 'name': 'Ana Lopez', 'value': 'Individual Contributor', 'childre... |
| 3524 | Ana Perez | CFO | Individual Contributor | 5 | {'id': 3524, 'name': 'Ana Perez', 'value': 'Individual Contributor', 'childre... |
| 5248 | Lucia Lopez | Software Engineer | Individual Contributor | 10 | {'id': 5248, 'name': 'Lucia Lopez', 'value': 'Individual Contributor', 'child... |
| 2185 | Carlos Torres | Recruiter | Individual Contributor | 10 | {'id': 2185, 'name': 'Carlos Torres', 'value': 'Individual Contributor', 'chi... |

---

## business.mv_monthly_kpis_bynapo

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|

### Muestra (5 registros)

| snapshot_date | country_iso3 | headcount_active | headcount_terminated | avg_salary_usd | avg_tenure |
| --- | --- | --- | --- | --- | --- |
| 2020-03-31 | MEX | 667 | 4 | 955.25 | 36.8 |
| 2021-09-30 | PER | 796 | 71 | 915.63 | 45.9 |
| 2022-03-31 | USA | 717 | 85 | 848.70 | 50.5 |
| 2026-02-28 | ESP | 917 | 271 | 902.31 | 73.8 |
| 2021-04-30 | PER | 771 | 54 | 930.25 | 43.2 |

---

## business.mv_demographics_agg

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|

### Muestra (5 registros)

| snapshot_date | country_iso3 | department_name | job_level_1 | job_level_2 | work_center_id | total_hc | altas | bajas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021-04-30 | ESP | Finance | Individual Contributor | Senior | WC-ESP | 44 | 0 | 1 |
| 2025-02-28 | USA | IT | Management | Senior | WC-USA | 3 | 0 | 0 |
| 2024-07-31 | CHL | IT | Management | Lead | WC-CHL | 3 | 0 | 0 |
| 2025-06-30 | COL | Sales | Individual Contributor | Junior | WC-COL | 121 | 0 | 0 |
| 2022-07-31 | MEX | IT | Individual Contributor | Senior | WC-MEX | 34 | 0 | 0 |

---

> **Checksum MD5:** 094acefa205bf1c1b66520fa075d34db
