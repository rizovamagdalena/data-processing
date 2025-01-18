from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import os


class StockService:

    @staticmethod
    def scrape_stock_data():
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
                # Use a static starting date or a placeholder value
                scrape_from_date = ten_years_ago

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
                                date = datetime.strptime(cols[0].get_text().strip(), '%d.%m.%Y')
                                record = (
                                    stock_code,
                                    date.strftime("%Y-%m-%d"),
                                    # cols[0].get_text().strip(),
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

                        # Save data locally
                        if batch_data:
                            StockService.save_data_to_csv(batch_data)
                            StockService.read_csv_and_send_to_api('scraped_stockdata.csv')

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

        if not value or not value.strip():
            return "0.00"  # Default to 0.00 if the value is empty

        try:
            # Replace thousands separator '.' with '' and decimal separator ',' with '.'
            cleaned_value = value.replace('.', '').replace(',', '.').strip()
            # Convert to float and format to 2 decimal places
            formatted_value = f"{float(cleaned_value):.2f}"
            return formatted_value
        except ValueError as e:
            # Log an error for unexpected formats
            print(f"Error formatting price '{value}': {e}")
            return "0.00"  # Return default value if parsing fails

    @staticmethod
    def check_for_zero(value):
        """Ensure values default to '0' if empty."""
        return "0" if not value else value

    @staticmethod
    def save_data_to_csv(batch_data, file_name="scraped_stockdata.csv"):
        """Save scraped data to a CSV file with proper headers."""
        # Check if the file already exists
        file_exists = os.path.exists(file_name)

        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # If the file does not exist, write the headers
            if not file_exists:
                writer.writerow(["code", "date", "last_price", "max_price", "min_price", "avg_price",
                                 "percent_change", "quantity", "revenue_best_denars", "total_revenue_denars"])

            # Write the data
            for record in batch_data:
                writer.writerow(record)

    @staticmethod
    def read_csv_and_send_to_api(csv_file):
        #print(f"File exists: {os.path.exists(csv_file)}")
        stock_data = []
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock_data.append({
                    "code": row["code"],  # Adjust keys based on actual header
                    "date": row["date"],
                    "last_price": float(row["last_price"]),
                    "max_price": float(row["max_price"]),
                    "min_price": float(row["min_price"]),
                    "avg_price": float(row["avg_price"]),
                    "percent_change": row["percent_change"],
                    "quantity": float(row["quantity"]),
                    "revenue_best_denars": float(row["revenue_best_denars"]),
                    "total_revenue_denars": float(row["total_revenue_denars"]),
                })
        # Send the data to the API
        StockService.send_scraped_data_to_api(stock_data)

    @staticmethod
    def send_scraped_data_to_api(data):
        print(f"Sending data to API: {data}")
        url = "http://127.0.0.1:5003/api/stocks"  # Endpoint of Stock Data Microservice
        try:
            response = requests.post(url, json={"records": data})
            if response.status_code == 200:
                print("Data sent successfully")
            else:
                print("Failed to send data:", response.json())
        except requests.exceptions.RequestException as e:
            print("Error sending data:", str(e))
