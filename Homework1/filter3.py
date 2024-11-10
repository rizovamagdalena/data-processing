import time
import csv
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # Add additional options if necessary (e.g., window size for scraping)

    service = Service(r"C:\webdrivers\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("[INFO] Selenium WebDriver initialized.")
    return driver


def fetch_stock_data_for_issuer(issuer_code, start_date, end_date):
    driver = get_driver()

    url = f"https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}"
    print(f"[INFO] Opening URL: {url}")
    driver.get(url)

    print("[INFO] Waiting for the page to load...")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'FromDate')))

    current_date = datetime.strptime(start_date, "%d.%m.%Y")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = []

    while current_date < end_date:
        next_date = current_date + timedelta(days=365)
        if next_date > end_date:
            next_date = end_date

        from_date_str = current_date.strftime("%d.%m.%Y")
        to_date_str = next_date.strftime("%d.%m.%Y")

        print(f"[INFO] Setting dates: From {from_date_str} to {to_date_str}")

        from_date_input = driver.find_element(By.ID, "FromDate")
        to_date_input = driver.find_element(By.ID, "ToDate")
        from_date_input.clear()
        from_date_input.send_keys(from_date_str)
        to_date_input.clear()
        to_date_input.send_keys(to_date_str)

        submit_button = driver.find_element(By.XPATH, '//input[@value="Прикажи"]')
        print("[INFO] Clicking the 'Прикажи' button...")
        submit_button.click()

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'resultsTable')))

        time.sleep(random.uniform(2, 4))  # Random sleep between 2 and 4 seconds

        table = driver.find_element(By.ID, 'resultsTable')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        for row in reversed(rows[1:]):  # Reversed to handle the most recent data first
            cells = row.find_elements(By.TAG_NAME, 'td')

            if len(cells) > 1:
                last_column_value = cells[7].get_attribute('innerHTML').strip()
                second_last_column_value = cells[8].get_attribute('innerHTML').strip()

                if last_column_value == "0" and second_last_column_value == "0":
                    continue

                data = {
                    'date': cells[0].get_attribute('innerHTML').strip(),
                    'last_transaction_price': format_price(cells[1].text.strip()),
                    'max_price': format_price(cells[2].get_attribute('innerHTML').strip()),
                    'min_price': format_price(cells[3].get_attribute('innerHTML').strip()),
                    'average_price': format_price(cells[4].get_attribute('innerHTML').strip()),
                    'percentage_change': check_for_zero(cells[5].get_attribute('innerHTML')),
                    'quantity': check_for_zero(cells[6].get_attribute('innerHTML').strip()),
                    'turnover_best_in_denars': format_price(cells[7].get_attribute('innerHTML').strip()),
                    'total_turnover_in_denars': format_price(cells[8].get_attribute('innerHTML').strip())
                }
                all_data.append(data)

        current_date = next_date

        time.sleep(random.uniform(1, 2))  # Random sleep for next iteration to avoid pattern detection

    print("[INFO] Data extraction complete. Closing the WebDriver.")
    driver.quit()

    return all_data


def format_price(value):
    """Format price values properly, handling different formats."""
    if value == "" or value is None:
        return "0.00"

    if isinstance(value, float):
        value = str(value)

    is_negative = value.startswith('-')
    if is_negative:
        value = value[1:]

    if ',' in value and '.' in value:
        value = value.replace('.', '')
        value = value.replace(',', '.')
    elif ',' in value:
        value = value.replace(',', '.')
    elif '.' in value:
        value = value.replace('.', '')

    if '.' in value:
        parts = value.split('.')
        if len(parts) > 2:
            value = f"{parts[0]}.{''.join(parts[1:2])}"  # Join all parts after the first period
        integer_part, decimal_part = parts[0], parts[1]
    else:
        integer_part, decimal_part = value, '00'

    decimal_part = (decimal_part + '00')[:2]

    try:
        integer_part = f"{int(integer_part):,}"
    except ValueError:
        return "0.00"

    formatted_value = f"{integer_part}.{decimal_part}"

    if is_negative:
        formatted_value = f"-{formatted_value}"

    return formatted_value


def check_for_zero(value):
    """Check if the value is empty or None and return '0'."""
    return "0" if value == "" or value is None else value


def write_data_to_csv(issuer_code, stock_data):
    """Write the fetched stock data to a CSV file."""
    filename = "stock_data.csv"

    # Check if the file already exists, and if not, write headers
    file_exists = False
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass  # File doesn't exist, will be created

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'issuer_code', 'date', 'last_transaction_price', 'max_price', 'min_price',
            'average_price', 'percentage_change', 'quantity', 'turnover_best_in_denars',
            'total_turnover_in_denars'
        ])

        if not file_exists:
            writer.writeheader()  # Write header only if file doesn't exist

        for entry in stock_data:
            entry['issuer_code'] = issuer_code  # Add issuer_code to each entry
            writer.writerow(entry)

    print(f"[INFO] Data for {issuer_code} written to {filename}.")


def fill_missing_data_for_issuer(issuer_code, start_date):
    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"[INFO] Fetching data for {issuer_code} from {start_date} to {end_date}...")
    stock_data = fetch_stock_data_for_issuer(issuer_code, start_date, end_date)

    if not stock_data:
        print(f"[ERROR] No data fetched for {issuer_code} from {start_date} to {end_date}.")
        return

    print(f"[INFO] Writing data for {issuer_code} into CSV file...")
    write_data_to_csv(issuer_code, stock_data)

    print(f"[INFO] Data for {issuer_code} from {start_date} to {end_date} successfully filled in.")


# Example usage:
if __name__ == "__main__":
    # Replace with actual issuer codes and start date
    issuer_codes = ['REPL', 'ADIN']
    for issuer_code in issuer_codes:
        start_date = "01.01.2020"  # Replace with the actual start date
        fill_missing_data_for_issuer(issuer_code, start_date)
