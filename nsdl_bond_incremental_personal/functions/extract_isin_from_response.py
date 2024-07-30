import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error
import sys
from requests.exceptions import ConnectionError, Timeout
import time
from functions import insert_response_into_database, log, send_mail
from config import nsdl_config
import sys
import json
import traceback

# Function to fetch details with retries and exponential backoff
def fetch_details(url, headers, retries=7, backoff_factor=1):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError as e:
                    print(f"Error parsing JSON for URL: {url}, Error: {e}")
                    return None
            elif response.status_code == 400:
                print(f"Error 400: No Record Found for URL: {url}")
                return None
            elif response.status_code == 503:
                print(f"Error 503: Service Unavailable for URL: {url}. Retrying...")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except (ConnectionError, Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        
        # Calculate exponential backoff delay
        delay = backoff_factor * (2 ** attempt)
        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)
        attempt += 1
    print("All attempts failed")
    return None


def create_db_connection_with_retry(max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host='4.213.77.165',
                user='root1',
                password='Mysql1234$',
                database='nsdl'
            )
            if connection.is_connected():
                print(f"Successfully connected to MySQL on attempt {attempt + 1}")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    print("Failed to connect to MySQL after multiple attempts")
    return None

# Function to fetch existing data for an ISIN from the database
def fetch_existing_data_for_isin(connection, isin):
    cursor = None
    try:
        if not connection or not connection.is_connected():
            print("Connection lost. Attempting to reconnect...")
            connection = create_db_connection_with_retry()
            if not connection:
                print("Failed to reconnect. Returning empty result.")
                return None

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nsdl_instrument_details WHERE isin = %s", (isin,))
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    except Error as e:
        print(f"Error fetching data for ISIN {isin} from database: {e}")
        return None
    finally:
        if cursor:
            cursor.close()


# Function to fetch all ISINs from the database to check missed isins
def fetch_all_isins_from_db(connection):
    cursor = None
    try:
        if not connection or not connection.is_connected():
            print("Connection lost. Attempting to reconnect...")
            connection = create_db_connection_with_retry()
            if not connection:
                print("Failed to reconnect. Returning empty set.")
                return set()

        cursor = connection.cursor()
        cursor.execute("SELECT isin FROM nsdl_instrument_details")
        result = cursor.fetchall()
        return {row[0] for row in result}
    except Error as e:
        print(f"Error fetching ISINs from database: {e}")
        return set()
    finally:
        if cursor:
            cursor.close()


# Main processing script
def extract_isin_from_response(increment_data_excel_path):
    print("extract_isin_from_response function is called")
    # Read ISINs from Excel
    isin_df = pd.read_excel(increment_data_excel_path)

    # Ensure ISIN column exists
    if 'isin' not in isin_df.columns:
        print("ISIN column not found in the provided Excel file.")
        sys.exit(1)

    # Headers for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.indiabondinfo.nsdl.com/',
        'Origin': 'https://www.indiabondinfo.nsdl.com'
    }

    # Connect to MySQL database
    connection = create_db_connection_with_retry()
    if not connection:
        sys.exit(1)

    # DataFrame to store results
    results = []
    
    try:
        for isin in isin_df['isin']:
            try:
                print(f"Processing ISIN: {isin}")
                
                # URLs to fetch details
                issuer_details_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/isins?isin={isin}"
                instrument_details_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={isin}"
                coupondetail_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/coupondetail?isin={isin}"
                redemptions_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/redemptions?isin={isin}"
                credit_ratings_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin={isin}"
                listings_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/listings?isin={isin}"
                restructuring_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/restructuring?isin={isin}"
                defaultdetail_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/defaultdetail?isin={isin}"
                keycontacts_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin={isin}"
                keydocuments_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin={isin}"

                # Fetch instrument details
                issuer_details = fetch_details(issuer_details_url, headers)
                instrument_details = fetch_details(instrument_details_url, headers)
                coupondetail = fetch_details(coupondetail_url, headers)
                redemptions = fetch_details(redemptions_url, headers)
                credit_ratings = fetch_details(credit_ratings_url, headers)
                listings = fetch_details(listings_url, headers)
                restructuring = fetch_details(restructuring_url, headers)
                defaultdetail = fetch_details(defaultdetail_url, headers)
                keycontacts = fetch_details(keycontacts_url, headers)
                keydocuments = fetch_details(keydocuments_url, headers)
                
                # Extract the type if available
                issuer_type = issuer_details.get('secTypeDesc', '')
    
                # Prepare the result dictionary
                result = {
                    'ISIN': isin,
                    'issuer_details': str(issuer_details) if issuer_details else None,
                    'type': issuer_type,  # Empty column for now
                    'instrument_details': str(instrument_details) if instrument_details else None,
                    'coupon_details': str(coupondetail) if coupondetail else None,
                    'redemption_details': str(redemptions) if redemptions else None,
                    'credit_ratings': str(credit_ratings) if credit_ratings else None,
                    'listing_details': str(listings) if listings else None,
                    'restructuring': str(restructuring) if restructuring else None,
                    'default_details': str(defaultdetail) if defaultdetail else None,
                    'keycontacts': str(keycontacts) if keycontacts else None,
                    'keydocuments': str(keydocuments) if keydocuments else None
                }

                # Append to results
                results.append(result)
                
                # Insert or update the result in the MySQL database
                # insert_response_into_database.insert_or_update_response_data_in_db(connection, result)

            except Exception as e:
                traceback.print_exc()
                nsdl_config.log_list[1] = "Failure"
                nsdl_config.log_list[2] = "error in extract isin details from response part"
                log.insert_log_into_table(nsdl_config.log_list)
                # print("error in extract isin details from response part:" ,nsdl_config.log_list)
                send_mail.send_email("nsdl instrument details error in extract isin details from response part", e)
                nsdl_config.log_list = [None] * 4

                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
                print(f"Exception Type: {exc_type}")
                print(f"Exception Object: {exc_obj}")
                print(f"Traceback: {exc_tb}")
                sys.exit()

        # Create DataFrame from results
        result_df = pd.DataFrame(results)
 
        final_excel_sheet_name = f"final_sheet_{nsdl_config.current_date}.xlsx"
        final_excel_sheet_path = fr"C:\Users\Premkumar.8265\Desktop\nsdl_bond\data\final_excel_sheet\{final_excel_sheet_name}"
        result_df.to_excel(final_excel_sheet_path, index=False)

        # Insert the result into MySQL database
        insert_response_into_database.insert_or_update_response_data_in_db(connection, result_df)

        # Fetch all ISINs from the database
        db_isins = fetch_all_isins_from_db(connection)

        # Validation step to ensure all ISINs are stored in the database
        input_isins = set(isin_df['isin'])
        missing_isins_db = input_isins - db_isins

        if missing_isins_db:
            print(f"Missing ISINs in the database: {missing_isins_db}")
            # nsdl_config.no_data_scraped = nsdl_config.no_data_avaliable - len(missing_isins_db)
        
        else:
            print("All ISINs from the input file are stored in the database.")

        # # Validation step to ensure all ISINs are saved
        # input_isins = set(isin_df['ISIN'])
        # output_isins = set(result_df['ISIN'])

        # missing_isins = input_isins - output_isins

        # if missing_isins:
        #     print(f"Missing ISINs in the output file: {missing_isins}")
        # else:
        #     print("All ISINs from the input file are stored in the output file.")
    
    except Exception as e:
        traceback.print_exc()
        nsdl_config.log_list[1] = "Failure"
        nsdl_config.log_list[2] = "error in extract isin details from response part"
        log.insert_log_into_table(nsdl_config.log_list)
        # print("error in extract isin details from response part:" ,nsdl_config.log_list)
        send_mail.send_email("nsdl instrument details error in extract isin details from response part", e)
        nsdl_config.log_list = [None] * 4

        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")

    finally:
        if connection:
            connection.close()    # Close the database connection
       
