from flask import Flask, jsonify
import sqlite3
from scrapingData import scrape_data
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)


def run_scraping():
    print("Starting scraping process...")
    scrape_data()

# Assuming you already have a function to get the database connection
def get_db_connection():
    conn = sqlite3.connect('stock_data_PROTOTYPE.db')
    conn.row_factory = sqlite3.Row  # To fetch rows as dictionaries
    return conn


@app.route('/api/stocks/ADIN', methods=['GET'])
def get_stock_data():
    try:
        issuer_code = 'ADIN'  # Hardcoding the issuer code to ADIN

        # Query to get all data for the specified issuer
        query = """
            SELECT * FROM stock_data_PROTOTYPE
            WHERE code = ?
        """
        params = [issuer_code]

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
        print("Response data:", data)

        return jsonify(data)

    except sqlite3.DatabaseError as e:
        # Handle database error
        return jsonify({"error": "Database error", "message": str(e)}), 500

    except Exception as e:
        # Catch all for any other unexpected errors
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500

if __name__ == "__main__":
    run_scraping()  # Run the scraping before starting the app
    app.run(debug=True)
