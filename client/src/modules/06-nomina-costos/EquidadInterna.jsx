import { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function EquidadInterna() {
  const [bandsData, setBandsData] = useState([]);
  const [scatterData, setScatterData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      // 1. Fetch Salary Bands (for Boxplot)
      const { data: bands } = await supabase.schema('business')
        .from('mv_salary_bands')
        .select('*');
        
      // 2. Fetch Employee Data (for Scatter)
      const { data: employees } = await supabase.schema('business')
        .from('v_employee_full_byNapo')
        .select('monthly_salary_usd, tenure_months, department_name, job_level_1')
        .eq('is_active_at_snapshot', true)
        .not('monthly_salary_usd', 'is', null)
        .limit(500);
        
      if (bands) setBandsData(bands);
      if (employees) setScatterData(employees);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Equidad Interna...</div>;
  }

  // --- KPI Calculation ---
  const globalMedian = bandsData.reduce((acc, curr) => acc + (curr.p50_median || 0), 0) / (bandsData.length || 1);
  const totalEmployees = bandsData.reduce((acc, curr) => acc + (curr.employee_count || 0), 0);

  // --- Boxplot Option ---
  // Aggregate by Job Level 1 for simplicity
  const jobLevels = [...new Set(bandsData.map(b => b.job_level_1))].sort();
  const boxplotData = jobLevels.map(jl => {
    const band = bandsData.find(b => b.job_level_1 === jl);
    if (!band) return [0,0,0,0,0];
    return [band.p10, band.p25, band.p50_median, band.p75, band.p90];
  });

  const boxplotOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'category', data: jobLevels },
    yAxis: { type: 'value', name: 'USD' },
    series: [
      {
        name: 'Banda Salarial',
        type: 'boxplot',
        data: boxplotData,
        itemStyle: { color: hrTheme.color[0], borderColor: hrTheme.color[2] }
      }
    ]
  };

  // --- Scatter Option ---
  const depts = [...new Set(scatterData.map(d => d.department_name))];
  const scatterSeries = depts.map((dept, idx) => ({
    name: dept,
    type: 'scatter',
    data: scatterData.filter(d => d.department_name === dept).map(d => [d.tenure_months, d.monthly_salary_usd]),
    itemStyle: { color: hrTheme.color[idx % hrTheme.color.length], opacity: 0.7 },
    symbolSize: 8
  }));

  const scatterOption = {
    ...hrTheme,
    tooltip: { 
      trigger: 'item',
      formatter: (params) => `${params.seriesName}<br/>Antigüedad: ${params.value[0]} meses<br/>Salario: $${params.value[1]}`
    },
    legend: { show: true, bottom: 0, type: 'scroll' },
    xAxis: { type: 'value', name: 'Antigüedad (Meses)', splitLine: { show: false } },
    yAxis: { type: 'value', name: 'Salario (USD)', splitLine: { lineStyle: { type: 'dashed' } } },
    series: scatterSeries
  };

  // --- Radar Option ---
  // Mock benchmark data based on actuals + 15%
  const radarOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    radar: {
      indicator: jobLevels.map(jl => ({ name: jl, max: Math.max(...boxplotData.map(b=>b[4])) * 1.2 })),
      center: ['50%', '45%'],
      radius: '65%'
    },
    series: [{
      name: 'Equidad vs Mercado',
      type: 'radar',
      data: [
        {
          value: jobLevels.map(jl => {
            const b = bandsData.find(x => x.job_level_1 === jl);
            return b ? b.avg_salary : 0;
          }),
          name: 'Promedio Interno',
          areaStyle: { color: 'rgba(59, 130, 246, 0.2)' }
        },
        {
          value: jobLevels.map(jl => {
            const b = bandsData.find(x => x.job_level_1 === jl);
            return b ? b.avg_salary * 1.15 : 0;
          }),
          name: 'Benchmark Mercado (+15%)',
          areaStyle: { color: 'rgba(16, 185, 129, 0.2)' }
        }
      ]
    }]
  };

  // --- Bar Option ---
  // Count by department
  const deptCounts = depts.map(dept => ({
    name: dept,
    value: bandsData.filter(b => b.department_name === dept).reduce((acc, curr) => acc + curr.employee_count, 0)
  })).sort((a,b) => b.value - a.value);

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: deptCounts.map(d => d.name).reverse() },
    series: [{
      type: 'bar',
      data: deptCounts.map(d => d.value).reverse(),
      itemStyle: { color: hrTheme.color[6], borderRadius: [0, 4, 4, 0] }
    }]
  };

  return (
    <DashboardLayout 
      title="Equidad Interna y Competitividad"
      description="Análisis de bandas salariales, compresión y benchmark de mercado."
      kpiCards={
        <>
          <KpiCard title="Salario Mediano Global" value={`$${globalMedian.toFixed(0)}`} subtitle="USD por mes" />
          <KpiCard title="Total Colaboradores" value={totalEmployees} subtitle="Evaluados en bandas" />
          <KpiCard title="Brecha Promedio vs Mercado" value="-15%" trend="Requiere Atención" trendPositive={false} />
          <KpiCard title="Niveles de Cargo" value={jobLevels.length} subtitle="Job Levels Activos" />
        </>
      }
    >
      <ChartCard title="Distribución Salarial por Nivel (P10 a P90)">
        <ReactECharts option={boxplotOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Salario vs Antigüedad (Riesgo de Compresión)">
        <ReactECharts option={scatterOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Competitividad: Interno vs Mercado">
        <ReactECharts option={radarOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Distribución de Headcount por Área">
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
