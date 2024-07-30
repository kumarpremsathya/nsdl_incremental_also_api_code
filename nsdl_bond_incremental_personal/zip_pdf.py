import os
import time
import shutil
import zipfile
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import ast
import requests
import pdfkit


# Function to extract PDFs from a zip file
def extract_pdfs_from_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file in os.listdir(extract_to):
            if file.endswith(".zip"):
                nested_zip_path = os.path.join(extract_to, file)
                with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip_ref:
                    nested_zip_ref.extractall(extract_to)

# Function to download and extract zip files
def download_zip(zip_url, zip_dir, temp_pdf_dir, max_retries=10, delay=10):
    # Set up Chrome options to specify the download directory
    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": zip_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    filename = os.path.basename(urlparse(zip_url).path)  # Get the filename from the URL
    attempt = 0
    while attempt < max_retries:
        try:
            # Create a new instance of the Chrome driver with the specified options
            driver = webdriver.Chrome(options=chrome_options)

            # Navigate to the URL
            driver.get(zip_url)

            # Wait for the ZIP file to download
            time.sleep(40)  # Adjust the delay as needed

            # Check if the download was successful
            file_path = os.path.join(zip_dir, filename)
            if os.path.exists(file_path):
                print(f"ZIP file '{filename}' downloaded successfully!")
                driver.quit()
                
                # Extract PDFs from the downloaded ZIP file to a temporary directory
                extract_pdfs_from_zip(file_path, temp_pdf_dir)
                return True
            else:
                print(f"Download failed for '{filename}'. Retrying...")
        except WebDriverException as e:
            print(f"Error: {e}")
        except Exception as e:
            print("Error:", e)
        finally:
            # Close the browser
            driver.quit()

        attempt += 1
        print(f"Retrying '{filename}'... ({attempt}/{max_retries})")
        time.sleep(delay)

    print(f"Failed to download ZIP file '{filename}' after multiple attempts.")
    return False


# Function to download a PDF file
def download_pdf(pdf_url, pdf_dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/pdf',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    try:
        response = requests.get(pdf_url, headers=headers)
        if response.status_code == 200:
            # Parse the filename from the URL
            pdf_name = os.path.basename(urlparse(pdf_url).path)
            save_path = os.path.join(pdf_dir, pdf_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF file {pdf_name} downloaded successfully!")
            return pdf_name
        else:
            print(f"Failed to download PDF file from {pdf_url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")
        return None



# Function to convert HTML page to PDF
def convert_html_to_pdf(html_url, pdf_dir, config):
    try:
        # Extract the filename from the URL
        parsed_url = urlparse(html_url)
        filename = os.path.splitext(parsed_url.path.split('/')[-1])[0] + '.pdf'
        save_path = os.path.join(pdf_dir, filename)
        
        # Convert the URL to PDF
        pdfkit.from_url(html_url, save_path, configuration=config)
        print(f"PDF file '{filename}' generated successfully!")
        return filename
    except Exception as e:
        print(f"Error converting {html_url} to PDF: {e}")
        return None




def main(excel_path, pdf_dir, zip_dir, temp_pdf_dir, wkhtmltopdf_path):
    # Create save directories if they do not exist
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
    if not os.path.exists(temp_pdf_dir):
        os.makedirs(temp_pdf_dir)
    
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Create a column for storing the PDF filenames
    df['pdf_filenames'] = None
    
    # Configure pdfkit with the correct path to the wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    # Loop through the rows and process the downloadLink in keydocuments column
    for index, row in df.iterrows():
        isin = row['ISIN']
        isin_pdf_dir = os.path.join(pdf_dir, isin)
        if not os.path.exists(isin_pdf_dir):
            os.makedirs(isin_pdf_dir)
        
        keydocuments = row['keydocuments']
        pdf_names = []  # Reset the list for each row
        non_download_links = []  # List for non-downloadable links
        if pd.notna(keydocuments):
            keydocuments_list = ast.literal_eval(keydocuments)
            for doc in keydocuments_list:
                if 'downloadLink' in doc:
                    download_link = doc['downloadLink']
                    if download_link.endswith('.pdf'):
                        pdf_name = download_pdf(download_link, isin_pdf_dir)
                        if pdf_name:
                            pdf_names.append(pdf_name)
                    elif download_link.endswith('.zip'):
                        # Clear the temporary directory before extracting
                        for temp_file in os.listdir(temp_pdf_dir):
                            os.remove(os.path.join(temp_pdf_dir, temp_file))
                        
                        if download_zip(download_link, zip_dir, temp_pdf_dir):
                            # Move the extracted PDFs to the ISIN PDF directory
                            for temp_file in os.listdir(temp_pdf_dir):
                                if temp_file.endswith('.pdf'):
                                    shutil.move(os.path.join(temp_pdf_dir, temp_file), os.path.join(isin_pdf_dir, temp_file))
                                    pdf_names.append(temp_file)
                    elif download_link.endswith('.html'):
                        pdf_name = convert_html_to_pdf(download_link, isin_pdf_dir, config)
                        if pdf_name:
                            pdf_names.append(pdf_name)
                    

                    else:
                        # Add non-downloadable link to the list
                        non_download_links.append(download_link)
            
            # Store the PDF filenames back to the dataframe
            df.at[index, 'pdf_filenames'] = ', '.join(pdf_names)
            df.at[index, 'non_download_pdf_links'] = ', '.join(non_download_links)
    
    # Save the updated dataframe back to Excel
    output_excel_path = os.path.splitext(excel_path)[0] + '_with_pdfs.xlsx'
    df.to_excel(output_excel_path, index=False)
    print(f"Updated Excel file saved as {output_excel_path}")
    

# Example usage

excel_path = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\instrument_details.xlsx"
pdf_dir = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\extracted_pdfs"
zip_dir = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\extracted_zips"
temp_pdf_dir = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond\temp_extracted_pdfs"
wkhtmltopdf_path = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

main(excel_path, pdf_dir, zip_dir, temp_pdf_dir, wkhtmltopdf_path)
