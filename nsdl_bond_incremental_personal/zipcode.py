import pandas as pd

# Paths to the Excel files
first_excel_path = r'C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details.xlsx'
second_excel_path = r'C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details_update_new_100.xlsx'
output_excel_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\merged_results.xlsx"


# Read the Excel files
first_df = pd.read_excel(first_excel_path)
second_df = pd.read_excel(second_excel_path)


# Drop duplicate columns from the first DataFrame except 'ISIN'
columns_to_keep = ['ISIN'] + [col for col in first_df.columns if col not in second_df.columns]
first_df = first_df[columns_to_keep]


# Merge the DataFrames on the ISIN column
merged_df = first_df.merge(second_df, on='ISIN', how='outer')

# Drop duplicate rows based on the ISIN column
merged_df.drop_duplicates(subset='ISIN', inplace=True)

# Save the merged DataFrame to a new Excel file
merged_df.to_excel(output_excel_path, index=False)
print(f"Merged data saved to {output_excel_path}")


# # Read the Excel files
# first_df = pd.read_excel(first_excel_path)
# second_df = pd.read_excel(second_excel_path)

# # Drop duplicate columns from the first DataFrame except 'ISIN'
# columns_to_keep = ['ISIN'] + [col for col in first_df.columns if col not in second_df.columns]
# first_df_filtered = first_df[columns_to_keep]

# # Merge the DataFrames on the ISIN column without creating duplicate columns
# merged_df = pd.merge(first_df_filtered, second_df, on='ISIN', how='outer')

# # Save the merged DataFrame to a new Excel file
# merged_df.to_excel(output_excel_path, index=False)
# print(f"Merged data saved to {output_excel_path}")



# import requests
# import time

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import WebDriverException
# import time
# import os
# from urllib.parse import urlparse
# import zipfile


# # Function to extract PDFs from a zip file
# def extract_pdfs_from_zip(zip_path, extract_to):
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_to)
#         for file in os.listdir(extract_to):
#             if file.endswith(".zip"):
#                 nested_zip_path = os.path.join(extract_to, file)
#                 with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip_ref:
#                     nested_zip_ref.extractall(extract_to)



# def download_zip(zip_urls, download_dir, max_retries=10, delay=10):
#     # Set up Chrome options to specify the download directory
#     chrome_options = Options()
#     chrome_prefs = {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     }
#     chrome_options.add_experimental_option("prefs", chrome_prefs)

#     for zip_url in zip_urls:
#         filename = os.path.basename(urlparse(zip_url).path)  # Get the filename from the URL
#         attempt = 0
#         while attempt < max_retries:
#             try:
#                 # Create a new instance of the Chrome driver with the specified options
#                 driver = webdriver.Chrome(options=chrome_options)

#                 # Navigate to the URL
#                 driver.get(zip_url)

#                 # Wait for the ZIP file to download
#                 time.sleep(40)  # Adjust the delay as needed

#                 # Check if the download was successful
#                 file_path = os.path.join(download_dir, filename)
#                 if os.path.exists(file_path):
#                     print(f"ZIP file '{filename}' downloaded successfully!")
#                     break  # Exit the retry loop if the download is successful
#                 else:
#                     print(f"Download failed for '{filename}'. Retrying...")
#             except WebDriverException as e:
#                 print(f"Error: {e}")
#             except Exception as e:
#                 print("Error:", e)
#             finally:
#                 # Close the browser
#                 driver.quit()

#             attempt += 1
#             print(f"Retrying '{filename}'... ({attempt}/{max_retries})")
#             time.sleep(delay)

#         if attempt == max_retries:
#             print(f"Failed to download ZIP file '{filename}' after multiple attempts.")

# # List of URLs to download
# zip_urls = [
#     "https://www.bseindia.com/corporates/download/344212/PPDIDisclosureDocuments_20210706135807.zip",
#     "https://www.bseindia.com/corporates/download/9889/PPDIDisclosureDocuments_20210930165057.zip"
# ]

# download_directory = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\extracted_pdfs"

# # Create the download directory if it doesn't exist
# os.makedirs(download_directory, exist_ok=True)

# download_zip(zip_urls, download_directory)

# # Extract PDFs from the downloaded zip file
# for file in os.listdir(download_directory):
#     if file.endswith(".zip"):
#         zip_path = os.path.join(download_directory, file)
#         extract_pdfs_from_zip(zip_path, download_directory)



# from selenium import webdriver
# import time

# # Create a new instance of the Chrome driver
# driver = webdriver.Chrome()

# # Navigate to the URL
# url = "https://www.bseindia.com/corporates/download/344212/PPDIDisclosureDocuments_20210706135807.zip"
# driver.get(url)

# # Wait for the ZIP file to download
# time.sleep(10)  # Adjust the delay as needed

# # Close the browser
# driver.quit()















# def download_zip(zip_url, filename, max_retries=10, delay=10):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Accept': 'application/zip',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Referer': 'https://www.indiabondinfo.nsdl.com/',
#         'Origin': 'https://www.indiabondinfo.nsdl.com',
#         'Cookie': 'NLOk562d5a=0; OtherCookieValues=abcd1234; anothercookie=efgh5678',  # Include relevant cookies here
#     }

#     session = requests.Session()
#     session.headers.update(headers)

#     attempt = 0
#     while attempt < max_retries:
#         try:
#             response = session.get(zip_url)
#             if response.status_code == 200:
#                 with open(filename, 'wb') as f:
#                     f.write(response.content)
#                 print("ZIP file downloaded successfully!")
#                 return
#             else:
#                 print("Failed to download ZIP file. Status code:", response.status_code)
#         except Exception as e:
#             print("Error:", e)
        
#         attempt += 1
#         print(f"Retrying... ({attempt}/{max_retries})")
#         time.sleep(delay)
    
#     print("Failed to download ZIP file after multiple attempts.")

# # Use the correct URL here
# download_zip(r"https://www.bseindia.com/corporates/download/344212/PPDIDisclosureDocuments_20210706135807.zip", "PPDIDisclosureDocuments_20210706135807.zip")






