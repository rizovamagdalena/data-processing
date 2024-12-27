import os
import sqlite3
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Database Utility
DATABASE_PATH = 'stock_data.db'


def initialize_database():
    """Create the stock_data table if it doesn't already exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            code TEXT,
            date TEXT,
            last_price TEXT,
            max_price TEXT,
            min_price TEXT,
            avg_price TEXT,
            percent_change TEXT,
            quantity TEXT,
            revenue_best_denars TEXT,
            total_revenue_denars TEXT,
            UNIQUE(code, date) ON CONFLICT IGNORE
        )
    ''')
    conn.commit()
    conn.close()


def get_latest_date(cursor, stock_code):
    """Retrieve the latest date from the database for a specific stock code."""
    cursor.execute("SELECT date FROM stock_data WHERE code = ? ORDER BY date DESC LIMIT 1", (stock_code,))
    result = cursor.fetchone()
    return datetime.strptime(result[0], '%d.%m.%Y') if result else None




def format_price(value):
    """Format price values into a consistent decimal format."""
    if not value:
        return "0.00"
    try:
        formatted_value = f"{float(value.replace(',', '.').replace('-', '').strip()):.2f}"
        return f"-{formatted_value}" if value.startswith('-') else formatted_value
    except ValueError:
        return "0.00"


def check_for_zero(value):
    """Ensure value is not empty or None."""
    return "0" if not value else value


def scrape_stock_data():
    """Main function to scrape stock data and save it into the database."""
    initialize_database()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    current_date = datetime.now()
    ten_years_ago = current_date - timedelta(days=10 * 365)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to get stock codes
        page.goto('https://www.mse.mk/mk/stats/symbolhistory/ADIN')
        soup = BeautifulSoup(page.content(), 'html.parser')
        stock_codes = [
            option['value'].strip()
            for option in soup.select('#Code option')
            if option['value'].strip() and not any(char.isdigit() for char in option['value'])
        ]
        print(f"Found stock codes: {stock_codes}")

        try:
            for stock_code in stock_codes:
                print(f"Processing stock code: {stock_code}")
                latest_date = get_latest_date(cursor, stock_code)
                scrape_from_date = latest_date + timedelta(days=1) if latest_date else ten_years_ago

                while scrape_from_date <= current_date:
                    year = scrape_from_date.year
                    from_date = scrape_from_date.strftime('%d.%m.%Y')

                    # If 'to_date' exceeds 'current_date', use 'current_date' instead
                    to_date = scrape_from_date.replace(year=year) + timedelta(days=364)
                    to_date = min(to_date, current_date)  # Ensure 'to_date' does not exceed 'current_date'

                    to_date_str = to_date.strftime('%d.%m.%Y')  # Format 'to_date' as a string

                    print(f"Fetching data for {stock_code}: {from_date} to {to_date_str}")
                    page.goto(f'https://www.mse.mk/mk/stats/symbolhistory/{stock_code}')
                    try:
                        # Check for table existence
                        table_exists = page.query_selector("#resultsTable") is not None

                        if not table_exists:
                            scrape_from_date = scrape_from_date.replace(year=year + 1)
                            continue  # Skip processing if table doesn't exist

                        page.fill('#FromDate', from_date)
                        page.fill('#ToDate', to_date_str)
                        page.click('.btn.btn-primary-sm')
                        page.wait_for_selector("#resultsTable", timeout=1000)

                        table_html = page.inner_html('#resultsTable')
                        table_soup = BeautifulSoup(table_html, 'html.parser')
                        rows = table_soup.find_all("tr")[1:]  # Skip header row

                        batch_data = []
                        for row in rows:
                            cols = row.find_all('td')
                            if len(cols) < 9:
                                continue
                            record = (
                                stock_code,
                                cols[0].get_text().strip(),
                                format_price(cols[1].get_text()),
                                format_price(cols[2].get_text()),
                                format_price(cols[3].get_text()),
                                format_price(cols[4].get_text()),
                                check_for_zero(cols[5].get_text()),
                                check_for_zero(cols[6].get_text()),
                                format_price(cols[7].get_text()),
                                format_price(cols[8].get_text()),
                            )
                            batch_data.append(record)

                        if batch_data:
                            cursor.executemany(''' 
                                INSERT INTO stock_data (
                                    code, date, last_price, max_price, min_price, avg_price,
                                    percent_change, quantity, revenue_best_denars, total_revenue_denars
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                            ''', batch_data)
                            conn.commit()
                            print(f"Inserted {len(batch_data)} records for {stock_code}.")
                    except Exception as e:
                        print(f"Error fetching data for {stock_code}: {e}")
                        scrape_from_date = scrape_from_date.replace(year=year + 1)
                        continue

                    # Move to next year
                    scrape_from_date = scrape_from_date.replace(year=year + 1)

        except Exception as e:
            print(f"Scraping error: {e}")
        browser.close()

    conn.close()
    print("Scraping completed.")

if __name__ == "__main__":
    scrape_stock_data()
