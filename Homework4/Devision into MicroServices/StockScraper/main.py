from flask import Flask, request, jsonify
from src.stock_service import StockService

'''import requests

test_data = {"records": [{"code": "TEST", "date": "01.01.2023", "last_price": 123.45, "max_price": 150.0, "min_price": 120.0, "avg_price": 135.0, "percent_change": "5%", "quantity": 100, "revenue_best_denars": 12345.67, "total_revenue_denars": 56789.01}]}

response = requests.post("http://127.0.0.1:5003/api/stocks", json=test_data)
print(response.status_code)
print(response.json())'''

app = Flask(__name__)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'GET':
        return jsonify({"message": "Scraping service is up. Use POST to trigger scraping."}), 200

    # Your existing POST logic
    data = request.json
    try:
        StockService.scrape_stock_data()
        return jsonify({"message": "Scraping completed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002)
