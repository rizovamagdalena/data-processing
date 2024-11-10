
import sqlite3
from filter1 import get_issuer_codes
from filter2 import process_issuer_codes
from filter3 import fill_missing_data_for_issuer
import time;

def create_db_table():
    """Create the stock_prices table if it doesn't exist."""
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_prices (
            issuer_code TEXT,  -- Unique identifier for each stock issuer
            date TEXT,  -- Date of the stock data
            last_transaction_price TEXT,  -- Last transaction price
            max_price TEXT,  -- Maximum price for the day
            min_price TEXT,  -- Minimum price for the day
            average_price TEXT,  -- Average price for the day
            percentage_change TEXT,  -- Percentage change in price
            quantity INTEGER,  -- Quantity of stocks traded
            turnover_best_in_denars TEXT,  -- Best turnover in denars
            total_turnover_in_denars TEXT,  -- Total turnover in denars
            PRIMARY KEY (issuer_code, date)  -- Composite primary key for uniqueness
        );
    ''')

    conn.commit()
    conn.close()



def main():

    create_db_table()

    start_time = time.time()
    # Get the list of codes
    print("[INFO] Fetching issuer codes from Filter 1...")
    issuer_codes = get_issuer_codes()

    if not issuer_codes:
        print("[ERROR] No issuer codes found. Exiting process.")
        return


    # Determine the start date for each code
    print("[INFO] Processing issuer codes in Filter 2...")
    issuer_dates = process_issuer_codes(issuer_codes)

    if not issuer_dates:
        print("[ERROR] No issuer dates found. Exiting process.")
        return

    # Step 3: Fetch missing data for each code and insert into the database
    print("[INFO] Filling missing data in Filter 3...")
    for issuer_code, start_date in issuer_dates.items():
        print(f"[INFO] NOW FOR ISSUER {issuer_code}")
        fill_missing_data_for_issuer(issuer_code, start_date)

    end_time = time.time()
    print("[INFO] Process completed.")

    elapsed_time = end_time - start_time  #for execution time
    print(f"[INFO] Total time taken: {elapsed_time:.2f} seconds")  #to print execution time


if __name__ == "__main__":
    main()
