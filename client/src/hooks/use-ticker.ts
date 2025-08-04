import { useState, useEffect } from 'react';
import { getTickers, getTickerData } from '../services/ticker-service';
import type { TickerData } from '../types/ticker-data';

export const useTicker = (preSelected?: string | null) => {
  const [state, setState] = useState({
    tickers: [] as string[],
    selected: preSelected || '',
    data: [] as TickerData[],
    loading: false,
    error: ''
  });

  useEffect(() => {
    getTickers().then(tickers => {
      const selected = preSelected || tickers[0] || '';
      setState(prev => ({ ...prev, tickers, selected }));
      if (selected) fetchData(selected);
    }).catch(() => setState(prev => ({ ...prev, error: 'Failed to load tickers' })));
  }, [preSelected]);

  const fetchData = async (ticker: string) => {
    setState(prev => ({ ...prev, loading: true, error: '' }));
    try {
      const response = await getTickerData(ticker);
    const data: TickerData[] = response.data.sort((a: TickerData, b: TickerData) => new Date(a.date).getTime() - new Date(b.date).getTime());
      setState(prev => ({ ...prev, data, loading: false }));
    } catch {
      setState(prev => ({ ...prev, error: `Failed to load ${ticker}`, loading: false }));
    }
  };

  const selectTicker = (ticker: string) => {
    setState(prev => ({ ...prev, selected: ticker }));
    fetchData(ticker);
  };

  return { ...state, selectTicker };
};