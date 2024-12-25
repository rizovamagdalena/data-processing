import numpy as np
from sqlalchemy.engine import cursor
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, MACD, EMAIndicator, CCIIndicator
from ta.volume import VolumePriceTrendIndicator
import sqlite3
import pandas as pd
import datetime


# Get database connection
def get_db_connection():
    conn = sqlite3.connect('stock_data.db')  # Replace with your actual database file
    conn.row_factory = sqlite3.Row
    return conn


# Fetch stock codes
def get_stock_codes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT code FROM stock_data")
    stock_codes = [row['code'] for row in cursor.fetchall()]
    conn.close()
    return stock_codes


# Clean data for stock prices and quantities
def clean_price_columns(df):
    price_columns = ['last_price', 'max_price', 'min_price']
    for col in price_columns:
        df[col] = pd.to_numeric(df[col].replace({',': ''}, regex=True), errors='coerce')
    return df


def clean_data(df):
    df['last_price'] = df['last_price'].replace({',': ''}, regex=True)
    df['last_price'] = pd.to_numeric(df['last_price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df = df.dropna(subset=['last_price', 'quantity'])  # Remove rows with missing price or quantity
    return df


# Fetch stock data for a specific code
def get_stock_data(conn, stock_code):
    query = "SELECT * FROM stock_data WHERE code = ? ORDER BY date ASC;"
    df = pd.read_sql_query(query, conn, params=(stock_code,))
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')  # Convert date column
    df = clean_price_columns(df)  # Clean the data
    df = df.dropna(subset=['date', 'last_price', 'max_price', 'min_price'])  # Drop rows with invalid data
    df = df.sort_values('date')  # Sort data by date
    return df


# Calculate Weighted Moving Average (WMA)
def weighted_moving_average(df, window):
    weights = np.arange(1, window + 1)  # Generate weights based on window size
    wma_values = df['last_price'].rolling(window=window).apply(
        lambda prices: np.dot(prices, weights) / weights.sum(), raw=True
    )
    return wma_values


# Calculate technical indicators
def calculate_indicators(df):
    df['RSI'] = RSIIndicator(close=df['last_price'], window=14).rsi()  # RSI Indicator
    df['SMA_14'] = SMAIndicator(close=df['last_price'], window=14).sma_indicator()  # Simple Moving Average (SMA)
    df['EMA_14'] = EMAIndicator(close=df['last_price'], window=14).ema_indicator()  # Exponential Moving Average (EMA)
    df['WMA_14'] = weighted_moving_average(df, window=14)  # Weighted Moving Average (WMA)

    macd = MACD(close=df['last_price'], window_slow=26, window_fast=12, window_sign=9)  # MACD
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    stochastic = StochasticOscillator(high=df['max_price'], low=df['min_price'], close=df['last_price'], window=14,
                                      smooth_window=3)  # Stochastic Oscillator
    df['Stochastic'] = stochastic.stoch()

    df['CCI'] = CCIIndicator(high=df['max_price'], low=df['min_price'], close=df['last_price'],
                             window=20).cci()  # CCI Indicator

    df['VPT'] = VolumePriceTrendIndicator(close=df['last_price'],
                                          volume=df['quantity']).volume_price_trend()  # Volume-Price Trend (VPT)

    return df


# Generate buy/sell signals based on indicators
def generate_signals(df):
    df['Signal'] = 'Hold'

    df.loc[(df['RSI'] < 30) & (df['last_price'] > df['SMA_14']), 'Signal'] = 'Buy'
    df.loc[(df['RSI'] > 70) & (df['last_price'] < df['SMA_14']), 'Signal'] = 'Sell'

    df.loc[df['MACD'] > df['MACD_signal'], 'Signal'] = 'Buy'
    df.loc[df['MACD'] < df['MACD_signal'], 'Signal'] = 'Sell'

    df.loc[df['Stochastic'] > 80, 'Signal'] = 'Sell'
    df.loc[df['Stochastic'] < 20, 'Signal'] = 'Buy'

    df.loc[df['CCI'] > 100, 'Signal'] = 'Sell'
    df.loc[df['CCI'] < -100, 'Signal'] = 'Buy'

    df.loc[df['VPT'] > df['VPT'].shift(1), 'Signal'] = 'Buy'
    df.loc[df['VPT'] < df['VPT'].shift(1), 'Signal'] = 'Sell'

    return df


# Filter data by time period (1D, 1W, 1M)
def filter_time_period(df, period):
    current_date = pd.to_datetime(df['date'].max())
    if period == "1D":
        start_date = current_date - datetime.timedelta(days=1)
    elif period == "1W":
        start_date = current_date - datetime.timedelta(weeks=1)
    elif period == "1M":
        start_date = current_date - datetime.timedelta(weeks=4)
    else:
        raise ValueError("Invalid period specified!")
    return df[pd.to_datetime(df['date']) >= start_date]


# Create stock_indicators table
def create_table(conn):
    print("CREATING TABLE")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            date TEXT,
            time_period TEXT,
            cci REAL,
            vpt REAL,
            signal TEXT
        );
    ''')
    conn.commit()


# Save indicators to the database
def save_indicators_to_db(conn, code, df, time_period):
    for _, row in df.iterrows():
        # Convert the date to string before insertion (e.g., in YYYY-MM-DD format)
        date_str = row['date'].strftime('%Y-%m-%d')  # Adjust format as needed

        conn.execute("""
            INSERT INTO stock_indicators (code, date, time_period, cci, vpt, signal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (code, date_str, time_period, row['CCI'], row['VPT'], row['Signal']))
    conn.commit()



# Main program to process and store results
def main():
    conn = get_db_connection()
    create_table(conn)  # Create table if not already created
    stock_codes = get_stock_codes()  # Fetch the stock codes

    # Loop through each stock code and process data
    for code in stock_codes:
        print(f"Processing Stock Code: {code}")
        df = get_stock_data(conn, code)  # Get data for the stock code
        df = clean_data(df)  # Clean the data
        df = calculate_indicators(df)  # Calculate indicators
        df = generate_signals(df)  # Generate signals

        # Store results for 1-day, 1-week, and 1-month periods
        save_indicators_to_db(conn, code, filter_time_period(df, "1D"), '1D')  # Save daily data
        save_indicators_to_db(conn, code, filter_time_period(df, "1W"), '1W')  # Save weekly data
        save_indicators_to_db(conn, code, filter_time_period(df, "1M"), '1M')  # Save monthly data

    conn.close()  # Close connection


if __name__ == "__main__":
    main()
