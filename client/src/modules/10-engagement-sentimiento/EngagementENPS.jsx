import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import 'echarts-wordcloud'; // Import wordcloud extension
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function EngagementENPS() {
  const [enpsData, setEnpsData] = useState([]);
  const [sentimentData, setSentimentData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: enps } = await supabase.schema('business').from('mv_enps_trend').select('*');
      const { data: sentiment } = await supabase.schema('business').from('mv_sentiment_summary').select('*');
      
      if (enps) setEnpsData(enps);
      if (sentiment) setSentimentData(sentiment);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Engagement & eNPS...</div>;
  }

  // --- KPI Calculation ---
  const totalResponses = enpsData.reduce((acc, curr) => acc + (curr.total_responses || 0), 0);
  const totalPromoters = enpsData.reduce((acc, curr) => acc + (curr.promoters || 0), 0);
  const totalDetractors = enpsData.reduce((acc, curr) => acc + (curr.detractors || 0), 0);
  const globalEnps = totalResponses > 0 ? ((totalPromoters - totalDetractors) / totalResponses) * 100 : 0;

  // --- Gauge Chart (eNPS Score) ---
  const gaugeOption = {
    ...hrTheme,
    series: [{
      type: 'gauge',
      startAngle: 210, endAngle: -30,
      min: -100, max: 100,
      splitNumber: 4,
      itemStyle: {
        color: globalEnps > 30 ? hrTheme.color[1] : (globalEnps > 0 ? hrTheme.color[3] : hrTheme.color[4])
      },
      progress: { show: true, width: 20 },
      pointer: { show: false },
      axisLine: { lineStyle: { width: 20 } },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: {
        valueAnimation: true,
        formatter: '{value}',
        color: 'inherit',
        fontSize: 40,
        offsetCenter: [0, 0]
      },
      data: [{ value: globalEnps.toFixed(1), name: 'eNPS' }]
    }]
  };

  // --- Word Cloud (Feedback Sentiment) ---
  const words = [
    { name: 'Cultura', value: 1000 },
    { name: 'Liderazgo', value: 850 },
    { name: 'Salario', value: 600 },
    { name: 'Beneficios', value: 550 },
    { name: 'Flexibilidad', value: 500 },
    { name: 'Crecimiento', value: 400 },
    { name: 'Compañeros', value: 300 },
    { name: 'Innovación', value: 250 },
    { name: 'Estrés', value: 150 },
    { name: 'Reconocimiento', value: 450 }
  ];

  const wordCloudOption = {
    tooltip: { show: true },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center', top: 'center',
      width: '90%', height: '90%',
      sizeRange: [12, 40],
      rotationRange: [-45, 45],
      gridSize: 8,
      textStyle: {
        fontFamily: 'Inter',
        color: () => {
          // Random color from theme
          return hrTheme.color[Math.floor(Math.random() * hrTheme.color.length)];
        }
      },
      data: words
    }]
  };

  // --- Stacked Bar (Promoters vs Detractors by Dept) ---
  const depts = [...new Set(enpsData.map(d => d.department_name))];
  const stackedData = depts.map(dept => {
    const deptRows = enpsData.filter(d => d.department_name === dept);
    const promoters = deptRows.reduce((a,c) => a + c.promoters, 0);
    const detractors = deptRows.reduce((a,c) => a + c.detractors, 0);
    const total = deptRows.reduce((a,c) => a + c.total_responses, 0);
    const passives = total - promoters - detractors;
    return { name: dept, promoters, passives, detractors };
  });

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { bottom: 0 },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: depts },
    series: [
      { name: 'Promotores', type: 'bar', stack: 'total', data: stackedData.map(d => d.promoters), itemStyle: { color: hrTheme.color[1] } },
      { name: 'Pasivos', type: 'bar', stack: 'total', data: stackedData.map(d => d.passives), itemStyle: { color: '#cbd5e1' } }, // Slate 300
      { name: 'Detractores', type: 'bar', stack: 'total', data: stackedData.map(d => d.detractors), itemStyle: { color: hrTheme.color[4] } }
    ]
  };

  // --- Line Chart (Historical eNPS) ---
  const periods = [...new Set(enpsData.map(d => d.periodo))].sort();
  const enpsTrend = periods.map(p => {
    const pData = enpsData.filter(d => d.periodo === p);
    const pResp = pData.reduce((a,c) => a + c.total_responses, 0);
    const pProm = pData.reduce((a,c) => a + c.promoters, 0);
    const pDetr = pData.reduce((a,c) => a + c.detractors, 0);
    return pResp > 0 ? ((pProm - pDetr) / pResp) * 100 : 0;
  });

  const lineOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: periods },
    yAxis: { type: 'value', name: 'Score' },
    series: [{
      name: 'eNPS',
      type: 'line',
      smooth: true,
      data: enpsTrend.map(v => v.toFixed(1)),
      itemStyle: { color: hrTheme.color[2] },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(99, 102, 241, 0.4)' }, { offset: 1, color: 'rgba(99, 102, 241, 0.05)' }]
        }
      }
    }]
  };

  return (
    <DashboardLayout 
      title="Engagement y eNPS (Employee Net Promoter Score)"
      description="Análisis del sentimiento de los colaboradores, promotores de marca empleadora y clima laboral."
      kpiCards={
        <>
          <KpiCard title="eNPS Global" value={globalEnps.toFixed(1)} subtitle="Rango: -100 a 100" trend="Muy Bueno" trendPositive={true} />
          <KpiCard title="Participación" value={`${((totalResponses / 1500)*100).toFixed(0)}%`} subtitle="Tasa de respuesta" />
          <KpiCard title="Promotores" value={totalPromoters} subtitle="Puntaje 9 - 10" />
          <KpiCard title="Detractores" value={totalDetractors} subtitle="Puntaje 0 - 6" trend="Disminuyendo" trendPositive={true} />
        </>
      }
    >
      <ChartCard title="Score eNPS Actual">
        <ReactECharts option={gaugeOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Tópicos de Cultura (Word Cloud)">
        <ReactECharts option={wordCloudOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Evolución Histórica de eNPS" fullWidth>
        <ReactECharts option={lineOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Distribución de Promotores por Área" fullWidth>
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
