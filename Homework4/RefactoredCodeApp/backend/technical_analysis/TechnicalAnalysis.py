import numpy as np
import sqlite3
import pandas as pd
import datetime
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, MACD, EMAIndicator, CCIIndicator
from ta.volume import VolumePriceTrendIndicator
from src.backend.repositories import *
from src.backend.repositories.stock_repository import StockRepository
from src.technical_analysis.TechnicalAnalysis_repository import TechnicalAnalysisRepository


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
        'Stochastic': StochasticOscillator(high=df['max_price'], low=df['min_price'], close=df['last_price'],
                                               window=14,
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


# Save indicators to the database
def save_indicators_to_db(code, df, time_period):
    for _, row in df.iterrows():
        date_str = row['date']
        TechnicalAnalysisRepository.TechnicalAnalysisRepository.insert_row(row, code, date_str, time_period)


# Main program to process and store results
class TechnicalAnalysis:

    @staticmethod
    def init():
        TechnicalAnalysisRepository.TechnicalAnalysisRepository.initialize_database()
        stock_codes = StockRepository.fetch_all_stock_codes()

        for code in stock_codes:
            print(f"Processing Stock Code: {code}")
            df = StockRepository.get_clean_stock_data_for_code(code)
            if df.empty:
                print(f"No data found for {code}. Skipping.")
                continue

            #df = StockRepository.clean_data()

            df = calculate_indicators(df)  # Calculate technical indicators
            df = generate_signals(df)  # Generate signals


            # Store data for each time period (1D, 1W, 1M)
            for period in ["1D", "1W", "1M"]:
                period_data = filter_time_period(df, period)
                save_indicators_to_db(code, period_data, period)  # Save to DB
