import time
import sqlite3
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

        time.sleep(3)

        table = driver.find_element(By.ID, 'resultsTable')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        counter = 0

        for row in reversed(rows[1:]):

            cells = row.find_elements(By.TAG_NAME, 'td')

            if len(cells) > 1:

                last_column_value = cells[7].get_attribute('innerHTML').strip()
                second_last_column_value = cells[8].get_attribute('innerHTML').strip()

                if last_column_value == "0" and second_last_column_value == "0":
                    continue

                if cells[0].get_attribute('innerHTML').strip() == "21.10.2024":
                    print(f"[INFO]  cell 2 {cells[1].get_attribute('innerHTML')}")
                    print(f"[INFO]  cell 3 {cells[2].get_attribute('innerHTML')}")
                    print(f"[INFO]  cell 4 {cells[3].get_attribute('innerHTML')}")
                    print(f"[INFO]  cell 5 {cells[4].get_attribute('innerHTML')}")
                    print(f"[INFO]  cell 2 Form {format_price(cells[1].get_attribute('innerHTML'))}")
                    print(f"[INFO]  cell 3 Form {format_price(cells[2].get_attribute('innerHTML'))}")
                    print(f"[INFO]  cell 4 Form {format_price(cells[3].get_attribute('innerHTML'))}")
                    print(f"[INFO]  cell 5 Form {format_price(cells[4].get_attribute('innerHTML'))}")


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
                if cells[0].get_attribute('innerHTML').strip() == "21.10.2024":
                    print(f"[INFO]  {data}")

        current_date = next_date

        time.sleep(2)

    print("[INFO] Data extraction complete. Closing the WebDriver.")
    driver.quit()

    return all_data


def format_price(value):
    if value == "" or value is None:
        return "0.00"


    if isinstance(value, float):
        value = str(value)

    # if len(value) > 2 and value[-3] == '.':
    #     return value  # No formatting needed if the third-to-last character is a dot

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
            parts = value.split('.')  # Re-split after cleaning the string
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


print(format_price("1.650,00"))

def check_for_zero(value):
    if value == "" or value is None:
        return "0"
    else:
        return value



def insert_data_into_db(issuer_code, stock_data):
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    print("[INFO] Inserting data into the database...")

    for entry in stock_data:
        date = entry['date']
        last_transaction_price = format_price(entry['last_transaction_price'])
        max_price = format_price(entry.get('max_price', 0.0))
        min_price = format_price(entry.get('min_price', 0.0))
        average_price = format_price(entry.get('average_price', 0.0))
        percentage_change = entry.get('percentage_change', 0.0)
        quantity = entry.get('quantity', 0)
        turnover_best_in_denars = format_price(entry.get('turnover_best_in_denars', 0.0))
        total_turnover_in_denars = format_price(entry.get('total_turnover_in_denars', 0.0))

        cursor.execute('''
            SELECT 1 FROM stock_prices WHERE issuer_code = ? AND date = ?
        ''', (issuer_code, date))

        if cursor.fetchone() is None:

            cursor.execute('''
                INSERT INTO stock_prices (
                    issuer_code, date, last_transaction_price, max_price, min_price,
                    average_price, percentage_change, quantity, turnover_best_in_denars,
                    total_turnover_in_denars
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                issuer_code, date, last_transaction_price, max_price, min_price,
                average_price, percentage_change, quantity, turnover_best_in_denars,
                total_turnover_in_denars
            ))

    conn.commit()
    conn.close()
    print("[INFO] Data inserted into the database successfully.")


def fill_missing_data_for_issuer(issuer_code, start_date):
    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"[INFO] Fetching data for {issuer_code} from {start_date} to {end_date}...")
    stock_data = fetch_stock_data_for_issuer(issuer_code, start_date, end_date)

    if not stock_data:
        print(f"[ERROR] No data fetched for {issuer_code} from {start_date} to {end_date}.")
        return

    print(f"[INFO] Inserting data for {issuer_code} into the database...")
    insert_data_into_db(issuer_code, stock_data)

    print(f"[INFO] Data for {issuer_code} from {start_date} to {end_date} successfully filled in.")
