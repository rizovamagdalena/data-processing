import sqlite3

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
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = StockRepository.fetch_stock_data_by_code(code, start_date, end_date)
        if not data:
            return jsonify({"message": f"No data found for stock code {code}."}), 404
        return jsonify({"data": data}), 200
    except sqlite3.DatabaseError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
