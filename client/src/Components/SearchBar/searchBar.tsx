import React, { useRef, useEffect } from 'react'
import './searchBar.css'
import { useTicker } from '../Tickers/tickerList';
type searchBarProps = {
    placeHolder: string
    onFocus?: () => void;
    onBlur?: () => void;
}

export default function searchBar(props: searchBarProps) {
    const inputRef = useRef<HTMLInputElement>(null);
    const { tickers, error, loading } = useTicker();

    if (loading) return <p>Loading tickers...</p>;
    if (error) return <p>Error: {error}</p>;
    
    return(
        <div>
            <input ref={inputRef} placeholder={props.placeHolder} onFocus={props.onFocus} onBlur={props.onBlur}></input>
                <ul className="dropdown">
                    {tickers.map((ticker: string, index: number) => (
                        <li key={index} className="dropdown-item"> {ticker} </li>
                    ))}
                </ul> 
        </div>
    )
}