# Service Layer
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.backend.repositories.stock_repository import StockRepository


class StockService:

    @staticmethod
    def scrape_stock_data():
        # Initialize the database
        StockRepository.initialize_database()

        # Define the date range
        current_date = datetime.now()
        ten_years_ago = current_date - timedelta(days=10 * 365)

        # Initialize WebDriver
        driver = webdriver.Chrome()

        try:
            # Navigate to the initial page to retrieve stock codes
            driver.get('https://www.mse.mk/mk/stats/symbolhistory/ADIN')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            stock_codes = [
                option['value'].strip()
                for option in soup.select('#Code option')
                if option['value'].strip() and not any(char.isdigit() for char in option['value'])
            ]

            for stock_code in stock_codes:
                # Determine the starting date for scraping
                latest_date = StockRepository.get_latest_date(stock_code)
                scrape_from_date = latest_date + timedelta(days=1) if latest_date else ten_years_ago

                while scrape_from_date <= current_date:
                    # Set date range
                    from_date = scrape_from_date
                    to_date = min(scrape_from_date + timedelta(days=364), current_date)

                    # Navigate to the stock page
                    driver.get(f'https://www.mse.mk/mk/stats/symbolhistory/{stock_code}')

                    try:
                        # Locate the date fields and fill in the values
                        input_field = driver.find_element(By.ID, "FromDate")
                        input_field2 = driver.find_element(By.ID, "ToDate")

                        input_field.clear()
                        input_field2.clear()

                        input_field.send_keys(from_date.strftime("%d.%m.%Y"))
                        input_field2.send_keys(to_date.strftime("%d.%m.%Y"))

                        # Locate and click the refresh button
                        refresh_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary-sm")
                        refresh_button.click()

                        # Wait for the results table to load
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "resultsTable"))
                        )

                        # Get the updated HTML and parse it
                        updated_html = driver.page_source
                        soup = BeautifulSoup(updated_html, 'html.parser')

                        # Extract data from the table
                        table = soup.find('table', {'id': 'resultsTable'})
                        batch_data = []
                        if table:
                            table_rows = table.find_all('tr')[1:]  # Skip header row
                            for row in table_rows:
                                cols = row.find_all("td")
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

                        # Insert data into the database
                        if batch_data:
                            StockRepository.insert_batch_data(batch_data)

                        # Move to the next year
                        scrape_from_date += timedelta(days=365)

                    except Exception as e:
                        print(f"Timeout or error for stock code {stock_code} from {from_date} to {to_date}: {e}")
                        break  # Break the inner loop and move to the next stock_code

        finally:
            # Close the driver
            driver.quit()

    @staticmethod
    def format_price(value):
        """Format price to a consistent format with 2 decimal places."""
        if not value:
            return "0.00"
        try:
            formatted_value = f"{float(value.replace(',', '.').replace('-', '').strip()):.2f}"
            return f"-{formatted_value}" if value.startswith('-') else formatted_value
        except ValueError:
            return "0.00"

    @staticmethod
    def check_for_zero(value):
        """Ensure values default to '0' if empty."""
        return "0" if not value else value
