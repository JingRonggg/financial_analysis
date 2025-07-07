import requests
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API")
database_connection_string = os.getenv("DATABASE_CONNECTION_STRING")

try:
    engine = create_engine(database_connection_string)
    with engine.connect() as conn:
        print("Database connection successful!")
except OperationalError as e:
    if "does not exist" in str(e):
        print("Database doesn't exist. Creating it...")
        base_url = database_connection_string.rsplit("/", 1)[0]
        temp_engine = create_engine(
            f"{base_url}/postgres", isolation_level="AUTOCOMMIT"
        )

        try:
            with temp_engine.connect() as temp_conn:
                temp_conn.execute(text("CREATE DATABASE financial_analysis"))
            print("Database 'financial_analysis' created successfully!")

            engine = create_engine(database_connection_string)
            with engine.connect() as conn:
                print("Connected to new database!")
        except Exception as create_error:
            print(f"Failed to create database: {create_error}")
            exit(1)
    else:
        print(f"Database connection failed: {e}")
        print("Please check your DATABASE_CONNECTION_STRING in .env file")
        exit(1)

# i gonna track MANGO + FAANG + banks
ticker_symbols = [
    "NVDA",
    "AAPL",
    "AMZN",
    "META",
    "GOOG",
    "NFLX",
    "JPM",
    "MS",
    "GS",
    "AMD",
]

for ticker_symbol in ticker_symbols:
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker_symbol}&apikey={api_key}"
    response = requests.get(url)
    daily_data = response.json().get("Time Series (Daily)")

    rows = []

    for key, value in daily_data.items():
        row = {
            "ticker_symbol": ticker_symbol,
            "date": key,
            "open": float(value["1. open"]),
            "high": float(value["2. high"]),
            "low": float(value["3. low"]),
            "close": float(value["4. close"]),
            "volume": int(value["5. volume"]),
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    try:
        df.to_sql("ticker_daily_data", engine, if_exists="append", index=False)
        print("Data successfully written to database!")

        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT COUNT(*) FROM ticker_daily_data WHERE ticker_symbol = :symbol"
                ),
                {"symbol": ticker_symbol},
            )
            count = result.fetchone()[0]
            print(f"Total records for {ticker_symbol}: {count}")

            latest_data = conn.execute(
                text(
                    """
                SELECT * FROM ticker_daily_data 
                WHERE ticker_symbol = :symbol 
                ORDER BY date DESC 
                LIMIT 5
            """
                ),
                {"symbol": ticker_symbol},
            )
            print(f"Latest 5 records for {ticker_symbol}:")
            for row in latest_data:
                print(row)

    except Exception as e:
        print(f"Error writing to database: {e}")
