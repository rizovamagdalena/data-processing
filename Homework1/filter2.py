import sqlite3
from datetime import datetime, timedelta


def get_last_date_from_db(issuer_code):
    try:
        conn = sqlite3.connect('stock_data.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT date FROM stock_prices WHERE issuer_code = ?''', (issuer_code,))
        rows = cursor.fetchall()

        if rows:
            dates = [datetime.strptime(row[0], '%d.%m.%Y') for row in rows]

            most_recent_date = max(dates)

            return most_recent_date.strftime('%d.%m.%Y')  # Return the last date found (already in European format)
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error fetching last date: {e}")
        return None
    finally:
        conn.close()


def convert_to_european_format(date_str):
    try:
        american_date = datetime.strptime(date_str, "%Y-%m-%d")
        return american_date.strftime("%d.%m.%Y")
    except ValueError:
        return date_str


def get_or_default_last_date(issuer_code):
    last_date = get_last_date_from_db(issuer_code)

    if not last_date:
        last_date = datetime.now() - timedelta(days=365 * 10)
        return last_date.strftime("%d.%m.%Y")
    else:
        return convert_to_european_format(last_date)


def process_issuer_codes(issuer_codes):
    issuer_dates = {}
    for issuer_code in issuer_codes:
        last_date = get_or_default_last_date(issuer_code)
        issuer_dates[issuer_code] = last_date

    return issuer_dates


# # Example usage
# if __name__ == "__main__":
#     # Example list of issuer codes
#     issuer_codes = ['REPL', 'ADIN']
#
#     # Process issuer codes and get the last date for each (in European format)
#     issuer_dates = process_issuer_codes(issuer_codes)
#
#     # Output the last dates for each issuer
#     print(issuer_dates)
