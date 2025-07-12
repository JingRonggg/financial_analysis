import yfinance as yf
import asyncio
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from datetime import datetime, timedelta
from server.util.config import getConfig


def create_database_connection():
    """Create and return database connection engine."""
    config = getConfig()
    database_connection_string = config.get_database_url()

    try:
        engine = create_engine(database_connection_string)
        with engine.connect() as conn:
            print("Database connection successful!")
        return engine
    except OperationalError as e:
        if "does not exist" in str(e):
            return create_database_if_not_exists(database_connection_string)
        else:
            print(f"Database connection failed: {e}")
            print("Please check your DATABASE_CONNECTION_STRING in .env file")
            exit(1)


def create_database_if_not_exists(connection_string):
    """Create database if it doesn't exist."""
    print("Database doesn't exist. Creating it...")
    base_url = connection_string.rsplit("/", 1)[0]
    temp_engine = create_engine(f"{base_url}/postgres", isolation_level="AUTOCOMMIT")

    try:
        with temp_engine.connect() as temp_conn:
            temp_conn.execute(text("CREATE DATABASE financial_analysis"))
        print("Database 'financial_analysis' created successfully!")

        engine = create_engine(connection_string)
        with engine.connect() as conn:
            print("Connected to new database!")
        return engine
    except Exception as create_error:
        print(f"Failed to create database: {create_error}")
        exit(1)


def create_tables_if_not_exist(engine):
    """Create ticker data tables if they don't exist."""
    daily_table_sql = """
    CREATE TABLE IF NOT EXISTS daily_ticker_data (
        id SERIAL PRIMARY KEY,
        ticker_symbol VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        open DECIMAL(10,2) NOT NULL,
        high DECIMAL(10,2) NOT NULL,
        low DECIMAL(10,2) NOT NULL,
        close DECIMAL(10,2) NOT NULL,
        volume BIGINT NOT NULL,
        interval VARCHAR(10) NOT NULL DEFAULT 'daily',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker_symbol, date)
    );
    """

    hourly_table_sql = """
    CREATE TABLE IF NOT EXISTS hourly_ticker_data (
        id SERIAL PRIMARY KEY,
        ticker_symbol VARCHAR(10) NOT NULL,
        date TIMESTAMP NOT NULL,
        open DECIMAL(10,2) NOT NULL,
        high DECIMAL(10,2) NOT NULL,
        low DECIMAL(10,2) NOT NULL,
        close DECIMAL(10,2) NOT NULL,
        volume BIGINT NOT NULL,
        interval VARCHAR(10) NOT NULL DEFAULT 'hourly',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker_symbol, date)
    );
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(daily_table_sql))
            conn.execute(text(hourly_table_sql))
            conn.commit()
            print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")


def fetch_stock_data(ticker_symbol, interval="daily", days=365):
    """Fetch stock data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        if interval == "hourly":
            # hourly data only can 7 days
            start_date = end_date - timedelta(days=7)
            hist_data = ticker.history(start=start_date, end=end_date, interval="1h")
        else:
            hist_data = ticker.history(start=start_date, end=end_date, interval="1d")

        if hist_data.empty:
            print(f"No data available for {ticker_symbol}")
            return None

        hist_data.reset_index(inplace=True)
        return hist_data
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None


def prepare_data_for_db(hist_data, ticker_symbol, interval="daily"):
    """Convert Yahoo Finance data to database format."""
    rows = []
    for _, row in hist_data.iterrows():
        date_format = "%Y-%m-%d %H:%M:%S" if interval == "hourly" else "%Y-%m-%d"

        data_row = {
            "ticker_symbol": ticker_symbol,
            "date": (
                row["Datetime"].strftime(date_format)
                if interval == "hourly"
                else row["Date"].strftime(date_format)
            ),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
            "interval": interval,
        }
        rows.append(data_row)

    return pd.DataFrame(rows)


def remove_duplicates_and_insert(df, engine, table_name):
    """Remove duplicates and insert data into database."""
    try:
        with engine.connect() as conn:
            # Get existing records to avoid duplicates
            existing_query = text(
                f"SELECT ticker_symbol, date FROM {table_name} WHERE ticker_symbol = :symbol"
            )
            existing_data = conn.execute(
                existing_query, {"symbol": df.iloc[0]["ticker_symbol"]}
            )
            existing_records = {(row[0], str(row[1])) for row in existing_data}

            # Filter out duplicates
            df_filtered = df[
                ~df.apply(
                    lambda x: (x["ticker_symbol"], x["date"]) in existing_records,
                    axis=1,
                )
            ]

            if not df_filtered.empty:
                df_filtered.to_sql(table_name, engine, if_exists="append", index=False)
                print(f"Inserted {len(df_filtered)} new records")
            else:
                print("No new records to insert")

    except Exception as e:
        print(f"Error writing to database: {e}")


def load_stock_data(ticker_symbols, interval="daily", days=365):
    """Main function to load stock data."""
    engine = create_database_connection()

    # Create tables if they don't exist
    create_tables_if_not_exist(engine)

    table_name = "daily_ticker_data" if interval == "daily" else "hourly_ticker_data"

    for ticker_symbol in ticker_symbols:
        print(f"Processing {ticker_symbol} ({interval})...")

        hist_data = fetch_stock_data(ticker_symbol, interval, days)
        if hist_data is None:
            continue

        df = prepare_data_for_db(hist_data, ticker_symbol, interval)
        remove_duplicates_and_insert(df, engine, table_name)


async def run_data_loading():
    """Run data loading on startup."""
    print("Starting data loading process...")

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

    try:
        # Load daily data
        await asyncio.to_thread(load_stock_data, ticker_symbols, "daily", 365)

        # Load hourly data
        await asyncio.to_thread(load_stock_data, ticker_symbols, "hourly", 7)

        print("Data loading completed successfully!")
    except Exception as e:
        print(f"Error during data loading: {e}")
