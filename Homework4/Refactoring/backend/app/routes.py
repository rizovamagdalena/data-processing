#WORK IN PROGRESS

import sqlite3
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from src.backend.repositories.stock_repository import StockRepository


stock_routes = Blueprint('stock_routes', __name__)

@stock_routes.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    try:
        stock_codes = StockRepository.fetch_all_stock_codes()
        return jsonify({"stocks": stock_codes}), 200
    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

@stock_routes.route('/api/stocks/<string:code>', methods=['GET'])
def get_stock_data(code):
    try:
        # Get 'start_date' and 'end_date' from query parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        #-----------------------------------------------------------------------------------
        print(f"start: {start_date_str}, end: {end_date_str}")  # Debugging output
        #------------------------------------------------------------------------------------

        # Fetch the stock data for the specified period
        stock_data = StockRepository.search_stock_data_by_code_in_interval(code, start_date_str, end_date_str)
        if not stock_data:
            return jsonify({"message": f"No data found for stock code {code}."}), 404

        return jsonify({"data": stock_data}), 200
    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500

@stock_routes.route('/api/search', methods=['GET'])
def search_stocks():
    try:
        search_query = request.args.get('query', '').strip()

        if not search_query:
            return jsonify({"message": "Search query is required."}), 400

        all_stock_codes = StockRepository.fetch_all_stock_codes()

        filtered_stock_codes = [code for code in all_stock_codes if code.lower().startswith(search_query.lower())]

        if not filtered_stock_codes:
            return jsonify({"message": "No stocks match your query."}), 404

        return jsonify({"stocks": filtered_stock_codes}), 200

    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


'''@stock_routes.route('/api/stock_indicators/<string:code>/<string:period>', methods=['GET'])
def get_stock_indicators(code, period):
    """
    Fetches stock indicators (e.g., RSI, SMA, CCI) for a specific stock and time period.
    """
    try:
        indicators = StockRepository.fetch_stock_indicators(code, period)

        if not indicators:
            return jsonify({"message": f"No indicators found for stock {code} and period {period}."}), 404

        return jsonify({"indicators": indicators}), 200
    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@stock_routes.route('/api/featured-stock', methods=['GET'])
def get_featured_stock():
    """
    Fetch and return the featured stock of the day based on the highest percent change.
    """
    try:
        featured_stock = StockRepository.fetch_featured_stock_of_the_day()

        if featured_stock:
            return jsonify({"featured_stock": featured_stock}), 200
        else:
            return jsonify({"message": "No featured stock found for today."}), 404
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500'''
