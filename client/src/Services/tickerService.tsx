import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface TickerListProps {}

const TickerList: React.FC<TickerListProps> = () => {
  const [tickers, setTickers] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    axios.get<string[]>('http://localhost:8000/ticker/')
      .then(response => {
        setTickers(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Error fetching tickers');
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading tickers...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul>
      {tickers.map((ticker, index) => (
        <li key={index}>{ticker}</li>
      ))}
    </ul>
  );
};

export default TickerList;
