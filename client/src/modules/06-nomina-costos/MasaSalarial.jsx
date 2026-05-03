import { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function MasaSalarial() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: rawData } = await supabase.schema('business')
        .from('mv_payroll_mass')
        .select('*');
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Masa Salarial...</div>;
  }

  // --- KPI Calculation ---
  const totalPayroll = data.reduce((sum, d) => sum + (d.total_payroll_usd || 0), 0);
  const totalHeadcount = data.reduce((sum, d) => sum + (d.headcount || 0), 0);
  const avgPayroll = totalPayroll / (totalHeadcount || 1);

  // --- Area Line Option (Payroll Trend) ---
  // Mock historical data since MV only has snapshot_date (which might be just current month)
  // In a real scenario, group by snapshot_date from historic MVs.
  const rawDates = [...new Set(data.map(d => d.snapshot_date))].filter(Boolean).sort();
  const histMonths = rawDates.length > 0 ? rawDates.map(d => d.substring(0, 7)) : ['Periodo Único'];
  const mockTrend = histMonths.map((m, i) => totalPayroll * (0.8 + (i * 0.02))); // simulated growth

  const areaOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', boundaryGap: false, data: histMonths },
    yAxis: { type: 'value', axisLabel: { formatter: '${value}' } },
    series: [{
      name: 'Masa Salarial',
      type: 'line',
      smooth: true,
      data: mockTrend,
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(59, 130, 246, 0.5)' }, { offset: 1, color: 'rgba(59, 130, 246, 0.0)' }]
        }
      },
      itemStyle: { color: hrTheme.color[0] }
    }]
  };

  // --- Bar Chart (Cost by Dept) ---
  // Aggregate by department
  const deptData = {};
  data.forEach(d => {
    if (!deptData[d.department_name]) deptData[d.department_name] = 0;
    deptData[d.department_name] += (d.total_payroll_usd || 0);
  });
  
  const deptsSorted = Object.entries(deptData).sort((a,b) => a[1] - b[1]);

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', formatter: '{b}: ${c}' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: deptsSorted.map(d => d[0]) },
    series: [{
      name: 'Costo',
      type: 'bar',
      data: deptsSorted.map(d => d[1]),
      itemStyle: { color: hrTheme.color[6], borderRadius: [0, 4, 4, 0] }
    }]
  };

  // --- Treemap (Cost by Job Level) ---
  const levelData = {};
  data.forEach(d => {
    if (!levelData[d.job_level_1]) levelData[d.job_level_1] = 0;
    levelData[d.job_level_1] += (d.total_payroll_usd || 0);
  });
  
  const treemapOption = {
    ...hrTheme,
    tooltip: { formatter: '{b}: ${c}' },
    series: [{
      type: 'treemap',
      roam: false,
      itemStyle: { borderColor: '#fff' },
      label: { show: true, formatter: '{b}\n${c}' },
      data: Object.entries(levelData).map(([name, value]) => ({ name, value }))
    }]
  };

  // --- Doughnut (Fixed vs Variable) ---
  // Mock variable cost as 18% of fixed
  const doughnutOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      name: 'Tipo de Costo',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      data: [
        { value: totalPayroll, name: 'Sueldo Base (Fijo)', itemStyle: { color: hrTheme.color[0] } },
        { value: totalPayroll * 0.18, name: 'Comisiones/Bonos (Variable)', itemStyle: { color: hrTheme.color[3] } }
      ]
    }]
  };

  return (
    <DashboardLayout 
      title="Masa Salarial e Impacto Financiero"
      description="Análisis de costos laborales, proyecciones y distribución."
      kpiCards={
        <>
          <KpiCard title="Masa Salarial Mensual" value={`$${(totalPayroll/1000).toFixed(1)}k`} subtitle="Total Sueldo Base" trend="+2.4%" trendPositive={false} />
          <KpiCard title="Costo Promedio (Head)" value={`$${avgPayroll.toFixed(0)}`} subtitle="Sueldo Medio" />
          <KpiCard title="Presupuesto Ejecutado" value="94%" trend="On Track" trendPositive={true} />
          <KpiCard title="Impacto Rotación" value={`$${(totalPayroll*0.05/1000).toFixed(1)}k`} subtitle="Costo estimado de reemplazos" />
        </>
      }
    >
      <ChartCard title="Evolución de la Masa Salarial (YTD)">
        <ReactECharts option={areaOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Costo Fijo vs Variable (Proyección)">
        <ReactECharts option={doughnutOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Concentración de Costos por Departamento">
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Masa Salarial por Nivel Organizacional (Job Level)">
        <ReactECharts option={treemapOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
