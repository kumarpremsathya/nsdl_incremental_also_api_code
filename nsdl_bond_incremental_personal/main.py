import sys
import traceback
from config import nsdl_config
from functions import check_increment_isin_db, log


def main():
    print("main function is called")
    
    if nsdl_config.source_status == "Active":
        check_increment_isin_db.check_increment_isin_db()
        print("finished")
        
    elif nsdl_config.source_status == "Hibernated":
        nsdl_config.log_list[1] = "not run"
        log.insert_log_into_table(nsdl_config.log_list)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")
            
    elif nsdl_config.source_status == "Inactive":
        nsdl_config.log_list[1] = "not run"
        log.insert_log_into_table(nsdl_config.log_list)
        nsdl_config.log_list = [None] * 4
        traceback.print_exc()
      
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error occurred at line {exc_tb.tb_lineno}:")
        print(f"Exception Type: {exc_type}")
        print(f"Exception Object: {exc_obj}")
        print(f"Traceback: {exc_tb}")
        sys.exit("script error")


if __name__ == "__main__":
    main()
