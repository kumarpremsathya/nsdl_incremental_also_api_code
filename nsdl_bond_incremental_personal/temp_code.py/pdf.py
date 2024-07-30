# import pandas as pd
# import requests
# import os
# from urllib.parse import urlparse
# import ast

# def download_pdf(pdf_url, save_dir):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Accept': 'application/pdf',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#     }
#     try:
#         response = requests.get(pdf_url, headers=headers)
#         if response.status_code == 200:
#             # Parse the filename from the URL
#             pdf_name = os.path.basename(urlparse(pdf_url).path)
#             save_path = os.path.join(save_dir, pdf_name)
#             with open(save_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"PDF file {pdf_name} downloaded successfully!")
#             return pdf_name
#         else:
#             print(f"Failed to download PDF file from {pdf_url}. Status code: {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"Error downloading {pdf_url}: {e}")
#         return None

# def main(excel_path, save_dir):
#     # Create save directory if it does not exist
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
    
#     # Read the Excel file
#     df = pd.read_excel(excel_path)
    
#     # Create a column for storing the PDF filenames
#     df['pdf_filenames'] = None
    
#     # Loop through the rows and process the downloadLink in keydocuments column
#     for index, row in df.iterrows():
#         keydocuments = row['keydocuments']
#         if pd.notna(keydocuments):
#             keydocuments_list = ast.literal_eval(keydocuments)
#             pdf_names = []
#             for doc in keydocuments_list:
#                 if 'downloadLink' in doc and doc['downloadLink'].endswith('.pdf'):
#                     pdf_url = doc['downloadLink']
#                     pdf_name = download_pdf(pdf_url, save_dir)
#                     if pdf_name:
#                         pdf_names.append(pdf_name)
#             # Store the PDF filenames back to the dataframe
#             df.at[index, 'pdf_filenames'] = ', '.join(pdf_names)
    
#     # Save the updated dataframe back to Excel
#     output_excel_path = os.path.splitext(excel_path)[0] + '_with_pdfs.xlsx'
#     df.to_excel(output_excel_path, index=False)
#     print(f"Updated Excel file saved as {output_excel_path}")

# # Example usage
# excel_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details.xlsx"

# save_dir = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond"
# main(excel_path, save_dir)





# def download_pdf(pdf_url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Accept': 'application/pdf',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#     }
   
#     try:
#         response = requests.get(pdf_url, headers=headers)
#         if response.status_code == 200:

#             #Parse the filename from the URL
#             pdf_name = os.path.basename(urlparse(pdf_url).path)
#             with open(pdf_name, 'wb') as f:
#                 f.write(response.content)
#             print("PDF file downloaded successfully!")
#             print("pdf_name====", pdf_name)
#         else:
#             print("Failed to download PDF file. Status code:", response.status_code)
#     except Exception as e:
#         print(e)


# download_pdf(r"'https://www.crisilratings.com/mnt/winshare/Ratings/RatingList/RatingDocs/YarrowInfrastructurePrivateLimited_January%2030,%202023_RR_310264.html'")
# download_pdf(r"https://www.indiaratings.co.in/pressrelease/62428")

# download_pdf(r"https://www.careratings.com/upload/CompanyFiles/PR/202311161122_Reliance_Industries_Limited.pdf")
# download_pdf(r"https://www.careratings.com/upload/CompanyFiles/PR/202307120748_Reliance_Industries_Limited.pdf")




# import pdfkit
# import time
# from urllib.parse import urlparse
# import os

# urls = [
#     "https://www.crisilratings.com/mnt/winshare/Ratings/RatingList/RatingDocs/YarrowInfrastructurePrivateLimited_January%2030,%202023_RR_310264.html",
#     "https://www.crisil.com/mnt/winshare/Ratings/RatingList/RatingDocs/YarrowInfrastructurePrivateLimited_November%2022,%202022_RR_305253.html",
# ]
#     # Add more URLs here

# # Correct path to the wkhtmltopdf executable
# config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

# for url in urls:
#     # Extract the filename from the URL
#     parsed_url = urlparse(url)
#     filename = os.path.splitext(parsed_url.path.split('/')[-1])[0] + '.pdf'

#     # Add a delay if needed
#     time.sleep(10)

#     # Convert the URL to PDF
#     pdfkit.from_url(url, filename, configuration=config)
#     print(f"PDF file '{filename}' generated successfully!")






from selenium import webdriver
import pdfkit
from urllib.parse import urlparse
import os

urls = [
    # "https://www.indiaratings.co.in/pressrelease/62428",
    # "https://www.icra.in/Rationale/ShowRationaleReport?Id=125340",
    "https://www.nseindia.com/companies-listing/corporate-filings-offer-documents"
    # Add more URLs here
]

# Correct path to the wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

for url in urls:
    # Extract the filename from the URL
    parsed_url = urlparse(url)
    filename = os.path.splitext(parsed_url.path.split('/')[-1])[0] + '.pdf'

    # Navigate to the website
    driver.get(url)

    # Wait for the page to load (you can adjust the delay or use more sophisticated methods)
    driver.implicitly_wait(30)

    # Convert the rendered page to PDF
    pdfkit.from_string(driver.page_source, filename, configuration=config)

    print(f"PDF file '{filename}' generated successfully!")

# Close the browser
driver.quit()





# import requests
# import time

# import requests
# import time

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





# import requests

# def download_zip(zip_url, filename):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Accept': 'application/zip',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Referer': 'https://www.indiabondinfo.nsdl.com/',
#         'Origin': 'https://www.indiabondinfo.nsdl.com'
#     }
   
#     try:
#         response = requests.get(zip_url, headers=headers)
#         if response.status_code == 200:
#             with open(filename, 'wb') as f:
#                 f.write(response.content)
#             print("ZIP file downloaded successfully!")
#         else:
#             print("Failed to download ZIP file. Status code:", response.status_code)
#     except Exception as e:
#         print(e)

# download_zip(r"https://www.bseindia.com/corporates/download/344212/PPDIDisclosureDocuments_20210706135807.zip", "PPDIDisclosureDocuments_20210706135807.zip")



# def download_zip(zip_url, filename, max_retries=10, delay=10):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Accept': 'application/zip',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Referer': 'https://www.indiabondinfo.nsdl.com/',
#         'Origin': 'https://www.indiabondinfo.nsdl.com'
#     }

#     attempt = 0
#     while attempt < max_retries:
#         try:
#             response = requests.get(zip_url, headers=headers)
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

# download_zip(r"https://www.bseindia.com/corporates/download/344212/PPDIDisclosureDocuments_20210706135807.zip", "PPDIDisclosureDocuments_20210706135807.zip")



# # import pdfkit

# # url = "https://www.crisilratings.com/mnt/winshare/Ratings/RatingList/RatingDocs/YarrowInfrastructurePrivateLimited_January%2030,%202023_RR_310264.html"
# # filename = "YarrowInfrastructurePrivateLimited.pdf"

# # pdfkit.from_url(url, filename)
# # print("PDF file generated successfully!")