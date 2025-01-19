from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from stock_service import StockService

# Initialize and configure the scheduler
scheduler = BackgroundScheduler()

def start_scheduler():
    """ Start the scheduler for periodic tasks """
    scheduler.add_job(
        StockService.scrape_stock_data,
        IntervalTrigger(hours=24),
        id='scraping_job',
        next_run_time=datetime.now()  # Run immediately when app starts
    )
    scheduler.start()
