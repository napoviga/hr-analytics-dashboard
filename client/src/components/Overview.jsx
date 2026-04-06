import ReactECharts from 'echarts-for-react';

export default function Overview({ data }) {
  if (!data || data.length === 0) return null;

  // 1. Process KPIs
  const totalEmployees = data.length;
  const attritionAlerts = data.filter(emp => emp.attrition === 'Yes').length;

  // 2. Process data for Chart (Distribution by Department)
  const deptCounts = data.reduce((acc, emp) => {
    const dept = emp.department || 'Desconocido';
    acc[dept] = (acc[dept] || 0) + 1;
    return acc;
  }, {});

  const departments = Object.keys(deptCounts);
  const employeeCounts = Object.values(deptCounts);

  // Configure ECharts Horizontal Bar Chart
  const chartOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#9ca3af' },
      splitLine: { lineStyle: { color: '#374151' } }
    },
    yAxis: {
      type: 'category',
      data: departments,
      axisLabel: { color: '#e5e7eb', fontWeight: 'bold' }
    },
    series: [
      {
        name: 'Empleados',
        type: 'bar',
        data: employeeCounts,
        itemStyle: {
          color: '#3b82f6', // Tailwind blue-500
          borderRadius: [0, 4, 4, 0]
        }
      }
    ]
  };

  return (
    <div className="flex flex-col space-y-6">
      {/* KPIs Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 shadow-xl flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-semibold uppercase tracking-wider mb-1">Total Colaboradores</p>
            <h3 className="text-4xl font-extrabold text-white">{totalEmployees}</h3>
          </div>
          <div className="bg-blue-900/50 p-4 rounded-full">
            <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5V4H2v16h5m10 0v-4H7v4m10 0H7M9 8h6M9 12h6" />
            </svg>
          </div>
        </div>
        
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 shadow-xl flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-semibold uppercase tracking-wider mb-1">Alertas de Fuga</p>
            <h3 className="text-4xl font-extrabold text-red-500">{attritionAlerts}</h3>
          </div>
          <div className="bg-red-900/50 p-4 rounded-full">
            <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Bar Chart */}
      <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 shadow-xl">
        <h3 className="text-xl font-bold text-gray-200 mb-6">Distribución por Departamento</h3>
        <ReactECharts 
          option={chartOption} 
          style={{ height: '350px', width: '100%' }} 
          opts={{ renderer: 'svg' }}
        />
      </div>
    </div>
  );
}
