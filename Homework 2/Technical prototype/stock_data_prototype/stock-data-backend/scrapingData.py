import time
import sqlite3
import traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os


def delete_database():
    try:
        # Specify the path to your database file
        db_path = 'stock_data_PROTOTYPE.db'

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
    conn = sqlite3.connect('stock_data_PROTOTYPE.db')
    cursor = conn.cursor()

    # Create a table for stock data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data_PROTOTYPE (
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

    # Initialize Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the target webpage for ADIN issuer code
        page.goto('https://www.mse.mk/mk/stats/symbolhistory/ADIN')

        start_time = time.time()

        try:
            # Start year_counter from 2 for the last 2 years (2023 and 2024)
            year_counter = 2
            current_year = 2024  # You can dynamically fetch the current year if necessary

            # Loop over the last 2 years
            while year_counter >= 1:
                try:
                    year = current_year - year_counter
                    new_from_date = f"01.1.{year}"
                    new_to_date = f"31.12.{year}"

                    # Check for table existence
                    table_exists = page.query_selector("#resultsTable") is not None

                    if not table_exists:
                        year_counter -= 1
                        continue  # Skip processing if table doesn't exist

                    # Find and set fields for the dates and the search button
                    search_button = page.query_selector(".btn.btn-primary-sm")
                    from_date_input = page.query_selector("#FromDate")
                    to_date_input = page.query_selector("#ToDate")

                    from_date_input.fill(new_from_date)
                    to_date_input.fill(new_to_date)

                    search_button.click()

                    # Wait for the table to load
                    page.wait_for_selector("#resultsTable", timeout=3000)

                    # Process the table data
                    table_of_data = page.query_selector("#resultsTable")
                    rows = table_of_data.inner_html()
                    soup = BeautifulSoup(rows, 'html.parser')
                    rows = soup.find_all("tr")

                    # Process each row and write to database
                    for row in rows:
                        data = row.find_all('td')

                        if len(data) < 9:
                            continue

                        if str(data[7].get_text()) == "0" and str(data[8].get_text()) == "0":
                            continue

                        cleaned_data = (
                            "ADIN",
                            str(data[0].get_text()),
                            format_price(str(data[1].get_text())),
                            format_price(str(data[2].get_text())),
                            format_price(str(data[3].get_text())),
                            format_price(str(data[4].get_text())),
                            check_for_zero(str(data[5].get_text())),
                            check_for_zero(str(data[6].get_text())),
                            format_price(str(data[7].get_text())),
                            format_price(str(data[8].get_text()))
                        )

                        cursor.execute(''' 
                            INSERT INTO stock_data_PROTOTYPE (
                                code, date, last_price, max_price, min_price, avg_price, percent_change, 
                                quantity, revenue_best_denars, total_revenue_denars
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', cleaned_data)
                        conn.commit()

                    year_counter -= 1  # Move to the previous year

                except Exception as e:
                    print(f"Error during scraping year {current_year - year_counter}: {e}")
                    year_counter -= 1  # Continue even if error happens for the current year

        except Exception as e:
            print(f"Scraping error: {e}")

        browser.close()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time
    elapsed_minutes = elapsed_time // 60
    elapsed_seconds = elapsed_time % 60

    print("Scraping completed and data saved to SQLite database.")
    print(f"Total time taken: {int(elapsed_minutes)} minutes and {int(elapsed_seconds)} seconds.")

    conn.close()
