from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from stock_service import StockService  # Import the StockService
import time

app = Flask(__name__)
DATABASE_URL = "sqlite:///database/stock_data.db"  # Store the database in the 'database' folder


# Scheduler setup to run every 24 hours (scraping)
scheduler = BackgroundScheduler()

def start_scraping_task():
    """ Function that starts scraping and saves the stock data to the database. """
    try:
        StockService.scrape_stock_data()
        print("Stock scraping finished successfully.")
    except Exception as e:
        print(f"Error during scraping: {str(e)}")

# Schedule the scraping task to run every 24 hours
scheduler.add_job(
    start_scraping_task,
    IntervalTrigger(hours=24),
    id='scraping_job',
    next_run_time=None  # It will start after the program starts, so setting the first run immediately.
)

# API endpoint to manually trigger scraping via POST request
@app.route('/api/scrape', methods=['POST'])
def trigger_scraping():
    """ API endpoint to manually trigger the stock scraping task. """
    try:
        print("Triggered")
        StockService.scrape_stock_data()
        return jsonify({"message": "Scraping started successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to check the status of the scraping task
@app.route('/api/status', methods=['GET'])
def check_status():
    """ Returns the status of the scraping service. """
    return jsonify({"status": "Scraping service is running"}), 200

# Start the scheduler when Flask app starts
def start_scheduler():
    print("Scheduler starting...")  # Debug message
    scheduler.start()
    print(scheduler.get_jobs())

# Main entry point
if __name__ == "__main__":
    # Start the scheduler for periodic tasks
    start_scheduler()
    # start_scraping_task() #JUST FOR TEST PURPOSES


    # Run the Flask application
    app.run(debug=True, use_reloader=False,port=8080)  # use_reloader=False to avoid duplicate jobs in development

    # Keep the service running (required to prevent Flask's auto-reloading)
    while True:
        time.sleep(60)
