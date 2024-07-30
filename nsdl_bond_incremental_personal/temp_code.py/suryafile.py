



# from selenium import webdriver

# from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.by import By

# from selenium.webdriver.chrome.options import Options

# import time

# from selenium.webdriver.support.ui import WebDriverWait

# from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup

# import json

# import pandas as pd




# chrome_options = webdriver.ChromeOptions()

# # chrome_options.binary_location = 'C:\\Chrome\\chrome-win64\\chrome.exe'

# driver = webdriver.Chrome(options=chrome_options)

# driver.maximize_window()




# driver.get('https://www.indiabondinfo.nsdl.com/')




# wait = WebDriverWait(driver, 20)  # Increased wait time




# def parse_details_to_dict(details_text):

#     details_dict = {}

#     lines = details_text.split('\n')

#     for line in lines:

#         if ':' in line:  # Assuming ':' is the delimiter

#             key, value = line.split(':', 1)

#             details_dict[key.strip()] = value.strip()

#     return details_dict




# try:

#     # Switch to the frame by its name

#     driver.switch_to.frame("main")
    
#     # Use explicit wait to wait for the search field to be present

#     search_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchfield']")))


#     # Interact with the search field

#     search_field.send_keys('INE008A08S88')



#     # Wait for the button to be clickable and then click it

#     button_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button'][1]")))

#     button_click.click()



#     # Wait for a few seconds to observe the results (if needed)

#     time.sleep(5)

    

#     element_xpath_pattern = "/html/body/app-root/div/app-header/section/div/div[2]/div[1]/div/ul/li[{index}]/a"

#     for i in range(1, 10):  # Adjust the range based on the number of elements you want to interact with

#         element_xpath = element_xpath_pattern.format(index=i)

#         try:

#             issuer_details = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))

#             issuer_details.click()

#             details = ["app-issuer-details","app-instrument-details","app-coupon-details","app-redemption-details","app-credit-rating-details","app-listing-details","restructuring-details","app-default-details","app-key-contacts"]

#             # Add a short delay to ensure the page has fully loaded

#             time.sleep(2)

            

#             for detail in details :

#                 data_xpath = "/html/body/app-root/div/app-header/section/div/div[2]/div[2]/app-redemption-details/ul/li[2]/a"
                
    
#                 print("detail====", detail)

#                 details_data = "/html/body/app-root/div/app-header/section/div/div[2]/div[2]/{detail}/div"
            
                

#                 # Locate the data element

#                 data_element = wait.until(EC.presence_of_element_located((By.XPATH, data_xpath)))

#                 data_element.click()

#                 details_element = wait.until(EC.presence_of_element_located((By.XPATH, details_data)))

                

#                 # Extract text from the data element

#                 data_text = data_element.text

#                 print(f"Data from element {i}: {data_text}")

                

#                 details_html = details_element.get_attribute('innerHTML')

#                 print(f"Inner HTML of details {i}: {details_html}")




#                 # Parse the HTML content using BeautifulSoup

#                 soup = BeautifulSoup(details_html, 'html.parser')




#                 details = {}

#                 labels = soup.find_all('label', class_='lbl-1')

#                 for label in labels:

#                     key = label.get_text(strip=True)

#                     value_tag = label.find_next('p', class_='val-1')

#                     value = value_tag.get_text(strip=True) if value_tag else ""

#                     details[key] = value

                

#                 # Convert the details dictionary to JSON

#                 details_json = json.dumps(details, indent=4)

#                 print("JSON data:", details_json)


#                 # Save the JSON data to an Excel file in a single cell

#                 df = pd.DataFrame([{"Instrument Details": details_json}])

#                 df.to_excel('instrument_details.xlsx', index=False)



#                 print("Data saved to instrument_details.xlsx")




#                 time.sleep(10)  # Additional wait if needed




#         except Exception as e:

#             print(f"An error occurred while interacting with element {i}: {str(e)}")




# except Exception as e:

#     print(f"An error occurred: {str(e)}")




# finally:

#     # Close the browser

#     driver.quit()


