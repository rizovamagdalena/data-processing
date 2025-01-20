# Repository Layer
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

from models.database import Database


class StockRepository:
    """Handles database operations for stock data."""

    @staticmethod

    @staticmethod
    def get_latest_date(stock_code):
        db = Database()
        db.execute("SELECT date FROM stock_data WHERE code = ? ORDER BY date DESC LIMIT 1", (stock_code,))
        result = db.fetchone()
        return datetime.strptime(result[0], '%Y-%m-%d') if result else None



    @staticmethod
    def fetch_all_stock_codes():
        print("Fetching all stock codes")
        db = Database()
        db.execute("SELECT DISTINCT code FROM stock_data")
        print("OAKY")
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

    @staticmethod
    def fetch_all_stock_data(start_date=None, end_date=None):
        db = Database()
        query = "SELECT * FROM stock_data"
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params=[start_date, end_date]
            db.execute(query, params)
        else:
            db.execute(query)
        return db.fetchall()

    @staticmethod
    def search_stock_data_by_code_in_interval(code, start_date, end_date):
        db = Database()
        query = "SELECT * FROM stock_data WHERE code = ?"
        params = [code]
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        db.execute(query, params)

        data = db.fetchall()
        print(data)

        return data

    @staticmethod
    def search_stock_data_by_code(code):
        db = Database()
        query = "SELECT * FROM stock_data WHERE code LIKE ?"
        db.execute(query, (f"{code}%",))
        return db.fetchall()
#--------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_dataframe_with_numeric_columns():
        df = pd.DataFrame(StockRepository.fetch_all_stock_data(),
                          columns=['code', 'date', 'last_price', 'max_price', 'min_price', 'avg_price',
                                   'percent_change', 'quantity', 'revenue_best_denars', 'total_revenue_denars'])

        for col in ['last_price', 'max_price', 'min_price', 'avg_price']:
            df[col] = pd.to_numeric(df[col].replace({',': ''}, regex=True), errors='coerce')

        for col in ['quantity', 'revenue_best_denars', 'total_revenue_denars']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['percent_change'] = pd.to_numeric(df['percent_change'], errors='coerce')

        return df

    @staticmethod
    def clean_data():
        df = StockRepository.get_dataframe_with_numeric_columns()

        df = df.dropna(subset=['last_price', 'quantity', 'date'])

        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        return df

    @staticmethod
    def get_clean_stock_data_for_code(stock_code):
        df = StockRepository.get_dataframe_with_numeric_columns()

        df = df[df['code'] == stock_code]

        return df.dropna(subset=['date', 'last_price', 'max_price', 'min_price'])

    @staticmethod
    def fetch_most_traded_stocks(period):
        now = datetime.now()
        db = Database()
        print("in method")

        # Set the date range based on the period
        if period == "1M":
            start_date = now - timedelta(days=30)
        elif period == "1Y":
            start_date = now - timedelta(days=365)
        else:
            raise ValueError("Invalid period")

        query = """
            SELECT code, SUM(quantity) AS total_quantity
            FROM stock_data
            WHERE date >= ?
            GROUP BY code
            ORDER BY total_quantity DESC
            LIMIT 20;
        """
        print("before query")

        db.execute(query, (start_date,))
        result = db.fetchall()
        print(result)
        db.close()

        # Format response
        stocks = [{"stock_code": row[0], "total_quantity": row[1]} for row in result]
        print(stocks)
        return stocks
