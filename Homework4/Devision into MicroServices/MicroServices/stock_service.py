from datetime import datetime, timedelta
from stock_repository import StockRepository
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StockService:
    """ Service to handle the scraping of stock data """

    @staticmethod
    def scrape_stock_data():
        """ Main method to scrape stock data """
        StockRepository.initialize_database()
        current_date = datetime.now()
        ten_years_ago = current_date - timedelta(days=10 * 365)

        # Setup Selenium WebDriver
        driver = webdriver.Chrome()

        try:
            driver.get('https://www.mse.mk/mk/stats/symbolhistory/ADIN')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            stock_codes = [
                option['value'].strip()
                for option in soup.select('#Code option')
                if option['value'].strip() and not any(char.isdigit() for char in option['value'])
            ]

            for stock_code in stock_codes:
                print("Stock CODE: " + stock_code)
                latest_date = StockRepository.get_latest_date(stock_code)
                scrape_from_date = latest_date + timedelta(days=1) if latest_date else ten_years_ago

                while scrape_from_date <= current_date:
                    from_date = scrape_from_date
                    to_date = min(scrape_from_date + timedelta(days=364), current_date)

                    driver.get(f'https://www.mse.mk/mk/stats/symbolhistory/{stock_code}')
                    try:
                        input_field = driver.find_element(By.ID, "FromDate")
                        input_field2 = driver.find_element(By.ID, "ToDate")
                        input_field.clear()
                        input_field2.clear()

                        input_field.send_keys(from_date.strftime("%d.%m.%Y"))
                        input_field2.send_keys(to_date.strftime("%d.%m.%Y"))
                        refresh_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary-sm")
                        refresh_button.click()

                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "resultsTable"))
                        )

                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        table = soup.find('table', {'id': 'resultsTable'})
                        batch_data = []

                        if table:
                            table_rows = table.find_all('tr')[1:]  # Skip header row
                            for row in table_rows:
                                cols = row.find_all("td")
                                if len(cols) < 9: continue
                                if str(cols[7].get_text()) == "0" and str(cols[8].get_text()) == "0":
                                    continue

                                date = datetime.strptime(cols[0].get_text().strip(), '%d.%m.%Y')
                                record = (
                                    stock_code,
                                    date.strftime("%Y-%m-%d"),
                                    StockService.format_price(cols[1].get_text().strip()),
                                    StockService.format_price(cols[2].get_text().strip()),
                                    StockService.format_price(cols[3].get_text().strip()),
                                    StockService.format_price(cols[4].get_text().strip()),
                                    StockService.check_for_zero(cols[5].get_text().strip()),
                                    StockService.check_for_zero(cols[6].get_text().strip()),
                                    StockService.format_price(cols[7].get_text().strip()),
                                    StockService.format_price(cols[8].get_text().strip())
                                )
                                batch_data.append(record)

                        if batch_data:
                            StockRepository.insert_batch_data(batch_data)

                        scrape_from_date += timedelta(days=365)

                    except Exception as e:
                        print(f"Error for stock {stock_code} from {from_date} to {to_date}: {e}")
                        break

        finally:
            driver.quit()

    @staticmethod
    def format_price(value):
        """ Helper function to format prices """
        if not value.strip():
            return "0.00"
        try:
            cleaned_value = value.replace('.', '').replace(',', '.').strip()
            return f"{float(cleaned_value):.2f}"
        except ValueError:
            return "0.00"

    @staticmethod
    def check_for_zero(value):
        """ Ensure zero handling in the data """
        return "0" if not value else value
