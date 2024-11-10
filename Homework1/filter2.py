import csv
from datetime import datetime, timedelta
import os

# Setup logging configuration

def get_last_date_from_csv(issuer_code, csv_file):
    try:
        # Open the CSV file and read its content
        if not os.path.exists(csv_file):
            # print(f"CSV file {csv_file} does not exist.")
            return None

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            last_date = None
            for row in reader:
                if row['issuer_code'] == issuer_code:
                    # Parse the date and compare to find the most recent one
                    current_date = datetime.strptime(row['date'], '%d.%m.%Y')
                    if not last_date or current_date > last_date:
                        last_date = current_date

            if last_date:
                return last_date.strftime('%d.%m.%Y')  # Return the last date found in European format
            else:
                return None

    except Exception as e:
        print(f"Error fetching last date for issuer {issuer_code}: {e}")
        return None


def convert_to_european_format(date_str):
    """Convert date string from ISO format (YYYY-MM-DD) to European format (DD.MM.YYYY)."""
    try:
        american_date = datetime.strptime(date_str, "%Y-%m-%d")
        return american_date.strftime("%d.%m.%Y")
    except ValueError:
        # print(f"Date conversion failed for {date_str}. Returning original string.")
        return date_str


def get_or_default_last_date(issuer_code, csv_file):
    """Get the most recent date for an issuer from the CSV file or return a default date if none exists."""
    last_date = get_last_date_from_csv(issuer_code, csv_file)

    if not last_date:
        # If no date is found, set the default to 10 years ago
        last_date = datetime.now() - timedelta(days=365 * 10)
        print(f"No data found for {issuer_code}. Using default date {last_date.strftime('%d.%m.%Y')}.")
        return last_date.strftime("%d.%m.%Y")
    else:
        return last_date


def process_issuer_codes(issuer_codes, csv_file):
    """Process multiple issuer codes and return the most recent date for each."""
    issuer_dates = {}
    for issuer_code in issuer_codes:
        print(f"Processing issuer code: {issuer_code}")
        last_date = get_or_default_last_date(issuer_code, csv_file)
        issuer_dates[issuer_code] = last_date

    return issuer_dates


# Example usage
if __name__ == "__main__":
    # Example list of issuer codes
    issuer_codes = ['REPL', 'ADIN']
    csv_file = 'stock_data.csv'  # Path to your CSV file

    # Process issuer codes and get the last date for each (in European format)
    issuer_dates = process_issuer_codes(issuer_codes, csv_file)

    # Output the last dates for each issuer
    print("Last dates for each issuer:")
    for issuer_code, date in issuer_dates.items():
        print(f"{issuer_code}: {date}")
