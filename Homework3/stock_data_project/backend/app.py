from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from flask import Flask, jsonify, request
import sqlite3
from scrapingData import scrape_data
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Initialize Background Scheduler
scheduler = BackgroundScheduler(daemon=True)

# Utility Functions
def get_db_connection():
    """Returns a database connection with SQLite."""
    conn = sqlite3.connect('stock_data.db')
    conn.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return conn

# Periodic Task to scrape data every day
def scheduled_scrape():
    print(f"Scraping started at {datetime.now()}")
    scrape_data()

# Configure Scheduler to run every 24 hours
scheduler.add_job(
    scheduled_scrape,
    IntervalTrigger(hours=24),
    next_run_time=datetime.now()  # Starts scraping immediately upon server launch
)

# Start scheduler
scheduler.start()

# API Endpoints
@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    """
    Returns all distinct stock codes with their related historical data.
    The response includes an array of records for each stock code.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch unique stock codes
        cursor.execute("SELECT DISTINCT code FROM stock_data")
        stock_codes = [row['code'] for row in cursor.fetchall()]

        response = {}
        for stock_code in stock_codes:
            cursor.execute("SELECT * FROM stock_data WHERE code = ?", (stock_code,))
            stock_data = cursor.fetchall()
            response[stock_code] = [dict(row) for row in stock_data]

        conn.close()
        return jsonify(response), 200

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_stocks():
    """
    Searches stocks based on the query provided.
    Matches stock codes starting with the search query.
    """
    try:
        search_query = request.args.get('query', '').strip()
        if not search_query:
            return jsonify({"message": "Search query is required."}), 400

        query = """
            SELECT DISTINCT code FROM stock_data
            WHERE code LIKE ?
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (f"{search_query}%",))
        rows = [row['code'] for row in cursor.fetchall()]
        conn.close()

        if not rows:
            return jsonify({"message": "No stocks match your query."}), 404

        return jsonify(rows), 200

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@app.route('/api/stocks/<string:code>', methods=['GET'])
def get_stock_data(code):
    """
    Retrieves stock data for a given code, optionally filtered by date range.
    Supports start_date and end_date query parameters.
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = "SELECT * FROM stock_data WHERE code = ?"
        params = [code]

        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not rows:
            return jsonify({"message": f"No data found for stock code {code}."}), 404

        return jsonify(rows), 200

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@app.route('/stock/stock_indicators/<string:code>/<string:period>', methods=['GET'])
def get_stock_indicators(code, period):
    """
    Fetches stock indicators (e.g., RSI, SMA, CCI) for a specific stock and time period.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT date, cci, vpt, signal FROM stock_indicators
            WHERE code = ? AND time_period = ?
        """
        cursor.execute(query, (code, period))
        indicators = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not indicators:
            return jsonify({"message": f"No indicators found for stock {code} and period {period}."}), 404

        return jsonify(indicators), 200

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


def get_featured_stock_of_the_day():
    """Find the featured stock of the day based on the highest percent change."""
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    # Get the latest date available in the stock_data table
    cursor.execute("SELECT MAX(date) FROM stock_data")
    latest_date = cursor.fetchone()[0]

    # Find the stock with the highest percent change on the latest date
    cursor.execute("""
        SELECT code, date, last_price, percent_change
        FROM stock_data
        WHERE date = ?
        ORDER BY percent_change DESC
        LIMIT 1
    """, (latest_date,))

    featured_stock = cursor.fetchone()
    conn.close()

    if featured_stock:
        featured_stock_data = {
            "code": featured_stock[0],
            "date": featured_stock[1],
            "last_price": featured_stock[2],
            "percent_change": featured_stock[3]
        }
        return featured_stock_data
    else:
        return None


@app.route('/api/featured-stock', methods=['GET'])
def get_featured_stock():
    """Fetch and return the featured stock of the day based on the highest percent change."""
    try:
        featured_stock = get_featured_stock_of_the_day()

        if featured_stock:
            return jsonify(featured_stock), 200
        else:
            return jsonify({"message": "No featured stock found for today."}), 404

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


# App Initialization
if __name__ == "__main__":
    scrape_data()
    app.run(debug=True)
