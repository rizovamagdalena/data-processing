# Service Layer
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.backend.config.config import STOCK_BASE_URL
from src.backend.repositories.stock_repository import StockRepository


class StockService:

    @staticmethod
    def scrape_stock_data():
        StockRepository.initialize_database()
        current_date = datetime.now()
        ten_years_ago = current_date - timedelta(days=10 * 365)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f'{STOCK_BASE_URL}ADIN')
            soup = BeautifulSoup(page.content(), 'html.parser')
            stock_codes = [
                option['value'].strip()
                for option in soup.select('#Code option')
                if option['value'].strip() and not any(char.isdigit() for char in option['value'])
            ]

            for stock_code in stock_codes:
                latest_date = StockRepository.get_latest_date(stock_code)
                scrape_from_date = latest_date + timedelta(days=1) if latest_date else ten_years_ago

                while scrape_from_date <= current_date:
                    year = scrape_from_date.year
                    from_date = scrape_from_date.strftime('%d.%m.%Y')
                    to_date = min(scrape_from_date.replace(year=year) + timedelta(days=364), current_date)
                    to_date_str = to_date.strftime('%d.%m.%Y')

                    page.goto(f'{STOCK_BASE_URL}{stock_code}')

                    if page.query_selector("#resultsTable") is None:
                        scrape_from_date = scrape_from_date.replace(year=year + 1)
                        continue

                    page.fill('#FromDate', from_date)
                    page.fill('#ToDate', to_date_str)
                    page.click('.btn.btn-primary-sm')
                    page.wait_for_selector("#resultsTable", timeout=1000)

                    table_html = page.inner_html('#resultsTable')
                    table_soup = BeautifulSoup(table_html, 'html.parser')
                    rows = table_soup.find_all("tr")[1:]

                    batch_data = []
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) < 9:
                            continue
                        record = (
                            stock_code,
                            cols[0].get_text().strip(),
                            StockService.format_price(cols[1].get_text()),
                            StockService.format_price(cols[2].get_text()),
                            StockService.format_price(cols[3].get_text()),
                            StockService.format_price(cols[4].get_text()),
                            StockService.check_for_zero(cols[5].get_text()),
                            StockService.check_for_zero(cols[6].get_text()),
                            StockService.format_price(cols[7].get_text()),
                            StockService.format_price(cols[8].get_text()),
                        )
                        batch_data.append(record)

                    if batch_data:
                        StockRepository.insert_batch_data(batch_data)

                    scrape_from_date = scrape_from_date.replace(year=year + 1)
            browser.close()

    @staticmethod
    def format_price(value):
        if not value:
            return "0.00"
        try:
            formatted_value = f"{float(value.replace(',', '.').replace('-', '').strip()):.2f}"
            return f"-{formatted_value}" if value.startswith('-') else formatted_value
        except ValueError:
            return "0.00"

    @staticmethod
    def check_for_zero(value):
        return "0" if not value else value