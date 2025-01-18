from flask import Flask, request, jsonify
from src.stock_service import StockService

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
