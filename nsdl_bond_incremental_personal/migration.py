import pymysql
from datetime import datetime

# Connect to local database
local_connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='nsdl'
)

# Connect to live database
live_connection = pymysql.connect(
    host='4.213.77.165',
    user='root1',
    password='Mysql1234$',
    database='sys'
)

try:
    # Create cursors for local and live databases
    local_cursor = local_connection.cursor()
    live_cursor = live_connection.cursor()

    # Fetch data from local nsdl_details table
    local_cursor.execute("SELECT isin, coupon_details, redemption_details, listing_details FROM nsdl_details")
    rows = local_cursor.fetchall()

    
    # Insert or update data in live nsdl_instrument_details table
    for row in rows:
        isin, coupon_details, redemption_details, listing_details = row
        query = """
            INSERT INTO nsdl_instrument_details (isin, coupon_details, redemption_details, listing_details, updated_date)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              coupon_details = VALUES(coupon_details),
              redemption_details = VALUES(redemption_details),
              listing_details = VALUES(listing_details),
              updated_date = VALUES(updated_date);
        """
        live_cursor.execute(query, (isin, coupon_details, redemption_details, listing_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


    # Commit changes on live database
    live_connection.commit()

finally:
    # Close connections
    local_cursor.close()
    local_connection.close()
    live_cursor.close()
    live_connection.close()

print("Data transferred successfully!")
