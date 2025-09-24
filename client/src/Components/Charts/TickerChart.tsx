import React, { useRef } from 'react';
import {
  createChart,
  CrosshairMode,
  CandlestickSeries,
  type IChartApi,
  type ISeriesApi,
} from 'lightweight-charts';
import type { TickerData } from '../../types/ticker-data';

interface TickerChartProps {
  data: TickerData[];
  tickerSymbol: string;
}

const TickerChart: React.FC<TickerChartProps> = ({ data, tickerSymbol }) => {
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const resizeObserverRef = useRef<ResizeObserver | null>(null);

  const setChartContainerRef = (node: HTMLDivElement | null) => {
    if (!node) {
      // Cleanup
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
        resizeObserverRef.current = null;
      }
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
        candleSeriesRef.current = null;
      }
      return;
    }

    if (chartRef.current) return; // Avoid duplicate chart

    // Create chart
    const newChart = createChart(node, {
      width: node.clientWidth,
      height: node.clientHeight,
      layout: {
        background: { color: '#222' },
        textColor: '#DDD',
      },
      grid: {
            vertLines: { color: '#444' },
            horzLines: { color: '#444' },
      },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#485c7b' },
      timeScale: {
        borderColor: '#485c7b',
        rightOffset: 10,
        barSpacing: 8,
        visible: true,
      },
    });

    chartRef.current = newChart;


    const newCandleSeries = chartRef.current.addSeries(CandlestickSeries,{
      // upColor: '#4bffb5',
      // downColor: '#ff4976',
      // borderDownColor: '#ff4976',
      // borderUpColor: '#4bffb5',
      // wickDownColor: '#838ca1',
      // wickUpColor: '#838ca1',
    });

    candleSeriesRef.current = newCandleSeries;

    // Transform TickerData to Lightweight Charts format
    const formattedData = data.map(item => ({
      time: item.date, // expects 'YYYY-MM-DD' string for Time type
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    if (formattedData.length) {
      newCandleSeries.setData(formattedData);
      newChart.timeScale().fitContent();
      newCandleSeries.priceScale().applyOptions({
        autoScale: false, // disables auto scaling based on visible content
        scaleMargins: {
            top: 0.1,
            bottom: 0.2,
        },
      });

      newChart.timeScale().applyOptions({
        borderColor: '#71649C',
        barSpacing: 10,
      });

    }

    // Resize observer
    const observer = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      chartRef.current?.applyOptions({ width, height });
    });
    observer.observe(node);
    resizeObserverRef.current = observer;
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '400px' }}>
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: '50%',
          transform: 'translateX(-50%)',
          color: 'white',
          fontWeight: 'bold',
          fontSize: '16px',
          padding: '8px',
          zIndex: 10,
          pointerEvents: 'none',
        }}
      >
        {tickerSymbol}
        <span style={{ marginLeft: '8px', fontWeight: 'normal' }}>
          {data.length ? data[0].interval : ''}
        </span>
      </div>
    <div className="ticker-chart-container" ref={setChartContainerRef} style={{ width: '100%', height: '400px' }} />
    </div>
  );
};

export default TickerChart;
