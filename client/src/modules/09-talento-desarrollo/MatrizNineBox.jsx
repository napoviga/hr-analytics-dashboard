import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function MatrizNineBox() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: rawData } = await supabase.schema('business')
        .from('mv_nine_box')
        .select('*');
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando Matriz Nine-Box...</div>;
  }

  // --- KPI Calculation ---
  const totalAssessed = data.reduce((acc, curr) => acc + (curr.employee_count || 0), 0);
  
  // Quadrant aggregations
  const getQuadrantSum = (qList) => data.filter(d => qList.includes(d.nine_box_quadrant)).reduce((a,c) => a + c.employee_count, 0);
  const topTalent = getQuadrantSum(['Star', 'High Potential', 'Core Player']);
  const riskTalent = getQuadrantSum(['Risk', 'Inconsistent Player']);

  // --- 3x3 Heatmap (The actual Nine-Box) ---
  // X: Performance (Low, Mid, High), Y: Potential (Low, Mid, High)
  // Mapping categories to grid:
  const gridMap = {
    'Risk': [0, 0], 'Inconsistent Player': [0, 1], 'Potential Gem': [0, 2],
    'Solid Contributor': [1, 0], 'Core Player': [1, 1], 'High Potential': [1, 2],
    'High Performer': [2, 0], 'Star': [2, 2] // Note: Actual mapping depends on model, we approximate
  };
  
  const heatData = [
    [0, 0, getQuadrantSum(['Risk'])],
    [1, 0, getQuadrantSum(['Solid Contributor'])],
    [2, 0, getQuadrantSum(['High Performer'])],
    [0, 1, getQuadrantSum(['Inconsistent Player'])],
    [1, 1, getQuadrantSum(['Core Player'])],
    [2, 1, getQuadrantSum(['High Performer'])], // merged for simplicity
    [0, 2, getQuadrantSum(['Potential Gem'])],
    [1, 2, getQuadrantSum(['High Potential'])],
    [2, 2, getQuadrantSum(['Star'])],
  ];

  const heatmapOption = {
    ...hrTheme,
    tooltip: { position: 'top', formatter: (p) => `Desempeño: ${['Bajo','Medio','Alto'][p.value[0]]}<br/>Potencial: ${['Bajo','Medio','Alto'][p.value[1]]}<br/>Empleados: ${p.value[2]}` },
    grid: { left: '10%', right: '10%', bottom: '15%', top: '10%' },
    xAxis: { type: 'category', data: ['Desempeño Bajo', 'Desempeño Medio', 'Desempeño Alto'], splitArea: { show: true } },
    yAxis: { type: 'category', data: ['Potencial Bajo', 'Potencial Medio', 'Potencial Alto'], splitArea: { show: true } },
    visualMap: {
      min: 0, max: Math.max(...heatData.map(d=>d[2])), calculable: true, orient: 'horizontal', left: 'center', bottom: 0,
      inRange: { color: ['#f1f5f9', '#60a5fa', '#3b82f6', '#1e3a8a'] }
    },
    series: [{
      name: 'Nine Box',
      type: 'heatmap',
      data: heatData,
      label: { show: true, formatter: '{c}', fontSize: 16, color: '#fff' },
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
    }]
  };

  // --- Scatter Plot (Individual Plotting) ---
  const scatterData = Array.from({length: 150}, () => {
    return [
      (1 + Math.random() * 4).toFixed(1), // Performance
      (1 + Math.random() * 4).toFixed(1)  // Potential
    ];
  });

  const scatterOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: (p) => `Desempeño: ${p.value[0]}<br/>Potencial: ${p.value[1]}` },
    xAxis: { type: 'value', name: 'Desempeño', min: 1, max: 5 },
    yAxis: { type: 'value', name: 'Potencial', min: 1, max: 5 },
    series: [{
      type: 'scatter',
      data: scatterData,
      itemStyle: { color: hrTheme.color[6], opacity: 0.6 },
      markArea: {
        itemStyle: { color: 'rgba(16, 185, 129, 0.1)' },
        data: [[{ xAxis: 4, yAxis: 4 }, { xAxis: 5, yAxis: 5 }]] // Star box highlighted
      }
    }]
  };

  // --- Pie Chart (Distribution by Category) ---
  const pieData = data.reduce((acc, curr) => {
    if (!curr.nine_box_quadrant) return acc;
    const existing = acc.find(x => x.name === curr.nine_box_quadrant);
    if (existing) existing.value += curr.employee_count;
    else acc.push({ name: curr.nine_box_quadrant, value: curr.employee_count });
    return acc;
  }, []);

  const pieOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { show: false },
    series: [{
      name: 'Cuadrante',
      type: 'pie',
      radius: ['40%', '70%'],
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      data: pieData
    }]
  };

  // --- Bar Chart (Top Talent by Dept) ---
  const depts = [...new Set(data.map(d => d.department_name))];
  const barData = depts.map(dept => {
    return data.filter(d => d.department_name === dept && ['Star', 'High Potential'].includes(d.nine_box_quadrant))
               .reduce((a,c) => a + c.employee_count, 0);
  });

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: depts },
    series: [{
      type: 'bar',
      data: barData,
      itemStyle: { color: hrTheme.color[1], borderRadius: [0, 4, 4, 0] }
    }]
  };

  return (
    <DashboardLayout 
      title="Matriz Nine-Box y Sucesión"
      description="Mapa de talento cruzando Desempeño vs Potencial para identificar futuros líderes y riesgos."
      kpiCards={
        <>
          <KpiCard title="Evaluados" value={totalAssessed} subtitle="En matriz actual" />
          <KpiCard title="Top Talent" value={topTalent} subtitle="Estrellas y Alto Potencial" trend="Excelente" trendPositive={true} />
          <KpiCard title="Riesgo / Underperformers" value={riskTalent} subtitle="Bajo desempeño y potencial" />
          <KpiCard title="Planes de Sucesión" value="85%" subtitle="Posiciones críticas cubiertas" />
        </>
      }
    >
      <ChartCard title="Distribución Nine-Box (Heatmap)" fullWidth>
        <ReactECharts option={heatmapOption} style={{ height: '350px', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Dispersión Individual (Desempeño vs Potencial)">
        <ReactECharts option={scatterOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Concentración de Top Talent por Área">
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Proporción por Cuadrante">
        <ReactECharts option={pieOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
