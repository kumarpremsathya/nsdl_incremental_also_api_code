from datetime import datetime
import mysql.connector
from selenium import webdriver

source_status = "Active"
source_name = "nsdl_instrument_details"


log_list = [None] * 4
no_data_avaliable = 0
no_data_scraped = 0
deleted_sources = ""
deleted_source_count = 0
updated_count = 0

url = 'https://www.indiabondinfo.nsdl.com/'


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f"--disable-notifications")  
# chrome_options.add_experimental_option("prefs", {
#     "download.default_directory": download_folder,
#     "download.prompt_for_download": False,
#     "download.directory_upgrade": True
# })
browser = webdriver.Chrome(options=chrome_options)

current_date = datetime.now().strftime("%Y-%m-%d")


# host = "localhost"
# user = "root"
# password = "root"
# database = "nsdl"
# auth_plugin = "mysql_native_password"


host = "4.213.77.165"
user = "root1"
password = "Mysql1234$"
database = "nsdl"
auth_plugin = "mysql_native_password"
def db_connection():
    connection = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database,
        # auth_plugin = auth_plugin

    )
    return connection


# host = "localhost"
# user = "root"
# password = "root"
# database = "nsdl"
# auth_plugin = "mysql_native_password"

# def db_connection_local():
#     connection = mysql.connector.connect(
#         host = host,
#         user = user,
#         password = password,
#         database = database,
#         # auth_plugin = auth_plugin

#     )
#     return connection
