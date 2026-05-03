from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

# ──────────────────────────────────────────────────────────────
# LINEAGE MAP: MV → { script, submenus, components, charts }
# ──────────────────────────────────────────────────────────────
LINEAGE = {
    # M01 – Visión Ejecutiva
    'mv_alerts_anomalies': {
        'script': 'm01_vision_ejecutiva.py', 'module': 'M01',
        'submenus': ['Alertas & Anomalías'],
        'components': ['AlertasAnomalias.jsx'],
        'charts': ['Bar distribución', 'Pie concentración', 'Area tendencia', 'Scatter correlación']
    },
    'mv_salary_bands': {
        'script': 'm06_nomina_costos.py', 'module': 'M01/M06',
        'submenus': ['Benchmarking de Mercado', 'Equidad Interna', 'Estructura & Bandas Salariales'],
        'components': ['Benchmarking.jsx', 'EquidadInterna.jsx', 'Compensations.jsx'],
        'charts': ['Boxplot', 'Scatter salario/antigüedad', 'Radar benchmark', 'Bar comparativo']
    },
    # M02 – Reclutamiento
    'mv_recruitment_funnel': {
        'script': 'm02_reclutamiento.py', 'module': 'M02',
        'submenus': ['Eficiencia & Ciclos', 'Fit Score Predictivo', 'Auditoría de Sesgos', 'NPS del Candidato'],
        'components': ['EficienciaCiclos.jsx', 'FitScore.jsx', 'AuditoriaSesgos.jsx', 'NpsCandidato.jsx'],
        'charts': ['Funnel', 'Gauge SLA', 'Bar horizontal', 'Line trend']
    },
    'mv_time_to_fill': {
        'script': 'm02_reclutamiento.py', 'module': 'M02',
        'submenus': ['Calidad de Contratación'],
        'components': ['CalidadContratacion.jsx'],
        'charts': ['Scatter fit score', 'Radar competencias', 'Bar retención', 'Pie diversidad']
    },
    # M03 – Onboarding
    'mv_onboarding_status': {
        'script': 'm03_onboarding.py', 'module': 'M03',
        'submenus': ['Procesos Activos', 'Tiempo a Productividad'],
        'components': ['ProcesosActivos.jsx', 'TiempoProductividad.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    'mv_early_turnover': {
        'script': 'm03_onboarding.py', 'module': 'M03',
        'submenus': ['Rotación Temprana (<90d)'],
        'components': ['RotacionTemprana.jsx'],
        'charts': ['Line cohortes', 'Bar causas', 'Heatmap dept/mes', 'Pie por área']
    },
    # M04 – Ciclo de Vida
    'mv_lifecycle_cohorts': {
        'script': 'm04_ciclo_vida.py', 'module': 'M04',
        'submenus': ['Comportamiento de Grupos', 'Causalidad & Correlaciones'],
        'components': ['ComportamientoGrupos.jsx', 'CausalidadCorrelaciones.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    'mv_critical_moments': {
        'script': 'm04_ciclo_vida.py', 'module': 'M04',
        'submenus': ['Mapa de Momentos Críticos'],
        'components': ['MapaMomentos.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M05 – Fuerza Laboral
    'mv_demographics_agg': {
        'script': 'm05_fuerza_laboral.py', 'module': 'M05',
        'submenus': ['Demografía & Headcount'],
        'components': ['Demographics.jsx'],
        'charts': ['Pirámide', 'Heatmap bajas', 'Mapa países', 'Burbujas experiencia']
    },
    'mv_diversity_pyramid': {'script': 'm05_fuerza_laboral.py', 'module': 'M05', 'submenus': ['Demografía & Headcount'], 'components': ['Demographics.jsx'], 'charts': ['Pirámide']},
    'mv_bajas_heatmap': {'script': 'm05_fuerza_laboral.py', 'module': 'M05', 'submenus': ['Demografía & Headcount'], 'components': ['Demographics.jsx'], 'charts': ['Heatmap']},
    'mv_country_dist': {'script': 'm05_fuerza_laboral.py', 'module': 'M05', 'submenus': ['Demografía & Headcount'], 'components': ['Demographics.jsx'], 'charts': ['Mapa geográfico']},
    'mv_experience_bubbles': {'script': 'm05_fuerza_laboral.py', 'module': 'M05', 'submenus': ['Demografía & Headcount'], 'components': ['Demographics.jsx'], 'charts': ['Bubble chart']},
    # M06 – Nómina & Costos
    'mv_compa_ratio': {
        'script': 'm06_nomina_costos.py', 'module': 'M06',
        'submenus': ['Compa-Ratio vs. Mercado', 'Simulador de Escenarios'],
        'components': ['CompaRatio.jsx', 'SimuladorSalarial.jsx'],
        'charts': ['Gauge', 'Area histórico', 'Bar stacked', 'Pie compresión']
    },
    'mv_payroll_mass': {
        'script': 'm06_nomina_costos.py', 'module': 'M06',
        'submenus': ['Masa Salarial & Presupuesto'],
        'components': ['MasaSalarial.jsx'],
        'charts': ['Treemap', 'Bar payroll', 'Doughnut fijo/variable']
    },
    'mv_turnover_cost': {
        'script': 'm06_nomina_costos.py', 'module': 'M06',
        'submenus': ['Impacto Financiero de Rotación'],
        'components': ['ImpactoFinanciero.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M07 – Tiempo & Bienestar
    'mv_absenteeism': {
        'script': 'm07_tiempo_bienestar.py', 'module': 'M07',
        'submenus': ['Ausentismo & Permisos', 'Malla de Vacaciones', 'Optimización de Turnos'],
        'components': ['Ausentismo.jsx', 'MallaVacaciones.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    'mv_overtime_summary': {
        'script': 'm07_tiempo_bienestar.py', 'module': 'M07',
        'submenus': ['Horas Extra & Jornada'],
        'components': ['HorasExtra.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    'mv_sst_incidents': {
        'script': 'm07_tiempo_bienestar.py', 'module': 'M07',
        'submenus': ['Salud Ocupacional (SST)', 'Índice de Bienestar & Burnout'],
        'components': ['SaludOcupacional.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M08 – Desempeño
    'mv_performance_summary': {
        'script': 'm08_desempeno.py', 'module': 'M08',
        'submenus': ['Evaluación 360°', 'Avance de OKRs', 'Planes de Mejora (PIP)', 'Ranking & Top Performers'],
        'components': ['Evaluacion360.jsx', 'AvanceOKRs.jsx', 'PlanesMejora.jsx', 'RankingPerformers.jsx'],
        'charts': ['Bar stacked', 'Treemap', 'Radar competencias', 'Scatter auto/manager', 'Gauge PIP']
    },
    # M09 – Talento & Desarrollo
    'mv_nine_box': {
        'script': 'm09_talento_desarrollo.py', 'module': 'M09',
        'submenus': ['Matriz 9-Box', 'Continuidad & Sucesión', 'Movilidad Interna'],
        'components': ['MatrizNineBox.jsx', 'MapaSucesion.jsx', 'BrechasSkills.jsx'],
        'charts': ['Heatmap 3x3', 'Scatter', 'Bar por área', 'Pie proporciones']
    },
    'mv_training_roi': {
        'script': 'm09_talento_desarrollo.py', 'module': 'M09',
        'submenus': ['ROI de Capacitación', 'Ejecución de L&D'],
        'components': ['RoiCapacitacion.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M10 – Engagement
    'mv_enps_trend': {
        'script': 'm10_engagement.py', 'module': 'M10',
        'submenus': ['Engagement & eNPS', 'Diversidad & Inclusión (DEI)'],
        'components': ['EngagementENPS.jsx', 'DiversidadInclusion.jsx'],
        'charts': ['Gauge score', 'WordCloud', 'Line histórico', 'Bar stacked promotores']
    },
    'mv_sentiment_summary': {
        'script': 'm10_engagement.py', 'module': 'M10',
        'submenus': ['Heatmap de Engagement'],
        'components': ['HeatmapEngagement.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M11 – Compliance
    'mv_compliance_dashboard': {
        'script': 'm11_compliance.py', 'module': 'M11',
        'submenus': ['Cumplimiento Laboral', 'Relaciones Sindicales'],
        'components': ['CumplimientoLaboral.jsx', 'RelacionesSindicales.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M12 – Retención
    'mv_turnover_analysis': {
        'script': 'm12_retencion.py', 'module': 'M12',
        'submenus': ['Score Predictivo de Fuga', 'Benchmarking de Turnover'],
        'components': ['ScoreFuga.jsx', 'BenchmarkingTurnover.jsx'],
        'charts': ['Heatmap dept/nivel', 'Scatter riesgo/impacto', 'Treemap causas']
    },
    'mv_manager_turnover': {
        'script': 'm12_retencion.py', 'module': 'M12',
        'submenus': ['Correlación Manager-Fuga'],
        'components': ['CorrelacionManager.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    # M13 – Calidad de Datos
    'mv_monthly_kpis_bynapo': {
        'script': 'm13_calidad_datos.py', 'module': 'M13',
        'submenus': ['Log de Datos Maestros'],
        'components': ['LogDatosMaestros.jsx'],
        'charts': ['Bar', 'Pie', 'Area', 'Scatter']
    },
    'mv_ui_global_filters': {
        'script': 'm13_calidad_datos.py', 'module': 'M13',
        'submenus': ['Diccionario de Datos'],
        'components': ['DiccionarioDatos.jsx'],
        'charts': ['Bar', 'Pie']
    },
}

MODULE_ORDER = [
    'M01', 'M02', 'M03', 'M04', 'M05', 'M06',
    'M07', 'M08', 'M09', 'M10', 'M11', 'M12', 'M13'
]

MODULE_NAMES = {
    'M01': 'Visión Ejecutiva',
    'M02': 'Reclutamiento & Selección',
    'M03': 'Onboarding & Integración',
    'M04': 'Ciclo de Vida & Clústeres',
    'M05': 'Fuerza Laboral & Estructura',
    'M06': 'Nómina, Costos & Equidad',
    'M07': 'Tiempo, Asistencia & Bienestar',
    'M08': 'Gestión del Desempeño',
    'M09': 'Talento & Desarrollo',
    'M10': 'Engagement & Sentimiento',
    'M11': 'Compliance & Relaciones',
    'M12': 'Retención & Riesgo de Fuga',
    'M13': 'Calidad de Datos',
}

def get_row_counts():
    """Query live row counts from Supabase for all MVs."""
    counts = {}
    mv_list = pd.read_sql(
        "SELECT matviewname FROM pg_matviews WHERE schemaname = 'business' ORDER BY matviewname",
        engine
    )
    for mv in mv_list['matviewname']:
        try:
            n = pd.read_sql(f'SELECT COUNT(*) as c FROM business.{mv}', engine).iloc[0, 0]
            counts[mv] = int(n)
        except Exception:
            counts[mv] = -1
    return counts


def status_icon(rows):
    if rows < 0:
        return '❓'
    elif rows == 0:
        return '🔴'
    elif rows < 10:
        return '🔴'
    elif rows < 100:
        return '🟡'
    elif rows > 500_000:
        return '🟢⚠️'
    else:
        return '🟢'


def fmt_rows(rows):
    if rows < 0:
        return 'Error'
    elif rows == 0:
        return '**0**'
    elif rows >= 1_000_000:
        return f'{rows:,}'
    else:
        return f'{rows:,}'


def generate_lineage_md(row_counts: dict) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # ── Health summary ──────────────────────────────────────────
    ok = sum(1 for r in row_counts.values() if r >= 100)
    warn = sum(1 for r in row_counts.values() if 0 < r < 100)
    crit = sum(1 for r in row_counts.values() if r <= 0)

    # Build module → mv map (preserve module order)
    module_mv_map: dict[str, list] = {m: [] for m in MODULE_ORDER}
    unassigned = []
    for mv, info in LINEAGE.items():
        for mod in info['module'].split('/'):
            mod = mod.strip()
            if mod in module_mv_map:
                if mv not in [x['mv'] for x in module_mv_map[mod]]:
                    module_mv_map[mod].append({
                        'mv': mv,
                        'script': info['script'],
                        'submenus': info['submenus'],
                        'components': info['components'],
                        'charts': info['charts'],
                        'rows': row_counts.get(mv, -1),
                    })

    # Check for MVs in DB not in lineage
    for mv, rows in row_counts.items():
        if mv not in LINEAGE:
            unassigned.append((mv, rows))

    lines = []

    # Header
    lines += [
        f'# 🗺️ Dashboard Lineage — GDH Analytics',
        f'> **Auto-generado por `92_generate_lineage.py`** · Última ejecución: `{now}`',
        f'> Ejecutar `00_full_run_pipeline.py` para actualizar los row counts en tiempo real.',
        '',
        '---',
        '',
        '## 📊 Sección 1 — Salud del Pipeline',
        '',
        f'| 🟢 Datos OK (≥100 rows) | 🟡 Escasas (1–99 rows) | 🔴 Críticas (0 rows) | Total MVs |',
        f'|------------------------|------------------------|----------------------|-----------|',
        f'| **{ok}** | **{warn}** | **{crit}** | **{len(row_counts)}** |',
        '',
        '### 🚨 Prioridades de Enriquecimiento (ordenadas por urgencia)',
        '',
        '| # | MV | Rows | Módulo | Script a Intervenir |',
        '|---|-----|------|--------|---------------------|',
    ]
    priority_mvs = sorted(
        [(mv, r) for mv, r in row_counts.items() if r < 100],
        key=lambda x: x[1]
    )
    for i, (mv, rows) in enumerate(priority_mvs, 1):
        info = LINEAGE.get(mv, {})
        script = info.get('script', '—')
        module = info.get('module', '—')
        lines.append(f'| {i} | `{mv}` | {status_icon(rows)} {fmt_rows(rows)} | {module} | `{script}` |')

    # ── Section 2: Module accordion ─────────────────────────────
    lines += ['', '---', '', '## 📋 Sección 2 — Linaje por Módulo (Orden del Menú)', '',
              '> *Nota: Algunos componentes .jsx listados aquí son aspiracionales/planeados y pueden no existir aún en la carpeta client/src/modules/.*', '']

    for mod in MODULE_ORDER:
        mod_name = MODULE_NAMES.get(mod, mod)
        mv_list = module_mv_map.get(mod, [])
        lines += [f'### {mod} · {mod_name}', '']

        if not mv_list:
            lines += ['> *(Sin MVs mapeadas para este módulo)*', '']
            continue

        lines += [
            '| Submenú | Gráficas | MV Fuente | Rows | Script ETL |',
            '|---------|----------|-----------|------|------------|',
        ]
        for item in mv_list:
            charts_str = ', '.join(item['charts'][:3]) + ('…' if len(item['charts']) > 3 else '')
            for i, submenu in enumerate(item['submenus']):
                mv_col = f'`{item["mv"]}`' if i == 0 else ''
                rows_col = f'{status_icon(item["rows"])} {fmt_rows(item["rows"])}' if i == 0 else ''
                script_col = f'`{item["script"]}`' if i == 0 else ''
                charts_col = charts_str if i == 0 else ''
                lines.append(f'| {submenu} | {charts_col} | {mv_col} | {rows_col} | {script_col} |')
        lines.append('')

    # ── Section 3: Inverse lineage ──────────────────────────────
    lines += ['---', '', '## 🔗 Sección 3 — Lineage Inverso: MV → Submenús', '',
              '| MV | Rows | Script Creador | Submenús | Componentes .jsx (Planeados/Reales) |',
              '|----|------|---------------|----------|---------------------------------------|']

    for mv in sorted(row_counts.keys()):
        info = LINEAGE.get(mv)
        rows = row_counts[mv]
        if info:
            submenus = ', '.join(info['submenus'])
            comps = ', '.join(info['components'])
            lines.append(f'| `{mv}` | {status_icon(rows)} {fmt_rows(rows)} | `{info["script"]}` | {submenus} | {comps} |')
        else:
            lines.append(f'| `{mv}` | {status_icon(rows)} {fmt_rows(rows)} | *(sin mapeo)* | — | — |')

    # ── Section 4: Pending submenus ─────────────────────────────
    lines += [
        '', '---', '',
        '## ⚪ Sección 4 — Submenús Sin Componente (Pendientes)',
        '',
        '| Submenú | Módulo | ID Router | Acción Requerida |',
        '|---------|--------|-----------|-----------------|',
        '| Organigrama de Costos | M05 | org_costos | Crear OrgCostos.jsx usando mv_payroll_mass |',
        '| Distribución Geográfica | M05 | distribucion-geografica | Crear componente usando mv_country_dist |',
        '| Forecast de Dotación | M05 | forecast-dotacion | Crear MV predictiva en m05 + componente |',
        '',
        '---',
        f'*Auto-generado: {now} · Fuente: Supabase schema `business`*',
    ]

    return '\n'.join(lines)


def run():
    print('[Lineage] Generando Dashboard Lineage...')
    row_counts = get_row_counts()
    md = generate_lineage_md(row_counts)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'docs', '02-data-governance', '92_dashboard_lineage.md'
    )
    output_path = os.path.normpath(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f'[OK] Lineage actualizado -> {output_path}')

    # Print summary to console
    ok = sum(1 for r in row_counts.values() if r >= 100)
    crit = sum(1 for r in row_counts.values() if r <= 0)
    print(f'   OK: {ok} MVs con datos | CRITICAS: {crit} MVs vacias')


if __name__ == '__main__':
    run()
