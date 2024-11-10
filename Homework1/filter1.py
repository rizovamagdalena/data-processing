import requests
from bs4 import BeautifulSoup
import time


def get_issuer_codes():
    url = 'https://www.mse.mk/mk/stats/symbolhistory/ADIN'

    # Retry logic in case it fails
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")

        if attempt < retries - 1:
            print(f"[INFO] Retrying... ({attempt + 1}/{retries})")
            time.sleep(3)  # Wait before retrying

    if response.status_code != 200:
        print(f"[ERROR] Failed to retrieve the page after {retries} attempts.")
        return []

    sp = BeautifulSoup(response.content, 'html.parser')

    select_element = sp.find('select', {'id': 'Code'})

    issuer_codes = []
    if select_element:
        options = select_element.find_all('option')

        for option in options:
            issuer_code = option['value'].strip()

            if issuer_code and not any(char.isdigit() for char in issuer_code):
                issuer_codes.append(issuer_code)

    return issuer_codes


# # Test function
# if __name__ == "__main__":
#     # Simulating test scenario
#     print("[INFO] Starting the test...")
#
#     # Call the function to fetch issuer codes
#     issuer_codes = get_issuer_codes()
#
#     # Print the result of fetched issuer codes
#     if issuer_codes:
#         print(f"[INFO] Retrieved {len(issuer_codes)} issuer codes:")
#         # Print only issuer codes
#         for code in issuer_codes:
#             print(code)
#     else:
#         print("[ERROR] No issuer codes retrieved.")
