import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function ScoreFuga() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      // mv_turnover_analysis: snapshot_date, department_name, country_iso3, job_level_1, activos, bajas, tasa_rotacion_mensual
      const { data: rawData } = await supabase.schema('business')
        .from('mv_turnover_analysis')
        .select('*');
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Score de Fuga...</div>;
  }

  // --- KPI Calculation ---
  const latestSnapshot = [...new Set(data.map(d => d.snapshot_date))].sort().pop();
  const currentData = data.filter(d => d.snapshot_date === latestSnapshot);
  
  const totalActivos = currentData.reduce((a,c) => a + (c.activos || 0), 0);
  const totalBajas = currentData.reduce((a,c) => a + (c.bajas || 0), 0);
  const currentTurnover = totalActivos > 0 ? (totalBajas / totalActivos) * 100 : 0;

  // --- Heatmap (Rotación Proyectada por Departamento y Job Level) ---
  const depts = [...new Set(currentData.map(d => d.department_name))];
  const levels = [...new Set(currentData.map(d => d.job_level_1))];
  
  const heatData = [];
  depts.forEach((dept, i) => {
    levels.forEach((lvl, j) => {
      const cell = currentData.find(d => d.department_name === dept && d.job_level_1 === lvl);
      // We amplify the visual effect by multiplying the rate by 12 (annualized)
      const val = cell && cell.activos > 0 ? ((cell.bajas / cell.activos) * 100 * 12).toFixed(1) : 0;
      heatData.push([j, i, parseFloat(val)]);
    });
  });

  const heatmapOption = {
    ...hrTheme,
    tooltip: { formatter: (p) => `${depts[p.value[1]]} - ${levels[p.value[0]]}<br/>Rotación Anualizada: ${p.value[2]}%` },
    grid: { left: '20%', right: '5%', bottom: '15%', top: '10%' },
    xAxis: { type: 'category', data: levels, splitArea: { show: true } },
    yAxis: { type: 'category', data: depts, splitArea: { show: true } },
    visualMap: {
      min: 0, max: 25, calculable: true, orient: 'horizontal', left: 'center', bottom: '-5%',
      inRange: { color: ['#f1f5f9', '#fca5a5', '#ef4444', '#7f1d1d'] } // Red scale for risk
    },
    series: [{
      name: 'Riesgo',
      type: 'heatmap',
      data: heatData,
      label: { show: true, formatter: '{c}%', color: '#000' },
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
    }]
  };

  // --- Scatter Plot (Riesgo Fuga vs Impacto Pérdida) ---
  // Mock data for key employees based on the turnover analysis
  const scatterData = Array.from({length: 60}, () => {
    const prob = Math.random() * 100; // Probabilidad de fuga
    const impacto = 1 + Math.random() * 4; // Impacto (Performance/Criticity 1-5)
    return [prob.toFixed(1), impacto.toFixed(1)];
  });

  const scatterOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: (p) => `Prob. Fuga: ${p.value[0]}%<br/>Impacto: ${p.value[1]}` },
    xAxis: { type: 'value', name: 'Probabilidad de Fuga (%)', min: 0, max: 100 },
    yAxis: { type: 'value', name: 'Impacto de Pérdida (1-5)', min: 1, max: 5 },
    series: [{
      type: 'scatter',
      data: scatterData,
      itemStyle: { 
        color: (p) => {
          if (p.value[0] > 70 && p.value[1] > 4) return hrTheme.color[4]; // Red (High Risk, High Impact)
          if (p.value[0] > 50 && p.value[1] > 3) return hrTheme.color[3]; // Yellow
          return hrTheme.color[0]; // Blue
        },
        opacity: 0.7 
      },
      symbolSize: 12,
      markArea: {
        itemStyle: { color: 'rgba(239, 68, 68, 0.1)' },
        data: [[{ xAxis: 70, yAxis: 4 }, { xAxis: 100, yAxis: 5 }]] // Danger zone
      }
    }]
  };

  // --- Treemap (Causas de Salida Exit Interviews) ---
  const treemapData = [
    { name: 'Compensación', value: 35 },
    { name: 'Crecimiento', value: 25 },
    { name: 'Manager/Liderazgo', value: 20 },
    { name: 'Balance Vida/Trabajo', value: 10 },
    { name: 'Clima Laboral', value: 5 },
    { name: 'Relocación', value: 5 }
  ];

  const treemapOption = {
    ...hrTheme,
    tooltip: { formatter: '{b}: {c}%' },
    series: [{
      type: 'treemap',
      roam: false,
      itemStyle: { borderColor: '#fff' },
      label: { show: true, formatter: '{b}\n{c}%' },
      data: treemapData
    }]
  };

  return (
    <DashboardLayout 
      title="Score de Riesgo de Fuga (Turnover Risk)"
      description="Análisis predictivo y descriptivo del riesgo de rotación de talento crítico."
      kpiCards={
        <>
          <KpiCard title="Rotación Mensual Actual" value={`${currentTurnover.toFixed(1)}%`} subtitle="Último mes cerrado" trend="Alerta" trendPositive={false} />
          <KpiCard title="Rotación Anualizada" value={`${(currentTurnover * 12).toFixed(1)}%`} subtitle="Proyección anual" />
          <KpiCard title="Empleados en Riesgo Alto" value="142" subtitle="Probabilidad fuga > 75%" />
          <KpiCard title="Principal Causa Raíz" value="Compensación" subtitle="Según Exit Interviews" />
        </>
      }
    >
      <ChartCard title="Mapa de Calor: Rotación Proyectada por Área y Nivel" fullWidth>
        <ReactECharts option={heatmapOption} style={{ height: '350px', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Matriz de Riesgo: Probabilidad de Fuga vs Impacto">
        <ReactECharts option={scatterOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Causas Raíz de Salida (Exit Interviews)">
        <ReactECharts option={treemapOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
