import sqlite3
from filter1 import get_issuer_codes
from filter2 import process_issuer_codes
from filter3 import fill_missing_data_for_issuer
import time;




def main():


    start_time = time.time()
    # Get the list of codes
    print("[INFO] Fetching issuer codes from Filter 1...")
    issuer_codes = get_issuer_codes()

    if not issuer_codes:
        print("[ERROR] No issuer codes found. Exiting process.")
        return

    csv_file = 'stock_data.csv'
    # Determine the start date for each code
    print("[INFO] Processing issuer codes in Filter 2...")
    issuer_dates = process_issuer_codes(issuer_codes,csv_file)

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
