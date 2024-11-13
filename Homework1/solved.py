import time
import csv
import traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


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


# Initialize Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open the target webpage
    page.goto('https://www.mse.mk/mk/stats/symbolhistory/ADIN')

    time.sleep(2)
    page.evaluate("location.href='/mk/Home/AcceptCookiesConsent';")
    page.goto("https://www.mse.mk/mk/stats/symbolhistory/ADIN")

    # Get the list of stock codes
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

    print(stock_codes)

    # Define the output CSV file
    file_path = 'stock_data.csv'
    headers = ['Code', 'date', 'last price', 'max', 'min', 'avg price', 'percent',
               'quantity', 'revenue in best denars', 'total revenue in denars']

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers

        # Start the timer for loading data for each code
        start_time = time.time()

        # Iterate over stock codes and gather data
        for stock_code in stock_codes:
            try:
                # Navigate to the specific stock code page
                page.goto(f'https://www.mse.mk/mk/stats/symbolhistory/{stock_code}')

                # Loop through the years to gather data
                year_counter = 10
                while year_counter >= 0:
                    try:
                        # Prepare the date range for the search
                        year = 2024 - year_counter
                        new_from_date = f"01.1.{year}"
                        new_to_date = f"31.12.{year}"

                        # Find and set fields for the dates and the search button
                        search_button = page.query_selector(".btn.btn-primary-sm")
                        from_date_input = page.query_selector("#FromDate")
                        to_date_input = page.query_selector("#ToDate")

                        from_date_input.fill(new_from_date)
                        to_date_input.fill(new_to_date)

                        # print("From " + new_from_date)
                        # print("To " + new_to_date)

                        search_button.click()

                        page.wait_for_selector("#resultsTable", timeout=20000)

                        table_of_data = page.query_selector("#resultsTable")
                        rows = table_of_data.inner_html()
                        soup = BeautifulSoup(rows, 'html.parser')
                        rows = soup.find_all("tr")

                        # Process each row and write to CSV
                        for row in rows:
                            data = row.find_all('td')

                            if len(data) < 9:
                                continue

                            if str(data[7].get_text()) == "0" and str(data[8].get_text()) == "0":  # Index 7 and 8 are the 8th and 9th cells
                                continue

                            cleaned_data = [stock_code, str(data[0].get_text()), format_price(str(data[1].get_text())),
                                            format_price(str(data[2].get_text())), format_price(str(data[3].get_text())),
                                            format_price(str(data[4].get_text())), check_for_zero(str(data[5].get_text())),
                                            check_for_zero(str(data[6].get_text())), format_price(str(data[7].get_text())),
                                            format_price(str(data[8].get_text()))]

                            writer.writerow(cleaned_data)

                        # Move to the next year after processing the current year's data
                        year_counter -= 1
                    except Exception as e:
                        print(f"Error processing data for stock code {stock_code} in year {2024 - year_counter}: {e}")
                        year_counter -= 1

            except Exception as e:
                print(f"Error: {e}")

    browser.close()

end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time
elapsed_minutes = elapsed_time // 60
elapsed_seconds = elapsed_time % 60

print(f"Scraping completed and data saved to {file_path}.")
print(f"Total time taken: {int(elapsed_minutes)} minutes and {int(elapsed_seconds)} seconds.")
