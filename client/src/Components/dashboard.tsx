import React from 'react';
import { useParams } from 'react-router-dom';
import TickerChart from './Charts/TickerChart';
import Widget from './Widget/Widget';
import { useTicker } from '../hooks/use-ticker';
import '../Styles/dashboard.css';

const Dashboard: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const { selected, data, loading, error } = useTicker(ticker);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Financial Analysis Dashboard</h1>
      </div>
      
      <div className="dashboard-grid">
        <Widget title="Stock Chart" className="chart-widget">
          {loading ? <div className="loading">Loading...</div> : 
           error ? <div className="error">Error: {error}</div> : 
           data.length > 0 ? <TickerChart data={data} tickerSymbol={selected} /> : 
           <p>No data available.</p>}
        </Widget>

        <Widget title="Place holder for AI analysis" className='widget 1'>
          <p> Place holder for AI analysis</p>
        </Widget>

        <Widget title="widget 2" className='widget 2'>
          <p> feature 2</p>
        </Widget>

        <Widget title="widget 3" className='widget 3'>
          <p> feature 3</p>
        </Widget>

        <Widget title="widget 4" className='widget 4'>
          <p> feature 4</p>
        </Widget>
      </div>
    </div>
  );
};

export default Dashboard;