export interface TickerData {
  id: number;
  ticker_symbol: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
	volume: number;
  interval: string;
  created_at: string;
}