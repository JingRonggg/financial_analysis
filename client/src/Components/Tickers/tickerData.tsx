import { getTickerData } from "../../Services/tickerService"
import { useState, useEffect } from 'react'

type TickerEntry = {
  id: number;
  ticker_symbol: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  interval: string;
  created_at: string;
};

export function useTickerData( ticker: string ) {
    const [ data, setData ] = useState<TickerEntry[]>([]);
    const [ error, setError ] = useState<string |null>(null);
    const [ loading, setLoading ] = useState<boolean>(true);

    useEffect(()=>{
        setLoading(true);
        console.log("Fetching data for", ticker);
        getTickerData(ticker)
        .then(result => { 
            console.log("Result:", result);
            setData(result.data)
        })
        .catch(err => setError(err.message || "Error fetching tickers"))
        .finally(()=> setLoading(false));

    }, [ticker]);

    return { data, error, loading };

}