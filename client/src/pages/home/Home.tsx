import SearchBar from "../../components/SearchBar/SearchBar";
import { useState } from "react";
import '../../Styles/home.css'

export default function Home() {
  const [isFocused, setFocus ] = useState<boolean>(false);

  return (
    <div className={`container ${isFocused ? "darken" : ""}`}>
        <div className="content">
            <h1>Financial Analysis</h1>
            <SearchBar placeHolder="Search tickers here..." 
              onFocus={() => setFocus(true)}
              onBlur={()=> setFocus(false)}
            />
        </div>
    </div>
  );
}
