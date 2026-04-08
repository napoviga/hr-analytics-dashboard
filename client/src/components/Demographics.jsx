import React, { useState, useEffect } from 'react';
import { supabase } from '../lib/supabaseClient';
import ReactECharts from 'echarts-for-react'; // <-- IMPORTANTE: Nueva importación

const Demographics = () => {
  const [filters, setFilters] = useState({
    periodDate: '2026-03-31',
    country: '',
    department: '',
  });

  const [data, setData] = useState({ kpis: {}, gender_dist: [], level_dist: [], trend_12m: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDemographicsData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const { data: rpcData, error: rpcError } = await supabase.rpc('get_demographics_dashboard', {
          p_period_date: filters.periodDate,
          p_country: filters.country || null,
          p_department: filters.department || null,
        });

        if (rpcError) {
          throw rpcError;
        }

        setData(rpcData || { kpis: {}, gender_dist: [], level_dist: [], trend_12m: [] });
      } catch (err) {
        console.error('Error fetching demographics data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDemographicsData();
  }, [filters]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const renderKPIs = () => {
    const kpis = data?.kpis || {};
    const entries = Object.entries(kpis);

    if (entries.length === 0) {
      return Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="bg-white p-5 rounded-md shadow-sm border border-gray-200 flex flex-col justify-between">
          <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">KPI Placeholder {i + 1}</span>
          <span className="mt-2 text-3xl font-light text-gray-800">-</span>
        </div>
      ));
    }

    return entries.slice(0, 4).map(([key, value]) => (
      <div key={key} className="bg-white p-5 rounded-md shadow-sm border border-gray-200 flex flex-col justify-between">
        <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">
          {key.replace(/_/g, ' ')}
        </span>
        <span className="mt-2 text-3xl font-light text-gray-800">
          {value !== null && value !== undefined ? value.toLocaleString() : '-'}
        </span>
      </div>
    ));
  };

  // ==========================================
  // CONFIGURACIONES DE ECHARTS
  // ==========================================

  const getGenderOption = () => ({
    tooltip: { trigger: 'item' },
    legend: { bottom: '0%', left: 'center' },
    color: ['#3b82f6', '#ec4899', '#8b5cf6'], // Azul, Rosa, Morado
    series: [
      {
        name: 'Género',
        type: 'pie',
        radius: ['40%', '70%'], // Esto lo convierte en un gráfico de "Donut"
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
        label: { show: false, position: 'center' },
        emphasis: {
          label: { show: true, fontSize: '20', fontWeight: 'bold' }
        },
        labelLine: { show: false },
        data: data.gender_dist || []
      }
    ]
  });

  const getLevelOption = () => ({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value' },
    yAxis: { 
      type: 'category', 
      data: (data.level_dist || []).map(item => item.name),
      axisLabel: { interval: 0, width: 100, overflow: 'truncate' }
    },
    series: [
      {
        name: 'Headcount',
        type: 'bar',
        itemStyle: { color: '#10b981', borderRadius: [0, 4, 4, 0] }, // Verde estilo Power BI
        data: (data.level_dist || []).map(item => item.value)
      }
    ]
  });

  const getTrendOption = () => ({
    tooltip: { trigger: 'axis' },
    legend: { data: ['Activos', 'Bajas'], bottom: '0%' },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: { 
      type: 'category', 
      boundaryGap: false, 
      data: (data.trend_12m || []).map(item => item.month_lbl) 
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'Activos',
        type: 'line',
        smooth: true,
        itemStyle: { color: '#3b82f6' },
        areaStyle: { opacity: 0.1, color: '#3b82f6' },
        data: (data.trend_12m || []).map(item => item.active_hc)
      },
      {
        name: 'Bajas',
        type: 'line',
        smooth: true,
        itemStyle: { color: '#ef4444' }, // Rojo
        data: (data.trend_12m || []).map(item => item.terminated_hc)
      }
    ]
  });

  return (
    <div className="flex flex-col h-full bg-gray-50 p-6 space-y-6 animate-fade-in">
      {/* Top Filter Bar */}
      <div className="flex flex-wrap items-center gap-6 bg-white px-6 py-4 rounded-md shadow-sm border border-gray-200">
        <div className="flex flex-col">
          <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Periodo</label>
          <select name="periodDate" value={filters.periodDate} onChange={handleFilterChange} className="border border-gray-300 rounded text-sm px-3 py-1.5 focus:ring-1 focus:ring-blue-600 outline-none">
            <option value="2026-03-31">Marzo 2026</option>
            <option value="2026-02-28">Febrero 2026</option>
            <option value="2026-01-31">Enero 2026</option>
            <option value="2025-12-31">Diciembre 2025</option>
          </select>
        </div>
        <div className="flex flex-col">
          <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">País</label>
          <select name="country" value={filters.country} onChange={handleFilterChange} className="border border-gray-300 rounded text-sm px-3 py-1.5 focus:ring-1 focus:ring-blue-600 outline-none">
            <option value="">Todos los Países</option>
            <option value="USA">Estados Unidos</option>
            <option value="MEX">México</option>
            <option value="ESP">España</option>
            <option value="PER">Perú</option>
            <option value="COL">Colombia</option>
            <option value="CHL">Chile</option>
          </select>
        </div>
        <div className="flex flex-col">
          <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Departamento</label>
          <select name="department" value={filters.department} onChange={handleFilterChange} className="border border-gray-300 rounded text-sm px-3 py-1.5 focus:ring-1 focus:ring-blue-600 outline-none">
            <option value="">Todos los Departamentos</option>
            <option value="IT">IT</option>
            <option value="Sales">Ventas</option>
            <option value="HR">Recursos Humanos</option>
            <option value="Finance">Finanzas</option>
            <option value="Operations">Operaciones</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center p-12 bg-white rounded-md shadow-sm border border-gray-200">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <span className="mt-4 text-gray-500 font-medium">Cargando métricas...</span>
        </div>
      ) : error ? (
        <div className="flex-1 flex items-center justify-center p-12 bg-white rounded-md shadow-sm border border-red-200">
          <div className="text-red-500 font-medium">Error cargando datos: {error}</div>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {renderKPIs()}
          </div>

          {/* Gráficos ECharts */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-md shadow-sm border border-gray-200 p-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-2 uppercase tracking-wide">Distribución por Género</h3>
              <ReactECharts option={getGenderOption()} style={{ height: '300px', width: '100%' }} />
            </div>

            <div className="bg-white rounded-md shadow-sm border border-gray-200 p-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-2 uppercase tracking-wide">Distribución por Nivel</h3>
              <ReactECharts option={getLevelOption()} style={{ height: '300px', width: '100%' }} />
            </div>

            <div className="bg-white rounded-md shadow-sm border border-gray-200 p-4 lg:col-span-3">
              <h3 className="text-sm font-semibold text-gray-700 mb-2 uppercase tracking-wide">Evolución de Headcount (Últimos 12 Meses)</h3>
              <ReactECharts option={getTrendOption()} style={{ height: '350px', width: '100%' }} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Demographics;