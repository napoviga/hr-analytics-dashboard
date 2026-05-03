import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function EficienciaCiclos() {
  const [funnelData, setFunnelData] = useState([]);
  const [ttfData, setTtfData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: funnel } = await supabase.schema('business').from('mv_recruitment_funnel').select('*');
      const { data: ttf } = await supabase.schema('business').from('mv_time_to_fill').select('*');
      
      if (funnel) setFunnelData(funnel);
      if (ttf) setTtfData(ttf);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Eficiencia de Ciclos...</div>;
  }

  // --- KPI Calculation ---
  const totalApplied = funnelData.reduce((acc, curr) => acc + (curr.applied || 0), 0);
  const totalHired = funnelData.reduce((acc, curr) => acc + (curr.hired || 0), 0);
  const conversionRate = totalApplied > 0 ? ((totalHired / totalApplied) * 100) : 0;
  
  const avgTtf = ttfData.reduce((acc, curr) => acc + (curr.avg_days_to_fill || 0), 0) / (ttfData.length || 1);
  const avgNps = funnelData.reduce((acc, curr) => acc + (curr.avg_nps || 0), 0) / (funnelData.length || 1);

  // --- Funnel Chart ---
  const funnelStages = {
    'Aplicantes': funnelData.reduce((acc, c) => acc + c.applied, 0),
    'Filtro': funnelData.reduce((acc, c) => acc + c.screened, 0),
    'Entrevistas': funnelData.reduce((acc, c) => acc + c.interviewed, 0),
    'Ofertas': funnelData.reduce((acc, c) => acc + c.offered, 0),
    'Contratados': funnelData.reduce((acc, c) => acc + c.hired, 0),
  };

  const funnelOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: '{b} : {c} ({d}%)' },
    series: [
      {
        name: 'Embudo',
        type: 'funnel',
        left: '10%',
        width: '80%',
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 2,
        label: { show: true, position: 'inside', formatter: '{b}: {c}' },
        itemStyle: { borderColor: '#fff', borderWidth: 1 },
        data: Object.entries(funnelStages).map(([name, value], idx) => ({ 
          name, value, itemStyle: { color: hrTheme.color[idx] } 
        }))
      }
    ]
  };

  // --- Line Chart (Time to Fill History) ---
  const periods = [...new Set(ttfData.map(d => d.periodo))].sort();
  const ttfTrend = periods.map(p => {
    const dataPeriod = ttfData.filter(d => d.periodo === p);
    return dataPeriod.reduce((acc, c) => acc + c.avg_days_to_fill, 0) / (dataPeriod.length || 1);
  });

  const lineOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: periods },
    yAxis: { type: 'value', name: 'Días' },
    series: [{
      name: 'Time to Fill Promedio',
      type: 'line',
      smooth: true,
      data: ttfTrend.map(v => v.toFixed(1)),
      itemStyle: { color: hrTheme.color[2] },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(99, 102, 241, 0.4)' }, { offset: 1, color: 'rgba(99, 102, 241, 0.05)' }]
        }
      }
    }]
  };

  // --- Gauge Chart (SLA Cumplimiento) ---
  // Mocking SLA compliance based on TTF < 45 days
  const slaCompliance = avgTtf < 45 ? 85 : 65; 
  const gaugeOption = {
    ...hrTheme,
    series: [{
      type: 'gauge',
      progress: { show: true, width: 18 },
      axisLine: { lineStyle: { width: 18 } },
      axisTick: { show: false },
      splitLine: { length: 15, lineStyle: { width: 2, color: '#999' } },
      axisLabel: { distance: 25, color: '#999', fontSize: 10 },
      anchor: { show: true, showAbove: true, size: 25, itemStyle: { borderWidth: 10 } },
      title: { show: false },
      detail: { valueAnimation: true, fontSize: 30, offsetCenter: [0, '70%'], formatter: '{value}%' },
      data: [{ value: slaCompliance, name: 'SLA' }],
      itemStyle: { color: hrTheme.color[1] } // Emerald
    }]
  };

  // --- Horizontal Bar Chart (Bottlenecks) ---
  // Mock days per stage based on Total TTF
  const stagesDays = {
    'Sourcing': avgTtf * 0.2,
    'Screening': avgTtf * 0.15,
    'Interviews': avgTtf * 0.45,
    'Offer/BG Check': avgTtf * 0.2
  };
  
  const hBarOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', name: 'Días Promedio' },
    yAxis: { type: 'category', data: Object.keys(stagesDays) },
    series: [{
      name: 'Días',
      type: 'bar',
      data: Object.values(stagesDays).map(v => v.toFixed(1)),
      itemStyle: { color: hrTheme.color[3], borderRadius: [0, 4, 4, 0] } // Amber
    }]
  };

  return (
    <DashboardLayout 
      title="Eficiencia de Ciclos de Reclutamiento"
      description="Análisis del embudo de contratación, tiempos y cumplimiento de acuerdos de nivel de servicio (SLA)."
      kpiCards={
        <>
          <KpiCard title="Time to Fill" value={`${avgTtf.toFixed(0)} d`} subtitle="Días para cerrar vacante" trend="-2 d" trendPositive={true} />
          <KpiCard title="Conversión Total" value={`${conversionRate.toFixed(1)}%`} subtitle="Aplicantes a Contratados" />
          <KpiCard title="Candidatos Contratados" value={totalHired} subtitle="En el periodo evaluado" />
          <KpiCard title="NPS Candidato" value={avgNps.toFixed(1)} subtitle="Experiencia de entrevista (1-10)" trend="+0.4" trendPositive={true} />
        </>
      }
    >
      <ChartCard title="Embudo de Reclutamiento (Global)">
        <ReactECharts option={funnelOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Evolución Histórica: Time-to-Fill">
        <ReactECharts option={lineOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Cuellos de Botella (Días Promedio por Fase)">
        <ReactECharts option={hBarOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Cumplimiento SLA (TTF < 45 Días)">
        <ReactECharts option={gaugeOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
