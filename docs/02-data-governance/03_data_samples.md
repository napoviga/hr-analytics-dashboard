# 📑 Volcado de Muestras de Datos (Data Samples Dump)

> **Generado el:** 2026-04-09 13:53:18
> **Propósito:** Proveer un contexto estricto de cinco registros por cada vista CORE para el análisis futuro y desarrollo frontend.

---

## 📊 business.v_employee_full_byNapo

### Esquema de Columnas y Tipos SQL

| column_name           | data_type                |
|:----------------------|:-------------------------|
| snapshot_date         | date                     |
| employee_id           | integer                  |
| employee_code         | text                     |
| full_name             | text                     |
| gender                | text                     |
| country_iso3          | text                     |
| department_name       | text                     |
| job_role              | text                     |
| job_level_1           | text                     |
| job_level_2           | text                     |
| employment_status     | text                     |
| hire_date             | date                     |
| termination_date      | date                     |
| monthly_salary_local  | numeric(12,2)            |
| currency_iso3         | text                     |
| fx_rate_to_usd        | numeric(10,4)            |
| monthly_salary_usd    | numeric(12,2)            |
| work_center_id        | text                     |
| manager_employee_id   | integer                  |
| tenure_months         | numeric                  |
| is_active_at_snapshot | boolean                  |
| processed_at          | timestamp with time zone |

### Muestra (TOP 5 Registros)

| snapshot_date   |   employee_id | employee_code   | full_name       | gender   | country_iso3   | department_name   | job_role     | job_level_1            | job_level_2   | employment_status   | hire_date   | termination_date   |   monthly_salary_local | currency_iso3   |   fx_rate_to_usd |   monthly_salary_usd | work_center_id   | manager_employee_id   |   tenure_months | is_active_at_snapshot   | processed_at                     |
|:----------------|--------------:|:----------------|:----------------|:---------|:---------------|:------------------|:-------------|:-----------------------|:--------------|:--------------------|:------------|:-------------------|-----------------------:|:----------------|-----------------:|---------------------:|:-----------------|:----------------------|----------------:|:------------------------|:---------------------------------|
| 2020-01-31      |             1 | EMP-00001       | Pedro Lopez     | Female   | PER            | Operations        | CEO          | Management             | Senior        | Active              | 2015-11-25  | NULL               |                3504.29 | PEN             |              3.5 |              1001.23 | WC-PER           | NULL                  |              50 | True                    | 2026-04-09 18:53:20.892190+00:00 |
| 2020-01-31      |             2 | EMP-00002       | Luis Torres     | Female   | COL            | IT                | Data Analyst | Management             | Lead          | Active              | 2015-09-28  | NULL               |                3019.04 | COP             |              3.5 |               862.58 | WC-COL           | 1027.0                |              52 | True                    | 2026-04-09 18:53:20.892190+00:00 |
| 2020-01-31      |             3 | EMP-00003       | Carlos Martinez | Female   | CHL            | Operations        | Operator     | Individual Contributor | Junior        | Active              | 2017-12-22  | NULL               |                4910.33 | CLP             |              3.5 |              1402.95 | WC-CHL           | 3330.0                |              25 | True                    | 2026-04-09 18:53:20.892190+00:00 |
| 2020-01-31      |             4 | EMP-00004       | Luis Torres     | Male     | ESP            | IT                | DevOps       | Individual Contributor | Senior        | Active              | 2016-01-05  | NULL               |                2369.88 | EUR             |              3.5 |               677.11 | WC-ESP           | 2187.0                |              48 | True                    | 2026-04-09 18:53:20.892190+00:00 |
| 2020-01-31      |             5 | EMP-00005       | Maria Rodriguez | Male     | USA            | HR                | Recruiter    | Individual Contributor | Junior        | Active              | 2014-09-22  | NULL               |                2419.51 | USD             |              3.5 |               691.29 | WC-USA           | 3254.0                |              64 | True                    | 2026-04-09 18:53:20.892190+00:00 |

---

## 📊 business.v_org_tree_byNapo

### Esquema de Columnas y Tipos SQL

| column_name   | data_type   |
|:--------------|:------------|
| employee_id   | integer     |
| full_name     | text        |
| job_role      | text        |
| job_level_1   | text        |
| depth         | integer     |
| echarts_node  | json        |

### Muestra (TOP 5 Registros)

|   employee_id | full_name       | job_role        | job_level_1            |   depth | echarts_node                                                                            |
|--------------:|:----------------|:----------------|:-----------------------|--------:|:----------------------------------------------------------------------------------------|
|             1 | Pedro Lopez     | CEO             | Management             |       0 | {'id': 1, 'name': 'Pedro Lopez', 'value': 'Management', 'children': None}               |
|            17 | Juan Rodriguez  | Logistics Coord | Management             |       0 | {'id': 17, 'name': 'Juan Rodriguez', 'value': 'Management', 'children': None}           |
|          3187 | Sofia Rodriguez | Sales Rep       | Management             |       0 | {'id': 3187, 'name': 'Sofia Rodriguez', 'value': 'Management', 'children': None}        |
|             8 | Ana Rodriguez   | Logistics Coord | Individual Contributor |       1 | {'id': 8, 'name': 'Ana Rodriguez', 'value': 'Individual Contributor', 'children': None} |
|           126 | Lucia Perez     | Recruiter       | Individual Contributor |       1 | {'id': 126, 'name': 'Lucia Perez', 'value': 'Individual Contributor', 'children': None} |

---

## 📊 business.mv_monthly_kpis_byNapo

### Esquema de Columnas y Tipos SQL

| column_name          | data_type   |
|:---------------------|:------------|
| snapshot_date        | date        |
| country_iso3         | text        |
| headcount_active     | bigint      |
| headcount_terminated | bigint      |
| avg_salary_usd       | numeric     |
| avg_tenure           | numeric     |

### Muestra (TOP 5 Registros)

| snapshot_date   | country_iso3   |   headcount_active |   headcount_terminated |   avg_salary_usd |   avg_tenure |
|:----------------|:---------------|-------------------:|-----------------------:|-----------------:|-------------:|
| 2020-01-31      | CHL            |                664 |                      0 |           923.46 |         33.4 |
| 2020-01-31      | COL            |                651 |                      0 |           926.83 |         35.6 |
| 2020-01-31      | ESP            |                702 |                      0 |           951.91 |         34.5 |
| 2020-01-31      | MEX            |                663 |                      0 |           960.79 |         35.2 |
| 2020-01-31      | PER            |                718 |                      0 |           914.4  |         34.2 |

---

## 📊 business.mv_demographics_agg

### Esquema de Columnas y Tipos SQL

| column_name     | data_type   |
|:----------------|:------------|
| snapshot_date   | date        |
| country_iso3    | text        |
| department_name | text        |
| job_level_1     | text        |
| job_level_2     | text        |
| work_center_id  | text        |
| total_hc        | bigint      |
| altas           | bigint      |
| bajas           | bigint      |

### Muestra (TOP 5 Registros)

| snapshot_date   | country_iso3   | department_name   | job_level_1            | job_level_2   | work_center_id   |   total_hc |   altas |   bajas |
|:----------------|:---------------|:------------------|:-----------------------|:--------------|:-----------------|-----------:|--------:|--------:|
| 2023-09-30      | CHL            | IT                | Management             | Lead          | WC-CHL           |          3 |       0 |       0 |
| 2022-05-31      | COL            | HR                | Management             | Junior        | WC-COL           |          6 |       0 |       0 |
| 2023-10-31      | MEX            | IT                | Management             | Senior        | WC-MEX           |          6 |       0 |       0 |
| 2025-03-31      | COL            | HR                | Individual Contributor | Senior        | WC-COL           |         35 |       0 |       1 |
| 2020-10-31      | COL            | Sales             | Management             | Senior        | WC-COL           |          6 |       0 |       1 |

---

