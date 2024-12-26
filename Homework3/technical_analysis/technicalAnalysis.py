import numpy as np
import sqlite3
import pandas as pd
import datetime
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, MACD, EMAIndicator, CCIIndicator
from ta.volume import VolumePriceTrendIndicator


# Get database connection
def get_db_connection(db_name='stock_data.db'):
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None


# Fetch all stock codes from database
def get_stock_codes(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT code FROM stock_data")
        return [row['code'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching stock codes: {e}")
        return []


# Clean stock price columns by converting values to numeric
def clean_price_columns(df):
    for col in ['last_price', 'max_price', 'min_price']:
        df[col] = pd.to_numeric(df[col].replace({',': ''}, regex=True), errors='coerce')
    return df


# Clean data, removing missing values and invalid entries
def clean_data(df):
    df = df.dropna(subset=['last_price', 'quantity', 'date'])
    df['last_price'] = pd.to_numeric(df['last_price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    return df


# Fetch stock data from the database for a given stock code
def get_stock_data(conn, stock_code):
    query = "SELECT * FROM stock_data WHERE code = ? ORDER BY date ASC;"
    try:
        df = pd.read_sql_query(query, conn, params=(stock_code,))
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')  # Convert to datetime
        df = clean_price_columns(df)
        return df.dropna(subset=['date', 'last_price', 'max_price', 'min_price'])
    except sqlite3.Error as e:
        print(f"Error fetching data for stock {stock_code}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error


# Calculate Weighted Moving Average (WMA)
def weighted_moving_average(df, window):
    weights = np.arange(1, window + 1)
    return df['last_price'].rolling(window=window).apply(
        lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)


# Calculate all technical indicators using the 'ta' library
def calculate_indicators(df):
    indicators = {
        'RSI': RSIIndicator(close=df['last_price'], window=14).rsi(),
        'SMA_14': SMAIndicator(close=df['last_price'], window=14).sma_indicator(),
        'EMA_14': EMAIndicator(close=df['last_price'], window=14).ema_indicator(),
        'WMA_14': weighted_moving_average(df, window=14),
        'MACD': MACD(close=df['last_price'], window_slow=26, window_fast=12, window_sign=9).macd(),
        'MACD_signal': MACD(close=df['last_price'], window_slow=26, window_fast=12, window_sign=9).macd_signal(),
        'Stochastic': StochasticOscillator(high=df['max_price'], low=df['min_price'], close=df['last_price'], window=14,
                                           smooth_window=3).stoch(),
        'CCI': CCIIndicator(high=df['max_price'], low=df['min_price'], close=df['last_price'], window=20).cci(),
        'VPT': VolumePriceTrendIndicator(close=df['last_price'], volume=df['quantity']).volume_price_trend()
    }

    for indicator, values in indicators.items():
        df[indicator] = values

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


# Filter data based on time period (1D, 1W, 1M)
def filter_time_period(df, period):
    current_date = pd.to_datetime(df['date'].max())
    period_map = {
        "1D": datetime.timedelta(days=1),
        "1W": datetime.timedelta(weeks=1),
        "1M": datetime.timedelta(weeks=4)
    }

    if period not in period_map:
        raise ValueError("Invalid period specified!")

    start_date = current_date - period_map[period]
    return df[pd.to_datetime(df['date']) >= start_date]


# Create the stock_indicators table in the database if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        date TEXT,
        time_period TEXT,
        cci REAL,
        vpt REAL,
        signal TEXT
    );''')
    conn.commit()


# Save indicators to the database
def save_indicators_to_db(conn, code, df, time_period):
    for _, row in df.iterrows():
        date_str = row['date'].strftime('%Y-%m-%d')  # Ensure consistent format
        existing = conn.execute("""
            SELECT 1 FROM stock_indicators 
            WHERE code = ? AND date = ? AND time_period = ?""", (code, date_str, time_period)).fetchone()

        if not existing:
            conn.execute("""
                INSERT INTO stock_indicators (code, date, time_period, cci, vpt, signal)
                VALUES (?, ?, ?, ?, ?, ?)""",
                         (code, date_str, time_period, row['CCI'], row['VPT'], row['Signal']))
    conn.commit()


# Main program to process and store results
def main():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to database. Exiting.")
        return

    create_table(conn)  # Ensure the table exists
    stock_codes = get_stock_codes(conn)  # Get all stock codes

    for code in stock_codes:
        print(f"Processing Stock Code: {code}")
        df = get_stock_data(conn, code)  # Fetch the stock data
        if df.empty:
            print(f"No data found for {code}. Skipping.")
            continue

        df = clean_data(df)  # Clean the data
        df = calculate_indicators(df)  # Calculate technical indicators
        df = generate_signals(df)  # Generate signals

        # Store data for each time period (1D, 1W, 1M)
        for period in ["1D", "1W", "1M"]:
            period_data = filter_time_period(df, period)
            save_indicators_to_db(conn, code, period_data, period)  # Save to DB

    conn.close()  # Close the database connection


if __name__ == "__main__":
    main()
