import axios from 'axios';

export const getTickers = async () => {
  const res = await axios.get<string[]>('http://localhost:8000/ticker/');
  return res.data;
}


export const getTickerData = async (tickerName: string) => {
  const res = await axios.get(`http://localhost:8000/ticker/${tickerName}`);
  return res.data;
}