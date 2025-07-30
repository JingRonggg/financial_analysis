import React, { useEffect, useState } from 'react'
import { getTickers } from '../../Services/tickerService'

export function useTicker() {
    const [ tickers , setTickers ] = useState<string[]>([]);
    const [ error, setError ] = useState<string | null>(null);
    const [ loading, setLoading ] = useState<boolean>(true);

    useEffect(() =>{   
        getTickers()
        .then(setTickers)
        .catch(err => setError(err.message || "Error fetching tickers"))
        .finally(()=> setLoading(false));

    }, []);

    return { tickers, error, loading };
}