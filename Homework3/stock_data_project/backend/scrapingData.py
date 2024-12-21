import time
import sqlite3
import traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os

def delete_database():
    try:
        # Specify the path to your database file
        db_path = 'stock_data.db'

        # Delete the database file
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Database file '{db_path}' has been deleted.")
        else:
            print(f"The file '{db_path}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")


def scrape_data():
    delete_database()

    def format_price(value):
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
                value = f"{parts[0]}.{''.join(parts[1:2])}"
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
        return "0" if value == "" or value is None else value

    # Initialize SQLite database
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    # Create a table for stock data
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
           total_revenue_denars TEXT
       )
       ''')
    conn.commit()

    # Initialize Playwright to interact with the web page
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the target webpage for retrieving stock codes
        page.goto('https://www.mse.mk/mk/stats/symbolhistory/ADIN')

        # Get the list of stock codes from the dropdown
        html = page.content()
        sp = BeautifulSoup(html, 'html.parser')

        select_element = sp.find('select', {'id': 'Code'})
        stock_codes = []
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                issuer_code = option['value'].strip()
                if issuer_code and not any(char.isdigit() for char in issuer_code):
                    stock_codes.append(issuer_code)

        print(f"Found stock codes: {stock_codes}")

        start_time = time.time()

        try:
            for stock_code in stock_codes:
                print(f"Saving data for stock: {stock_code}")
                # Start year_counter for each stock code
                year_counter = 10  # Loop over the last 2 years (e.g. 2023 and 2024)
                current_year = 2024

                while year_counter >= 1:
                    try:
                        year = current_year - year_counter
                        new_from_date = f"01.01.{year}"
                        new_to_date = f"31.12.{year}"

                        # Check for table existence
                        table_exists = page.query_selector("#resultsTable") is not None

                        if not table_exists:
                            year_counter -= 1
                            continue  # Skip processing if table doesn't exist

                        # Find and set fields for dates and search button for this stock code
                        search_button = page.query_selector(".btn.btn-primary-sm")
                        from_date_input = page.query_selector("#FromDate")
                        to_date_input = page.query_selector("#ToDate")

                        from_date_input.fill(new_from_date)
                        to_date_input.fill(new_to_date)

                        search_button.click()

                        # Wait for the table to load
                        page.wait_for_selector("#resultsTable", timeout=2000)

                        # Process the table data
                        table_of_data = page.query_selector("#resultsTable")
                        rows = table_of_data.inner_html()
                        soup = BeautifulSoup(rows, 'html.parser')
                        rows = soup.find_all("tr")

                        # Process each row and write to the database
                        for row in rows:
                            data = row.find_all('td')

                            if len(data) < 9:
                                continue

                            # Skip rows
                            if str(data[2].get_text()) == "" and str(data[3].get_text()) == "":
                                continue

                            cleaned_data = (
                                stock_code,
                                str(data[0].get_text()),  # Date
                                format_price(str(data[1].get_text())),  # Last price
                                format_price(str(data[2].get_text())),  # Max price
                                format_price(str(data[3].get_text())),  # Min price
                                format_price(str(data[4].get_text())),  # Avg price
                                check_for_zero(str(data[5].get_text())),  # Percent change
                                check_for_zero(str(data[6].get_text())),  # Quantity
                                format_price(str(data[7].get_text())),  # Revenue best
                                format_price(str(data[8].get_text()))  # Total revenue
                            )

                            # Insert cleaned data for each stock code
                            cursor.execute(''' 
                                INSERT INTO stock_data (
                                    code, date, last_price, max_price, min_price, avg_price, percent_change, 
                                    quantity, revenue_best_denars, total_revenue_denars
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', cleaned_data)
                            conn.commit()

                        year_counter -= 1  # Move to the previous year

                    except Exception as e:
                        print(f"Error during scraping year {current_year - year_counter} for stock {stock_code}: {e}")
                        year_counter -= 1  # Continue even if error happens for this year

        except Exception as e:
            print(f"Scraping error: {e}")

        browser.close()

        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_minutes = elapsed_time // 60
        elapsed_seconds = elapsed_time % 60

        print("Scraping completed and data saved to SQLite database.")
        print(f"Total time taken: {int(elapsed_minutes)} minutes and {int(elapsed_seconds)} seconds.")

    conn.close()
    print(f"Total time taken: {int(elapsed_minutes)} minutes and {int(elapsed_seconds)} seconds.")