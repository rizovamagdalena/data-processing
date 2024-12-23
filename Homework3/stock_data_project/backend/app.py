from flask import Flask, jsonify, request
import sqlite3
from scrapingData import scrape_data
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)



def run_scraping():
    if not os.path.exists('stock_data.db'):  # Check if the DB already exists
        print("Starting scraping process...")
        scrape_data()
    else:
        print("Scraping process already completed. Skipping.")

def get_db_connection():
    conn = sqlite3.connect('stock_data.db')
    conn.row_factory = sqlite3.Row  # To fetch rows as dictionaries
    return conn


@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    try:

        conn = get_db_connection()  # Use helper function for connection
        cursor = conn.cursor()

        # Query to get all data
        cursor.execute("SELECT DISTINCT code FROM stock_data")
        stock_codes = cursor.fetchall()

        response = {}

        for stock_code in stock_codes:
            stock_code = stock_code['code']
            cursor.execute("SELECT * FROM stock_data WHERE code = ?", (stock_code,))
            stock_data = cursor.fetchall()
            response[stock_code] = [dict(row) for row in stock_data]

        conn.close()
        return jsonify(response)

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_stocks():
    try:
        search_query = request.args.get('query', '')  # Get search query from URL parameter
        if not search_query:
            return jsonify({"message": "No query provided."}), 400

        # Query to find all unique stocks that start with the search query in the 'code' column
        query = """
            SELECT DISTINCT code FROM stock_data
            WHERE code LIKE ? 
        """
        params = [f"{search_query}%"]  # The '%' wildcard allows matching all codes starting with the query

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({"message": "No stocks found matching your query."}), 404

        # Return just the list of unique stock codes
        data = [row[0] for row in rows]
        return jsonify(data)

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500



@app.route('/api/stocks/<string:code>', methods=['GET'])
def get_stock_data(code):
    try:
        # Get the start and end dates if present in the query params
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # The `code` parameter is dynamically passed via URL
        issuer_code = code

        # print(f"Fetching data for stock: {code} from {start_date} to {end_date}")

        # Base query to get stock data
        query = """
                   SELECT * FROM stock_data
                   WHERE code = ?
               """
        params = [issuer_code]

        # Apply date filter if start_date and end_date are provided
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        # Get data from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # If no data is found for the issuer, return an empty array
        if not rows:
            return jsonify({"message": "No data found for the given issuer code."}), 404

        # Convert the rows to a list of dictionaries (for easier JSON serialization)
        data = [dict(row) for row in rows]
        # print("Response data:", data)

        return jsonify(data)

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500





if __name__ == "__main__":
    run_scraping()  # Run the scraping before starting the app
    app.run(debug=True)
