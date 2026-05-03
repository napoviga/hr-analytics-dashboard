import { useState, useEffect, useRef, useCallback } from 'react';
import { supabase } from '../../../lib/supabaseClient';

export function useDemographicsData(filters) {
  const [data, setData] = useState({ total_activos_card: null, altas_card: null, bajas_card: null });
  const [advancedData, setAdvancedData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const debounceRef = useRef(null);
  const abortRef = useRef(false);

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
        console.warn('Advanced charts RPC failed, cards still shown:', advRes.reason || advRes.value.error);
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

  return { data, advancedData, loading, error };
}

export function useDemographicsFilters() {
  const [filterOptions, setFilterOptions] = useState({
    periods: [], countries: [], departments: [],
    job_levels_1: [], job_levels_2: [], work_centers: []
  });
  const [filters, setFilters] = useState({
    periodDate: '', country: '', department: '',
    jobLevel1: '', jobLevel2: '', workCenter: '',
  });

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

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  return { filterOptions, filters, handleFilterChange };
}
