import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { supabase } from '../../lib/supabaseClient';

export default function CausalidadCorrelaciones() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const { data: rawData, error } = await supabase.schema('business').from('mv_critical_moments').select('*').limit(100);
      if (!error && rawData) {
        setData(rawData);
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  const getOption = () => {
    if (!data.length) return {};
    
    // Find category key (usually a string like 'periodo', 'department_name', etc.)
    const categoryKey = Object.keys(data[0]).find(k => 
      ['periodo', 'snapshot_date', 'department_name', 'country_iso3', 'job_level_1', 'status'].includes(k)
    ) || Object.keys(data[0])[0];

    // Find numeric keys
    const keys = Object.keys(data[0]).filter(k => 
      k !== categoryKey && !k.includes('id') && !k.includes('name')
    );
    
    if (!keys.length) return {};

    return {
      tooltip: { trigger: 'axis' },
      legend: { data: keys },
      xAxis: { type: 'category', data: data.map(d => d[categoryKey] || 'N/A') },
      yAxis: { type: 'value' },
      series: keys.map(k => ({
        name: k,
        type: 'bar',
        data: data.map(d => parseFloat(d[k]) || 0),
        itemStyle: { borderRadius: [4, 4, 0, 0] }
      }))
    };
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-slate-800 mb-2">Correlaciones</h2>
      <p className="text-slate-500 mb-6">Factores de impacto.</p>
      
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 min-h-[400px]">
        {loading ? (
          <div className="flex items-center justify-center h-full text-slate-400">Cargando datos desde mv_critical_moments...</div>
        ) : data.length > 0 ? (
          <ReactECharts option={getOption()} style={{ height: '400px' }} />
        ) : (
          <div className="flex items-center justify-center h-full text-slate-400">No hay datos disponibles en mv_critical_moments.</div>
        )}
      </div>
    </div>
  );
}
