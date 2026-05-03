import React from 'react';
import ReactECharts from 'echarts-for-react';
import { DashboardLayout, KpiCard, ChartCard } from '../../components/DashboardLayout';
import { hrTheme } from '../../lib/echartsTheme';

export default function Overview({ data }) {
  if (!data || data.length === 0) {
    return <div className="p-12 text-center text-slate-500">Cargando métricas ejecutivas...</div>;
  }

  // Fallback seguro: Si faltan columnas clave, mostrar mensaje amistoso
  const sampleEmployee = data[0];
  if (!sampleEmployee || typeof sampleEmployee.monthly_salary_usd === 'undefined') {
    return (
      <DashboardLayout title="Dashboard C-Level" description="Visión ejecutiva integral de talento.">
        <div className="col-span-full p-12 text-center text-slate-500">Conectando con la vista ejecutiva de talento...</div>
      </DashboardLayout>
    );
  }

  // --- KPIs ---
  const totalEmployees = data.length;
  const activeEmployees = data.filter(e => e.is_active_at_snapshot).length;
  const attritionCount = totalEmployees - activeEmployees;
  const attritionRate = totalEmployees > 0 ? (attritionCount / totalEmployees) * 100 : 0;
  
  const totalPayroll = data.reduce((acc, e) => acc + (e.monthly_salary_usd || 0), 0);
  const avgIncome = totalPayroll / (totalEmployees || 1);

  // --- Chart 1: Attrition by Department (Treemap) ---
  const deptCounts = {};
  data.forEach(e => {
    const dept = e.department_name || 'N/A';
    if (!deptCounts[dept]) deptCounts[dept] = { total: 0, attrition: 0 };
    deptCounts[dept].total++;
    if (!e.is_active_at_snapshot) deptCounts[dept].attrition++;
  });

  const treemapData = Object.keys(deptCounts).map(dept => ({
    name: dept,
    value: deptCounts[dept].total,
    attritionRate: (deptCounts[dept].attrition / deptCounts[dept].total) * 100
  }));

  const treemapOption = {
    ...hrTheme,
    tooltip: { formatter: (p) => `${p.name}<br/>Total: ${p.value}<br/>Rotación: ${p.data.attritionRate.toFixed(1)}%` },
    series: [{
      type: 'treemap',
      roam: false,
      itemStyle: { borderColor: '#fff', gapWidth: 2 },
      label: { show: true, formatter: '{b}\n({c})', fontSize: 14 },
      data: treemapData,
      colorMappingBy: 'value',
      visualMap: {
        type: 'continuous',
        dimension: 2, 
        min: 0,
        max: 30,
        inRange: { color: ['#93c5fd', '#3b82f6', '#1e3a8a'] }
      }
    }]
  };

  // --- Chart 2: Experience vs Income (Scatter) ---
  const scatterData = data.slice(0, 300).map(e => [
    (e.tenure_months || 0) / 12,
    e.monthly_salary_usd || 0,
    e.job_role || 'N/A',
    !e.is_active_at_snapshot ? 1 : 0
  ]);

  const scatterOption = {
    ...hrTheme,
    tooltip: { trigger: 'item', formatter: (p) => `Tenure: ${p.value[0].toFixed(1)} años<br/>Ingreso: $${p.value[1]}<br/>Rol: ${p.value[2]}` },
    xAxis: { type: 'value', name: 'Años en la Compañía' },
    yAxis: { type: 'value', name: 'Salario Mensual (USD)' },
    series: [{
      type: 'scatter',
      data: scatterData,
      symbolSize: (val) => val[3] === 1 ? 12 : 8,
      itemStyle: {
        color: (p) => p.value[3] === 1 ? hrTheme.color[4] : hrTheme.color[0], // Red if attrition, Blue if active
        opacity: 0.6
      }
    }]
  };

  // --- Chart 3: Tenure Distribution (Area) ---
  const tenureBuckets = { '< 1 Año': 0, '1-3 Años': 0, '4-6 Años': 0, '7-10 Años': 0, '> 10 Años': 0 };
  data.forEach(e => {
    const years = (e.tenure_months || 0) / 12;
    if (years < 1) tenureBuckets['< 1 Año']++;
    else if (years <= 3) tenureBuckets['1-3 Años']++;
    else if (years <= 6) tenureBuckets['4-6 Años']++;
    else if (years <= 10) tenureBuckets['7-10 Años']++;
    else tenureBuckets['> 10 Años']++;
  });

  const areaOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: Object.keys(tenureBuckets), boundaryGap: false },
    yAxis: { type: 'value' },
    series: [{
      name: 'Distribución Antigüedad',
      type: 'line',
      smooth: true,
      data: Object.values(tenureBuckets),
      itemStyle: { color: hrTheme.color[1] },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(16, 185, 129, 0.4)' }, { offset: 1, color: 'rgba(16, 185, 129, 0.05)' }]
        }
      }
    }]
  };

  // --- Chart 4: Salary by Job Level (Bar) ---
  const validRoles = [...new Set(data.map(e => e.job_level_1).filter(r => r))].slice(0, 6);
  const roleRates = validRoles.map(role => {
    const roleData = data.filter(e => e.job_level_1 === role);
    return roleData.reduce((acc, e) => acc + (e.monthly_salary_usd || 0), 0) / (roleData.length || 1);
  });

  const barOption = {
    ...hrTheme,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'category', data: validRoles.map(r => r.split(' ')[0]), axisLabel: { interval: 0, rotate: 30 } }, 
    yAxis: { type: 'value', name: 'Salario Promedio' },
    series: [{
      name: 'Salario (USD)',
      type: 'bar',
      data: roleRates.map(v => Math.round(v)),
      itemStyle: { color: hrTheme.color[3], borderRadius: [4, 4, 0, 0] }
    }]
  };

  // --- Chart 5: Gender & Diversity (Donut) ---
  const genderCounts = {};
  data.forEach(e => {
    const g = e.gender || 'Other';
    genderCounts[g] = (genderCounts[g] || 0) + 1;
  });

  const donutOption = {
    ...hrTheme,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      name: 'Género',
      type: 'pie',
      radius: ['45%', '75%'],
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      data: Object.keys(genderCounts).map(k => ({ name: k, value: genderCounts[k] }))
    }]
  };

  // --- Chart 6: Overall Attrition Rate (Gauge) ---
  const gaugeOption = {
    ...hrTheme,
    series: [{
      type: 'gauge',
      startAngle: 180, endAngle: 0,
      min: 0, max: 50,
      radius: '100%',
      center: ['50%', '80%'],
      axisLine: {
        lineStyle: {
          width: 15,
          color: [[0.2, hrTheme.color[1]], [0.4, hrTheme.color[3]], [1, hrTheme.color[4]]] 
        }
      },
      pointer: { length: '50%', width: 8, offsetCenter: [0, '-20%'] },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: { fontSize: 30, offsetCenter: [0, '20%'], formatter: '{value}%', color: 'inherit' },
      data: [{ value: attritionRate.toFixed(1), name: 'Rotación Global' }]
    }]
  };

  return (
    <DashboardLayout 
      title="Dashboard C-Level"
      description="Visión ejecutiva integral de talento, demografía, riesgo y compensaciones."
      kpiCards={
        <>
          <KpiCard title="Headcount Activo" value={activeEmployees} subtitle="Colaboradores activos" trend="+2.4%" trendPositive={true} />
          <KpiCard title="Tasa de Fuga (Attrition)" value={`${attritionRate.toFixed(1)}%`} subtitle="Histórico general" trend="En riesgo" trendPositive={false} />
          <KpiCard title="Masa Salarial Mensual" value={`$${(totalPayroll / 1000).toFixed(0)}k`} subtitle="Gasto promedio" />
          <KpiCard title="Ingreso Promedio" value={`$${avgIncome.toFixed(0)}`} subtitle="Per cápita" trend="Estable" trendPositive={true} />
        </>
      }
    >
      <ChartCard title="Distribución de Headcount por Departamento" fullWidth>
        <ReactECharts option={treemapOption} style={{ height: '350px', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Matriz de Equidad: Antigüedad vs Ingreso">
        <ReactECharts option={scatterOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Curva de Antigüedad (Tenure en Años)">
        <ReactECharts option={areaOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>

      <ChartCard title="Salario Promedio por Nivel Jerárquico">
        <ReactECharts option={barOption} style={{ height: '100%', width: '100%' }} />
      </ChartCard>
      
      <div className="grid grid-cols-2 gap-6 h-full">
        <div className="bg-white border border-slate-100 rounded-2xl shadow-sm p-5 h-[350px]">
          <h3 className="text-lg font-bold text-slate-800 mb-4 tracking-tight">Diversidad de Género</h3>
          <ReactECharts option={donutOption} style={{ height: '250px', width: '100%' }} />
        </div>
        <div className="bg-white border border-slate-100 rounded-2xl shadow-sm p-5 h-[350px]">
          <h3 className="text-lg font-bold text-slate-800 mb-4 tracking-tight">Termómetro de Fuga</h3>
          <ReactECharts option={gaugeOption} style={{ height: '250px', width: '100%' }} />
        </div>
      </div>
    </DashboardLayout>
  );
}
