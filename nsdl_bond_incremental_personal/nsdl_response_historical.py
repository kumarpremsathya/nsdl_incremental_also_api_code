import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error
import sys
from requests.exceptions import ConnectionError, Timeout
import time
import json
from deepdiff import DeepDiff

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




# Function to create the table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nsdl_instrument_details (
            sr_no int NOT NULL AUTO_INCREMENT,
            isin varchar(20) NOT NULL UNIQUE,
            issuer_details text,
            type varchar(255) DEFAULT NULL,
            instrument_details longtext,
            coupondetail longtext,
            redemptions longtext,
            credit_ratings longtext,
            listings longtext,
            restructuring longtext,
            defaultdetail longtext,
            keycontacts longtext,
            keydocuments longtext,
            updated_date varchar(250) DEFAULT NULL,
            date_scraped timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (sr_no)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")


# Function to fetch existing data for an ISIN from the database
# def fetch_existing_data_for_isin(connection, isin):
#     cursor = None
#     try:
#         if not connection or not connection.is_connected():
#             print("Connection lost. Attempting to reconnect...")
#             connection = create_db_connection_with_retry()
#             if not connection:
#                 print("Failed to reconnect. Returning empty result.")
#                 return None

#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM nsdl_instrument_details WHERE isin = %s", (isin,))
#         result = cursor.fetchone()
#         if result:
#             columns = [desc[0] for desc in cursor.description]
#             return dict(zip(columns, result))
#         return None
#     except Error as e:
#         print(f"Error fetching data for ISIN {isin} from database: {e}")
#         return None
#     finally:
#         if cursor:
#             cursor.close()

def fetch_existing_data_for_isin(connection, isin):
    cursor = None
    try:
        if not connection or not connection.is_connected():
            print("Connection lost. Attempting to reconnect...")
            connection = create_db_connection_with_retry()
            if not connection:
                print("Failed to reconnect. Returning empty result.")
                return None

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM nsdl_instrument_details WHERE isin = %s ORDER BY date_scraped DESC LIMIT 1"
        cursor.execute(query, (isin,))
        result = cursor.fetchone()
        if result:
            print(f"Existing data found for ISIN {isin}")
        else:
            print(f"No existing data found for ISIN {isin}")
        return result
    except Error as e:
        print(f"Error fetching data for ISIN {isin} from database: {e}")
        return None
    finally:
        if cursor:
            cursor.close()



# def normalize_json_string(json_string):
#     if json_string is None:
#         return None
#     try:
#         parsed = json.loads(json_string)
#         return json.dumps(parsed, sort_keys=True, ensure_ascii=False)
#     except json.JSONDecodeError:
#         return json_string
    
    

import ast


def compare_data(existing, new):
    try:
        # Convert string representations of dictionaries to actual dictionaries
        existing_obj = ast.literal_eval(existing) if existing else {}
        new_obj = ast.literal_eval(new) if new else {}

        # Perform a deep comparison
        diff = DeepDiff(existing_obj, new_obj,
                        ignore_order=True,
                        report_repetition=True,
                        ignore_string_type_changes=True,
                        ignore_numeric_type_changes=True,
                        ignore_type_in_groups=[(str, int, float)])

        # Filter out unwanted changes
        relevant_changes = {}
        if 'values_changed' in diff:
            relevant_changes['values_changed'] = diff['values_changed']
        if 'dictionary_item_added' in diff:
            relevant_changes['dictionary_item_added'] = diff['dictionary_item_added']
        if 'dictionary_item_removed' in diff:
            relevant_changes['dictionary_item_removed'] = diff['dictionary_item_removed']
        
        if relevant_changes:
            print("Relevant changes found:", relevant_changes)
            return relevant_changes
        else:
            print("No relevant changes found")
            return None

    except (ValueError, SyntaxError) as e:
        print(f"Error parsing data: {e}")
        return None
    except Exception as e:
        print(f"Error comparing data: {e}")
        return None
            


def insert_or_update_data(connection, data):
    cursor = None
    try:
        if not connection or not connection.is_connected():
            print("Connection lost. Attempting to reconnect...")
            connection = create_db_connection_with_retry()
            if not connection:
                print("Failed to reconnect. Skipping data insertion.")
                return

        cursor = connection.cursor(dictionary=True)

        # Fetch data for existing ISIN
        existing_data = fetch_existing_data_for_isin(connection, data['ISIN'])

        if existing_data:
             # Extract the relevant columns for comparison
            existing_relevant_data = {
                'issuer_details': existing_data['issuer_details'],
                # 'type': existing_data['type'],
                'instrument_details': existing_data['instrument_details'],
                'coupon_details': existing_data['coupon_details'],
                'redemption_details': existing_data['redemption_details'],
                'credit_ratings': existing_data['credit_ratings'],
                'listing_details': existing_data['listing_details'],
                'restructuring': existing_data['restructuring'],
                'default_details': existing_data['default_details'],
                'keycontacts': existing_data['keycontacts'],
                'keydocuments': existing_data['keydocuments'],
            }

            new_relevant_data = {
                'issuer_details': data['issuer_details'],
                # 'type': data['type'],
                'instrument_details': data['instrument_details'],
                'coupon_details': data['coupon_details'],
                'redemption_details': data['redemption_details'],
                'credit_ratings': data['credit_ratings'],
                'listing_details': data['listing_details'],
                'restructuring': data['restructuring'],
                'default_details': data['default_details'],
                'keycontacts': data['keycontacts'],
                'keydocuments': data['keydocuments'],
            }

            print(f"ISIN: {data['ISIN']}")

            changes_detected = False

            for key in existing_relevant_data.keys():
                diff = compare_data(existing_relevant_data[key], new_relevant_data[key])
                if diff:
                    changes_detected = True

            if changes_detected:
                print(f"Updates found for ISIN {data['ISIN']}:")

                current_timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_query = """
                INSERT INTO nsdl_instrument_details 
                (ISIN, issuer_details, type, instrument_details, coupon_details, redemption_details, 
                credit_ratings, listing_details, restructuring, default_details, keycontacts, keydocuments, updated_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    data['ISIN'], data.get('issuer_details'), data.get('type'), data.get('instrument_details'),  data.get('coupon_details'),
                    data.get('redemption_details'), data.get('credit_ratings'), data.get('listing_details'), data.get('restructuring'),
                    data.get('default_details'), data.get('keycontacts'), data.get('keydocuments'), current_timestamp
                ))
                connection.commit()
                print(f"New row inserted for updated ISIN {data['ISIN']}")
            else:
                print(f"No differences found for ISIN {data['ISIN']}. No new row added.")
        else:
            # Insert new record if no existing data is found
            insert_query = """
            INSERT INTO nsdl_instrument_details 
            (ISIN, issuer_details, type, instrument_details, coupon_details, redemption_details, 
            credit_ratings, listing_details, restructuring, default_details, keycontacts, keydocuments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['ISIN'], data.get('issuer_details'), data.get('type'), data.get('instrument_details'), data.get('coupon_details'),
                data.get('redemption_details'), data.get('credit_ratings'), data.get('listing_details'), data.get('restructuring'),
                data.get('default_details'), data.get('keycontacts'), data.get('keydocuments')
            ))
            connection.commit()
            print(f"Data for new ISIN {data['ISIN']} inserted successfully")
    except Error as e:
        print(f"Error inserting or updating data: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()




# # Function to insert or update data into the table
# def insert_or_update_data(connection, data):
#     cursor = None
#     try:
#         if not connection or not connection.is_connected():
#             print("Connection lost. Attempting to reconnect...")
#             connection = create_db_connection_with_retry()
#             if not connection:
#                 print("Failed to reconnect. Skipping data insertion.")
#                 return
            
#         cursor = connection.cursor()
        
#         # Fetch data for existing isin
#         existing_data = fetch_existing_data_for_isin(connection, data['ISIN'])
        
#         if existing_data:
#              # Extract the relevant columns for comparison
#             existing_relevant_data = {
#                 'issuer_details': existing_data['issuer_details'],
#                 'type': existing_data['type'],
#                 'instrument_details': existing_data['instrument_details'],
#                 'coupon_details': existing_data['coupon_details'],
#                 'redemption_details': existing_data['redemption_details'],
#                 'credit_ratings': existing_data['credit_ratings'],
#                 'listing_details': existing_data['listing_details'],
#                 'restructuring': existing_data['restructuring'],
#                 'default_details': existing_data['default_details'],
#                 'keycontacts': existing_data['keycontacts'],
#                 'keydocuments': existing_data['keydocuments'],
#             }

#             new_relevant_data = {
#                 'issuer_details': data['issuer_details'],
#                 'type': data['type'],
#                 'instrument_details': data['instrument_details'],
#                 'coupon_details': data['coupon_details'],
#                 'redemption_details': data['redemption_details'],
#                 'credit_ratings': data['credit_ratings'],
#                 'listing_details': data['listing_details'],
#                 'restructuring': data['restructuring'],
#                 'default_details': data['default_details'],
#                 'keycontacts': data['keycontacts'],
#                 'keydocuments': data['keydocuments'],
#             }

#             # Compare new data with existing data
#             diff = DeepDiff(existing_relevant_data, new_relevant_data, ignore_order=True, report_repetition=True).to_dict()
            
            
#             if diff:
#                 print(f"Differences found for ISIN {data['ISIN']}: {diff}")
#                 # Update the record if differences are found

#                 current_timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
#                 update_query = """
#                 UPDATE nsdl_instrument_details
#                 SET issuer_details = %s,
#                     type = %s,
#                     instrument_details = %s,
#                     coupon_details = %s,
#                     redemption_details = %s,
#                     credit_ratings = %s,
#                     listing_details = %s,
#                     restructuring = %s,
#                     default_details = %s,
#                     keycontacts = %s,
#                     keydocuments = %s,
#                     updated_date = %s
#                 WHERE isin = %s
#                 """
#                 cursor.execute(update_query, (
#                     data['issuer_details'], data['type'], data['instrument_details'], data['coupon_details'], data['redemption_details'], 
#                     data['credit_ratings'], data['listing_details'], data['restructuring'], data['default_details'], 
#                     data['keycontacts'], data['keydocuments'], current_timestamp, data['ISIN']
#                 ))
#                 connection.commit()
#                 print(f"Data for ISIN {data['ISIN']} updated successfully")
#             else:
#                 print(f"No differences found for ISIN {data['ISIN']}. No update needed.")
#         else:
#             # Insert new record if no existing data is found
#             insert_query = """
#             INSERT INTO nsdl_instrument_details (ISIN, issuer_details, type, instrument_details, coupon_details, redemption_details, credit_ratings, listing_details, restructuring, default_details, keycontacts, keydocuments)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_query, (
#                 data['ISIN'], data['issuer_details'], data['type'], data['instrument_details'], data['coupon_details'], 
#                 data['redemption_details'], data['credit_ratings'], data['listing_details'], data['restructuring'], 
#                 data['default_details'], data['keycontacts'], data['keydocuments']
#             ))
#             connection.commit()
#             print(f"Data for ISIN {data['ISIN']} inserted successfully")
#     except Error as e:
#         print(f"Error inserting or updating data: {e}")
#         if connection:
#             connection.rollback()
#     finally:
#         if cursor:
#             cursor.close()






# Function to fetch all ISINs from the database for checking missed isins
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
def main():
    # Read ISINs from Excel
    isin_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond_incremental_personal\List_of_securitites_active_matured.xlsx"
   
    isin_df = pd.read_excel(isin_file_path)

    # Ensure ISIN column exists
    if 'ISIN' not in isin_df.columns:
        print("ISIN column not found in the provided Excel file.")
        sys.exit(1)

    # Limit to the first 100 rows
    # isin_df = isin_df.head(5)
    isin_df = isin_df.iloc[1:2]

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

    # Create table if not exists
    create_table(connection)

    # DataFrame to store results
    results = []
    
    try:
        for isin in isin_df['ISIN']:
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
                insert_or_update_data(connection, result)

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
                print(f"Exception Type: {exc_type}")
                print(f"Exception Object: {exc_obj}")
                print(f"Traceback: {exc_tb}")

        # Create DataFrame from results
        result_df = pd.DataFrame(results)

        # Save the DataFrame to an Excel file
        output_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond_incremental_personal\List_of_securitites_active_matured_results.xlsx"
        result_df.to_excel(output_file_path, index=False)
        print(f"Data saved to {output_file_path}")


        # Fetch all ISINs from the database
        db_isins = fetch_all_isins_from_db(connection)

        # Validation step to ensure all ISINs are stored in the database
        input_isins = set(isin_df['ISIN'])
        missing_isins_db = input_isins - db_isins

        if missing_isins_db:
            print(f"Missing ISINs in the database: {missing_isins_db}")
        else:
            print("All ISINs from the input file are stored in the database.")


        # Validation step to ensure all ISINs are saved
        input_isins = set(isin_df['ISIN'])
        output_isins = set(result_df['ISIN'])

        missing_isins = input_isins - output_isins

        if missing_isins:
            print(f"Missing ISINs in the output file: {missing_isins}")
        else:
            print("All ISINs from the input file are stored in the output file.")
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")


    finally:
        if connection:
            connection.close()    # Close the database connection
       

if __name__ == "__main__":
    main()
