import { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function CompaRatio() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      // The MV has granular row-level compa-ratio. We fetch all for current snapshot.
      // To prevent massive payloads, we limit, but 500-1000 is usually fine for frontend aggregation
      const { data: rawData } = await supabase.schema('business')
        .from('mv_compa_ratio')
        .select('*')
        .limit(1000);
      
      if (rawData) setData(rawData);
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas de Compa-Ratio...</div>;
  }

  // --- KPI Calculation ---
  const validData = data.filter(d => d.compa_ratio_pct !== null);
  const avgCompaRatio = validData.reduce((sum, d) => sum + d.compa_ratio_pct, 0) / (validData.length || 1);
  const belowRange = validData.filter(d => d.range_status === 'Below Range').length;
  const inRange = validData.filter(d => d.range_status === 'In Range').length;
  const aboveRange = validData.filter(d => d.range_status === 'Above Range').length;

  // --- Gauge Option (Average Compa-Ratio) ---
  const gaugeOption = {
    ...hrTheme,
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        center: ['50%', '75%'],
        radius: '90%',
        min: 60,
        max: 140,
        splitNumber: 8,
        axisLine: {
          lineStyle: {
            width: 10,
            color: [
              [0.25, hrTheme.color[4]], // Red (< 80)
              [0.75, hrTheme.color[1]], // Green (80-120)
              [1, hrTheme.color[3]]     // Yellow (> 120)
            ]
          }
        },
        pointer: { icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z', length: '12%', width: 20, offsetCenter: [0, '-60%'] },
        axisTick: { length: 12, lineStyle: { color: 'auto', width: 2 } },
        splitLine: { length: 20, lineStyle: { color: 'auto', width: 5 } },
        axisLabel: { color: '#464646', fontSize: 12, distance: -60 },
        title: { offsetCenter: [0, '-10%'], fontSize: 14 },
        detail: { fontSize: 24, offsetCenter: [0, '0%'], valueAnimation: true, formatter: '{value}%', color: 'inherit' },
        data: [{ value: avgCompaRatio.toFixed(1), name: 'CR Global' }]
      }
    ]
  };

  // --- Histogram / Line Area Option ---
  // We'll bin the compa-ratios in ranges of 10
  const bins = { '60-70':0, '70-80':0, '80-90':0, '90-100':0, '100-110':0, '110-120':0, '120-130':0, '130+':0 };
  validData.forEach(d => {
    const v = d.compa_ratio_pct;
    if(v<70) bins['60-70']++; else if(v<80) bins['70-80']++; else if(v<90) bins['80-90']++; 
    else if(v<100) bins['90-100']++; else if(v<110) bins['100-110']++; else if(v<120) bins['110-120']++; 
    else if(v<130) bins['120-130']++; else bins['130+']++;
  });
  
  const histOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: Object.keys(bins) },
    yAxis: { type: 'value' },
    series: [{
      data: Object.values(bins),
      type: 'line',
      smooth: true,
      areaStyle: { color: 'rgba(99, 102, 241, 0.2)' },
      itemStyle: { color: hrTheme.color[2] }
    }]
  };

  // --- Stacked Bar Option (Status by Department) ---
  const depts = [...new Set(validData.map(d => d.department_name))];
  const stackedSeries = ['Below Range', 'In Range', 'Above Range'].map((status, idx) => ({
    name: status,
    type: 'bar',
    stack: 'total',
    data: depts.map(dept => validData.filter(d => d.department_name === dept && d.range_status === status).length),
    itemStyle: { color: [hrTheme.color[4], hrTheme.color[1], hrTheme.color[3]][idx] }
  }));

  const stackedOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { show: true, bottom: 0 },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: depts },
    series: stackedSeries
  };

  // --- Pie Option ---
  const pieOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [
      {
        name: 'Distribución',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        data: [
          { value: belowRange, name: 'Below Range (<80%)', itemStyle: { color: hrTheme.color[4] } },
          { value: inRange, name: 'In Range (80-120%)', itemStyle: { color: hrTheme.color[1] } },
          { value: aboveRange, name: 'Above Range (>120%)', itemStyle: { color: hrTheme.color[3] } }
        ]
      }
    ]
  };

  return (
    <DashboardLayout 
      title="Análisis de Compa-Ratio"
      description="Evaluación del alineamiento salarial con los puntos medios de mercado y bandas."
      kpiCards={
        <>
          <KpiCard title="Compa-Ratio Global" value={`${avgCompaRatio.toFixed(1)}%`} trend="Óptimo" trendPositive={true} />
          <KpiCard title="Bajo Rango" value={belowRange} subtitle="< 80% de la banda" />
          <KpiCard title="En Rango" value={inRange} subtitle="80% - 120%" />
          <KpiCard title="Sobre Rango" value={aboveRange} subtitle="> 120% de la banda" />
        </>
      }
    >
      <ChartCard title="Compa-Ratio Promedio Global">
        <ReactECharts option={gaugeOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <ChartCard title="Distribución de Frecuencia (Curva de Campana)">
        <ReactECharts option={histOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Alineamiento por Departamento" fullWidth>
        <ReactECharts option={stackedOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Concentración de Compresión Salarial">
        <ReactECharts option={pieOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
    </DashboardLayout>
  );
}
