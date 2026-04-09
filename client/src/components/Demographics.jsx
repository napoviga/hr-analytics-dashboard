import React, { useState, useEffect, useRef, useCallback } from 'react';
import { supabase } from '../lib/supabaseClient';
import ReactECharts from 'echarts-for-react';

// Paleta corporativa
const PALETTE = ['#3b82f6', '#ec4899', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

const Demographics = () => {
  const [filterOptions, setFilterOptions] = useState({
    periods: [], countries: [], departments: [],
    job_levels_1: [], job_levels_2: [], work_centers: []
  });
  const [filters, setFilters] = useState({
    periodDate: '', country: '', department: '',
    jobLevel1: '', jobLevel2: '', workCenter: '',
  });

  const [data, setData] = useState({ total_activos_card: null, altas_card: null, bajas_card: null });
  const [advancedData, setAdvancedData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const debounceRef = useRef(null);
  const abortRef = useRef(false);

  // ==========================================
  // 1. FETCH METADATA
  // ==========================================
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const { data, error } = await supabase.schema('business').from('mv_ui_global_filters').select('filter_options').single();
        if (error) throw error;
        const opts = data.filter_options || {};
        setFilterOptions({
          periods: opts.periods || [], countries: opts.countries || [],
          departments: opts.departments || [], job_levels_1: opts.job_levels_1 || [],
          job_levels_2: opts.job_levels_2 || [], work_centers: opts.work_centers || [],
        });
        if (opts.periods?.length > 0) {
          setFilters(prev => ({ ...prev, periodDate: opts.periods[0] }));
        }
      } catch (err) {
        console.error('Error fetching filter metadata:', err);
      }
    };
    fetchMetadata();
  }, []);

  // ==========================================
  // 2. FETCH RPCs EN PARALELO (Debounced)
  // ==========================================
  const buildRpcParams = (f) => ({
    p_period_date: f.periodDate,
    p_country: f.country || null,
    p_department: f.department || null,
    p_job_level_1: f.jobLevel1 || null,
    p_job_level_2: f.jobLevel2 || null,
    p_work_center: f.workCenter || null,
  });

  const fetchData = useCallback(async (currentFilters) => {
    abortRef.current = false;
    setLoading(true);
    setError(null);

    const params = buildRpcParams(currentFilters);

    try {
      const [cardsRes, advRes] = await Promise.allSettled([
        supabase.schema('business').rpc('get_demographics_dashboard', params),
        supabase.schema('business').rpc('get_advanced_demographics', params),
      ]);

      if (abortRef.current) return;

      if (cardsRes.status === 'fulfilled' && !cardsRes.value.error) {
        setData(cardsRes.value.data || { total_activos_card: null });
      } else {
        const err = cardsRes.status === 'rejected' ? cardsRes.reason : cardsRes.value.error;
        throw err;
      }

      if (advRes.status === 'fulfilled' && !advRes.value.error) {
        setAdvancedData(advRes.value.data);
      } else {
        console.warn('Advanced charts RPC failed, cards still shown:', advRes);
        setAdvancedData(null);
      }
    } catch (err) {
      if (!abortRef.current) {
        console.error('Error fetching demographics:', err);
        setError(err.message || String(err));
      }
    } finally {
      if (!abortRef.current) setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!filters.periodDate) return;
    abortRef.current = true;
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchData(filters), 600);
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [filters, fetchData]);

  // ==========================================
  // HELPERS
  // ==========================================
  const formatPeriodLabel = (dateStr) => {
    if (!dateStr) return '';
    const [year, month] = dateStr.split('-');
    return `${year}.${month}`;
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  // ==========================================
  // SNAPSHOT CARD CONFIG
  // ==========================================
  const getSparklineOption = (sparklineData) => {
    const labels = (sparklineData || []).map(d => d.label);
    const values = (sparklineData || []).map(d => d.value);
    return {
      grid: { top: 10, right: 10, bottom: 22, left: 36 },
      xAxis: { type: 'category', data: labels, axisLine: { show: false }, axisTick: { show: false },
        axisLabel: { fontSize: 9, color: '#9ca3af', interval: Math.max(0, Math.floor(labels.length / 6) - 1) } },
      yAxis: { type: 'value', show: false, min: (v) => Math.floor(v.min * 0.98) },
      tooltip: { trigger: 'axis', formatter: (p) => `${p[0].name}: ${p[0].value?.toLocaleString()}`, textStyle: { fontSize: 11 } },
      series: [{ name: 'Fuerza Laboral', type: 'line', data: values, smooth: true, symbol: 'circle', symbolSize: 3,
        lineStyle: { color: '#3b82f6', width: 2 }, itemStyle: { color: '#3b82f6' },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(59,130,246,0.18)' }, { offset: 1, color: 'rgba(59,130,246,0.01)' }] } },
      }],
    };
  };

  const renderDiffBadge = (diffAbs, diffPct) => {
    const pos = diffAbs >= 0;
    return (
      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${pos ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500'}`}>
        {pos ? '▲' : '▼'} {Math.abs(diffAbs)} ({diffPct > 0 ? '+' : ''}{diffPct}%)
      </span>
    );
  };

  const renderCard = (card, { colSpan = 1, accentColor = '#3b82f6', sparklineHeight = '80px' } = {}) => {
    if (!card) return (
      <div className={`${colSpan === 2 ? 'col-span-2' : ''} bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex items-center justify-center min-h-[240px]`}>
        <span className="text-gray-400 text-sm">Sin datos</span>
      </div>
    );

    const sparkOpt = (sd) => {
      const l = (sd || []).map(d => d.label), v = (sd || []).map(d => d.value);
      return {
        grid: { top: 8, right: 8, bottom: 20, left: 30 },
        xAxis: { type: 'category', data: l, axisLine: { show: false }, axisTick: { show: false },
          axisLabel: { fontSize: 8, color: '#9ca3af', interval: Math.max(0, Math.floor(l.length / 4) - 1) } },
        yAxis: { type: 'value', show: false, min: (val) => Math.floor(val.min * 0.95) },
        tooltip: { trigger: 'axis', formatter: (p) => `${p[0].name}: ${p[0].value?.toLocaleString()}`, textStyle: { fontSize: 10 } },
        series: [{ type: 'line', data: v, smooth: true, symbol: 'circle', symbolSize: 3,
          lineStyle: { color: accentColor, width: 2 }, itemStyle: { color: accentColor },
          areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: accentColor + '30' }, { offset: 1, color: accentColor + '05' }] } },
        }],
      };
    };

    return (
      <div className={`${colSpan === 2 ? 'col-span-2' : ''} bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden`}>
        <div className="px-5 pt-4 pb-1">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-widest">{card.title}</p>
          <p className="text-xs text-gray-400 mt-0.5">{card.current_month}</p>
        </div>
        <div className="px-5 flex items-end gap-3">
          <span className={`${colSpan === 2 ? 'text-5xl' : 'text-4xl'} font-extralight text-gray-900 tracking-tight leading-none`}>
            {card.current_value?.toLocaleString()}
          </span>
          {renderDiffBadge(card.diff_abs, card.diff_pct)}
        </div>
        <div className="px-5 mt-3 pb-2 border-b border-gray-100 space-y-1">
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span className="uppercase tracking-wide font-medium w-32">vs Mes Anterior</span>
            <span className="text-gray-400">({card.previous_month})</span>
            <span className="font-semibold text-gray-700">{card.previous_value?.toLocaleString()}</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span className="uppercase tracking-wide font-medium w-32">vs Año Anterior</span>
            <span className="text-gray-400">({card.yoy_month})</span>
            <span className="font-semibold text-gray-700">{card.yoy_value?.toLocaleString()}</span>
            {card.yoy_diff_abs !== 0 && (
              <span className={`text-xs font-bold ${card.yoy_diff_abs >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                ({card.yoy_diff_abs > 0 ? '+' : ''}{card.yoy_diff_pct}%)
              </span>
            )}
          </div>
        </div>
        <div className="px-1 pb-1">
          <ReactECharts option={colSpan === 2 ? getSparklineOption(card.sparkline_data) : sparkOpt(card.sparkline_data)} style={{ height: sparklineHeight, width: '100%' }} opts={{ renderer: 'svg' }} />
        </div>
      </div>
    );
  };

  // ==========================================
  // ADVANCED CHARTS - ECharts Configs
  // ==========================================

  // Q1: Pirámide de Diversidad
  const getDiversityPyramidOption = () => {
    const raw = advancedData?.diversity_pyramid || [];
    const levels = [...new Set(raw.map(r => r.level))];
    const maleData = levels.map(lv => { const found = raw.find(r => r.level === lv && r.gender === 'Male'); return found ? found.value : 0; });
    const femaleData = levels.map(lv => { const found = raw.find(r => r.level === lv && r.gender === 'Female'); return found ? -found.value : 0; });

    return {
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' },
        formatter: (params) => params.map(p => `${p.seriesName}: ${Math.abs(p.value).toLocaleString()}`).join('<br/>'),
      },
      legend: { data: ['Male', 'Female'], bottom: 0, textStyle: { fontSize: 11 } },
      grid: { left: '3%', right: '4%', bottom: '12%', top: '4%', containLabel: true },
      xAxis: { type: 'value', axisLabel: { formatter: (v) => Math.abs(v) } },
      yAxis: { type: 'category', data: levels, axisTick: { show: false },
        axisLabel: { fontSize: 11, color: '#374151' } },
      series: [
        { name: 'Male', type: 'bar', stack: 'total', data: maleData, itemStyle: { color: '#3b82f6', borderRadius: [0, 4, 4, 0] } },
        { name: 'Female', type: 'bar', stack: 'total', data: femaleData, itemStyle: { color: '#ec4899', borderRadius: [4, 0, 0, 4] } },
      ],
    };
  };

  // Q2: Heatmap de Bajas
  const getTurnoverHeatmapOption = () => {
    const raw = advancedData?.turnover_heatmap || [];
    const months = [...new Set(raw.map(r => r.month_label))].sort();
    const depts = [...new Set(raw.map(r => r.dept))].sort();
    const heatData = raw.map(r => [months.indexOf(r.month_label), depts.indexOf(r.dept), r.count]);
    const maxVal = Math.max(...raw.map(r => r.count), 1);

    return {
      tooltip: { position: 'top',
        formatter: (p) => `${depts[p.value[1]]} | ${months[p.value[0]]}<br/>Bajas: <b>${p.value[2]}</b>`,
      },
      grid: { top: '4%', right: '8%', bottom: '14%', left: '16%' },
      xAxis: { type: 'category', data: months, splitArea: { show: true },
        axisLabel: { fontSize: 9, rotate: 45, color: '#6b7280' } },
      yAxis: { type: 'category', data: depts, splitArea: { show: true },
        axisLabel: { fontSize: 10, color: '#374151' } },
      visualMap: { min: 0, max: maxVal, calculable: true, orient: 'vertical', right: '0%', top: 'center',
        inRange: { color: ['#fef2f2', '#fca5a5', '#ef4444', '#991b1b'] },
        textStyle: { fontSize: 10 } },
      series: [{ name: 'Bajas', type: 'heatmap', data: heatData,
        label: { show: true, fontSize: 9, color: '#374151' },
        emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' } },
      }],
    };
  };

  // Q3: Donut de Distribución por País
  const getCountryDonutOption = () => {
    const raw = advancedData?.country_distribution || [];
    const colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#ef4444', '#6366f1', '#14b8a6'];

    return {
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      legend: { bottom: 0, textStyle: { fontSize: 11 }, type: 'scroll' },
      color: colors,
      series: [{
        name: 'País', type: 'pie', radius: ['40%', '70%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false, position: 'center' },
        emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } },
        labelLine: { show: false },
        data: raw,
      }],
    };
  };


  // ==========================================
  // RENDER: CHART CARD WRAPPER
  // ==========================================
  const ChartCard = ({ title, children }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 flex flex-col">
      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-3">{title}</h3>
      <div className="flex-1">{children}</div>
    </div>
  );

  // ==========================================
  // MAIN RENDER
  // ==========================================
  const selectClass = "border border-gray-300 rounded text-sm px-3 py-1.5 focus:ring-1 focus:ring-blue-600 outline-none bg-white min-w-[140px] cursor-pointer";

  return (
    <div className="flex flex-col h-full bg-gray-50 p-6 space-y-6 animate-fade-in overflow-auto">
      {/* Top Filter Bar */}
      <div className="flex flex-wrap items-center gap-4 bg-white px-5 py-3.5 rounded-md shadow-sm border border-gray-200">
        {[
          { label: 'Periodo', name: 'periodDate', opts: filterOptions.periods, format: true },
          { label: 'País', name: 'country', opts: filterOptions.countries },
          { label: 'Departamento', name: 'department', opts: filterOptions.departments },
          { label: 'Nivel 1', name: 'jobLevel1', opts: filterOptions.job_levels_1 },
          { label: 'Nivel 2', name: 'jobLevel2', opts: filterOptions.job_levels_2 },
          { label: 'Centro', name: 'workCenter', opts: filterOptions.work_centers },
        ].map(({ label, name, opts, format }) => (
          <div key={name} className="flex flex-col">
            <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">{label}</label>
            <select name={name} value={filters[name]} onChange={handleFilterChange} className={selectClass}>
              {name !== 'periodDate' && <option value="">Todos</option>}
              {opts.map(opt => (
                <option key={opt} value={opt}>{format ? formatPeriodLabel(opt) : opt}</option>
              ))}
            </select>
          </div>
        ))}
      </div>

      {/* Content */}
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
          {/* Snapshot Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {renderCard(data?.total_activos_card, { colSpan: 2, accentColor: '#3b82f6', sparklineHeight: '90px' })}
            {renderCard(data?.altas_card, { colSpan: 1, accentColor: '#10b981', sparklineHeight: '70px' })}
            {renderCard(data?.bajas_card, { colSpan: 1, accentColor: '#ef4444', sparklineHeight: '70px' })}
          </div>

          {/* Advanced Charts Grid 2x2 */}
          {advancedData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Pirámide de Diversidad — Género vs Nivel">
                <ReactECharts option={getDiversityPyramidOption()} style={{ height: '320px' }}
                  notMerge={true} lazyUpdate={true} />
              </ChartCard>

              <ChartCard title="Heatmap de Bajas — Departamento x Mes">
                <ReactECharts option={getTurnoverHeatmapOption()} style={{ height: '320px' }}
                  notMerge={true} lazyUpdate={true} />
              </ChartCard>

              <ChartCard title="Distribución por País">
                <ReactECharts option={getCountryDonutOption()} style={{ height: '320px' }}
                  notMerge={true} lazyUpdate={true} />
              </ChartCard>

              {/* Third row element goes here optionally */}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Demographics;