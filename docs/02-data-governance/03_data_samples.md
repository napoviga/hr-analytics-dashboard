# Data Samples Dump — Volcado de Muestras Reales

> **Generado automáticamente:** 2026-04-11T06:15:50Z
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
| 2022-06-30 | 4400 | EMP-04400 | Lucia Martinez | Male | PER | HR | Software Engineer | Individual Contributor | Junior | Active | 2020-10-31 | *NULL* | 2007.42 | PEN | 3.5000 | 573.55 | WC-PER | 3005 | 19 | True | 2026-04-11 06:15:52.071831+00:00 |
| 2022-07-31 | 2279 | EMP-02279 | Ana Martinez | Male | ESP | HR | HR Specialist | Management | Senior | Active | 2015-01-12 | *NULL* | 4763.52 | EUR | 3.5000 | 1361.01 | WC-ESP | 2277 | 90 | True | 2026-04-11 06:15:52.071831+00:00 |
| 2024-03-31 | 5817 | EMP-05817 | Pedro Gomez | Male | ESP | IT | Software Engineer | Individual Contributor | Junior | Active | 2023-10-31 | *NULL* | 2571.28 | EUR | 3.5000 | 734.65 | WC-ESP | 2203 | 5 | True | 2026-04-11 06:15:52.071831+00:00 |
| 2026-03-31 | 5100 | EMP-05100 | Pedro Rodriguez | Male | CHL | Sales | CTO | Individual Contributor | Junior | Active | 2022-04-30 | *NULL* | 3314.53 | CLP | 3.5000 | 947.01 | WC-CHL | 414 | 47 | True | 2026-04-11 06:15:52.071831+00:00 |
| 2020-12-31 | 1909 | EMP-01909 | Pedro Perez | Male | PER | IT | Software Engineer | Individual Contributor | Lead | Active | 2018-02-02 | *NULL* | 2311.44 | PEN | 3.5000 | 660.41 | WC-PER | 758 | 34 | True | 2026-04-11 06:15:52.071831+00:00 |

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
| 5619 | Luis Lopez | Data Analyst | Individual Contributor | 2 | {'id': 5619, 'name': 'Luis Lopez', 'value': 'Individual Contributor', 'childr... |
| 464 | Ana Martinez | Recruiter | Individual Contributor | 10 | {'id': 464, 'name': 'Ana Martinez', 'value': 'Individual Contributor', 'child... |
| 2592 | Sofia Gomez | Sales Director | Individual Contributor | 7 | {'id': 2592, 'name': 'Sofia Gomez', 'value': 'Individual Contributor', 'child... |
| 5216 | Maria Rodriguez | CTO | Individual Contributor | 1 | {'id': 5216, 'name': 'Maria Rodriguez', 'value': 'Individual Contributor', 'c... |
| 2092 | Lucia Martinez | Ops Director | Individual Contributor | 5 | {'id': 2092, 'name': 'Lucia Martinez', 'value': 'Individual Contributor', 'ch... |

---

## business.mv_monthly_kpis_bynapo

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|

### Muestra (5 registros)

| snapshot_date | country_iso3 | headcount_active | headcount_terminated | avg_salary_usd | avg_tenure |
| --- | --- | --- | --- | --- | --- |
| 2020-09-30 | COL | 684 | 29 | 893.57 | 39.9 |
| 2024-01-31 | ESP | 849 | 165 | 916.20 | 62.9 |
| 2025-12-31 | MEX | 843 | 286 | 784.37 | 73.4 |
| 2025-03-31 | USA | 821 | 209 | 773.07 | 69.8 |
| 2023-06-30 | ESP | 823 | 142 | 907.34 | 59.1 |

---

## business.mv_demographics_agg

### Schema

| Columna | Tipo de Dato (SQL) |
|---------|--------------------|

### Muestra (5 registros)

| snapshot_date | country_iso3 | department_name | job_level_1 | job_level_2 | work_center_id | total_hc | altas | bajas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021-04-30 | CHL | IT | Individual Contributor | Senior | WC-CHL | 40 | 0 | 0 |
| 2020-06-30 | CHL | Finance | Management | Lead | WC-CHL | 2 | 0 | 0 |
| 2021-06-30 | USA | IT | Management | Lead | WC-USA | 4 | 0 | 0 |
| 2024-09-30 | MEX | Operations | Individual Contributor | Senior | WC-MEX | 38 | 0 | 0 |
| 2025-11-30 | CHL | Operations | Management | Lead | WC-CHL | 10 | 0 | 0 |

---

> **Checksum MD5:** 943e899e232b722814915e0fdbed8d30
