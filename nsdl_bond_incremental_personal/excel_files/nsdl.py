
import pyautogui
import time
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchWindowException


chrome_options = webdriver.ChromeOptions()

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()  

# Navigate to the PDF
browser.get('https://www.careratings.com/upload/CompanyFiles/PR/202311161122_Reliance_Industries_Limited.pdf')
time.sleep(200)  # Wait for the page to load


# browser.switch_to.window(browser.current_window_handle)
# time.sleep(2)
# pyautogui.hotkey('ctrl', 'p')
# time.sleep(2)

# all_windows = browser.window_handles

# # Switch to the new window
# new_window = [window for window in all_windows if window != browser.current_window_handle][0]
# print("new window =======",new_window)
# browser.switch_to.window(new_window)
# try:
#         WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//html/body/print-preview-app")))
       
#         print_preview_app = browser.find_element(By.XPATH, "//html/body/print-preview-app")
       
#         if print_preview_app :
#             shadow_element = browser.execute_script('return arguments[0].shadowRoot.querySelector("print-preview-sidebar").shadowRoot.querySelector("#container").querySelector("print-preview-destination-settings").shadowRoot.querySelector("print-preview-destination-select").shadowRoot.querySelector("print-preview-settings-section > div").querySelector(".md-select")', print_preview_app)

#             print(shadow_element)
#             if shadow_element:
#                 shadow_element.click()
#                 time.sleep(10)
#                 select = Select(shadow_element)
#                 time.sleep(10)
#                 select.select_by_value('Save as PDF/local/')
#                 shadow_element.click()
#                 time.sleep(5)
#                 print_preview_app = browser.find_element(By.XPATH, "//html/body/print-preview-app")
#                 if print_preview_app :
#                     shadow_element = browser.execute_script('return arguments[0].shadowRoot.querySelector("print-preview-sidebar").shadowRoot.querySelector("print-preview-button-strip").shadowRoot.querySelector(".controls").querySelector(".action-button")', print_preview_app)
#                     print("save button",shadow_element)
#                     if shadow_element:
#                         shadow_element.click()
#                         time.sleep(10)
                        
#                         pyautogui.press('enter')
#                         time.sleep(5)
#                 else:
#                     print("Shadow element save not found.")
#             else:
#                 print("Shadow element select not found.")

# except TimeoutException:
#         print("Timeout waiting for print preview to load.")
       
# except WebDriverException as e:
#         print("An error occurred:", e)
# browser.switch_to.window(browser.window_handles[0])
# browser.quit()

# # Simulate pressing Enter to print
# pyautogui.press('enter')

# # Close the driver after observing the effect
# browser.quit()







# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # import time



# # chrome_options = webdriver.ChromeOptions()
# # browser = webdriver.Chrome(options=chrome_options)
# # browser.maximize_window()  # Maximize the browser window
# # browser.get('https://www.indiabondinfo.nsdl.com/')
# # time.sleep(20)

# # # isin_input = browser.find_element(By.XPATH, '//*[@id="searchfield"]')

# # # isin_input.send_keys("INE001W07011")



# # # Wait for the element to be present on the page
# # wait = WebDriverWait(browser, 20)
# # isin_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchfield"]')))

# # isin_input.send_keys("INE001W07011")
# # time.sleep(10)
# # # search_button = browser.find_element(By.XPATH, '/html/body/app-root/div/app-header/section/div/div/div/app-home-screen/div[1]/div[2]/div/div[2]/div/div[2]/button[1]')
# # # cls

# # time.sleep(10)