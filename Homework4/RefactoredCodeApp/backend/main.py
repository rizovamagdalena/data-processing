# main.py
from src.backend.app.app import app
from src.backend.app.app import scheduler
from src.backend.services.stock_service import StockService
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from src.technical_analysis.TechnicalAnalysis import TechnicalAnalysis

if __name__ == "__main__":
    # Schedule the scraping task
    scheduler.add_job(
        StockService.scrape_stock_data,
        IntervalTrigger(hours=24),
        next_run_time=datetime.now()
    )

    scheduler.add_job(
        TechnicalAnalysis.init,
        IntervalTrigger(hours=24),
        next_run_time=datetime.now()
    )

    scheduler.start()


    # Run the Flask app
    app.run(debug=True)
