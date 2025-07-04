import requests
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

api_key=os.getenv("ALPHA_VANTAGE_API")
database_connection_string=os.getenv("DATABASE_CONNECTION_STRING")

# i gonna track MANGO + FAANG + banks
ticker_symbols = ["NVDA", "AAPL", "AMZN", "META", "GOOG", "NFLX", "JPM", "MS", "GS", "AMD"]

for ticker_symbol in ticker_symbols:
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker_symbol}&apikey={api_key}"
    response = requests.get(url)
    daily_data = response.json().get('Time Series (Daily)')
    headers = ["ticker_symbol", "date", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame(columns=headers)

    for key, value in daily_data.items():
        row = {
            "ticker_symbol": ticker_symbol,
            "date": key,
            "open": float(value['1. open']),
            "high": float(value['2. high']),
            "low": float(value['3. low']),
            "close": float(value['4. close']),
            "volume": int(value['5. volume'])
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    print(f"{df.head()=}")

engine = create_engine(database_connection_string)
df.to_sql('ticker_daily_data', engine)