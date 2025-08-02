import { useParams } from 'react-router-dom';
import { useTickerData } from '../Tickers/tickerData';

export default function ChartArea() {
    const { ticker } = useParams<{ ticker: string }>();
    const { data, error, loading } = useTickerData(ticker || '');

    if (loading) return <p>Loading ticker data...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
        <h2>{ticker} Stock Data</h2>
        {data.length > 0 && (
            <table>
            <thead>
                <tr>
                <th>Date</th>
                <th>Open</th>
                <th>High</th>
                <th>Low</th>
                <th>Close</th>
                <th>Volume</th>
                </tr>
            </thead>
            <tbody>
                {data.map((entry) => (
                <tr key={entry.id}>
                    <td>{entry.date}</td>
                    <td>{entry.open}</td>
                    <td>{entry.high}</td>
                    <td>{entry.low}</td>
                    <td>{entry.close}</td>
                    <td>{entry.volume.toLocaleString()}</td>
                </tr>
                ))}
            </tbody>
            </table>
        )}
        </div>
    );
}