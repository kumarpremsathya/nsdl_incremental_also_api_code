import sys
from config import nsdl_config
import mysql.connector






# Database connection parameters
# host = "4.213.77.165"
# user = "root1"
# password = "Mysql1234$"
# database = "nsdl"

# def db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database
#         )
#         return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         sys.exit(1)

# connection = db_connection()
# cursor = connection.cursor()


def get_data_count_database():
    connection = nsdl_config.db_connection()
    cursor = connection.cursor()
   
    try:
        print("get_data_count_database function is called")
        cursor.execute("SELECT COUNT(*) FROM nsdl_instrument_details;")
        # print("count from database",cursor.fetchone()[0])
        # return cursor.fetchone()[0]

        result = cursor.fetchone()
        print("Result from database query:", result)
        if result:
            return result[0]
        else:
            raise ValueError("Query did not return any results")
        
    except Exception as e:
            print("Error in get_data_count_database :", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Error occurred at line {exc_tb.tb_lineno}:")
            print(f"Exception Type: {exc_type}")
            print(f"Exception Object: {exc_obj}")
            print(f"Traceback: {exc_tb}")
