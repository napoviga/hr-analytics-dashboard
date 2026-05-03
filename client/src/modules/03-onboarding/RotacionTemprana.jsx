import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function RotacionTemprana() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      // mv_early_turnover contains columns: 
      // cohort_month, department_name, country_iso3, 
      // total_hires, early_leavers (left within 90 days), avg_days_to_leave
      const { data: rawData } = await supabase.schema('business')
        .from('mv_early_turnover')
        .select('*');
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Rotación Temprana...</div>;
  }

  // --- KPI Calculation ---
  const totalHires = data.reduce((acc, curr) => acc + (curr.total_hires || 0), 0);
  const totalLeavers = data.reduce((acc, curr) => acc + (curr.early_leavers || 0), 0);
  const avgDaysToLeave = data.reduce((acc, curr) => acc + (curr.avg_days_to_leave || 0), 0) / (data.filter(d => d.avg_days_to_leave).length || 1);
  const earlyTurnoverRate = totalHires > 0 ? (totalLeavers / totalHires) * 100 : 0;

  // --- Line Chart (Trend) ---
  const periods = [...new Set(data.map(d => d.cohort_month))].sort();
  const trendData = periods.map(p => {
    const periodData = data.filter(d => d.cohort_month === p);
    const hires = periodData.reduce((acc, c) => acc + c.total_hires, 0);
    const leavers = periodData.reduce((acc, c) => acc + c.early_leavers, 0);
    return hires > 0 ? ((leavers / hires) * 100).toFixed(1) : 0;
  });

  const lineOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', formatter: '{b}<br/>Tasa: {c}%' },
    xAxis: { type: 'category', data: periods },
    yAxis: { type: 'value', name: '% Rotación' },
    series: [{
      name: 'Rotación Temprana (< 90 días)',
      type: 'line',
      smooth: true,
      data: trendData,
      itemStyle: { color: hrTheme.color[4] }, // Red
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(239, 68, 68, 0.4)' }, { offset: 1, color: 'rgba(239, 68, 68, 0.05)' }]
        }
      }
    }]
  };

  // --- Bar Chart (Reasons - Mocked as not in MV) ---
  const reasons = { 'Expectativas no cumplidas': 35, 'Mejor oferta económica': 25, 'Cultura/Fit': 20, 'Liderazgo': 15, 'Otros': 5 };
  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', name: '% de Casos' },
    yAxis: { type: 'category', data: Object.keys(reasons).reverse() },
    series: [{
      name: '% de Bajas',
      type: 'bar',
      data: Object.values(reasons).reverse(),
      itemStyle: { color: hrTheme.color[3], borderRadius: [0, 4, 4, 0] }
    }]
  };

  // --- Heatmap (Risk by Manager/Dept - Mocked Structure) ---
  // We use department for rows and months for cols
  const heatDepts = [...new Set(data.map(d => d.department_name))].slice(0, 8); // top 8
  const heatData = [];
  heatDepts.forEach((dept, i) => {
    periods.forEach((period, j) => {
      const cell = data.find(d => d.department_name === dept && d.cohort_month === period);
      const val = cell && cell.total_hires > 0 ? (cell.early_leavers / cell.total_hires) * 100 : 0;
      heatData.push([j, i, val.toFixed(1)]);
    });
  });

  const heatmapOption = {
    ...hrTheme,
    tooltip: { position: 'top', formatter: (p) => `${heatDepts[p.value[1]]} (${periods[p.value[0]]})<br/>Rotación: ${p.value[2]}%` },
    grid: { left: '25%', right: '5%', bottom: '15%', top: '5%' },
    xAxis: { type: 'category', data: periods, splitArea: { show: true } },
    yAxis: { type: 'category', data: heatDepts, splitArea: { show: true } },
    visualMap: {
      min: 0, max: 30, calculable: true, orient: 'horizontal', left: 'center', bottom: '-5%',
      inRange: { color: ['#f1f5f9', '#fca5a5', '#ef4444', '#7f1d1d'] } // Slate to Dark Red
    },
    series: [{
      name: 'Rotación',
      type: 'heatmap',
      data: heatData,
      label: { show: true, color: '#000' },
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
    }]
  };

  // --- Pie Chart (By Role/Dept) ---
  const deptLeavers = {};
  data.forEach(d => {
    if (!deptLeavers[d.department_name]) deptLeavers[d.department_name] = 0;
    deptLeavers[d.department_name] += d.early_leavers;
  });

  const pieOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { type: 'scroll', bottom: 0 },
    series: [{
      name: 'Bajas por Dept.',
      type: 'pie',
      radius: ['40%', '70%'],
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      data: Object.entries(deptLeavers).filter(x => x[1] > 0).map(([name, value], idx) => ({
        name, value, itemStyle: { color: hrTheme.color[idx % hrTheme.color.length] }
      }))
    }]
  };

  return (
    <DashboardLayout 
      title="Análisis de Rotación Temprana (< 90 Días)"
      description="Evaluación de la retención durante el periodo de prueba y onboarding inicial."
      kpiCards={
        <>
          <KpiCard title="Tasa Global de Rotación Temprana" value={`${earlyTurnoverRate.toFixed(1)}%`} subtitle="De ingresos totales" trend="-0.8%" trendPositive={true} />
          <KpiCard title="Total Bajas (<90d)" value={totalLeavers} subtitle="En las cohortes activas" />
          <KpiCard title="Días Promedio a la Salida" value={`${avgDaysToLeave.toFixed(0)} d`} subtitle="Dentro de los 90 días" />
          <KpiCard title="Área de Mayor Riesgo" value={Object.entries(deptLeavers).sort((a,b)=>b[1]-a[1])[0]?.[0] || 'N/A'} subtitle="Acumula más bajas" />
        </>
      }
    >
      <ChartCard title="Evolución Histórica de Rotación Temprana (Cohortes)">
        <ReactECharts option={lineOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Causas Principales de Salida">
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Heatmap de Riesgo por Departamento" fullWidth>
        <ReactECharts option={heatmapOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Distribución de Bajas Tempranas por Área">
        <ReactECharts option={pieOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
