import { getTickerData } from "../../Services/tickerService"
import { useState, useEffect } from 'react'

export function useTickerData<T>( ticker: string ) {
    const [ data, setData ] = useState<T[] |  null>(null);
    const[ error, setError ] = useState<string |null>(null);
    const [ loading, setLoading ] = useState<boolean>(true);

    useEffect(()=>{
        getTickerData(ticker)
    })

}