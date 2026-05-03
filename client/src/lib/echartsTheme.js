export const hrTheme = {
  color: [
    '#3b82f6', // blue-500
    '#10b981', // emerald-500
    '#6366f1', // indigo-500
    '#f59e0b', // amber-500
    '#ef4444', // red-500
    '#8b5cf6', // violet-500
    '#14b8a6', // teal-500
    '#f43f5e', // rose-500
  ],
  backgroundColor: 'transparent',
  textStyle: {
    fontFamily: 'Inter, system-ui, sans-serif',
    color: '#64748b' // slate-500
  },
  title: {
    textStyle: {
      color: '#1e293b', // slate-800
      fontWeight: 600,
      fontSize: 14
    }
  },
  tooltip: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#e2e8f0', // slate-200
    borderWidth: 1,
    padding: [8, 12],
    textStyle: {
      color: '#334155', // slate-700
      fontSize: 13
    },
    axisPointer: {
      lineStyle: { color: '#cbd5e1' },
      crossStyle: { color: '#cbd5e1' }
    }
  },
  legend: {
    textStyle: { color: '#64748b' }, // slate-500
    bottom: 0,
    icon: 'circle',
    itemWidth: 10,
    itemHeight: 10
  },
  grid: {
    containLabel: true,
    left: '2%',
    right: '5%',
    bottom: '10%',
    top: '10%'
  },
  categoryAxis: {
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisTick: { show: false },
    axisLabel: { color: '#64748b' },
    splitLine: { show: false }
  },
  valueAxis: {
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748b' },
    splitLine: { 
      lineStyle: { 
        color: '#f1f5f9', // slate-100
        type: 'dashed' 
      } 
    }
  }
};
