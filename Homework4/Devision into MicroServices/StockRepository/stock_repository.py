from datetime import datetime

from src.database import Database


class StockRepository:
    """Handles database operations for stock data."""

    @staticmethod
    def initialize_database():
        db = Database()
        db.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
                code TEXT,
                date TEXT,
                last_price FLOAT,
                max_price FLOAT,
                min_price FLOAT,
                avg_price FLOAT,
                percent_change TEXT,
                quantity FLOAT,
                revenue_best_denars FLOAT,
                total_revenue_denars FLOAT,
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
        print(f"Inserting batch: {batch_data}")  # Debug statement

        # Convert the list of dictionaries into a list of tuples
        formatted_data = [
            (
                record["code"],
                record["date"],
                record["last_price"],
                record["max_price"],
                record["min_price"],
                record["avg_price"],
                record["percent_change"],
                record["quantity"],
                record["revenue_best_denars"],
                record["total_revenue_denars"]
            )
            for record in batch_data
        ]

        db = Database()
        print("Formatted data for insertion:", formatted_data)
        db.executemany('''
            INSERT INTO stock_data (
                code, date, last_price, max_price, min_price, avg_price,
                percent_change, quantity, revenue_best_denars, total_revenue_denars
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', formatted_data)
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