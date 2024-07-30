

# import requests
# import pandas as pd

# # Read ISINs from CSV file
# input_csv = r"C:\Users\Mohan.7482\Desktop\testing code\nsdl_instrument_details_202407161753.csv"  # Replace with your CSV file path
# isins_df = pd.read_csv(input_csv)
# isins = isins_df['isin'].tolist()

# # isins = isins[:10]
# error_isin = []
# # Function to flatten the nested JSON data
# def flatten_json(y):
#     out = {}

#     def flatten(x, name=''):
#         if isinstance(x, dict):
#             for a in x:
#                 flatten(x[a], name + a + '_')
#         elif isinstance(x, list):
#             if not x:  # Check if the list is empty
#                 out[name[:-1]] = '[]'
#             else:
#                 out[name[:-1]] = '; '.join([str(i) for i in x])
#         else:
#             out[name[:-1]] = x

#     flatten(y)
#     return out

# # Function to fetch and flatten ISIN data
# def fetch_and_flatten_isin_data(isin):
#     try:
#         url = f"https://nsdlisin.nextwealth.com:5004/api/v1/{isin}/getIsinDetails/"
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         api_json_data = response.json()
#         return flatten_json(api_json_data)
#     except Exception as e:
#         print(f"Error processing ISIN {isin}: {e}")
#         error_isin.append(isin)
#         return None

# # Collect data for all ISINs
# all_data = []
# for isin in isins:
#     flat_data = fetch_and_flatten_isin_data(isin)
#     if flat_data:
#         all_data.append(flat_data)

# # Convert the collected data into a DataFrame
# if all_data:
#     data_df = pd.DataFrame(all_data)
#     # Save the DataFrame to an Excel file
#     data_df.to_excel("api_response_data_for_all_data.xlsx", index=False)
#     print("Data has been written to api_response_data.xlsx")
# else:
#     print("No valid data was collected.")

# if error_isin:
#     error_isin_df = pd.DataFrame(error_isin)
#     # Save the DataFrame to an Excel file
#     error_isin_df.to_excel("error_isin_data.xlsx", index=False)
#     print("Data has been written to error_isin_data.xlsx")




import requests
import pandas as pd

# Read ISINs from CSV file
input_csv = r"C:\Users\Mohan.7482\Desktop\testing code\nsdl_instrument_details_202407161753.csv"  # Replace with your CSV file path
isins_df = pd.read_csv(input_csv)
isins = isins_df['isin'].tolist()

# isins = isins[:10]
error_isin = []

# Function to flatten the nested JSON data
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            if not x:  # Check if the list is empty
                out[name[:-1]] = '[]'
            else:
                out[name[:-1]] = '; '.join([str(i) if i is not None else '' for i in x])
        else:
            out[name[:-1]] = x if x is not None else ''

    flatten(y)
    return out

# Function to fetch and flatten ISIN data
def fetch_and_flatten_isin_data(isin):
    try:
        url = f"https://nsdlisin.nextwealth.com:5004/api/v1/{isin}/getIsinDetails/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        api_json_data = response.json()
        return flatten_json(api_json_data)
    except Exception as e:
        print(f"Error processing ISIN {isin}: {e}")
        error_isin.append(isin)
        return None

# Collect data for all ISINs
all_data = []
for isin in isins:
    flat_data = fetch_and_flatten_isin_data(isin)
    if flat_data:
        all_data.append(flat_data)

# Convert the collected data into a DataFrame
if all_data:
    data_df = pd.DataFrame(all_data)
    # Save the DataFrame to an Excel file
    data_df.to_excel("api_response_data_for_all_isin.xlsx", index=False)
    print("Data has been written to api_response_data_for_all_data.xlsx")
else:
    print("No valid data was collected.")

if error_isin:
    error_isin_df = pd.DataFrame(error_isin, columns=["ISIN"])
    # Save the DataFrame to an Excel file
    error_isin_df.to_excel("error_isin_data.xlsx", index=False)
    print("Data has been written to error_isin_data.xlsx")
