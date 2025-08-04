import { useRef, useState } from 'react'
import '../../Styles/searchBar.css'
import { useTicker } from '../Tickers/TickerList';
import { Link, useNavigate } from 'react-router-dom';

type searchBarProps = {
    placeHolder: string
    onFocus?: () => void;
    onBlur?: () => void;
}

export default function SearchBar(props: searchBarProps) {
    const inputRef = useRef<HTMLInputElement>(null);
    const { tickers, error, loading } = useTicker();
    const [ inputValue , setInputValue ] = useState<string>("");
    const [isFocused, setIsFocused] = useState(false);
    const navigate = useNavigate();

    if (loading) return <p>Loading tickers...</p>;
    if (error) return <p>Error: {error}</p>;

    const handleKeyDown =(e: { key: string; })=>{
        if (e.key === "Enter" && inputValue.trim() !==''){
            navigate(`/ticker/${inputValue.trim().toUpperCase()}`);
        }
    }

    return(
        <div>
            <input 
                ref={inputRef} 
                placeholder={props.placeHolder} 
                onFocus={() => {
                    setIsFocused(true);
                    props.onFocus?.();
                }}
                onBlur={() => {
                    setTimeout(() => {
                        setIsFocused(false);
                        if (props.onBlur) props.onBlur();
                    }, 100); //timeout so can render the link
                }}
                onChange={e => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}>
            </input>
                {isFocused && tickers.length > 0 && (
                <ul className="dropdown">
                    {tickers.map((ticker: string) => (
                    <li key={ticker}>
                        <Link to={`/ticker/${ticker}`}>{ticker}</Link>
                    </li>
                    ))}
                </ul>
                )}
        </div>
    )
}