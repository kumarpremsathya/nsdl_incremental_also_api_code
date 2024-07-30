
import os
import zipfile
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver options
chrome_options = webdriver.ChromeOptions()
download_directory = r"C:\Users\Premkumar.8265\Desktop\nsdl_bond"

chrome_options.add_experimental_option("prefs", {
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": download_directory  # Change to your preferred download directory
})

# Function to extract PDFs from a zip file
def extract_pdfs_from_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file in os.listdir(extract_to):
            if file.endswith(".zip"):
                nested_zip_path = os.path.join(extract_to, file)
                with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip_ref:
                    nested_zip_ref.extractall(extract_to)

# Function to automate download and extraction of PDFs
def automate_download_and_extraction():
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()  # Maximize the browser window
    browser.get('https://www.indiabondinfo.nsdl.com/')
    time.sleep(20)  # Wait for the page to load

    try:
        # Switch to the frame named "main"
        main_frame = browser.find_element(By.NAME, "main")
        browser.switch_to.frame(main_frame)

        # Locate and interact with elements within the frame
        wait = WebDriverWait(browser, 10)
        isin_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="searchfield"]')))
        isin_input.send_keys("INE001W07011")

        search_button = browser.find_element(By.XPATH, '/html/body/app-root/div/app-header/section/div/div/div/app-home-screen/div[1]/div[2]/div/div[2]/div/div[2]/button[1]')
        search_button.click()
        time.sleep(5)  # Wait for the search results to load

        wait = WebDriverWait(browser, 10)
        key_document_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[1]/div/ul/li[10]/a')))
        key_document_link.click()

        # Click on the "Instrument Details" link
        wait = WebDriverWait(browser, 10)
        key_documents_pdf_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-key-documents/div/div[1]/span/a')))
        key_documents_pdf_link.click()
        time.sleep(5) 

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")

    finally:
        browser.quit()

    # Wait for the download to complete
    time.sleep(30)

    # Extract PDFs from the downloaded zip file
    for file in os.listdir(download_directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(download_directory, file)
            extract_pdfs_from_zip(zip_path, download_directory)

# Run the function
automate_download_and_extraction()





# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import sys
# import time
# from bs4 import BeautifulSoup
# import pandas as pd
# import json

# # Set up Selenium WebDriver options
# chrome_options = webdriver.ChromeOptions()

# # Add options to disable PDF viewer and download automatically if necessary
# chrome_options.add_experimental_option("prefs", {
#     "plugins.always_open_pdf_externally": True,
#     "download.default_directory": r"C:\Users\Premkumar.8265\Desktop\nsdl_bond"  # Change to your preferred download directory
# })


# browser = webdriver.Chrome(options=chrome_options)
# browser.maximize_window()  # Maximize the browser window
# browser.get('https://www.indiabondinfo.nsdl.com/')
# time.sleep(20)  # Wait for the page to load

# try:
#     # Switch to the frame named "main"
#     main_frame = browser.find_element(By.NAME, "main")
#     browser.switch_to.frame(main_frame)

#     # Locate and interact with elements within the frame
#     wait = WebDriverWait(browser, 10)
#     isin_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="searchfield"]')))
#     isin_input.send_keys("INE001W07011")

#     search_button = browser.find_element(By.XPATH, '/html/body/app-root/div/app-header/section/div/div/div/app-home-screen/div[1]/div[2]/div/div[2]/div/div[2]/button[1]')
#     search_button.click()
#     time.sleep(5)  # Wait for the search results to load
     
#     wait = WebDriverWait(browser, 10)
#     key_document_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[1]/div/ul/li[10]/a')))
#     key_document_link.click()
     
    
#     # Click on the "Instrument Details" link
#     wait = WebDriverWait(browser, 10)
#     key_documents_pdf_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-key-documents/div/div[1]/span/a')))
#     key_documents_pdf_link.click()
#     time.sleep(5) 
    
#     # wait = WebDriverWait(browser, 10)
#     # pdf_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-key-documents/div/div[1]/span/a')))
    
#     # pdf_link.click( )
#     # time.sleep(10) 
    
#      # Access the shadow root and click on the download button
#     # download_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "cr-icon-button#download")))
    
#     # # Recursive function to access nested shadow roots
#     # def expand_shadow_element(element):
#     #     shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
#     #     return shadow_root

#     # shadow_root1 = expand_shadow_element(download_button)
#     # shadow_root2 = expand_shadow_element(shadow_root1.find_element(By.CSS_SELECTOR, 'viewer-download-controls'))
#     # shadow_root3 = expand_shadow_element(shadow_root2.find_element(By.CSS_SELECTOR, 'cr-icon-button#download'))
#     # download_icon = shadow_root3.find_element(By.CSS_SELECTOR, 'iron-icon')
#     # download_icon.click()

#     # time.sleep(10)  # Wait for the PDF to download

    
#     # Wait for the instrument details section to load
#     # instrument_contents = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]')))
#     # instrument_contents = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-instrument-details/div')))
   
#    # Wait for the instrument details section to load
# #     instrument_contents = WebDriverWait(browser, 10).until(
# #     EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-instrument-details/div'))
# # )
    
    
# #     pdf_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-key-documents/div/div[2]/span/a')))

    
#     # Get the HTML content of the element
#     # data_html = instrument_contents.get_attribute('innerHTML')
#     # # print("data_html :", data_html)

#     # # Parse the HTML content using BeautifulSoup
#     # soup = BeautifulSoup(data_html, 'html.parser')
#     # print("BeautifulSoup content ===", soup.prettify())

#     # # Extract all details
#     # details = {}

#     # # labels = soup.find_all('label', class_='lbl-1')
#     # # for label in labels:
#     # #     key = label.get_text(strip=True)
#     # #     # Check for the next sibling or the next element after label
#     # #     value_tag = label.find_next_sibling('p')
#     # #     if not value_tag:
#     # #         value_tag = label.find_next('p')
#     # #     value = value_tag.get_text(strip=True) if value_tag else ""
#     # #     details[key] = value
        
        
        
        
#     # labels = soup.find_all('label', class_='lbl-1')
#     # tag= soup.find_all('p', class_='val-1')
#     # print("tag===", tag)
#     # for label in labels:
       
#     #     key = label.get_text(strip=True)
#     #     value_tag = label.find_next('p', class_='val-1')
      
#     #     value = value_tag.get_text(strip=True) if value_tag else ""
#     #     details[key] = value

#     # # Convert the details dictionary to JSON
#     # details_json = json.dumps(details, indent=4)
#     # print("JSON data:", details_json)

#     # # Save the JSON data to an Excel file in a single cell
#     # df = pd.DataFrame([{"Instrument Details": details_json}])
#     # df.to_excel('instrument_details.xlsx', index=False)

#     # print("Data saved to instrument_details.xlsx")

#     # time.sleep(10)  # Additional wait if needed

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     print(f"Error occurred at line {exc_tb.tb_lineno}:")
#     print(f"Exception Type: {exc_type}")
#     print(f"Exception Object: {exc_obj}")
#     print(f"Traceback: {exc_tb}")

# finally:
#     browser.quit()
