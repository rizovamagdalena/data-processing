import os
from datetime import datetime, timedelta
import pandas as pd
from tornado.http1connection import parse_int

from src.technical_analysis.TechnicalAnalysis_models.database import Database


class TechnicalAnalysisRepository:

    @staticmethod
    def initialize_database():
        db = Database()
        db.execute('''CREATE TABLE IF NOT EXISTS stock_indicators (
        code TEXT,
        date TEXT,
        time_period TEXT,
        cci REAL,
        vpt REAL,
        signal TEXT,
        PRIMARY KEY (code,date, time_period)
    );''')
        db.commit()


    @staticmethod
    def insert_row(row, code, date_str, time_period):
        db = Database()

        existing = db.execute("""
                    SELECT 1 FROM stock_indicators 
                    WHERE code = ? AND date = ? AND time_period = ?""", (code, date_str, time_period))

        if not existing:
            db.execute("""
                        INSERT INTO stock_indicators (code, date, time_period, cci, vpt, signal)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                         (code, date_str, time_period, row['CCI'], row['VPT'], row['Signal']))

        db.commit()

    @staticmethod
    def fetch_stock_indicators_for_code_in_period(stock_code, period='1D'):
        db = Database()
        query = "SELECT * FROM stock_indicators WHERE code LIKE ?"
        query += " AND date BETWEEN ? AND ? AND time_period = ?"

        start_date = ''
        end_date = datetime.now().strftime('%Y-%m-%d')

        if period=='1D':
            start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        elif period=='1W':
            start_date = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')

        elif period=='1M':
            start_date = (datetime.now() - timedelta(weeks=4)).strftime('%Y-%m-%d')


        db.execute(query, (f"{stock_code}%", start_date, end_date, period))
        return db.fetchall()
