from flask import Flask, jsonify, request
from flask_cors import CORS

from src.stock_repository import StockRepository

app = Flask(__name__)
#CORS(app)

StockRepository.initialize_database()

@app.route('/api/stocks', methods=['POST'])
def save_stock_data():
    data = request.json
    print(data)
    try:
        # Insert the scraped data into the database (using the StockRepository)
        StockRepository.insert_batch_data(data["records"])
        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)