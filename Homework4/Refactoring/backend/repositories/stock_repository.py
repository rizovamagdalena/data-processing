# Repository Layer
from datetime import datetime

from src.backend.models.database import Database


class StockRepository:
    """Handles database operations for stock data."""

    @staticmethod
    def initialize_database():
        db = Database()
        db.execute('''
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
                UNIQUE(code, date) ON CONFLICT IGNORE
            )
        ''')

    @staticmethod
    def get_latest_date(stock_code):
        db = Database()
        db.execute("SELECT date FROM stock_data WHERE code = ? ORDER BY date DESC LIMIT 1", (stock_code,))
        result = db.fetchone()
        return datetime.strptime(result[0], '%d.%m.%Y') if result else None

    @staticmethod
    def insert_batch_data(batch_data):
        db = Database()
        db.executemany('''
            INSERT INTO stock_data (
                code, date, last_price, max_price, min_price, avg_price,
                percent_change, quantity, revenue_best_denars, total_revenue_denars
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', batch_data)
        db.commit()

    @staticmethod
    def fetch_all_stock_codes():
        db = Database()
        db.execute("SELECT DISTINCT code FROM stock_data")
        return [row[0] for row in db.fetchall()]

    @staticmethod
    def fetch_stock_data_by_code(code, start_date=None, end_date=None):
        db = Database()
        query = "SELECT * FROM stock_data WHERE code = ?"
        params = [code]
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        db.execute(query, params)
        return db.fetchall()
