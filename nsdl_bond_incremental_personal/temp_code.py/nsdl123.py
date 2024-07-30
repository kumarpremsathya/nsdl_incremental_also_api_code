from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from bs4 import BeautifulSoup


chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()  # Maximize the browser window
browser.get('https://www.indiabondinfo.nsdl.com/')
time.sleep(20)

# body = browser.find_element(By.XPATH, '/html/body')

# isin_input.send_keys("INE001W07011")
try:
    
    # Switch to the frame named "main"
    main_frame = browser.find_element(By.NAME, "main")
    browser.switch_to.frame(main_frame)

    # Now you can locate and interact with elements within the frame
    wait = WebDriverWait(browser, 10)
    isin_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="searchfield"]')))
    isin_input.send_keys("INE001W07011")

    # Switch back to the default content (out of the frame)
    # browser.switch_to.default_content()

    search_button = browser.find_element(By.XPATH, '/html/body/app-root/div/app-header/section/div/div/div/app-home-screen/div[1]/div[2]/div/div[2]/div/div[2]/button[1]')
    search_button.click()
    time.sleep(5)
    

    wait = WebDriverWait(browser, 10)
    instrument_details_link = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[1]/div/ul/li[2]/a')))
    instrument_details_link.click()
    
    
    
    instrument_contents = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-header/section/div/div[2]/div[2]')))
    
    
    # Get the HTML content of the element
    data_html = instrument_contents.get_attribute('innerHTML')
    print("data_html :", data_html)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(data_html, 'html.parser')
    
    print("BeautipulSoup===", soup.prettify())

    
    time.sleep(10)


except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(f"Error occurred at line {exc_tb.tb_lineno}:")
    print(f"Exception Type: {exc_type}")
    print(f"Exception Object: {exc_obj}")
    print(f"Traceback: {exc_tb}")