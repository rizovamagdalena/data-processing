import sqlite3
import os
from datetime import datetime

class StockRepository:
    """ Handles DB operations for stock data """

    # Use an environment variable or a default path for the database
    DATABASE_PATH = os.getenv('DATABASE_URL', 'database/stock_data.db')  # Relative path by default

    @staticmethod
    def initialize_database():
        """ Initialize database and create necessary tables if they don't exist """
        conn = sqlite3.connect(StockRepository.DATABASE_PATH)  # Using the relative path here
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            code TEXT,
            date TEXT,
            last_price TEXT,
            max_price TEXT,
            min_price TEXT,
            avg_price TEXT,
            percent_change TEXT,
            quantity TEXT,
            revenue_best_denars TEXT,
            total_revenue_denars TEXT,
            PRIMARY KEY (code, date)
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def get_latest_date(stock_code):
        """ Fetch the latest date for a given stock code """
        conn = sqlite3.connect(StockRepository.DATABASE_PATH)  # Connect using the relative path
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) FROM stock_data WHERE code = ?", (stock_code,))
        result = cursor.fetchone()
        conn.close()
        return datetime.strptime(result[0], "%Y-%m-%d") if result[0] else None

    @staticmethod
    def insert_batch_data(batch_data):
        """ Insert a batch of scraped stock data into the database """
        conn = sqlite3.connect(StockRepository.DATABASE_PATH)  # Connect using the relative path
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT OR REPLACE INTO stock_data (code, date, last_price, max_price, min_price, 
                                          avg_price, percent_change, quantity, revenue_best_denars,
                                          total_revenue_denars)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch_data)
        conn.commit()
        conn.close()
