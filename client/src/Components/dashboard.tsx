import React from 'react';
// import TickerChart from './Charts/TickerChart';
import Widget from './Widget/widget';
import '../Styles/dashboard.css';


const Dashboard: React.FC = () => {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Financial Analysis Dashboard</h1>
      </div>
      
      <div className="dashboard-grid">
        <Widget title="Stock Chart" className="chart-widget">
          {/* <TickerChart /> */}
          <p>ticker chart</p>
        </Widget>

        <Widget title="widget 1" className="widget 1">
          <div className="placeholder-content">
            <p>widget 1</p>
          </div>
        </Widget>

        <Widget title="widget 2" className="widget 2">
          <div className="placeholder-content">
            <p>widget 1</p>
          </div>
        </Widget>

        <Widget title="widget 3" className="widget 3">
          <div className="placeholder-content">
            <p>widget 1</p>
          </div>
        </Widget>

        <Widget title="widget 4" className="widget 4">
          <div className="placeholder-content">
            <p>widget 1</p>
          </div>
        </Widget>

      </div>
    </div>
  );
};

export default Dashboard;