import sys
import traceback
import pandas as pd
from datetime import datetime
from config import nsdl_config
from sqlalchemy import create_engine
from functions import extract_isin_from_response, log, send_mail
# download_pdf,  , send_mail,  updated_data_into_database_table
from sqlalchemy.sql import text


def check_increment_isin_db():
    print("check_increment_isin_db function is called")
    connection = nsdl_config.db_connection()
    cursor = connection.cursor()
    
    try:
        
        database_uri = f'mysql://{nsdl_config.user}:{nsdl_config.password}@{nsdl_config.host}/{nsdl_config.database}'

        engine = create_engine(database_uri)
        # query1 = "SELECT * FROM nsdl_instrument_details"
        # database1_df = pd.read_sql(query1, con=engine)

        # query2 = "SELECT * FROM nsdl_securities_report"
        # database2_df = pd.read_sql(query2, con=engine)

        missing_rows_in_db = []

        # for index, row in database2_df.iterrows():
        #     if row["isin"] not in database1_df["isin"].values:
        #         missing_rows_in_db.append(row)

        # Use a SQL join to find missing ISINs
         
        query = """
        SELECT nsr.* FROM nsdl_securities_report nsr
        LEFT JOIN nsdl_instrument_details nid ON nsr.isin = nid.isin
        WHERE nid.isin IS NULL
        """
        missing_rows_in_db = pd.read_sql(query, con=engine)
        
        print(len(missing_rows_in_db), "missing rows in database")
        nsdl_config.no_data_avaliable = len(missing_rows_in_db)
        # nsdl_config.no_data_scraped = len(missing_rows_in_db)
 
        if len(missing_rows_in_db) == 0:
            nsdl_config.log_list[1] = "Success"
            nsdl_config.log_list[3] = "no new isin"
            log.insert_log_into_table(nsdl_config.log_list)
            # print("log table====", nsdl_config.log_list)
            nsdl_config.log_list = [None] * 4
            sys.exit()
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        increment_file_name = f"incremental_excel_sheet_{current_date}.xlsx"
        
        increment_data_excel_path = fr"C:\Users\Premkumar.8265\Desktop\nsdl_bond\data\incremental_excel_sheet\{increment_file_name}"
        
        # missing_rows_in_db.to_excel(increment_data_excel_path, index=False)
        pd.DataFrame(missing_rows_in_db).to_excel(increment_data_excel_path, index=False)
        extract_isin_from_response.extract_isin_from_response(increment_data_excel_path)
              
    except Exception as e:
        traceback.print_exc()
        nsdl_config.log_list[1] = "Failure"
        nsdl_config.log_list[2] = "error in checking in incremental part"
        log.insert_log_into_table(nsdl_config.log_list)
        # print("checking incremental part error:" ,nsdl_config.log_list)
        send_mail.send_email("nsdl instrument details error in checking in incremental part", e)
        nsdl_config.log_list = [None] * 4
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")
        sys.exit()
