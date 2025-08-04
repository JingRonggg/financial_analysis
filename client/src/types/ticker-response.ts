import type { TickerData } from "./ticker-data";

export interface TickerResponse {
	ticker_symbol: string;
	count: number;
	data: TickerData[];
}