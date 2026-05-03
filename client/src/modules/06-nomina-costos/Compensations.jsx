import ReactECharts from 'echarts-for-react';

export default function Compensations({ data }) {
  if (!data || data.length === 0) return null;

  // 1. Calcular KPIs
  const totalDailyRate = data.reduce((acc, emp) => acc + (emp.dailyrate || 0), 0);
  const avgDailyRate = parseInt(totalDailyRate / data.length);

  const totalAge = data.reduce((acc, emp) => acc + (emp.age || 0), 0);
  const avgAge = (totalAge / data.length).toFixed(1);

  // 2. Procesar Datos para Dispersión (Scatter Plot)
  // [x, y, id]
  const attritionYesData = data
    .filter(emp => emp.attrition === 'Yes')
    .map(emp => [emp.age, emp.dailyrate, emp.employeenumber]);

  const attritionNoData = data
    .filter(emp => emp.attrition === 'No')
    .map(emp => [emp.age, emp.dailyrate, emp.employeenumber]);

  // Configuración de ECharts
  const chartOption = {
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        return `<div class="font-sans text-sm">
                  <strong>ID:</strong> ${params.value[2]}<br/>
                  <strong>Edad:</strong> ${params.value[0]} años<br/>
                  <strong>Tarifa Diaria:</strong> $${params.value[1]}
                </div>`;
      }
    },
    grid: {
      left: '4%',
      right: '6%',
      bottom: '8%',
      containLabel: true
    },
    xAxis: {
      name: 'Edad',
      nameLocation: 'middle',
      nameGap: 30,
      type: 'value',
      nameTextStyle: { color: '#9ca3af', fontWeight: 'bold' },
      axisLabel: { color: '#9ca3af' },
      splitLine: { lineStyle: { type: 'dashed', color: '#374151' } }
    },
    yAxis: {
      name: 'Tarifa Diaria ($)',
      nameLocation: 'middle',
      nameGap: 50,
      type: 'value',
      nameTextStyle: { color: '#9ca3af', fontWeight: 'bold' },
      axisLabel: { color: '#9ca3af' },
      splitLine: { lineStyle: { color: '#374151' } }
    },
    legend: {
      data: ['Fuga (Sí)', 'Fuga (No)'],
      textStyle: { color: '#e5e7eb' },
      top: 'bottom',
      icon: 'circle'
    },
    series: [
      {
        name: 'Fuga (Sí)',
        type: 'scatter',
        itemStyle: { color: '#ef4444' }, // red-500
        data: attritionYesData
      },
      {
        name: 'Fuga (No)',
        type: 'scatter',
        itemStyle: { color: '#10b981' }, // green-500
        data: attritionNoData
      }
    ]
  };

  return (
    <div className="flex flex-col space-y-6">
      {/* KPIs Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 shadow-xl flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-1">Promedio Tarifa Diaria</p>
            <h3 className="text-4xl font-extrabold text-white">${avgDailyRate}</h3>
          </div>
          <div className="bg-yellow-900/50 p-4 rounded-full">
            <svg className="w-8 h-8 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 shadow-xl flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-1">Edad Promedio</p>
            <h3 className="text-4xl font-extrabold text-blue-400">{avgAge} <span className="text-2xl text-slate-500">años</span></h3>
          </div>
          <div className="bg-blue-900/50 p-4 rounded-full">
            <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Analítica Visual - Scatter Plot */}
      <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 shadow-xl">
        <h3 className="text-xl font-bold text-slate-200 mb-6">Correlación: Edad vs. Tarifa Diaria</h3>
        <ReactECharts 
          option={chartOption} 
          className="h-[400px] w-full"
          opts={{ renderer: 'svg' }}
        />
      </div>
    </div>
  );
}
