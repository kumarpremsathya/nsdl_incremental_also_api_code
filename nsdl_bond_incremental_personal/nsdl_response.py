

import requests
import pandas as pd
import sys
from requests.exceptions import ConnectionError, Timeout
import time

# Function to fetch details with retries and exponential backoff
def fetch_details(url, headers, retries=5, backoff_factor=1):
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

# Read ISINs from Excel
isin_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\List_of_securitites_active_matured.xlsx"
isin_df = pd.read_excel(isin_file_path)

# Ensure ISIN column exists
if 'ISIN' not in isin_df.columns:
    print("ISIN column not found in the provided Excel file.")
    sys.exit(1)

# Limit to the first 10 rows
isin_df = isin_df.head(10)

# Headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.indiabondinfo.nsdl.com/',
    'Origin': 'https://www.indiabondinfo.nsdl.com'
}

# DataFrame to store results
results = []

for isin in isin_df['ISIN']:
    try:
        print(f"Processing ISIN: {isin}")
        
        # URLs to fetch details
        instrument_details_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={isin}"
        coupondetail_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/coupondetail?isin={isin}"
        redemptions_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/redemptions?isin={isin}"
        credit_ratings_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin={isin}"

        listings_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/listings?isin={isin}"



        restructuring_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/restructuring?isin={isin}"

        defaultdetail_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/defaultdetail?isin={isin}"
        keycontacts_url =        f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin={isin}"

        keydocuments_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin={isin}"

        # Fetch instrument details
        instrument_details = fetch_details(instrument_details_url, headers)
        

        coupondetail = fetch_details(coupondetail_url, headers)
        redemptions = fetch_details(redemptions_url, headers)
        credit_ratings = fetch_details(credit_ratings_url, headers)
        listings = fetch_details(listings_url, headers)
        restructuring = fetch_details(restructuring_url, headers)
        defaultdetail = fetch_details(defaultdetail_url, headers)
        keycontacts = fetch_details(keycontacts_url, headers)

        # Fetch key documents
        keydocuments = fetch_details(keydocuments_url, headers)
        
        # Append the results
        results.append({
            'ISIN': isin,
            'issuer_details': '',  # Empty column for now
            'type': '',  # Empty column for now
            'instrument_details': str(instrument_details) if instrument_details else None,
            'coupondetail': str(coupondetail) if coupondetail else None,
            'redemptions': str(redemptions) if redemptions else None,
            'credit_ratings': str(credit_ratings) if credit_ratings else None,
            'listings': str(listings) if listings else None,
            'restructuring': str(restructuring) if restructuring else None,
            'defaultdetail': str(defaultdetail) if defaultdetail else None,
            'keycontacts': str(keycontacts) if keycontacts else None,
            'keydocuments': str(keydocuments) if keydocuments else None
        })
        
    
        # Create DataFrame from results
        result_df = pd.DataFrame(results)

        # Save the DataFrame to an Excel file
        output_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\List_of_securitites_active_matured_results.xlsx"
        result_df.to_excel(output_file_path, index=False)
        print(f"Data saved to {output_file_path}")  
                    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")



# Validation step to ensure all ISINs are saved
input_isins = set(isin_df['ISIN'])
output_isins = set(result_df['ISIN'])

missing_isins = input_isins - output_isins

if missing_isins:
    print(f"Missing ISINs in the output file: {missing_isins}")
else:
    print("All ISINs from the input file are stored in the output file.")
    









########################################################################################################################################










import requests
import pandas as pd
import sys
from requests.exceptions import ConnectionError, Timeout
import time

# Function to fetch details with retries and exponential backoff
def fetch_details(url, headers, retries=5, backoff_factor=1):
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

# Read ISINs from Excel
isin_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\List_of_isin.xlsx"

isin_df = pd.read_excel(isin_file_path)

# Ensure ISIN column exists
if 'ISIN' not in isin_df.columns:
    print("ISIN column not found in the provided Excel file.")
    sys.exit(1)

# Headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.indiabondinfo.nsdl.com/',
    'Origin': 'https://www.indiabondinfo.nsdl.com'
}

# Load existing output file
output_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details_update_active.xlsx"
try:
    existing_result_df = pd.read_excel(output_file_path)
except FileNotFoundError:
    existing_result_df = pd.DataFrame()

# Get the list of existing ISINs and remaining ISINs
# input_isins = isin_df['ISIN'].tolist()
# existing_isins = existing_result_df['ISIN'].tolist()
# remaining_isins = [isin for isin in input_isins if isin not in existing_isins]
# remaining_isin_df = isin_df[isin_df['ISIN'].isin(remaining_isins)]

# DataFrame to store results
results = []

# for isin in remaining_isin_df['ISIN']:
#     try:
#         print(f"Processing ISIN: {isin}")
        
        # # URLs to fetch details
        # instrument_details_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={isin}"
        # keydocuments_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin={isin}"

        # # Fetch instrument details

        # instrument_details = fetch_details(instrument_details_url, headers)
        
        # # Fetch key documents
        # keydocuments = fetch_details(keydocuments_url, headers)
        
        # Append the results
        # results.append({
        #     'ISIN': isin,
        #     'instrument_details': str(instrument_details) if instrument_details else None,
            
        #     'keydocuments': str(keydocuments) if keydocuments else None
        # })
        
    #     # Create DataFrame from new results
    #     new_result_df = pd.DataFrame(results)

    #     # Combine existing and new results
    #     final_result_df = pd.concat([existing_result_df, new_result_df], ignore_index=True)

    #     # Save the final DataFrame to the output file
    #     final_result_df.to_excel(output_file_path, index=False)
    #     print(f"Data saved to {output_file_path}")
    
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
    #     print(f"Exception Type: {exc_type}")
    #     print(f"Exception Object: {exc_obj}")
    #     print(f"Traceback: {exc_tb}")



# # Validation step to ensure all ISINs are saved
input_isins = set(isin_df['ISIN'])
output_isins = set(existing_result_df['ISIN'])

missing_isins = input_isins - output_isins

if missing_isins:
    print(f"Missing ISINs in the output file: {missing_isins}")
else:
    print("All ISINs from the input file are stored in the output file.")






    

#######################################################################################################################

# import requests
# import pandas as pd
# import sys
# from requests.exceptions import ConnectionError, Timeout
# import time

# # Function to fetch details with retries
# def fetch_details(url, headers, retries=3, delay=5):
#     attempt = 0
#     while attempt < retries:
#         try:
#             response = requests.get(url, headers=headers, timeout=10)
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 print(f"Error: {response.status_code} - {response.text}")
#                 return None
#         except (ConnectionError, Timeout) as e:
#             print(f"Attempt {attempt + 1} failed: {e}")
#             attempt += 1
#             time.sleep(delay)
#     print("All attempts failed")
#     return None

# try:
#     # URLs to fetch details
#     instrument_details_url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin=INE001W07011"
#     keydocuments_url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin=INE001W07011"

#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'application/json',
#         'Referer': 'https://www.indiabondinfo.nsdl.com/',
#         'Origin': 'https://www.indiabondinfo.nsdl.com'
#     }
    
#     # Fetch instrument details
#     instrument_details = fetch_details(instrument_details_url, headers)
    
#     # Fetch key documents
#     keydocuments = fetch_details(keydocuments_url, headers)
    
#     if instrument_details and keydocuments:
#         # Convert the JSON responses to strings
#         instrument_details_str = str(instrument_details)
#         keydocuments_str = str(keydocuments)

#         # Create a DataFrame with the strings as the values in the respective columns
#         df = pd.DataFrame([{
#             'instrument_details': instrument_details_str,
#             'keydocuments': keydocuments_str
#         }])
        
#         print("df", df.to_string())
#         print("df123", df.to_html())

#         # Save the DataFrame to an Excel file
#         df.to_excel("instrument_details.xlsx", index=False)
#         print("Data saved to instrument_details.xlsx")
#     else:
#         print("Failed to fetch instrument details or key documents")

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     print(f"Error occurred at line {exc_tb.tb_lineno}:")
#     print(f"Exception Type: {exc_type}")
#     print(f"Exception Object: {exc_obj}")
#     print(f"Traceback: {exc_tb}")

# finally:
#     # browser.quit()
#     pass





# import requests

# import pandas as pd




# # Define the URL and headers for the request

# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin=INE003S07254"

# headers = {

#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

#     'Accept': 'application/json',

#     'Referer': 'https://www.indiabondinfo.nsdl.com/',

#     'Origin': 'https://www.indiabondinfo.nsdl.com'

# }




# # Use a session to handle cookies

# session = requests.Session()




# try:

#     # Send the GET request

#     response = session.get(url, headers=headers)

#     print(f"Status Code: {response.status_code}")

    

#     # Check if the request was successful

#     if response.status_code == 200:

#         data = response.json()

#         print(f"Response Content: {data}")

        

#         # Extract the ISIN number and download link

#         isin_number = "INE003S07254"

#         download_link = data[0]['downloadLink']

        

#         # Create a DataFrame to store the data

#         df = pd.DataFrame({

#             'ISIN': [isin_number],

#             'Download Link': [download_link]

#         })

        

#         # Write the DataFrame to an Excel file

#         excel_filename = "download_links.xlsx"

#         df.to_excel(excel_filename, index=False)

#         print(f"Data saved to {excel_filename}")

#     else:

#         print(f"Failed to retrieve data: {response.content}")

# except requests.exceptions.RequestException as e:

#     print(f"Request failed: {e}")
