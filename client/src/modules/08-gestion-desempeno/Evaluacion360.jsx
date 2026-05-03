import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function Evaluacion360() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: rawData } = await supabase.schema('business')
        .from('mv_performance_summary')
        .select('*');
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Desempeño...</div>;
  }

  // --- KPI Calculation ---
  const totalReviews = data.reduce((acc, curr) => acc + (curr.total_reviews || 0), 0);
  const avgRating = data.reduce((acc, curr) => acc + ((curr.avg_rating || 0) * curr.total_reviews), 0) / (totalReviews || 1);
  const highPerformers = data.reduce((acc, curr) => acc + (curr.high_performers || 0), 0);
  const lowPerformers = data.reduce((acc, curr) => acc + (curr.low_performers || 0), 0);

  // --- Treemap (Top Performers by Dept/Country) ---
  const treemapData = data.filter(d => d.high_performers > 0).map(d => ({
    name: `${d.department_name} (${d.country_iso3})`,
    value: d.high_performers
  }));

  const treemapOption = {
    ...hrTheme,
    tooltip: { formatter: '{b}: {c} Top Performers' },
    series: [{
      type: 'treemap',
      roam: false,
      itemStyle: { borderColor: '#fff' },
      label: { show: true, formatter: '{b}\n{c}' },
      data: treemapData
    }]
  };

  // --- Radar Chart (Company Average Competencies) ---
  // Mock competencies since MV only has overall rating
  const radarOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    radar: {
      indicator: [
        { name: 'Liderazgo', max: 5 },
        { name: 'Ejecución', max: 5 },
        { name: 'Trabajo en Equipo', max: 5 },
        { name: 'Innovación', max: 5 },
        { name: 'Comunicación', max: 5 }
      ],
      center: ['50%', '45%'],
      radius: '65%'
    },
    series: [{
      name: 'Competencias',
      type: 'radar',
      data: [
        {
          value: [avgRating, avgRating + 0.2, avgRating - 0.1, avgRating + 0.3, avgRating - 0.2].map(v => Math.min(5, v.toFixed(1))),
          name: 'Promedio Compañía',
          itemStyle: { color: hrTheme.color[0] },
          areaStyle: { color: 'rgba(59, 130, 246, 0.2)' }
        }
      ]
    }]
  };

  // --- Stacked Bar Chart (Performance Distribution by Dept) ---
  const depts = [...new Set(data.map(d => d.department_name))];
  const stackedData = depts.map(dept => {
    const deptRows = data.filter(d => d.department_name === dept);
    const total = deptRows.reduce((a,c) => a + c.total_reviews, 0);
    const high = deptRows.reduce((a,c) => a + c.high_performers, 0);
    const low = deptRows.reduce((a,c) => a + c.low_performers, 0);
    const mid = total - high - low;
    return { name: dept, high, mid, low };
  });

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { bottom: 0 },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: depts },
    series: [
      { name: 'Alto Desempeño (>4)', type: 'bar', stack: 'total', data: stackedData.map(d => d.high), itemStyle: { color: hrTheme.color[1] } },
      { name: 'Cumple Expectativas', type: 'bar', stack: 'total', data: stackedData.map(d => d.mid), itemStyle: { color: hrTheme.color[0] } },
      { name: 'Bajo Desempeño (<2.5)', type: 'bar', stack: 'total', data: stackedData.map(d => d.low), itemStyle: { color: hrTheme.color[4] } }
    ]
  };

  // --- Gauge (PIP Percentage) ---
  const pipRate = totalReviews > 0 ? (lowPerformers / totalReviews) * 100 : 0;
  const gaugeOption = {
    ...hrTheme,
    series: [{
      type: 'gauge',
      startAngle: 180, endAngle: 0,
      center: ['50%', '75%'], radius: '90%',
      min: 0, max: 20,
      axisLine: {
        lineStyle: {
          width: 10,
          color: [[0.25, hrTheme.color[1]], [0.5, hrTheme.color[3]], [1, hrTheme.color[4]]] // Green < 5%, Yellow < 10%, Red > 10%
        }
      },
      pointer: { length: '12%', width: 20, offsetCenter: [0, '-60%'] },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      title: { offsetCenter: [0, '-10%'] },
      detail: { fontSize: 24, offsetCenter: [0, '0%'], formatter: '{value}%' },
      data: [{ value: pipRate.toFixed(1), name: 'En PIP' }]
    }]
  };

  // --- Scatter Plot (Self vs Manager Evaluation Mock) ---
  const scatterData = Array.from({length: 100}, () => {
    const manager = 2.5 + Math.random() * 2.5;
    const self = Math.min(5, manager + (Math.random() * 1.5 - 0.2)); // Usually self is slightly higher
    return [self.toFixed(2), manager.toFixed(2)];
  });

  const scatterOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: (p) => `Auto: ${p.value[0]}<br/>Manager: ${p.value[1]}` },
    xAxis: { type: 'value', name: 'Autoevaluación', min: 1, max: 5 },
    yAxis: { type: 'value', name: 'Evaluación Manager', min: 1, max: 5 },
    series: [{
      type: 'scatter',
      data: scatterData,
      itemStyle: { color: hrTheme.color[2], opacity: 0.6 }
    }]
  };

  return (
    <DashboardLayout 
      title="Evaluación 360 y Desempeño"
      description="Análisis de las revisiones de desempeño, distribución de puntajes y planes de mejora."
      kpiCards={
        <>
          <KpiCard title="Evaluaciones Completadas" value={totalReviews} trend="98%" trendPositive={true} />
          <KpiCard title="Puntaje Promedio" value={avgRating.toFixed(2)} subtitle="Escala 1 al 5" />
          <KpiCard title="High Performers" value={highPerformers} subtitle="Puntaje > 4.0" />
          <KpiCard title="En Plan de Mejora (PIP)" value={lowPerformers} subtitle="Puntaje < 2.5" trend="Atención" trendPositive={false} />
        </>
      }
    >
      <ChartCard title="Distribución de Desempeño por Área" fullWidth>
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Concentración de Top Performers">
        <ReactECharts option={treemapOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Competencias: Promedio Global vs Expectativa">
        <ReactECharts option={radarOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Dispersión: Autoevaluación vs Manager">
        <ReactECharts option={scatterOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Tasa de Empleados en PIP">
        <ReactECharts option={gaugeOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
