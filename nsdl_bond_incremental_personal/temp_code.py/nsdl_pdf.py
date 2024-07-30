import requests
import pandas as pd
import zipfile
import io
import os
import sys
import time

# Function to fetch details with retries
def fetch_details(url, headers, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(delay)
    print("All attempts failed")
    return None

# Function to download and extract zip files
def download_and_extract_zip(url, headers, extract_to):
    pdf_names = []
    try:
        
        zip_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/zip'
        }
        response = requests.get(url, headers = zip_headers)
        print("response", response)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                pdf_names.extend(extract_zip_contents(z, extract_to))
        else:
            print(f"Failed to download zip file: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return pdf_names

# Function to extract contents of a zip file
def extract_zip_contents(z, extract_to):
    pdf_names = []
    for info in z.infolist():
        if info.filename.endswith('.pdf'):
            pdf_names.append(info.filename)
            z.extract(info, extract_to)
        elif info.filename.endswith('.zip'):
            with z.open(info) as nested_zip:
                with zipfile.ZipFile(io.BytesIO(nested_zip.read())) as nested_z:
                    pdf_names.extend(extract_zip_contents(nested_z, extract_to))
    return pdf_names

# Read ISINs from Excel
isin_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\isin_list.xlsx"
isin_df = pd.read_excel(isin_file_path)

# Ensure ISIN column exists
if 'ISIN' not in isin_df.columns:
    print("ISIN column not found in the provided Excel file.")
    sys.exit(1)

# Headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, application/zip',
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
        keydocuments_url = f"https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keydocuments?isin={isin}"

        # Fetch instrument details
        instrument_details = fetch_details(instrument_details_url, headers)
        
        # Fetch key documents
        keydocuments = fetch_details(keydocuments_url, headers)
        
        if instrument_details and keydocuments:
            pdf_names = []
            for doc in keydocuments:
                if 'downloadLink' in doc and doc['downloadLink'].endswith('.zip'):
                    extract_to = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\extracted_pdfs"
                    os.makedirs(extract_to, exist_ok=True)
                    pdf_names.extend(download_and_extract_zip(doc['downloadLink'], headers, extract_to))
            
            # Convert the JSON responses to strings
            instrument_details_str = str(instrument_details)
            keydocuments_str = str(keydocuments)
            
            # Append the results
            results.append({
                'ISIN': isin,
                'instrument_details': instrument_details_str,
                'keydocuments': keydocuments_str,
                'pdf_names': ', '.join(pdf_names)  # Join PDF names into a single string
            })
        else:
            print(f"Failed to fetch details for ISIN: {isin}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred for ISIN {isin} at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")

# Create DataFrame from results
result_df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
output_file_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details_pdf.xlsx"
result_df.to_excel(output_file_path, index=False)
print(f"Data saved to {output_file_path}")








# import requests

# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import sys
# import time
# from bs4 import BeautifulSoup
# import pandas as pd
# import json


# chrome_options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(options=chrome_options)
# browser.maximize_window()  # Maximize the browser window
# browser.get('https://www.bseindia.com/downloads/ipo/2020428161324RIL%20IM%2028042020.pdf')
# time.sleep(20)  # Wait for the page to load




# wait = WebDriverWait(browser, 30)
# wait.until(EC.visibility_of_element_located((By.XPATH, "//html/body")))
    
# # Find the print-preview-app element using XPath
# print_preview_app = browser.find_element(By.XPATH, '//html/body')

# if print_preview_app :
#     print("welcome")
#     shadow_element = browser.execute_script('return arguments[0].querySelector("#viewer").shadowRoot.querySelector("#toolbar").shadowRoot.querySelector("#toolbar").querySelector("#downloads").shadowRoot.querySelector("#download")', print_preview_app)
        
        
#     # Print the shadow element
#     print(shadow_element)
#     if shadow_element:
#         # print("Shadow element found:", shadow_element.tag_name)
#         # print("HTML of the located element:", shadow_element.get_attribute('outerHTML'))
#         shadow_element.click()
#         time.sleep(10)




    
