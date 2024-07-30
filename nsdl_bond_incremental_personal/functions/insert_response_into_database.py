import mysql.connector
from mysql.connector import Error
from functions import extract_isin_from_response, log, send_mail, get_data_count_database, check_increment_isin_db
import traceback
from config import nsdl_config
import sys
from deepdiff import DeepDiff
import pandas as pd


# Function to insert or update data into the table
def insert_or_update_response_data_in_db(connection, results_df):
    print("insert_or_update_response_data_in_db function is called")
    cursor = None
    try:
        for index, data in results_df.iterrows():

            if not connection or not connection.is_connected():
                print("Connection lost. Attempting to reconnect...")
                connection = extract_isin_from_response.create_db_connection_with_retry()
                if not connection:
                    print("Failed to reconnect. Skipping data insertion.")
                    return
                
            cursor = connection.cursor()
            
            # Fetch data for existing isin
            existing_data = extract_isin_from_response.fetch_existing_data_for_isin(connection, data['ISIN'])
            
            if existing_data:
                # Extract the relevant columns for comparison
                existing_relevant_data = {
                    'issuer_details': existing_data['issuer_details'],
                    'type': existing_data['type'],
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
                    'type': data['type'],
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

                # Compare new data with existing data
                diff = DeepDiff(existing_relevant_data, new_relevant_data, ignore_order=True, report_repetition=True).to_dict()
                   
                if diff:
                    print(f"Differences found for ISIN {data['ISIN']}: {diff}")
                    # Update the record if differences are found

                    current_timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                    update_query = """
                    UPDATE nsdl_instrument_details
                    SET issuer_details = %s,
                        type = %s,
                        instrument_details = %s,
                        coupon_details = %s,
                        redemption_details = %s,
                        credit_ratings = %s,
                        listing_details = %s,
                        restructuring = %s,
                        default_details = %s,
                        keycontacts = %s,
                        keydocuments = %s,
                        updated_date = %s
                    WHERE isin = %s
                    """
                    cursor.execute(update_query, (
                        data['issuer_details'], data['type'], data['instrument_details'], data['coupon_details'], data['redemption_details'],
                        data['credit_ratings'], data['listing_details'], data['restructuring'], data['default_details'],
                        data['keycontacts'], data['keydocuments'], current_timestamp, data['ISIN']
                    ))
                    connection.commit()
                    print(f"Data for ISIN {data['ISIN']} updated successfully")
                else:
                    print(f"No differences found for ISIN {data['ISIN']}. No update needed.")
            else:
                # Insert new record if no existing data is found
                insert_query = """
                INSERT INTO nsdl_instrument_details (ISIN, issuer_details, type, instrument_details, coupon_details, redemption_details, credit_ratings, listing_details, restructuring, default_details, keycontacts, keydocuments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    data['ISIN'], data['issuer_details'], data['type'], data['instrument_details'], data['coupon_details'],
                    data['redemption_details'], data['credit_ratings'], data['listing_details'], data['restructuring'],
                    data['default_details'], data['keycontacts'], data['keydocuments']
                ))
                connection.commit()
                print(f"Data for ISIN {data['ISIN']} inserted successfully")
            
        nsdl_config.log_list[1] = "Success"
        nsdl_config.no_data_scraped = len(results_df)
        nsdl_config.log_list[3] = f"{len(results_df)} data inserted, {nsdl_config.no_data_avaliable - len(results_df)} missed to extract isin data"
        log.insert_log_into_table(nsdl_config.log_list)
        # print(nsdl_config.log_list)
        nsdl_config.log_list = [None] * 4
        
    except Error as e:
        print(f"Error inserting or updating data in db: {e}")
        if connection:
            connection.rollback()
        
        print(f"Error inserting data in db: {e}")
        traceback.print_exc()
        nsdl_config.log_list[1] = "Failure"
        nsdl_config.log_list[2] = "error in insertion part in database"
        log.insert_log_into_table(nsdl_config.log_list)
        # print("error in insertion part:" ,nsdl_config.log_list)
        send_mail.send_email("nsdl instrument details error in insertion part in database", e)
        nsdl_config.log_list = [None] * 4
    
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")
        sys.exit()
    finally:
        if cursor:
            cursor.close()




