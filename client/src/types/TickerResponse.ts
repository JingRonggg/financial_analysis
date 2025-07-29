import type { TickerData } from "./TickerData";

export interface TickerResponse {
	ticker_symbol: string;
	count: number;
	data: TickerData[];
}