import os
import sqlite3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify, request
from flask_cors import CORS

# Constants
DATABASE_stock_data_PATH = 'C:/Users/Dimitrij/PycharmProjects/DIANS_stockdata/stock_data.db'
DATABASE_stock_indicators_PATH = 'C:/Users/Dimitrij/PycharmProjects/DIANS_stockdata/stock_indicators.db'
STOCK_BASE_URL = 'https://www.mse.mk/mk/stats/symbolhistory/'
